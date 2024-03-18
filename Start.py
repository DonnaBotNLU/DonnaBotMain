import subprocess
import time
import shutil 
import sys

def print_rainbow(message):
    colors = [
        '\033[91m',  # Red
        '\033[93m',  # Yellow
        '\033[92m',  # Green
        '\033[96m',  # Cyan
        '\033[94m',  # Blue
        '\033[95m',  # Magenta
    ]
    for color in colors:
        sys.stdout.write(color + message + '\033[0m')
        sys.stdout.flush()
        time.sleep(0.2)  # Adjust speed as needed

def start_rasa_actions():
    subprocess.Popen(['rasa', 'run', 'actions'])

def start_rasa_shell():
    subprocess.Popen(['rasa', 'shell'])

if __name__ == "__main__":
    print("What do you want to do?")
    print("1. Train Rasa")
    print("2. Run Rasa shell and actions server")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        print_rainbow("Starting Training")
        subprocess.Popen(['rasa', 'train'])
    elif choice == "2":
        start_rasa_actions()
        time.sleep(5)  # Wait for actions server to start (adjust delay as needed)
        start_rasa_shell()
    else:
        print("Invalid choice. Please enter 1 or 2.")
