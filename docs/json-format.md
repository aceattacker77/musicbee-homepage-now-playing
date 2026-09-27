# JSON format

## What the plugin writes

`%APPDATA%\MusicBee\HomepageNowPlaying\nowplaying.json`. The folder is
MusicBee's persistent storage path, so a portable MusicBee install writes
inside its own folder instead.

```json
{
  "state": "playing",
  "title": "Idioteque",
  "artist": "Radiohead",
  "album": "Kid A",
  "album_artist": "Radiohead",
  "position_ms": 61000,
  "duration_ms": 309000,
  "updated_at": "2026-09-27T13:46:01.1138647Z",
  "plugin_version": "1.0.0"
}
```

| Field | Meaning |
|---|---|
| `state` | `playing`, `paused`, `stopped`, or `closed` (written when MusicBee shuts down or the plugin is disabled) |
| `title` | Track title; falls back to the file name when the tag is empty |
| `artist`, `album`, `album_artist` | Tags; empty string when missing |
| `position_ms`, `duration_ms` | Player position and track length at `updated_at`. Duration is `0` for streams. |
| `updated_at` | UTC time of the write, ISO 8601 with 7 fractional digits and a `Z` |
| `plugin_version` | Plugin version |

When it's written:
- on every track change and play-state change;
- every 5 s as a heartbeat while MusicBee runs.

Each write goes to `nowplaying.json.tmp` first, which is then swapped into
place, so readers never see half a file.

## Reading it correctly

- **Position:** while `state` is `playing`, the live position is
  `position_ms + (now − updated_at)`, capped at `duration_ms`.
- **Closed:** if `updated_at` is more than ~20 s old, the heartbeat has stopped
  and MusicBee is no longer running, even if the file still says `playing`
  (for example after a crash).
- **Retries:** if a read fails because the file is mid-swap, retry on the next
  refresh.

`examples/now_playing.py` implements all three.

## What `examples/server.py` returns

`GET /now-playing`:

```json
{
  "state": "playing",
  "state_label": "▶ Playing",
  "status_line": "▶ Playing · 1:14 / 5:09",
  "title": "Idioteque",
  "artist": "Radiohead",
  "album": "Kid A",
  "position_ms": 74358,
  "duration_ms": 309000,
  "progress_label": "1:14 / 5:09",
  "progress_percent": 24,
  "updated_at": "2026-09-27T13:46:01.1138647Z"
}
```

`state` is one of the following:

| `state` | Meaning |
|---|---|
| `playing`, `paused`, `stopped` | As written by the plugin |
| `closed` | MusicBee exited, or the heartbeat went stale |
| `no-data` | No file yet: the plugin isn't installed, or MusicBee hasn't started since |
| `unavailable` | The file couldn't be read this time; the next refresh retries |
