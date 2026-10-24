---
name: security-banner
description: Create the 1200x630 PNG banner (hero + Open Graph image) for a Teknosoup security article. Use in Step 5 of every security article run, after the article and SEO fields are final.
---

# Security banner for teknosoup.com

Produces one 1200×630 PNG from a fixed HTML template, so every article banner looks consistent.
Do not design a new layout per run. Only fill in the fields below.

## Files in this skill
- `template.html` — the banner layout. Gets its content injected by the render script (window.BANNER); opening it directly shows a preview.
- `render_banner.py` — renders the template to PNG with headless Chromium (Playwright).

## One-time setup (skip if already installed)
```bash
pip install playwright
python -m playwright install chromium
```
If `pip` is blocked by the system, add `--break-system-packages` or use a virtualenv.

## Inputs to decide
| Field | Rule |
|---|---|
| `headline` | Max 8 words, max ~55 characters. A short hook, not the full article title. Indonesian. |
| `kicker` | One of: `CELAH KEAMANAN`, `DIEKSPLOITASI AKTIF`, `KEBOCORAN DATA`, `MALWARE`, `RANSOMWARE`, `PHISHING`, `PATCH PENTING`, `ADVISORY` |
| `severity` | `critical`, `high`, `medium` or `info`. Use the CVSS/advisory rating if there is one. Actively exploited means `critical`. |
| `icon` | `shield`, `lock`, `bug`, `alert`, `key` or `server` (pick the closest one to the story) |
| `cve` | Optional. The main CVE ID, e.g. `CVE-2026-12345`. Leave empty if none. |
| `date` | Article date, format `24 Okt 2026` |

Never put vendor logos, product screenshots, photos of real people or copyrighted images in the banner.

## Render
```bash
python render_banner.py \
  --headline "Celah Kritis di Router Populer Sedang Dieksploitasi" \
  --kicker "DIEKSPLOITASI AKTIF" \
  --severity critical \
  --icon bug \
  --cve "CVE-2026-12345" \
  --date "24 Okt 2026" \
  --out output/<slug>/banner.png
```
Run it from this skill's folder, or pass `--template /path/to/template.html`.

## Check before you continue
1. The file exists and is exactly 1200×630 (the script prints the size).
2. Open/view the PNG. The headline must not be cut off or overlap the icon. If it wraps past 3 lines,
   shorten the headline and render again.
3. Write the `alt` text: describe the banner plus the focus keyword naturally,
   e.g. "Banner artikel Teknosoup tentang celah keamanan router yang sedang dieksploitasi".

Then continue to the publish step and upload `banner.png` as the hero and meta image.
