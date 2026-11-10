"""Logging and memory probes for the spike."""
import ctypes
import os
import sys
import time
from ctypes import wintypes

_BASE = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(_BASE, "spike.log")
_T0 = time.perf_counter()


def log(msg):
    line = f"{time.strftime('%H:%M:%S')} +{time.perf_counter() - _T0:8.2f}s  {msg}"
    print(line, flush=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


class _PMC(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("PageFaultCount", wintypes.DWORD),
        ("PeakWorkingSetSize", ctypes.c_size_t),
        ("WorkingSetSize", ctypes.c_size_t),
        ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
        ("QuotaPagedPoolUsage", ctypes.c_size_t),
        ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
        ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
        ("PagefileUsage", ctypes.c_size_t),
        ("PeakPagefileUsage", ctypes.c_size_t),
        ("PrivateUsage", ctypes.c_size_t),
    ]


_k32 = ctypes.WinDLL("kernel32", use_last_error=True)
_k32.GetCurrentProcess.restype = wintypes.HANDLE
_k32.K32GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(_PMC), wintypes.DWORD]


def mem_mb():
    """Return (working_set_mb, private_bytes_mb) of this process."""
    pmc = _PMC()
    pmc.cb = ctypes.sizeof(_PMC)
    _k32.K32GetProcessMemoryInfo(_k32.GetCurrentProcess(), ctypes.byref(pmc), pmc.cb)
    return pmc.WorkingSetSize / 1048576, pmc.PrivateUsage / 1048576


def log_mem(label):
    ws, priv = mem_mb()
    log(f"MEM [{label}] working_set={ws:.1f} MB  private_bytes={priv:.1f} MB")
