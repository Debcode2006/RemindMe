# Spike results

Machine: ASUS TUF Gaming A15 (Ryzen 7 7435HS, 15.8 GB), Windows 11 build 26300, Python 3.12.7,
PySide6-Essentials 6.12.0, PyInstaller 6.22.3 (`--onedir --windowed`, default excludes, 101 MB on disk).
Sleep model: Modern Standby only (S0 Low Power Idle); no S3, no hibernate.

## 1. PySide6 memory and startup (packaged build)

| Metric | Result |
|---|---|
| Startup to ready (Qt app + tray + native filter) | ~250 ms |
| Idle RAM, private working set (Task Manager "Memory") at 20 s and 95 s | 19.0 MB |
| RAM with New Reminder window open | 20.7 MB |
| Total working set incl. shared DLL pages | ~51 MB idle, ~61 MB with window |
| Idle CPU | 0.03 CPU-seconds over 30 s (~0.1%) |

The 50 MB target holds under the private-working-set definition. Total working set is just above it,
so release notes should state which metric is used.

## 2. Global hotkey

- `RegisterHotKey` (Ctrl+Alt+R) delivered through a Qt native event filter works from another
  foreground app (tested from Chrome and VS Code with synthetic keypresses).
- Hotkey to first paint: ~65 ms for the first window creation, ~60 ms afterwards (window is reused).
- The window became the foreground window every time.
- Conflict: a second instance gets error 1409 (ERROR_HOTKEY_ALREADY_REGISTERED); the app keeps running.
- Gotcha: Qt hands each native message to the filter twice. Handlers must be idempotent or deduplicate
  per message id (message, wParam, lParam, time).

## 3. Sleep / resume / unlock / clock change

(pending manual run)
