import time
import subprocess
import sys

RASA_PROCESS_NAME = "rasa" 

def check_rasa_running():
    """Check if Rasa process is running"""
    output = subprocess.check_output(["ps", "aux"])
    processes = output.decode().splitlines()
    for p in processes:
        if RASA_PROCESS_NAME in p:
            return True
    return False

def restart_rasa():
    """Restart Rasa process"""
    subprocess.run(["rasa", "run"])

if __name__ == "__main__":
    while True:
        if not check_rasa_running():
            print("Rasa process not running!")
            restart = input("Restart Rasa? (y/n): ")
            if restart.lower() == 'y' or not restart:
                print("Restarting Rasa...")
                restart_rasa()
        time.sleep(10)