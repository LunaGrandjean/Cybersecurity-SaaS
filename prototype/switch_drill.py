"""Stop-switch (rollback) drill on the local prototype.

Usage: python -m prototype.switch_drill --operator "Full Name"
Runs on a fresh local database, never on real data, and writes evidence to evals/switch_drills/.
"""
import argparse
import json
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

from .server import Application

ROOT = Path(__file__).resolve().parents[1]
TICKET = {"account_id": "helix", "declared_priority": "P3", "language": "en", "title": "Drill ticket",
          "text": "An unknown privileged administrator changed our security policies without authorisation."}


def drill(operator):
    paris = timezone(timedelta(hours=1))
    started = datetime.now(paris).replace(microsecond=0)
    db_dir = ROOT / "prototype" / "runtime" / ("drill-" + started.strftime("%Y%m%d-%H%M%S"))
    db_dir.mkdir(parents=True, exist_ok=True)
    db = db_dir / "drill.sqlite3"
    app = Application(db)
    checks = []

    def check(name, ok, detail):
        checks.append({"check": name, "passed": bool(ok), "detail": detail})

    app.switch({"mode": "assisted", "actor": operator, "reason": "Drill: start in assisted mode"})
    before = app.create(dict(TICKET), operator)
    check("assisted mode raises a suspected P1", before["triage"]["effective_priority"] == "P1",
          f"declared P3 -> effective {before['triage']['effective_priority']}")

    t0 = time.perf_counter()
    app.switch({"mode": "suggestions", "actor": operator, "reason": "Drill: press the stop switch"})
    seconds = round(time.perf_counter() - t0, 3)
    check("switch executes in under 15 minutes", seconds < 900, f"{seconds} s")

    after = app.create(dict(TICKET), operator)
    check("after switch, new tickets are suggestions only (no raise)",
          after["triage"]["effective_priority"] == "P3" and after["triage"]["proposed_severity"] == "P1",
          f"proposed {after['triage']['proposed_severity']}, effective {after['triage']['effective_priority']}")
    kept = app.store.get(before["id"])["triage"]["effective_priority"]
    check("existing ticket is not downgraded by the switch", kept == "P1", f"earlier ticket still {kept}")
    try:
        app.action({"ticket_id": after["id"], "action": "accept", "actor": operator})
        blocked = False
    except ValueError:
        blocked = True
    check("acceptance is blocked until a human review is recorded", blocked, "accept without review rejected" if blocked else "accepted")
    switches = [e for e in app.store.events() if e["action"] == "switch_mode"]
    check("both switch actions are in the audit log with operator and reason",
          len(switches) == 2 and all(e["actor"] == operator for e in switches),
          f"{len(switches)} switch events")
    app.store.db.close()
    from .store import Store
    reopened = Store(db)
    check("suggestions mode persists after restart", reopened.mode() == "suggestions", f"mode after reopen: {reopened.mode()}")
    reopened.db.close()

    result = {"drill_at": started.isoformat(), "operator": operator, "database": str(db.relative_to(ROOT)),
              "switch_seconds": seconds, "passed": all(c["passed"] for c in checks), "checks": checks}
    out = ROOT / "evals" / "switch_drills"
    out.mkdir(parents=True, exist_ok=True)
    (out / ("drill_" + started.strftime("%Y-%m-%d_%H%M%S") + ".json")).write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--operator", required=True)
    result = drill(parser.parse_args().operator)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
