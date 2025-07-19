#!/usr/bin/env python3
"""
NDP Ticket Auto-Submit Bot (PoC) – **v2.0**  (2025-05-28)
========================================================
Author: Rohit Panda

This version integrates the bug-fixes we just discussed:
* **Defaults** – running with no flags submits for *NDP day, 4 tickets*.
* **Intro page step** – detects and clicks the ➡️ arrow before waiting for the
  “Login with Singpass” button, eliminating the infinite reload loop.
* **Safer polling loop** – no more `Page.reload()` after navigation, preventing
  the *TargetClosedError* you hit.
* **Robust exit** if the page/context is closed unexpectedly.

```bash
pip install --upgrade playwright          # if not already
playwright install chromium              # once per machine
python ndp_ticket_bot.py                 # defaults: ndp, 4 tickets
```

DISCLAIMER: Automating Singpass may violate its Terms of Use and the NDP ticket
ballot’s rules.  This script is for **educational purposes only**.  Use at your
own risk.
"""

import asyncio
import argparse
from datetime import datetime
import time
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

SHOW_VALUE = {
    "preview1": "26 Jul 2025 – Preview 1",
    "preview2": "02 Aug 2025 – Preview 2",
    "ndp": "09 Aug 2025 – NDP",
}

INTRO_ARROW_SELECTOR = "div[role='button'] >> visible=true"  # works on FormSG intro screens
LOGIN_BTN_TEXT = "Login with Singpass"

async def precise_sleep(seconds: float):
    end = time.time() + seconds
    while time.time() < end:
        time.sleep(min(0.2, end - time.time()))

async def wait_until(when: datetime):
    while True:
        delta = (when - datetime.now()).total_seconds()
        if delta <= 0:
            break
        print(f"Waiting {delta // 60:.0f}m {delta % 60:.0f}s…", end="\r", flush=True)
        await precise_sleep(1)

async def submit_application(args):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=args.headless)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            print("Opening ballot page…")
            await page.goto("https://go.gov.sg/ndp2025tickets", wait_until="domcontentloaded")

            # Handle intro screen & wait for Singpass button
            while True:
                if await page.query_selector(f"text={LOGIN_BTN_TEXT}"):
                    break  # button is visible – we’re good
                arrow = page.locator(INTRO_ARROW_SELECTOR)
                if await arrow.count() > 0:
                    print("Intro page detected – clicking ▶️ …")
                    await arrow.first.click()
                    # Give FormSG a moment to load the next page
                    await page.wait_for_timeout(500)
                    continue
                # No arrow, no login button → keep waiting a bit (no reload)
                await page.wait_for_timeout(500)

            # At this point the login button exists
            await page.click(f"text={LOGIN_BTN_TEXT}")
            print("Please complete Singpass authentication on your device…")

            try:
                await page.wait_for_selector("select[name='show']", timeout=300_000)
            except PlaywrightTimeoutError:
                print("❌ Timed out waiting for Singpass. Exiting.")
                return

            # Fill form
            await page.select_option("select[name='show']", SHOW_VALUE[args.show])
            await page.select_option("select[name='tickets']", str(args.tickets))
            if args.mobility:
                await page.check("input[name='mobility']")

            await page.click("button:has-text('Submit')")
            await page.wait_for_selector("text=Application submitted", timeout=10_000)
            print("✅ Application submitted successfully!")

        finally:
            await context.close()
            await browser.close()


def main():
    parser = argparse.ArgumentParser(
        description="Automate NDP 2025 ballot submission (educational PoC)")
    parser.add_argument("--show", choices=SHOW_VALUE.keys(), default="ndp",
                        help="Show to ballot for (default: ndp)")
    parser.add_argument("--tickets", type=int, choices=[2, 4, 6], default=4,
                        help="Ticket count (default: 4)")
    parser.add_argument("--schedule", help="ISO-8601 local time to start (optional)")
    parser.add_argument("--headless", action="store_true", help="Headless mode")
    parser.add_argument("--mobility", action="store_true", help="Wheelchair seating")
    args = parser.parse_args()

    if args.schedule:
        when = datetime.fromisoformat(args.schedule)
        asyncio.run(wait_until(when))

    asyncio.run(submit_application(args))


if __name__ == "__main__":
    main()
