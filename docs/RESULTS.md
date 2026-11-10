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

Run on the packaged build across three sleeps (2 s, ~12 min, ~56 min) with a lock/unlock around the last two.

| Question | Result |
|---|---|
| Are classic suspend/resume messages delivered on this Modern Standby-only laptop? | Yes. `APMSUSPEND`, `APMRESUMEAUTOMATIC` and `APMRESUMESUSPEND` arrived on every sleep and wake. |
| Display state / session events | `CONSOLE_DISPLAY_STATE` (on, dim, off), `SESSION_LOCK` and `SESSION_UNLOCK` arrived. The lock came right after resume; unlock came when the user signed in. |
| Clock change | `WM_TIMECHANGE` arrived at resume (the system corrects its clock on wake). A manual clock or time-zone change was not tested. |
| Lid switch | No `LIDSWITCH_STATE` event was logged; unclear whether the lid was used. Not required, because suspend/resume already covers it. |
| Do the app's clocks include sleep time? | Yes. Wall clock, `time.monotonic`, `perf_counter` and `QElapsedTimer` all advanced by the full sleep duration (706 s and 3364 s gaps). |
| Does a long one-shot `QTimer` fire on time across sleep? | **No.** A 600 s timer armed at 21:31:32 was due at 21:41:32 but fired at 22:49:14, **4061 s late**. Qt timers only count awake time: ~485 s awake before the final resume plus ~115 s after matches the observed firing time. |
| Does a short repeating `QTimer` recover after resume? | Yes. The 5 s heartbeat resumed immediately and detected the gap on its first tick. |

### Design consequences

- A single long one-shot `QTimer` cannot be the only trigger. A reminder due during sleep would
  fire late by the sleep duration (or, if it was due while awake time remained, never when expected).
- Re-query SQLite and re-arm the timer on `APMRESUMEAUTOMATIC`, `SESSION_UNLOCK` and `WM_TIMECHANGE`.
- Add a cheap safety net: cap the timer at about 30-60 s and compare against the wall clock each tick.
  Idle CPU stays near zero, and it also covers missed events.
- Show recovery after unlock as well as resume, since resume happens behind the lock screen.
- Still untested: manual clock/time-zone change, and behaviour when a reminder is due while the lid is closed.
