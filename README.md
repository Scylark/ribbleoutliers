# Ribble Outliers 2027, partner microsite

Live at https://scylark.github.io/ribbleoutliers/ behind a password gate.

## How it works

- The page is AES-encrypted. This repo only ever contains ciphertext, so the copy and pricing are not readable from the source.
- Minted links from `links.csv` carry the key in the URL fragment (`#k=...`), so prospects click straight through without typing anything. A bare visit shows the access-code screen.
- Access code: shared privately. To change it, edit `index.src.html` locally (kept outside this repo, in the Ribble Cycles/Microsite folder), run `python3 tools/encrypt.py "NEWCODE" index.src.html index.html`, update the links, and push.

## Tracking, live

Every visit logs to the private Google Sheet "Outliers site tracking" (vicivelo@gmail.com): open, 10-second heartbeats (read time), scroll depth, KOM view, tab clicks, tier expands, and contact clicks, each tagged with the prospect code from the minted link.

Read time per session = highest heartbeat count x 10 seconds.

The collector is a Google Apps Script web app bound to the sheet. `collector/apps-script.gs` holds the code for reference.

## Files

- `index.html` - the encrypted page served by GitHub Pages
- `img/` - photography and brand assets
- `links.csv` - minted per-prospect links for outreach
- `tools/encrypt.py` - rebuilds `index.html` from the private source
- `collector/apps-script.gs` - the tracking collector code
