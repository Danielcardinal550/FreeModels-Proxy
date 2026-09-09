import socket
import threading
import time
import tkinter as tk
import urllib.request
import webbrowser
from pathlib import Path
from tkinter import messagebox

import uvicorn
from main import app

APP_NAME = "FreeModels Proxy"
DEVELOPER = "Reza Kazemi"
GITHUB_URL = "https://github.com/rkfcode"
DONATE_IRR_URL = "https://daramet.com/RKFi"
DONATE_GLOBAL_URL = "https://donatr.ee/rkfcode/"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000

BG = "#0A0D14"
SURFACE = "#111722"
SURFACE_2 = "#171F2D"
SURFACE_3 = "#0D131E"
BORDER = "#263244"
TEXT = "#F8FAFC"
MUTED = "#94A3B8"
PURPLE = "#7C5CFC"
PURPLE_HOVER = "#947CFF"
GREEN = "#22C55E"
RED = "#EF476F"
AMBER = "#F59E0B"
BLUE = "#38BDF8"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1120x760")
        self.minsize(920, 640)
        self.configure(bg=BG)
        self._set_window_icon()

        self.lang = "en"
        self.server = None
        self.thread = None
        self.started_at = None
        self.start_attempt = 0
        self.closed = False

        self.host = tk.StringVar(value=DEFAULT_HOST)
        self.port = tk.StringVar(value=str(DEFAULT_PORT))
        self.base_url = tk.StringVar(value=f"http://{DEFAULT_HOST}:{DEFAULT_PORT}/v1")
        self.status = tk.StringVar(value="Starting")
        self.runtime = tk.StringVar(value="00:00")
        self.connection = tk.StringVar(value="Checking…")

        self._build()
        self._apply_language()
        self.after(350, self.start_proxy)
        self.after(250, self._tick)
        self.protocol("WM_DELETE_WINDOW", self._close)

    def _asset_path(self, name):
        # Works both from source and from a PyInstaller one-file build.
        base = Path(getattr(__import__("sys"), "_MEIPASS", Path(__file__).resolve().parent))
        return base / "assets" / name

    def _set_window_icon(self):
        try:
            icon_path = self._asset_path("freemodels-proxy.ico")
            self.iconbitmap(default=str(icon_path))
        except Exception:
            pass

    def label(self, parent, text="", size=10, weight="normal", fg=TEXT, bg=None):
        return tk.Label(parent, text=text, font=("Segoe UI", size, weight),
                        fg=fg, bg=bg if bg else parent.cget("bg"))

    def button(self, parent, text, command, bg=SURFACE_2, fg=TEXT):
        return tk.Button(parent, text=text, command=command, cursor="hand2",
                         relief="flat", bd=0, bg=bg, fg=fg,
                         activebackground=PURPLE_HOVER, activeforeground=TEXT,
                         font=("Segoe UI Semibold", 10), padx=16, pady=10)

    def card(self, parent):
        return tk.Frame(parent, bg=SURFACE, highlightthickness=1,
                        highlightbackground=BORDER)

    def _build(self):
        root = tk.Frame(self, bg=BG)
        root.pack(fill="both", expand=True, padx=28, pady=24)

        # Header
        header = tk.Frame(root, bg=BG)
        header.pack(fill="x")

        icon = tk.Canvas(header, width=48, height=48, bg=BG, highlightthickness=0)
        icon.pack(side="left")
        icon.create_oval(3, 3, 45, 45, fill=PURPLE, outline="")
        icon.create_text(24, 24, text="AI", fill="white",
                         font=("Segoe UI Semibold", 11, "bold"))

        titlebox = tk.Frame(header, bg=BG)
        titlebox.pack(side="left", padx=13)
        self.title_lbl = self.label(titlebox, APP_NAME, 24, "bold")
        self.title_lbl.pack(anchor="w")
        self.subtitle_lbl = self.label(titlebox, "", 10, fg=MUTED)
        self.subtitle_lbl.pack(anchor="w", pady=(2, 0))

        self.language_btn = self.button(header, "FA", self.toggle_language, SURFACE_2)
        self.language_btn.pack(side="right")

        # Hero
        hero = self.card(root)
        hero.pack(fill="x", pady=(22, 14))

        left = tk.Frame(hero, bg=SURFACE)
        left.pack(side="left", fill="both", expand=True, padx=22, pady=20)

        self.status_caption = self.label(left, "", 9, "bold", MUTED)
        self.status_caption.pack(anchor="w")

        row = tk.Frame(left, bg=SURFACE)
        row.pack(anchor="w", pady=(7, 0))
        self.dot = tk.Canvas(row, width=18, height=18, bg=SURFACE, highlightthickness=0)
        self.dot.pack(side="left", padx=(0, 8))
        self.dot_id = self.dot.create_oval(3, 3, 15, 15, fill=AMBER, outline="")
        self.status_lbl = self.label(row, "Starting", 20, "bold")
        self.status_lbl.pack(side="left")

        self.base_caption = self.label(left, "", 9, "bold", MUTED)
        self.base_caption.pack(anchor="w", pady=(16, 6))

        urlrow = tk.Frame(left, bg=SURFACE)
        urlrow.pack(fill="x")
        self.url_entry = tk.Entry(urlrow, textvariable=self.base_url, state="readonly",
                                  readonlybackground=SURFACE_3, fg=TEXT, relief="flat",
                                  font=("Cascadia Mono", 10))
        self.url_entry.pack(side="left", fill="x", expand=True, ipady=10)
        self.copy_btn = self.button(urlrow, "Copy", self.copy_url, PURPLE)
        self.copy_btn.pack(side="left", padx=(9, 0))

        controls = tk.Frame(hero, bg=SURFACE)
        controls.pack(side="right", padx=22, pady=20)
        self.start_btn = self.button(controls, "▶ Start Proxy", self.start_proxy, GREEN)
        self.start_btn.pack(fill="x", pady=(0, 8))
        self.stop_btn = self.button(controls, "■ Stop Proxy", self.stop_proxy, RED)
        self.stop_btn.pack(fill="x")

        # Stats
        stats = tk.Frame(root, bg=BG)
        stats.pack(fill="x", pady=(0, 14))
        stats.columnconfigure(tuple(range(4)), weight=1)
        self._stat(stats, 0, "HOST", self.host)
        self._stat(stats, 1, "PORT", self.port)
        self._stat(stats, 2, "UPTIME", self.runtime)
        self._stat(stats, 3, "CONNECTION", self.connection)

        # Quick actions
        actions = tk.Frame(root, bg=BG)
        actions.pack(fill="x", pady=(0, 14))
        self.docs_btn = self.button(actions, "◫ Open API Docs", self.open_docs)
        self.docs_btn.pack(side="left")
        self.test_btn = self.button(actions, "✓ Test Connection", self.test_connection)
        self.test_btn.pack(side="left", padx=8)
        self.restart_btn = self.button(actions, "↻ Restart", self.restart_proxy)
        self.restart_btn.pack(side="left")

        # Developer / Support section - intentionally prominent
        community = self.card(root)
        community.pack(fill="x", pady=(0, 14))
        c_left = tk.Frame(community, bg=SURFACE)
        c_left.pack(side="left", fill="both", expand=True, padx=20, pady=16)
        self.dev_title = self.label(c_left, "", 11, "bold")
        self.dev_title.pack(anchor="w")
        self.dev_name = self.label(c_left, "Reza Kazemi", 15, "bold", fg=PURPLE)
        self.dev_name.pack(anchor="w", pady=(4, 0))
        self.dev_link = self.label(c_left, "github.com/rkfcode", 9, fg=MUTED)
        self.dev_link.pack(anchor="w", pady=(2, 0))

        c_right = tk.Frame(community, bg=SURFACE)
        c_right.pack(side="right", padx=18, pady=16)
        self.github_btn = self.button(c_right, "◉ GitHub", lambda: webbrowser.open_new_tab(GITHUB_URL), "#1E293B")
        self.github_btn.pack(side="left", padx=4)
        self.irr_btn = self.button(c_right, "♥ IRR Support", lambda: webbrowser.open_new_tab(DONATE_IRR_URL), "#1D3340")
        self.irr_btn.pack(side="left", padx=4)
        self.global_btn = self.button(c_right, "◎ USD / Crypto", lambda: webbrowser.open_new_tab(DONATE_GLOBAL_URL), "#2A2140")
        self.global_btn.pack(side="left", padx=4)

        # Event log
        logcard = self.card(root)
        logcard.pack(fill="both", expand=True)
        loghead = tk.Frame(logcard, bg=SURFACE)
        loghead.pack(fill="x", padx=16, pady=(13, 7))
        self.log_title = self.label(loghead, "", 11, "bold")
        self.log_title.pack(side="left")
        self.clear_btn = self.button(loghead, "Clear", self.clear_log, SURFACE_2)
        self.clear_btn.pack(side="right")

        self.log = tk.Text(logcard, bg="#070B11", fg="#C7D2FE", relief="flat",
                           bd=0, font=("Cascadia Mono", 9), height=9,
                           insertbackground="white", wrap="word")
        self.log.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.write_log("Application started.")
        self.write_log("Developer: Reza Kazemi | GitHub: github.com/rkfcode")
        self.write_log("Proxy will start automatically…")

    def _stat(self, parent, column, title, var):
        box = self.card(parent)
        box.grid(row=0, column=column, sticky="nsew", padx=5)
        self.label(box, title, 8, "bold", MUTED).pack(anchor="w", padx=14, pady=(12, 3))
        value = self.label(box, "", 10, "bold")
        value.pack(anchor="w", padx=14, pady=(0, 12))
        var.trace_add("write", lambda *_: value.configure(text=var.get()))
        value.configure(text=var.get())

    def write_log(self, text):
        stamp = time.strftime("%H:%M:%S")
        self.log.insert("end", f"[{stamp}] {text}\n")
        self.log.see("end")

    def _set_status(self, text, color):
        self.status.set(text)
        self.status_lbl.configure(text=text)
        self.dot.itemconfigure(self.dot_id, fill=color)

    def _apply_language(self):
        en = self.lang == "en"
        if en:
            self.subtitle_lbl.configure(text="OpenAI-compatible local proxy for Cherry Studio")
            self.status_caption.configure(text="PROXY STATUS")
            self.base_caption.configure(text="CHERRY STUDIO BASE URL")
            self.copy_btn.configure(text="Copy")
            self.start_btn.configure(text="▶ Start Proxy")
            self.stop_btn.configure(text="■ Stop Proxy")
            self.docs_btn.configure(text="◫ Open API Docs")
            self.test_btn.configure(text="✓ Test Connection")
            self.restart_btn.configure(text="↻ Restart")
            self.dev_title.configure(text="DEVELOPED BY")
            self.github_btn.configure(text="◉ GitHub")
            self.irr_btn.configure(text="♥ IRR Support")
            self.global_btn.configure(text="◎ USD / Crypto")
            self.log_title.configure(text="LIVE ACTIVITY")
            self.clear_btn.configure(text="Clear")
            self.language_btn.configure(text="FA")
        else:
            self.subtitle_lbl.configure(text="پروکسی محلی سازگار با OpenAI برای Cherry Studio")
            self.status_caption.configure(text="وضعیت پروکسی")
            self.base_caption.configure(text="آدرس Base URL برای Cherry Studio")
            self.copy_btn.configure(text="کپی")
            self.start_btn.configure(text="▶ شروع پروکسی")
            self.stop_btn.configure(text="■ توقف پروکسی")
            self.docs_btn.configure(text="◫ مستندات API")
            self.test_btn.configure(text="✓ تست اتصال")
            self.restart_btn.configure(text="↻ راه‌اندازی مجدد")
            self.dev_title.configure(text="توسعه‌دهنده")
            self.github_btn.configure(text="◉ گیت‌هاب")
            self.irr_btn.configure(text="♥ حمایت ریالی")
            self.global_btn.configure(text="◎ حمایت ارزی / کریپتو")
            self.log_title.configure(text="فعالیت زنده")
            self.clear_btn.configure(text="پاک کردن")
            self.language_btn.configure(text="EN")

    def toggle_language(self):
        self.lang = "fa" if self.lang == "en" else "en"
        self._apply_language()

    def _port_open(self):
        try:
            with socket.create_connection((self.host.get(), int(self.port.get())), timeout=0.35):
                return True
        except OSError:
            return False

    def start_proxy(self):
        if self.thread and self.thread.is_alive():
            if self._port_open():
                self._set_status("Running" if self.lang == "en" else "در حال اجرا", GREEN)
            return

        if self._port_open():
            self._set_status("Running" if self.lang == "en" else "در حال اجرا", GREEN)
            self.connection.set("Ready")
            self.write_log("Port is already in use. Assuming proxy is already running.")
            return

        self._set_status("Starting…" if self.lang == "en" else "در حال شروع…", AMBER)
        self.connection.set("Starting")
        self.started_at = time.time()
        self.start_attempt += 1
        self.write_log(f"Starting proxy on {self.base_url.get()}")

        try:
            config = uvicorn.Config(
                app=app,
                host=self.host.get(),
                port=int(self.port.get()),
                reload=False,
                log_level="warning",
                access_log=False,
                log_config=None,
                use_colors=False,
            )
            self.server = uvicorn.Server(config)
            self.thread = threading.Thread(target=self._serve, daemon=True, name="FreeModelsProxy")
            self.thread.start()
            self.after(250, self._wait_ready, self.start_attempt)
        except Exception as exc:
            self._startup_failed(exc)

    def _serve(self):
        try:
            self.server.run()
        except BaseException as exc:
            self.after(0, lambda e=exc: self._startup_failed(e))

    def _wait_ready(self, attempt):
        if self.closed or attempt != self.start_attempt:
            return
        if self._port_open():
            self._set_status("Running" if self.lang == "en" else "در حال اجرا", GREEN)
            self.connection.set("Ready")
            self.write_log("Proxy is ready.")
            return
        if self.thread and self.thread.is_alive():
            self.after(250, self._wait_ready, attempt)
        else:
            self._startup_failed(RuntimeError("Server stopped before opening the port."))

    def _startup_failed(self, exc):
        if self.closed:
            return
        self.server = None
        self.thread = None
        self._set_status("Failed" if self.lang == "en" else "ناموفق", RED)
        self.connection.set("Failed")
        self.write_log(f"START ERROR: {exc}")
        messagebox.showerror(
            APP_NAME,
            ("Proxy could not start:\n" if self.lang == "en" else "پروکسی اجرا نشد:\n") + str(exc)
        )

    def stop_proxy(self):
        if self.server:
            self.write_log("Stopping proxy…")
            self.server.should_exit = True
            self._set_status("Stopping…" if self.lang == "en" else "در حال توقف…", AMBER)
            self.after(150, self._finish_stop)

    def _finish_stop(self):
        if self.thread and self.thread.is_alive():
            self.after(150, self._finish_stop)
            return
        self.server = None
        self.thread = None
        self.started_at = None
        self.runtime.set("00:00")
        self.connection.set("Stopped")
        self._set_status("Stopped" if self.lang == "en" else "متوقف", MUTED)
        self.write_log("Proxy stopped.")

    def restart_proxy(self):
        if self.server:
            self.server.should_exit = True
            self.after(350, self.start_proxy)
        else:
            self.start_proxy()

    def copy_url(self):
        self.clipboard_clear()
        self.clipboard_append(self.base_url.get())
        self.update()
        self.write_log("Base URL copied to clipboard.")

    def open_docs(self):
        webbrowser.open_new_tab(self.base_url.get().replace("/v1", "/docs"))

    def test_connection(self):
        def worker():
            try:
                url = self.base_url.get().replace("/v1", "/docs")
                with urllib.request.urlopen(url, timeout=4) as r:
                    ok = 200 <= r.status < 400
                if not ok:
                    raise RuntimeError(f"HTTP {r.status}")
                self.after(0, lambda: self._test_done(True, "Connection OK"))
            except Exception as exc:
                self.after(0, lambda e=exc: self._test_done(False, str(e)))
        threading.Thread(target=worker, daemon=True).start()

    def _test_done(self, ok, detail):
        if ok:
            self.connection.set("Ready")
            self.write_log("Connection test: OK")
            messagebox.showinfo(APP_NAME, "Proxy is reachable." if self.lang == "en" else "اتصال برقرار است.")
        else:
            self.connection.set("Failed")
            self.write_log(f"Connection test failed: {detail}")
            messagebox.showerror(APP_NAME, f"Connection test failed:\n{detail}")

    def clear_log(self):
        self.log.delete("1.0", "end")

    def _tick(self):
        if self.started_at and self.thread and self.thread.is_alive() and self._port_open():
            elapsed = int(time.time() - self.started_at)
            self.runtime.set(f"{elapsed // 60:02d}:{elapsed % 60:02d}")
        self.after(500, self._tick)

    def _close(self):
        self.closed = True
        if self.server:
            self.server.should_exit = True
        self.destroy()


if __name__ == "__main__":
    App().mainloop()
