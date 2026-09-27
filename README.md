# MusicBee → Homepage Now Playing

A [MusicBee](https://getmusicbee.com) plugin that shares the track you're playing
with a [Homepage](https://gethomepage.dev) dashboard card.

```
MusicBee ──plugin──▶ %APPDATA%\MusicBee\HomepageNowPlaying\nowplaying.json
                              │  on track / play-state change + every 5 s
examples/server.py ◀──────────┘  (or your own API)  GET /now-playing
        │
Homepage customapi widget ◀───┘
```

The card shows the track, artist, album and a live status line such as
`▶ Playing · 1:14 / 5:09`. The time keeps moving between updates, and the
card says **MusicBee closed** when MusicBee isn't running.

- **The plugin opens no network port.** It only writes one small JSON file.
- **No SDK or NuGet needed to build.** It compiles with the C# compiler that
  ships with Windows' .NET Framework 4.x.
- **No admin rights needed.** MusicBee loads it from your per-user plugin folder.

## Quick start

1. **Build and install the plugin** (PowerShell, from the repo root):
   ```powershell
   .\build.ps1 -Install
   ```
   Restart MusicBee. Check that **Homepage Now Playing** is ticked under
   *Edit → Preferences → Plugins*.
2. **Serve the JSON to Homepage** with the bundled example server (Python 3.11+,
   standard library only):
   ```powershell
   python examples\server.py          # http://0.0.0.0:8788/now-playing
   ```
3. **Add the card** to Homepage's `services.yaml`:
   ```yaml
   - Media:
       - Now Playing:
           icon: mdi-music-circle
           description: MusicBee
           widget:
             type: customapi
             url: http://host.docker.internal:8788/now-playing
             refreshInterval: 5000
             display: list
             mappings:
               - field: title
                 label: Track
               - field: artist
                 label: Artist
               - field: album
                 label: Album
               - field: status_line
                 label: Status
   ```
   Homepage fetches widget URLs server-side. If Homepage runs in Docker,
   `localhost` means the container itself, so use `host.docker.internal`
   (add `extra_hosts: ["host.docker.internal:host-gateway"]` on Linux hosts).

More detail:
- [docs/homepage-setup.md](docs/homepage-setup.md): Docker networking,
  running the server at logon, troubleshooting.
- [docs/json-format.md](docs/json-format.md): the file the plugin writes and
  the fields the server returns, if you want to build your own endpoint.

## Requirements

- Windows with .NET Framework 4.x. This is standard on Windows 10 and 11.
- MusicBee 3.x.
- Python 3.11+ for the example server only.

## Testing

```powershell
.\tests\run-smoke-test.ps1
```

This drives the plugin through a fake MusicBee API, so no MusicBee is needed.
It covers:
- startup
- pause
- the empty-title fallback to the file name
- JSON escaping
- the 5-second heartbeat
- shutdown

Exit code 0 means all checks passed.

## Uninstall

In MusicBee, open *Preferences → Plugins* and disable or uninstall **Homepage
Now Playing**. That also deletes its `HomepageNowPlaying` data folder.
Alternatively, delete `%APPDATA%\MusicBee\Plugins\mb_HomepageNowPlaying.dll`
while MusicBee is closed.

## Privacy

The file holds the current track's title, artist, album and position.
`examples/server.py` binds to all interfaces by default, so anyone who can
reach that port on your network can read it. Use `--host 127.0.0.1` if
Homepage runs on the same machine without Docker, or firewall the port.

## Licence

[MIT](LICENSE) for this plugin.

`src/MusicBeeInterface.cs` is MusicBee's plugin API definition, bundled
unmodified from the
[DiscordBee](https://github.com/sll552/DiscordBee) project under
[Apache-2.0](LICENSES/Apache-2.0.txt). See
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

This project is not affiliated with MusicBee or Homepage.
