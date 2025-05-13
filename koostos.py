from ttkbootstrap import Style
from ttkbootstrap.constants import *
import ttkbootstrap as ttk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import threading
import re

# ----- Logger ----
def log_event(message):
    output_box.insert("end", f"{time.strftime('%H:%M:%S')} - {message}\n")
    output_box.see("end")
    

# ----- Event Handler(place holder) ---- 
class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        log_event(f"🟢 File created: {event.src_path}")

    def on_modified(self, event):
        log_event(f"🟡 File modified: {event.src_path}")

# ---- IP Format Checker ----
def is_valid_ip(ip):
    pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    return re.match(pattern, ip) is not None

# ----- Fake IP Analysis -----
def analyze_ip():
    ip = ip_entry.get().strip()
    if not manual_mode.get():
        log_event("⚠️ Manual mode is disabled. Enable it to analyze a specific IP.")
        return
    
    log_event(f"🔍 Starting analysis on {ip}...")
    # Simulated log: pretend we found something weird
    time.sleep(1)
    log_event(f"⚠️ Unsual activity detected from {ip} on port 53.")
    log_event(f"🧠 suggested action: Simulate block or export report.")

# ----- Simulated Local Network Scan -----
def scan_my_network():
    log_event("♺ Scanning local network (192.168.1.0/24)....")
    time.sleep(2)

    # Simulated devices: (IP, Label)
    devices = [
        ("192.168.1.10", "Apple Inc."),
        ("192.168.1.12", "PC-Home"),
        ("192.168.1.14", "Unknown Devices")
    ]

    log_event("✅ Found 3 active devices:")

    flagged = 0
    for ip, label in devices:
        log_event(f"📍 {ip} - {label}")
        if "Unknown" in label or ip.endswith(".14"):
            flagged += 1
            log_event(f"⚠️ Suspicious activity from {ip} ({label})")
            log_event(f"🧠 Suggested action: Simulate block or investigate manually.")

    # Final summary
    log_event("🔍 Scan complete.")
    log_event(f"Summary: {len(devices)} devices found, {flagged} flagged for review.")

# ----- Toggle Manual Entry -----
def toggle_manual_mode():
    if manual_mode.get():
        ip_entry.config(state="normal")
        analyze_btn.config(state="normal")
    else:
        ip_entry.delete(0, END)
        ip_entry.config(state="disabled")
        analyze_btn.config(state="disabled")

# ---- GUI Setup ----
app = ttk.Window(themename="darkly")
app.title("Koostos - Offline Security Monitor")
app.geometry("750x550")

style = Style()

# ----- Header ----
ttk.Label(app, text="🛡️ Koostos - Offline Security Monitor", font=("Helvetica", 18, "bold")).pack(pady=15)

# ----- Scan Button ----
scan_btn = ttk.Button(app, text="Scan My Network", bootstyle=SUCCESS, command=scan_my_network)
scan_btn.pack(pady=10)

# ----- Manaul IP Mode -----
manual_mode = ttk.BooleanVar(value=False)

toggle_frame = ttk.Frame(app)
toggle_frame.pack(pady=5)
manual_checkbox = ttk.Checkbutton(toggle_frame, text="Enable Manual IP Entry", variable=manual_mode, command=toggle_manual_mode)
manual_checkbox.pack()

# ----- IP Entry + Analyze -----
ip_frame = ttk.Frame(app)
ip_frame.pack(pady=5)

ttk.Label(ip_frame, text="Target IP:").pack(side=LEFT, padx=5)
ip_entry = ttk.Entry(ip_frame, width=25, state="disabled")
ip_entry.pack(side=LEFT, padx=5)

analyze_btn = ttk.Button(ip_frame, text="Analyze IP", bootstyle=WARNING, command=analyze_ip, state="disabled")
analyze_btn.pack(pady=15)

# ----- Output Box -----
output_box = ttk.Text(app, height=15, width=90, wrap="word")
output_box.pack(pady=15)

app.mainloop()