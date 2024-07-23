import os
import subprocess
import sys
import time

def is_wsl():
    try:
        with open('/proc/version', 'r') as f:
            return 'Microsoft' in f.read() or 'WSL' in f.read()
    except FileNotFoundError:
        return False

def get_pid_on_port(port):
    result = subprocess.run(['lsof', '-t', f'-i:{port}'], capture_output=True, text=True)
    if result.stdout.strip():
        return result.stdout.strip()
    return None

def start_server(port, logfile):
    with open(logfile, 'w') as f:
        subprocess.Popen(['nohup', 'python3', '-m', 'http.server', str(port)], stdout=f, stderr=subprocess.STDOUT)

def run_webchrtspxy():
    result = subprocess.run(['python3', 'webchrtspxy.py'], capture_output=True, text=True)
    if result.returncode == 0:
        print("webchrtspxy.py ran successfully.")
    else:
        print(f"webchrtspxy.py encountered an error:\n{result.stderr}")

def main():
    if not is_wsl():
        print("Not running on WSL. Exiting.")
        sys.exit()

    print("Running on WSL")
    os.chdir(os.path.expanduser('~/pxy/sys/exe/run/web'))

    port = 8000
    logfile = 'server.log'

    while True:
        pid = get_pid_on_port(port)
        if pid:
            print(f"Process {pid} is already running on port {port}. Skipping server start.")
        else:
            print(f"No process found running on port {port}")
            print(f"Starting server on port {port}")
            start_server(port, logfile)
            print(f"Server started and logging to {logfile}")

        print("Running webchrtspxy.py")
        run_webchrtspxy()

        print("Waiting for 30 seconds...")
        time.sleep(30)

if __name__ == "__main__":
    main()

