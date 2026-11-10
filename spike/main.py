"""RemindMe technical spike: resident tray app used to measure memory/startup."""
import argparse
import sys
import time

from PySide6.QtCore import QAbstractNativeEventFilter, Qt, QTimer
from PySide6.QtGui import QAction, QColor, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMenu, QPushButton,
                               QSystemTrayIcon, QVBoxLayout, QWidget)
from ctypes import wintypes

import probe


class Dispatcher(QAbstractNativeEventFilter):
    """Routes raw Windows messages to registered handlers by message id."""

    def __init__(self):
        super().__init__()
        self._handlers = {}

    def on(self, msg_id, fn):
        self._handlers.setdefault(msg_id, []).append(fn)

    def nativeEventFilter(self, event_type, message):
        if bytes(event_type) == b"windows_generic_MSG":
            msg = wintypes.MSG.from_address(int(message))
            for fn in self._handlers.get(msg.message, ()):
                fn(msg)
        return False, 0


class NewReminderWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Reminder (spike)")
        self.resize(360, 140)
        self.trigger_t0 = None
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Title"))
        layout.addWidget(QLineEdit())
        layout.addWidget(QPushButton("Create Reminder"))
        self._painted = False

    def mark_trigger(self):
        self.trigger_t0 = time.perf_counter()
        self._painted = False

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self._painted and self.trigger_t0 is not None:
            self._painted = True
            probe.log(f"WINDOW first paint {(time.perf_counter() - self.trigger_t0) * 1000:.0f} ms after trigger")

    def closeEvent(self, event):
        event.ignore()  # stay resident; hide only
        self.hide()
        probe.log("WINDOW hidden")
        QTimer.singleShot(2000, lambda: probe.log_mem("window-hidden+2s"))


class SpikeApp:
    def __init__(self, app, args):
        self.app = app
        self.args = args
        self.window = None
        self.dispatcher = Dispatcher()
        app.installNativeEventFilter(self.dispatcher)

        # Hidden top-level widget: gives us a native HWND for message routing.
        self.msg_window = QWidget()
        self.hwnd = int(self.msg_window.winId())
        probe.log(f"message window hwnd={self.hwnd:#x}")

        self._build_tray()
        for secs in (5, 30, 120):
            QTimer.singleShot(secs * 1000, lambda s=secs: probe.log_mem(f"idle+{s}s"))
        if args.exit_after:
            QTimer.singleShot(args.exit_after * 1000, app.quit)

    def _build_tray(self):
        pm = QPixmap(32, 32)
        pm.fill(Qt.transparent)
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(QColor("#2d7ff9"))
        p.setPen(Qt.NoPen)
        p.drawEllipse(2, 2, 28, 28)
        p.end()
        self.tray = QSystemTrayIcon(QIcon(pm))
        menu = QMenu()
        a_new = QAction("New Reminder", menu)
        a_new.triggered.connect(lambda: self.show_window("tray-menu"))
        a_mem = QAction("Log memory now", menu)
        a_mem.triggered.connect(lambda: probe.log_mem("manual"))
        a_quit = QAction("Exit", menu)
        a_quit.triggered.connect(self.app.quit)
        for a in (a_new, a_mem, a_quit):
            menu.addAction(a)
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(
            lambda reason: self.show_window("tray-click") if reason == QSystemTrayIcon.Trigger else None)
        self.tray.show()

    def show_window(self, source):
        t0 = time.perf_counter()
        created = self.window is None
        if created:
            self.window = NewReminderWindow()
        self.window.mark_trigger()
        self.window.trigger_t0 = t0
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()
        probe.log(f"WINDOW shown via {source} (created={created}) show() took {(time.perf_counter() - t0) * 1000:.0f} ms")
        QTimer.singleShot(1500, lambda: probe.log_mem(f"window-open({source})+1.5s"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exit-after", type=int, default=0, help="quit after N seconds (0 = run until Exit)")
    ap.add_argument("--hotkey", default="ctrl+alt+r")
    ap.add_argument("--arm", type=int, default=0, help="arm a one-shot QTimer for N seconds")
    args = ap.parse_args()

    t0 = time.perf_counter()
    app = QApplication(sys.argv[:1])
    app.setQuitOnLastWindowClosed(False)
    spike = SpikeApp(app, args)
    probe.log(f"STARTUP python={sys.version.split()[0]} ready in {(time.perf_counter() - t0) * 1000:.0f} ms")
    probe.log_mem("startup")
    try:
        import hotkey
        hotkey.install(spike, args.hotkey)
    except ImportError:
        pass
    try:
        import sysevents
        sysevents.install(spike, args.arm)
    except ImportError:
        pass
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
