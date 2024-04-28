#!/usr/bin/env python3.8


import subprocess
import os
import threading
import time
import sys
from getch import getch

def install_requirements():
    """Install dependencies from requirements.txt using Python"""
    try:
        # Ensure setuptools is installed for Python 
        import subprocess
        subprocess.run(["python3.8", "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    except subprocess.CalledProcessError as e:
        # If the process returned a non-zero exit status, print the error output
        print(f"Error occurred while installing requirements: {e.stderr}", file=sys.stderr)
        # Re-raise the exception to allow the caller to handle it
        raise

def check_requirements():
    print("Checking requirements...")
    # Start the requirement check in a separate thread
    requirement_thread = threading.Thread(target=install_requirements)
    requirement_thread.start()

    # Create a flag to indicate if the user wants to skip the check
    skip_check = False

    # Function to check for key press
    def check_key_press():
        nonlocal skip_check
        getch()  # Wait for a key press
        skip_check = True
        print("Skipping requirements check.")

    # Start a thread to check for key press
    key_press_thread = threading.Thread(target=check_key_press)
    key_press_thread.daemon = True  # Daemon thread will exit when the main thread exits
    key_press_thread.start()

    # Wait for 5 seconds or until the user presses a key
    for i in range(5, 0, -1):
        print(f"Press any key to skip ({i} seconds remaining)...")
        time.sleep(1)
        if skip_check:
            requirement_thread.join(timeout=1)  # Wait for the thread to finish
            return

    # If the user doesn't press a key, wait for the requirement check to finish
    requirement_thread.join()
    print("Finished checking requirements.")


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

import os
import webbrowser

import os
import webbrowser

def setup_bot_files(directory, api_key_filename, discord_api_filename, deepseek_keys_filename):
    # Define the file paths
    api_key_file = os.path.join(directory, api_key_filename)
    discord_api_file = os.path.join(directory, discord_api_filename)
    deepseek_keys_file = os.path.join(directory, "Actions", deepseek_keys_filename)

    # Check if the directory exists, if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Check if the "Actions" directory exists, if not, create it
    actions_dir = os.path.join(directory, "Actions")
    if not os.path.exists(actions_dir):
        os.makedirs(actions_dir)

    # Flag to check if any file needs to be created
    files_created = False

    # Check if the files exist, if not, create them
    for file_path in [api_key_file, discord_api_file, deepseek_keys_file]:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write("")  # Write an empty string to the file
            files_created = True

    # If any file was created, open the webpages
    if files_created:
        print("api keys not found! Created api_key.txt, discord_api.txt, and deepseek_keys.txt; redirecting...")
        # Uncomment the following lines if you want to open the webpages
        #webbrowser.open("https://discord.com/developers/applications")
        #webbrowser.open("https://beta.openai.com/account/api-keys")
        #webbrowser.open("https://platform.deepseek.com/")



import requests

def generate_requirements_txt(packages, filename='requirements.txt'):
    with open(filename, 'w') as file:
        for package in packages:
            response = requests.get(f'https://pypi.org/pypi/{package}/json')
            if response.status_code == 200:
                data = response.json()
                latest_version = data['info']['version']
                file.write(f'{package}=={latest_version}\n')
            else:
                print(f'Failed to fetch information for {package}')

# List of packages
packages = [
#tbd
]


if __name__ == "__main__":
    print("installing requirements...")
    # Generate requirements.txt
    install_requirements()
    print("Checking files for Api Keys...")
    # Call the function with the directory and file names
    setup_bot_files("DonnaBotMain", "api_key.txt", "discord_api.txt", "deepseek_keys.txt")
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