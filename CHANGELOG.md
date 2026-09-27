# Changelog

## 1.0.0 — 2026-09-27

- First release: writes `nowplaying.json` on track / play-state change and a
  5 s heartbeat; writes `closed` on shutdown.
- Example stdlib HTTP server and reader with live position and stale detection.
- Smoke test against a fake MusicBee API.
