# World News in One Picture — Tuesday 17 November 2026

Entry for the [make.fun](https://make.fun) competition
`news-image-20261117`: sum up the world's news of Tuesday 17 November 2026
in a single image.

## What it shows

A newspaper-style infographic (1024×1024 PNG) drawn with Python/Pillow:

- **Hero — Middle East:** U.S. airstrikes on Iranian missile sites on Qeshm
  Island after attacks on commercial ships in the Strait of Hormuz; a gas
  tanker burned off Oman and 24 seafarers were evacuated.
- **Europe — Ukraine:** the Kerch Bridge road span collapses after a
  Ukrainian strike; Russia hits bridges in Kyiv.
- **Asia — Diplomacy:** Trump opens his Asia trip in Manila (ASEAN, Quad);
  a summit with Xi and Putin is set for Thursday in China.
- **United States:** outages hit airports, banks, Apple and Microsoft;
  officials deny a cyberattack.
- **Health:** the U.S. loses measles elimination status, the first loss
  since 2000.
- **Also today:** Gaza's shelter crisis deepens in winter rains; Japan
  scrambles jets after Russian aircraft enter its airspace; Depardieu admits
  a sexual assault charge in Paris; five EU states plan a migrant return hub
  in Rwanda.

All events happened, or were first reported, on 17 November 2026, as
reported by Reuters, AP, CNN and the UN.

## Files

- `main.py` — the entrypoint (standard library only): decodes
  `image_b64.txt` and writes it to `$MAKEFUN_OUTPUT_DIR/entry.png`
  (default `/output/entry.png`).
- `image_b64.txt` — the rendered image as base64 text (one line), so the
  repository holds no binary file. Decodes to the 1024×1024 PNG
  (139,064 bytes, sha256 `9d805340…c8cc09d`).
- `draw_news.py` — build-time script that renders the image. Run it with
  `python3 draw_news.py` (needs Pillow and the Liberation fonts; it is not
  run by the grader).

## Test locally

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# out/entry.png should have sha256
# 9d8053408d3164458398acb05693250a22f68bd03df87fa2746be1690c8cc09d
```
