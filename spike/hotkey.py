"""Experiment 2: global hotkey via RegisterHotKey, delivered through the native event filter."""
import ctypes
from ctypes import wintypes

from PySide6.QtWidgets import QSystemTrayIcon

import probe

WM_HOTKEY = 0x0312
MODS = {"alt": 0x1, "ctrl": 0x2, "shift": 0x4, "win": 0x8}
MOD_NOREPEAT = 0x4000
HOTKEY_ID = 0xB001

_u32 = ctypes.WinDLL("user32", use_last_error=True)
_u32.RegisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int, wintypes.UINT, wintypes.UINT]
_u32.UnregisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int]
_u32.GetForegroundWindow.restype = wintypes.HWND
_u32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]


def parse(spec):
    parts = [p.strip().lower() for p in spec.split("+")]
    mods = 0
    for p in parts[:-1]:
        mods |= MODS[p]
    key = parts[-1]
    if len(key) == 1:
        vk = ord(key.upper())
    elif key.startswith("f") and key[1:].isdigit():
        vk = 0x70 + int(key[1:]) - 1
    else:
        raise ValueError(f"unsupported key {key!r}")
    return mods, vk


def _fg_title():
    hwnd = _u32.GetForegroundWindow()
    buf = ctypes.create_unicode_buffer(256)
    _u32.GetWindowTextW(hwnd, buf, 256)
    return hwnd, buf.value


def install(spike, spec):
    mods, vk = parse(spec)
    ok = _u32.RegisterHotKey(spike.hwnd, HOTKEY_ID, mods | MOD_NOREPEAT, vk)
    if not ok:
        err = ctypes.get_last_error()
        hint = " (ERROR_HOTKEY_ALREADY_REGISTERED: another app owns it)" if err == 1409 else ""
        probe.log(f"HOTKEY registration FAILED for {spec}: error {err}{hint}; app keeps running")
        spike.tray.showMessage("RemindMe spike", f"Hotkey {spec} is unavailable", QSystemTrayIcon.MessageIcon.Warning, 4000)
        return
    probe.log(f"HOTKEY registered {spec}")
    spike.app.aboutToQuit.connect(lambda: _u32.UnregisterHotKey(spike.hwnd, HOTKEY_ID))

    def on_hotkey(msg):
        prev_hwnd, prev_title = _fg_title()
        probe.log(f"HOTKEY fired; foreground was {prev_title!r}")
        spike.show_window("hotkey")
        from PySide6.QtCore import QTimer

        def check():
            fg, title = _fg_title()
            mine = int(spike.window.winId())
            probe.log(f"HOTKEY window is foreground: {fg == mine} (foreground now {title!r})")
        QTimer.singleShot(200, check)

    spike.dispatcher.on(WM_HOTKEY, on_hotkey)
