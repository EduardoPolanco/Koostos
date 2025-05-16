from ttkbootstrap import Style
from ttkbootstrap.constants import *
import ttkbootstrap as ttk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import threading
import re
import os
import platform
import subprocess

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

# ----- Simulated Local Network Scan -----
def ping_device(ip):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=2
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False

def get_mac_address(ip):
    try:
        result = subprocess.check_output(["arp", "-n", ip]).decode()
        mac_match = re.search(r"(([a-FA-F0-9]{2}[:-]){5}[a-fA-F0-9]{2})", result)
        if not mac_match:
            return "N/A"
        return mac_match.group(0)
    except Exception:
        return "N/A"

def scan_my_network():
    log_event("-" * 60)
    start = time.time()
    log_event(f"🕛 Scan started at {time.strftime('%H:%M:%S')}")
    log_event("♻ Scanning local network (192.168.1.0/24)....")
    log_event("⏳ Please wait 5 seconds while scanning...")
    time.sleep(1)

    devices = []
    for i in range(1, 10):
        ip = f"192.168.1.{i}"
        if ping_device(ip):
            label = "Detected Device"
            mac = get_mac_address(ip)
            devices.append((ip, label, mac))
    if not devices:
        log_event("⚠️ No devices found.")
        return

    log_event(f"✅ Found {len(devices)} active devices(s):")
    flagged = 0

    for idx, (ip, label, mac) in enumerate(devices, start =1):
        log_event(f"{idx}. 📍 {ip}")
        # Simple condition to simulate a flag (customize this logic later if needed)
        if ip.endswith(".14"):
            flagged += 1
            log_event(f"⚠️ Suspicious activity from{ip}")

    # Final summary
    duration = round(time.time() - start, 2)
    log_event(f"🕛 Scan duration: {duration} seconds.")
    log_event("🔍 Scan complete.")
    log_event(f"Summary: {len(devices)} devices found, {flagged} flagged for review.")
    
    with open("koostos_scan_log.txt", "a") as f:
        f.write(f"\n--- {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        for idx, (ip, label, mac) in enumerate(devices, start=1):
            f.write(f"{idx}. {ip}\n")
        f.write(f"Scan duration: {duration} seconds\n")
        f.write(f"Flagged: {flagged} devices(s)\n")

# ---- GUI Setup ----
app = ttk.Window(themename="darkly")
app.title("Koostos - Offline Security Monitor")
app.geometry("750x550")

style = Style()

# ----- Header ----
ttk.Label(app, text="🛡️ Koostos - Offline Security Monitor", font=("Helvetica", 18, "bold")).pack(pady=15)

# ----- Scan Button ----
scan_btn = ttk.Button(app, text="Scan My Network", bootstyle=SUCCESS, command=lambda: threading.Thread(target=scan_my_network).start())
scan_btn.pack(pady=10)

# ----- Output Box -----
output_box = ttk.Text(app, height=15, width=90, wrap="word")
output_box.pack(pady=15)

app.mainloop()