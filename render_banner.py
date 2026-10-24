#!/usr/bin/env python3
"""Render the Teknosoup security banner (1200x630 PNG) from template.html."""
import argparse
import json
import struct
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
KICKERS = {"CELAH KEAMANAN", "DIEKSPLOITASI AKTIF", "KEBOCORAN DATA", "MALWARE",
           "RANSOMWARE", "PHISHING", "PATCH PENTING", "ADVISORY"}


def png_size(path: Path):
    with open(path, "rb") as f:
        head = f.read(24)
    return struct.unpack(">II", head[16:24])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--headline", required=True)
    p.add_argument("--kicker", default="CELAH KEAMANAN")
    p.add_argument("--severity", default="high", choices=["critical", "high", "medium", "info"])
    p.add_argument("--icon", default="shield",
                   choices=["shield", "lock", "bug", "alert", "key", "server"])
    p.add_argument("--cve", default="")
    p.add_argument("--date", default="")
    p.add_argument("--template", default=str(HERE / "template.html"))
    p.add_argument("--out", required=True)
    a = p.parse_args()

    if len(a.headline.split()) > 8 or len(a.headline) > 60:
        print("WARNING: headline is longer than 8 words / 60 chars; it may wrap badly.", file=sys.stderr)
    if a.kicker.upper() not in KICKERS:
        print(f"WARNING: kicker '{a.kicker}' is not in the allowed list.", file=sys.stderr)

    data = {"headline": a.headline, "kicker": a.kicker.upper(), "severity": a.severity,
            "icon": a.icon, "cve": a.cve, "date": a.date}
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
        page.add_init_script(f"window.BANNER = {json.dumps(data, ensure_ascii=False)};")
        page.goto(Path(a.template).resolve().as_uri(), wait_until="networkidle")
        page.wait_for_selector("body[data-ready='1']")
        page.evaluate("document.fonts.ready")
        # Count rendered headline lines; more than 3 pushes into the CVE/footer area
        lines = page.evaluate(
            "(() => { const h = document.getElementById('headline');"
            " return Math.round(h.getBoundingClientRect().height / parseFloat(getComputedStyle(h).lineHeight)); })()")
        overflow = lines > 3
        page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": 1200, "height": 630})
        browser.close()

    w, h = png_size(out)
    print(f"Saved {out} ({w}x{h}, headline {lines} lines)")
    if overflow:
        print("ERROR: headline wraps to more than 3 lines. Shorten it and render again.", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
