import subprocess
import time
import os
import sys

def install_requirements():
    """Install dependencies from requirements.txt"""
    
    process = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    

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

def start_rasa_actions():  #Will need to be changed for the windows and mac versions, this is linux feature only
    directory = os.path.expanduser("~/DonnaBotMain")
    command = f'cd {directory} && rasa run actions'

    # Open a new terminal window and execute the command
    os.system(f'gnome-terminal -- bash -c "{command}; exec bash"')

def start_rasa_shell():
    # Define the directory you want to run the command in
    directory = os.path.expanduser("~/DonnaBotMain")
    command = f'cd {directory} && rasa shell'
    
    # Start the Rasa shell inside the specified directory
    os.system(f'gnome-terminal -- bash -c "{command}; exec bash"')

def start_web_check():
    # Set the directory path to the Rasa folder
    directory = os.path.expanduser("~/DonnaBotMain")

    # Set the path to the web_check.py file
    web_check_path = os.path.join(directory, "Modules", "Web_check.py")

    # Run the web_check.py file using subprocess
    subprocess.Popen(["python3", web_check_path])


if __name__ == "__main__":
    install_requirements()
    print("What do you want to do?")
    print("1. Train Rasa")
    print("2. Run Rasa shell and actions server")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        print_rainbow("Starting Training")
        subprocess.Popen(['rasa', 'train'])
    elif choice == "2":
        start_rasa_actions()
        time.sleep(10)  # Wait for actions server to start (adjust delay as needed)
        start_rasa_shell()
        start_web_check()
    else:
        print("Invalid choice. Please enter 1 or 2.")
