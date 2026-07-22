import psutil

for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        cmdline = proc.info['cmdline']
        if cmdline and 'python' in proc.info['name'].lower():
            cmd_str = ' '.join(cmdline).lower()
            if 'uvicorn' in cmd_str or 'main:app' in cmd_str:
                print(f"Killing uvicorn process PID: {proc.info['pid']}")
                proc.kill()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

print("Python uvicorn processes killed (if any).")
