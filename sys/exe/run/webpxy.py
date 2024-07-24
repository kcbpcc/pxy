import os
import subprocess
import sys
import time
import logging

def get_pid_on_port(port):
    """Get the PID of the process running on the given port."""
    try:
        result = subprocess.run(['lsof', '-t', f'-i:{port}'], capture_output=True, text=True)
        if result.stdout.strip():
            return result.stdout.strip()
    except Exception as e:
        logging.error(f"Failed to get PID on port {port}: {e}")
    return None

def start_server(port, logfile):
    """Start the server on the given port and log output to the logfile."""
    try:
        with open(logfile, 'w') as f:
            subprocess.Popen(['nohup', 'python3', '-m', 'http.server', str(port)], stdout=f, stderr=subprocess.STDOUT)
        logging.info(f"Server started on port {port} and logging to {logfile}")
    except Exception as e:
        logging.error(f"Failed to start server on port {port}: {e}")

def run_webchrtspxy():
    """Run the webchrtspxy.py script."""
    try:
        result = subprocess.run(['python3', 'webchrtspxy.py'], capture_output=True, text=True)
        if result.returncode == 0:
            logging.info("webchrtspxy.py ran successfully.")
        else:
            logging.error(f"webchrtspxy.py encountered an error:\n{result.stderr}")
    except Exception as e:
        logging.error(f"Failed to run webchrtspxy.py: {e}")

def run_webinputpxy():
    """Run the webinputpxy.py script."""
    try:
        result = subprocess.run(['python3', 'webinputpxy.py'], capture_output=True, text=True)
        if result.returncode == 0:
            logging.info("webinputpxy.py ran successfully.")
        else:
            logging.error(f"webinputpxy.py encountered an error:\n{result.stderr}")
    except Exception as e:
        logging.error(f"Failed to run webinputpxy.py: {e}")

def main():
    """Main function to manage the server and run the webchrtspxy and webinputpxy scripts."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting script...")

    try:
        os.chdir(os.path.expanduser('~/pxy/sys/exe/run'))
    except Exception as e:
        logging.error(f"Failed to change directory: {e}")
        sys.exit(1)

    port = 8000
    logfile = 'server.log'

    while True:
        pid = get_pid_on_port(port)
        if pid:
            logging.info(f"Process {pid} is already running on port {port}. Skipping server start.")
        else:
            logging.info(f"No process found running on port {port}. Starting server.")
            start_server(port, logfile)

        logging.info("Running webchrtspxy.py")
        run_webchrtspxy()

        logging.info("Running webinputpxy.py")
        run_webinputpxy()

        try:
            from cyclepxy import cycle
            logging.info("Waiting for 30 seconds...")
            time.sleep(cycle)
        except ImportError as e:
            logging.error(f"Failed to import cycle from cyclepxy: {e}")
            break

if __name__ == "__main__":
    main()


