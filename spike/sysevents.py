"""Experiment 3: sleep/resume/lock/unlock/clock-change detection and timer drift."""
import ctypes
import time
from ctypes import wintypes

from PySide6.QtCore import QElapsedTimer, QTimer

import probe

WM_SETTINGCHANGE = 0x001A
WM_TIMECHANGE = 0x001E
WM_POWERBROADCAST = 0x0218
WM_WTSSESSION_CHANGE = 0x02B1

PBT = {0x4: "APMSUSPEND", 0x7: "APMRESUMESUSPEND", 0x12: "APMRESUMEAUTOMATIC",
       0xA: "APMPOWERSTATUSCHANGE", 0x8013: "POWERSETTINGCHANGE"}
WTS = {1: "CONSOLE_CONNECT", 2: "CONSOLE_DISCONNECT", 3: "REMOTE_CONNECT", 4: "REMOTE_DISCONNECT",
       5: "SESSION_LOGON", 6: "SESSION_LOGOFF", 7: "SESSION_LOCK", 8: "SESSION_UNLOCK"}


class GUID(ctypes.Structure):
    _fields_ = [("Data1", wintypes.DWORD), ("Data2", wintypes.WORD), ("Data3", wintypes.WORD),
                ("Data4", ctypes.c_ubyte * 8)]

    @classmethod
    def parse(cls, s):
        import uuid
        u = uuid.UUID(s)
        g = cls()
        g.Data1, g.Data2, g.Data3 = u.time_low, u.time_mid, u.time_hi_version
        for i, b in enumerate(u.bytes[8:]):
            g.Data4[i] = b
        return g


class POWERBROADCAST_SETTING(ctypes.Structure):
    _fields_ = [("PowerSetting", GUID), ("DataLength", wintypes.DWORD), ("Data", ctypes.c_ubyte * 4)]


SETTINGS = {
    "CONSOLE_DISPLAY_STATE": "6fe69556-704a-47a0-8f24-c28d936fda47",
    "LIDSWITCH_STATE": "ba3e0f4d-b817-4094-a2d1-d56379e6a0f3",
    "SESSION_DISPLAY_STATUS": "2b84c20e-ad23-4ddf-93db-05ffbd7efca5",
}
_NAME_BY_BYTES = {bytes(GUID.parse(v)): k for k, v in SETTINGS.items()}

_u32 = ctypes.WinDLL("user32", use_last_error=True)
_wts = ctypes.WinDLL("wtsapi32", use_last_error=True)
_u32.RegisterPowerSettingNotification.argtypes = [wintypes.HANDLE, ctypes.POINTER(GUID), wintypes.DWORD]
_u32.RegisterPowerSettingNotification.restype = wintypes.HANDLE
_u32.RegisterSuspendResumeNotification.argtypes = [wintypes.HANDLE, wintypes.DWORD]
_u32.RegisterSuspendResumeNotification.restype = wintypes.HANDLE
_wts.WTSRegisterSessionNotification.argtypes = [wintypes.HWND, wintypes.DWORD]


def _clock_snapshot():
    return time.time(), time.monotonic(), time.perf_counter()


def install(spike, arm_seconds):
    hwnd = spike.hwnd
    for name, guid in SETTINGS.items():
        h = _u32.RegisterPowerSettingNotification(hwnd, ctypes.byref(GUID.parse(guid)), 0)
        probe.log(f"EVENTS power-setting {name}: {'registered' if h else 'FAILED ' + str(ctypes.get_last_error())}")
    h = _u32.RegisterSuspendResumeNotification(hwnd, 0)
    probe.log(f"EVENTS suspend/resume notification: {'registered' if h else 'FAILED ' + str(ctypes.get_last_error())}")
    ok = _wts.WTSRegisterSessionNotification(hwnd, 0)
    probe.log(f"EVENTS session notification: {'registered' if ok else 'FAILED ' + str(ctypes.get_last_error())}")

    def on_power(msg):
        what = PBT.get(msg.wParam, f"{msg.wParam:#x}")
        extra = ""
        if msg.wParam == 0x8013 and msg.lParam:
            s = ctypes.cast(msg.lParam, ctypes.POINTER(POWERBROADCAST_SETTING)).contents
            name = _NAME_BY_BYTES.get(bytes(s.PowerSetting), "?")
            extra = f" {name}={s.Data[0]}"
        probe.log(f"EVENT WM_POWERBROADCAST {what}{extra}")

    def on_session(msg):
        probe.log(f"EVENT WM_WTSSESSION_CHANGE {WTS.get(msg.wParam, msg.wParam)}")

    def on_time(msg):
        probe.log("EVENT WM_TIMECHANGE (system clock or time zone changed)")

    def on_setting(msg):
        try:
            what = ctypes.wstring_at(msg.lParam) if msg.lParam else ""
        except OSError:
            what = "?"
        if what in ("intl", "TimeZoneInformation", "Environment") or "ime" in what:
            probe.log(f"EVENT WM_SETTINGCHANGE {what!r}")

    spike.dispatcher.on(WM_POWERBROADCAST, on_power)
    spike.dispatcher.on(WM_WTSSESSION_CHANGE, on_session)
    spike.dispatcher.on(WM_TIMECHANGE, on_time)
    spike.dispatcher.on(WM_SETTINGCHANGE, on_setting)

    # Heartbeat: any gap between wall clock and the app's own clocks shows time spent asleep/frozen.
    state = {"last": _clock_snapshot(), "n": 0}
    qt_elapsed = QElapsedTimer()
    qt_elapsed.start()
    state["qt"] = qt_elapsed.elapsed()

    def beat():
        wall, mono, perf = _clock_snapshot()
        lw, lm, lp = state["last"]
        qt_now = qt_elapsed.elapsed()
        d_wall, d_mono, d_perf, d_qt = wall - lw, mono - lm, perf - lp, (qt_now - state["qt"]) / 1000
        state["last"], state["qt"] = (wall, mono, perf), qt_now
        state["n"] += 1
        if d_wall > 8 or state["n"] % 12 == 0:
            flag = "  <-- GAP" if d_wall > 8 else ""
            probe.log(f"HEARTBEAT wall={d_wall:.1f}s monotonic={d_mono:.1f}s perf_counter={d_perf:.1f}s qt={d_qt:.1f}s (expected 5){flag}")

    hb = QTimer()
    hb.setInterval(5000)
    hb.timeout.connect(beat)
    hb.start()
    spike._heartbeat = hb

    if arm_seconds:
        target = time.time() + arm_seconds
        probe.log(f"TIMER armed one-shot for {arm_seconds}s; due at wall-clock {time.strftime('%H:%M:%S', time.localtime(target))}")

        def fired():
            late = time.time() - target
            probe.log(f"TIMER one-shot fired {late:+.1f}s relative to its wall-clock due time")
        t = QTimer()
        t.setSingleShot(True)
        t.timeout.connect(fired)
        t.start(arm_seconds * 1000)
        spike._armed = t
