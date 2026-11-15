"""Loopback-only HTTP API and static console; no customer-send endpoint."""
from __future__ import annotations

import argparse
import json
import uuid
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

if __name__ == "__main__":
    print("[1/3] Starting triage server: loading NumPy / scikit-learn. The first launch may take longer.", flush=True)

from .engine import DATA, PRIORITIES, TEAMS, TriageEngine, redact
from .store import Store

WEB = Path(__file__).parent


class Application:
    def __init__(self, db_path):
        self.engine = TriageEngine()
        self.store = Store(db_path)

    def create(self, raw, actor="demo-operator"):
        analysis = self.engine.analyze(raw, self.store.mode())
        ticket = {"id": "T-" + uuid.uuid4().hex[:8], "title": redact(str(raw.get("title", "New ticket"))[:160])["text"],
                  "language": raw.get("language", "en"), "status": "open", "taken_over": False,
                  "human_checked": False, "triage": analysis}
        self.store.put(ticket)
        self.store.event(ticket["id"], actor, "triage_created", {"priority": analysis["effective_priority"],
                         "proposal": analysis["proposed_severity"], "method": analysis["method"],
                         "model_version": analysis["model_version"]})
        return ticket

    def action(self, raw):
        with self.store.lock:
            ticket = self.store.get(raw.get("ticket_id", ""))
            triage = ticket["triage"]
            actor = str(raw.get("actor", "demo-operator"))[:80]
            action = raw.get("action")
            reason = redact(str(raw.get("reason", "")).strip())["text"]
            before = triage["effective_priority"]
            if action == "take_over":
                ticket["taken_over"], ticket["status"] = True, "human_triage"
            elif action == "review":
                if len(reason) < 5:
                    raise ValueError("Record what you verified (at least 5 characters).")
                ticket["human_checked"] = True
            elif action == "accept":
                if (ticket["taken_over"] or triage["requires_human"] or self.store.mode() == "suggestions") and not ticket["human_checked"]:
                    raise ValueError("Human verification must be recorded before acceptance.")
                ticket["status"] = "accepted"
            elif action == "change":
                priority = raw.get("priority", before)
                team = raw.get("team", triage["team"])
                if priority not in PRIORITIES or team not in TEAMS:
                    raise ValueError("Unknown priority or team.")
                if len(reason) < 5:
                    raise ValueError("An engineer reason is required for priority/team changes.")
                created = datetime.fromisoformat(triage["created_at"])
                account = self.engine.accounts.get(triage["account_id"])
                sla = account["sla_minutes"][priority] if account else {"P1":60,"P2":240,"P3":1440,"P4":4320}[priority]
                triage.update(effective_priority=priority, team=team, sla_minutes=sla,
                              sla_deadline=(created + timedelta(minutes=sla)).isoformat())
                ticket["human_checked"], ticket["status"] = True, "human_triage"
            else:
                raise ValueError("Unsupported action.")
            self.store.put(ticket)
            self.store.event(ticket["id"], actor, action, {"before": before, "after": triage["effective_priority"],
                             "team": triage["team"], "reason": reason})
            return ticket

    def switch(self, raw):
        mode = raw.get("mode")
        if mode not in ("suggestions", "assisted"):
            raise ValueError("Mode must be suggestions or assisted.")
        reason = redact(str(raw.get("reason", "")).strip())["text"]
        if len(reason) < 5:
            raise ValueError("A switch reason is required.")
        with self.store.lock:
            self.store.set_mode(mode, str(raw.get("actor", "demo-operator"))[:80], reason)
            # Existing priorities and engineer decisions are never undone by a switch.
            return {"mode": mode, "note": "Existing tickets preserved. Suggestions mode also blocks acceptance until human review."}


def make_handler(app):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass  # never log raw request bodies or ticket text

        def send(self, code, value, content_type="application/json; charset=utf-8"):
            body = json.dumps(value, ensure_ascii=False).encode() if isinstance(value, (dict, list)) else value
            try:
                self.send_response(code)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.send_header("X-Content-Type-Options", "nosniff")
                self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'")
                self.end_headers()
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                # Browser reload/navigation can cancel an in-flight response.
                # Do not try a second 503 response on the disconnected socket.
                return

        def do_GET(self):
            path = urlparse(self.path).path
            if path == "/api/health":
                self.send(200, {"status": "ok", "model_version": app.engine.model_version, "training_rows": len(app.engine.training)})
            elif path == "/api/state":
                self.send(200, {"mode": app.store.mode(), "tickets": app.store.tickets(),
                                "accounts": list(app.engine.accounts.values()), "teams": list(TEAMS)})
            elif path == "/api/audit":
                self.send(200, app.store.events())
            elif path in ("/", "/prototype_triage_copilot.html", "/console.css", "/console.js"):
                filename = "prototype_triage_copilot.html" if path in ("/", "/prototype_triage_copilot.html") else path[1:]
                mime = "text/html" if filename.endswith("html") else "text/css" if filename.endswith("css") else "text/javascript"
                self.send(200, (WEB / filename).read_bytes(), mime + "; charset=utf-8")
            else:
                self.send(404, {"error": "Not found"})

        def do_POST(self):
            try:
                origin = self.headers.get("Origin")
                if origin and origin != f"http://{self.headers.get('Host')}":
                    self.send(403, {"error": "Cross-origin requests are not accepted."})
                    return
                if not self.headers.get("Content-Type", "").startswith("application/json"):
                    self.send(415, {"error": "Use application/json."})
                    return
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > 65536:
                    raise ValueError("Request body must contain 1–65,536 bytes.")
                raw = json.loads(self.rfile.read(length))
                if not isinstance(raw, dict):
                    raise ValueError("Expected a JSON object.")
                path = urlparse(self.path).path
                if path == "/api/triage":
                    self.send(201, app.create(raw))
                elif path == "/api/action":
                    self.send(200, app.action(raw))
                elif path == "/api/switch":
                    self.send(200, app.switch(raw))
                elif path == "/api/demo":
                    fixtures = json.loads((DATA / "demo_tickets.json").read_text(encoding="utf-8"))
                    created = []
                    for item in fixtures:
                        item["created_at"] = (datetime.now(timezone.utc) - timedelta(minutes=item.pop("opened_minutes"))).isoformat()
                        created.append(app.create(item))
                    self.send(201, created)
                else:
                    self.send(404, {"error": "Not found"})
            except KeyError:
                self.send(404, {"error": "Ticket not found."})
            except (ValueError, TypeError, AttributeError):
                # No raw body, exception payload or secret reflected to callers.
                self.send(400, {"error": "Invalid request. Check required fields, timezone, priority and review reason."})
            except Exception:
                self.send(503, {"error": "Triage unavailable. Keep the declared priority and use human triage."})
    return Handler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--db", type=Path, default=WEB / "runtime" / "triage.sqlite3")
    args = parser.parse_args()
    print("[2/3] Preparing the local classifier (300 synthetic tickets) and source index...", flush=True)
    app = Application(args.db)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(app))
    print(f"[3/3] Ready: http://127.0.0.1:{server.server_port} (local demo, mode={app.store.mode()})", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
