import subprocess
import os


def display_menu():
    print("Welcome to Linux Toolbox Menu:")
    print("1. Disk Options")
    print("2. Repair options")
    print("3. Restart Donna AI")
    print("4. Install Donna AI [in progress]")
    print("5. Backup Donna AI")

def list_disks():
    try:
        # Use subprocess to execute a command to list available disks
        disk_list = subprocess.check_output(["lsblk", "-d", "-o", "name"])
        # Convert the output to string and split it by lines
        disk_list = disk_list.decode("utf-8").splitlines()
        # Remove the header from the disk list
        disk_list = [disk for disk in disk_list[1:] if disk]
        return disk_list
    except subprocess.CalledProcessError as e:
        print(f"Error listing disks: {e}")
        return []

def execute_disk_action(action_number):
    if action_number == 1:
        print("Select a source disk to copy:")
        source_disks = list_disks()
        if source_disks:
            for i, disk in enumerate(source_disks, start=1):
                print(f"{i}. {disk}")
            try:
                source_choice = int(input("Enter the number of the source disk: "))
                if 1 <= source_choice <= len(source_disks):
                    source_disk = source_disks[source_choice - 1]
                    print(f"You selected source disk: {source_disk}")

                    # Now list the destination disks excluding the source disk
                    print("\nSelect a destination disk to copy to:")
                    destination_disks = [disk for disk in source_disks if disk != source_disk]
                    for i, disk in enumerate(destination_disks, start=1):
                        print(f"{i}. {disk}")
                    try:
                        dest_choice = int(input("Enter the number of the destination disk: "))
                        if 1 <= dest_choice <= len(destination_disks):
                            dest_disk = destination_disks[dest_choice - 1]
                            print(f"You selected destination disk: {dest_disk}")
                            
                            # Prompt for confirmation
                            confirm = input("Do you want to continue? (y/n): ")
                            if confirm.lower() == 'y':
                                # Add logic to perform the copy operation using dd command
                                copy_disks(source_disk, dest_disk)
                            else:
                                print("Operation canceled.")
                        else:
                            print("Invalid choice. Please enter a number between 1 and", len(destination_disks))
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                else:
                    print("Invalid choice. Please enter a number between 1 and", len(source_disks))
            except ValueError:
                print("Invalid input. Please enter a number.")
        else:
            print("No disks found.")
    elif action_number == 2:
        print("Executing Repair options...")
        # Replace this line with the command you want to execute for Action 2
    elif action_number == 3:
        print("Restarting Donna AI...")
        # Replace this line with the command you want to execute for Action 3
    else:
        print("Invalid action number")

def copy_disks(source_disk, dest_disk):
    try:
        print("Copying disks...")
        # Use subprocess to execute the dd command to copy disks
        subprocess.run(["dd", f"if=/dev/{source_disk}", f"of=/dev/{dest_disk}", "bs=4M", "status=progress"])
        print("Disk copy completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error copying disks: {e}")

def execute_action(action_number):
    if action_number == 1:
        execute_disk_action(1)
    elif action_number == 2:
        print("Executing Repair options...")
        # Replace this line with the command you want to execute for Action 2
    elif action_number == 3:
        print("Restarting Donna AI...")
        # Replace this line with the command you want to execute for Action 3
    elif action_number == 4:
        print("Installing Donna AI [in progress]...")
        # Replace this line with the command you want to execute for Action 4
    elif action_number == 5:
        print("Backing up Donna Model...")
        directory = "./Documents/models/"
        try:
            # List all files in the directory
            files = os.listdir(directory)
            
            # Filter out the desired file based on your criteria
            desired_file = next((file for file in files if file.endswith('.zip')), None)
            
            if desired_file:
                # Perform the backup operation
                print(f"Backing up {desired_file}...")
                # Add your backup logic here
            else:
                print("No ZIP file found in the directory")
        except Exception as e:
            print(f"Error fetching file: {e}")
    else:
        print("Invalid action number")

def main():
    while True:
        display_menu()
        try:
            choice = int(input("Enter your choice (1-5): "))
            if 1 <= choice <= 5:
                execute_action(choice)
            else:
                print("Please enter a number between 1 and 5")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
