"""Optional real-browser engineering check; never opens evaluation cases.

Install Playwright separately for QA, start the local server, then run:
python -m prototype.verify_browser --url http://127.0.0.1:8765
Uses installed Edge; saves a screenshot and a JSON evidence file.
"""
import argparse
import json
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen


def main():
    from playwright.sync_api import sync_playwright
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8765")
    parser.add_argument("--out-dir", type=Path, help="New evidence directory; preserve older screenshots/checks.")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.out_dir:
        if args.out_dir.exists():
            raise ValueError("Use a new evidence directory to preserve earlier QA.")
        args.out_dir.mkdir(parents=True)
    runtime = root / "prototype/runtime"
    runtime.mkdir(exist_ok=True)
    profile = runtime / ("browser-" + uuid.uuid4().hex)
    profile.mkdir()
    errors, checks, external = [], [], []
    unique_title = "Browser regression - " + uuid.uuid4().hex[:8]
    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    with urlopen(args.url + "/api/health", timeout=10) as response:
        health = json.load(response)
    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(str(profile), channel="msedge", headless=True,
                     viewport={"width":1440,"height":1000}, args=["--disable-gpu"])
        page = context.pages[0]
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("request", lambda request: external.append(request.url) if not request.url.startswith(args.url) and not request.url.startswith("blob:") else None)
        page.goto(args.url)
        page.locator("#mode").filter(has_text="suggestions").wait_for()
        check("Console loads in suggestions-only mode", "suggestions" in page.locator("#mode").inner_text())
        page.get_by_role("button", name="Load demo tickets").click()
        page.locator(".ticket").first.wait_for()
        check("Six or more demo tickets rendered through API", page.locator(".ticket").count() >= 6)
        page.get_by_role("button", name="New ticket", exact=True).click()
        page.locator("#title").fill(unique_title)
        page.locator("#account").select_option("helix")
        page.locator("#declared").select_option("P3")
        page.locator("#text").fill("An unknown privileged administrator changed our security policies without authorisation. Contact test@example.com from 198.51.100.200.")
        page.get_by_role("button", name="Run local triage", exact=True).click()
        page.locator("#newDlg").wait_for(state="hidden")
        page.locator("#detail h2").filter(has_text=unique_title).wait_for()
        check("New ticket input reaches API and renders redacted", "test@example.com" not in page.locator("#detail").inner_text() and "[EMAIL-" in page.locator("#detail").inner_text())
        check("New ticket stays P3 in suggestions mode", page.locator(".proposal .big .sev").inner_text() == "P3")
        check("Acceptance blocked before required human review", page.locator("#accept").is_disabled())
        page.locator("#take").click()
        page.locator(".taken").wait_for()
        check("Takeover retains manual controls", page.locator("#review").is_visible())
        page.locator("#review").click()
        page.locator("#reviewPriority").select_option("P1")
        page.locator("#reviewTeam").select_option("Incident Response")
        page.locator("#reviewReason").fill("Engineering browser test: checked synthetic administrator evidence.")
        page.get_by_role("button", name="Save engineer decision").click()
        page.locator("#reviewDlg").wait_for(state="hidden")
        page.locator(".proposal .big .sev").filter(has_text="P1").wait_for()
        check("Engineer correction applied", page.locator(".proposal .big .sev").inner_text() == "P1")
        check("Acceptance available after explicit review", page.locator("#accept").is_enabled())
        page.locator("#accept").click()
        page.locator("#accept").filter(has_text="Triage accepted").wait_for()
        page.reload()
        page.locator(".ticket").first.wait_for()
        check("Tickets survive page reload", unique_title in page.locator("#queue").inner_text())
        page.locator("#switch").click()
        page.locator("#switchReason").fill("Engineering browser test: enable assisted mode.")
        page.get_by_role("button", name="Confirm mode").click()
        page.locator("#switchDlg").wait_for(state="hidden")
        page.locator("#mode").filter(has_text="raises enabled").wait_for()
        check("Global assisted switch works from UI", "raises enabled" in page.locator("#mode").inner_text())
        page.locator("#switch").click()
        page.locator("#switchReason").fill("Engineering browser test: return to suggestions-only.")
        page.get_by_role("button", name="Confirm mode").click()
        page.locator("#mode").filter(has_text="suggestions").wait_for()
        page.reload()
        page.locator("#mode").filter(has_text="suggestions").wait_for()
        check("Switch persists across page reload", "suggestions" in page.locator("#mode").inner_text())
        with page.expect_download() as event:
            page.locator("#audit").click()
        audit_path = runtime / "browser-audit.json"
        event.value.save_as(audit_path)
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        check("Audit download includes engineer corrections and switch", any(e["action"] == "change" for e in audit) and any(e["action"] == "switch_mode" for e in audit))
        page.locator(".ticket").filter(has_text="Empty scheduled report").first.click()
        page.locator("#detail h2").filter(has_text="Empty scheduled report").wait_for()
        check("Desktop panels scroll without expanding the page", page.evaluate("document.documentElement.scrollHeight <= innerHeight + 10"))
        screenshot = args.out_dir / "prototype.png" if args.out_dir else root / "prototype/prototype_v0.4.png"
        page.screenshot(path=str(screenshot), full_page=False)
        page.set_viewport_size({"width":390,"height":844})
        check("Mobile viewport has no horizontal overflow", page.evaluate("document.documentElement.scrollWidth <= innerWidth"))
        check("No browser JavaScript errors", not errors)
        check("No page requests leave local service", not external)
        context.close()
    # The profile belongs to this check and must be inside the intended runtime root.
    assert profile.resolve().is_relative_to(runtime.resolve()) and profile.name.startswith("browser-")
    shutil.rmtree(profile)
    result = {"checked_at":datetime.now(timezone.utc).isoformat(), "type":"engineering browser QA, not product evaluation",
              "health":health, "checks":checks, "browser_errors":errors, "external_requests":external}
    target = args.out_dir / "browser_checks.json" if args.out_dir else root / "evals/browser_checks.json"
    target.write_text(json.dumps(result,indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
