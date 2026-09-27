# Homepage setup

## Where Homepage runs

Homepage fetches `customapi` URLs from its server, not from your browser.
Which URL to use depends on where Homepage runs:

| Homepage runs… | Widget `url` | Server flag |
|---|---|---|
| In Docker Desktop on the same Windows PC | `http://host.docker.internal:8788/now-playing` | default (`--host 0.0.0.0`) |
| Natively on the same PC | `http://127.0.0.1:8788/now-playing` | `--host 127.0.0.1` |
| On another machine | `http://<this-pc-ip>:8788/now-playing` | default, plus a firewall rule allowing that machine only |

On Linux Docker hosts, add this to the Homepage service:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

## Running the server at logon

1. Create `now-playing-server.vbs` somewhere permanent. It starts the server
   with no console window:
   ```vbscript
   CreateObject("WScript.Shell").Run "pythonw.exe ""C:\path\to\repo\examples\server.py""", 0, False
   ```
2. Press `Win+R` and run `shell:startup` to open your Startup folder.
3. Put a shortcut to that `.vbs` file in the Startup folder.

## Suggested card layouts

The quick-start card uses `display: list`, with one row each for Track, Artist,
Album and Status.

For a more compact card, map fewer fields:

```yaml
mappings:
  - field: title
    label: Track
  - field: status_line
    label: Status
```

To show only a percentage, use `field: progress_percent` with
`format: percent`.

## Troubleshooting

| Card shows | Check |
|---|---|
| `No data — is the MusicBee plugin installed?` | Restart MusicBee after installing. Check that the plugin is ticked in Preferences → Plugins. Check that `%APPDATA%\MusicBee\HomepageNowPlaying\nowplaying.json` exists. |
| `MusicBee closed` while MusicBee is open | The plugin was disabled, or it failed to load. Re-enable it and restart MusicBee. |
| API error | Open the widget URL in a browser on the Homepage host. If it fails, the server isn't running or the port is blocked. |
| Portable MusicBee: no file in `%APPDATA%` | Portable installs store data in their own folder. Run `server.py --file <path>\HomepageNowPlaying\nowplaying.json`. |
