# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os

class ActionSetWebsite(Action):
    def name(self) -> Text:
        return "action_set_website"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the URL from the user
        url = tracker.latest_message.get("text")

        home_dir = os.path.expanduser("~")

        # Construct the full path to the script file
        script_file_path = os.path.join(home_dir, "Modules", "web_check.py")

        # Open and manipulate the script file
        with open(script_file_path, "r+") as script_file:
            content = script_file.read()
            script_file.seek(0)
            script_file.truncate(0)
            new_content = content.replace('url = "https://example.com"', f'url = "{url}"')
            script_file.write(new_content)

        dispatcher.utter_message(f"Website URL set to {url}")

        return []


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import subprocess

class ActionGetDisposableEmail(Action):
    def name(self) -> Text:
        return "action_get_disposable_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Execute the script to get a disposable email
        result = subprocess.run(['python', 'get_disposable_email.py'], capture_output=True, text=True)
        if result.returncode == 0:
            disposable_email = result.stdout.strip()
            dispatcher.utter_message(text=f"Your disposable email address is: {disposable_email}")
        else:
            dispatcher.utter_message(text="Failed to retrieve a disposable email address.")
        return []


import discord
from discord.ext import commands
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, SlotSet

class ActionSendToDiscord(Action):
    def name(self) -> Text:
        return "action_send_to_discord"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extract the channel ID from the slot
        channel_id = tracker.get_slot("channel_id")
        if not channel_id:
            # If channel ID is not set, prompt the user to provide it
            dispatcher.utter_message("Please provide the Discord channel ID where you want to send the message.")
            return []

        # Extract the user's message
        user_message = tracker.latest_message.get("text")

        # Read Discord API key from the file
        api_key_file = "discord_api.txt"
        with open(api_key_file, "r") as f:
            api_key = f.read().strip()

        # Initialize the Discord bot
        bot = commands.Bot(command_prefix='!')

        # Define a function to send a message to Discord
        async def send_message_to_discord():
            await bot.wait_until_ready()
            channel = bot.get_channel(channel_id)
            await channel.send(user_message)

        # Run the Discord bot to send the message
        bot.loop.create_task(send_message_to_discord())

        # Call Rasa to process the user's message
        return [UserUtteranceReverted()]

class ActionSetChannelID(Action):
    def name(self) -> Text:
        return "action_set_channel_id"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the channel ID from the user's message
        channel_id = tracker.latest_message.get("text")

        # Save the channel ID as a slot
        return [SlotSet("channel_id", channel_id)]

def start_discord_bot(channel_id):
    # Read Discord API key from the file
    api_key_file = "discord_api.txt"
    with open(api_key_file, "r") as f:
        api_key = f.read().strip()

    # Initialize the Discord bot
    bot = commands.Bot(command_prefix='!')

    @bot.event
    async def on_ready():
        print('Bot is ready.')

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        # Call Rasa to process the received message
        # Extract user's message from the Discord message object
        user_message = message.content
        # Use Rasa to process the message and get a response
        rasa_response = ...  # Call Rasa with user_message
        # Send the Rasa response back to Discord
        await message.channel.send(rasa_response)

    # Start the Discord bot
    bot.run(api_key)


class ActionUpdateNLUData(Action):
    def name(self):
        return "ActionUpdateNLUData"
        
        # If OpenAI couldn't generate a response, revert the last user utterance
        return []


from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class PreTrain1Action(Action):
    def name(self):
        return "pre_train1"

    def run(self, dispatcher, tracker, domain):

        return []

        
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionTakeNote(Action):
    def name(self) -> Text:
        return "action_take_note"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extract the note from the user's message
        note = tracker.latest_message.get("text")
        
        # Save the note to a file or database
        with open("notes.txt", "a") as notes_file:
            notes_file.write(f"- {note}\n")
        
        # Send a confirmation message to the user
        dispatcher.utter_message(text="I've taken note of that.")

        return []

class ActionCopy(Action):
    def name(self) -> Text:
        return "action_copy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extract the note from the user's message
        note = tracker.latest_message.get("text")
        
        # Save the note to a file or database
        with open("clipboard.txt", "a") as notes_file:
            notes_file.write(f"- {note}\n")
        
        # Send a confirmation message to the user
        dispatcher.utter_message(text="Copied!")

        return []

class ActionPaste(Action):
    def name(self) -> Text:
        return "action_paste"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Read the notes from the file
        with open("clipboard.txt", "r") as notes_file:
            notes = notes_file.readlines()
        
        # Send the read notes as a message to the user
        if notes:
            for note in notes:
                dispatcher.utter_message(text=note.strip())
        else:
            dispatcher.utter_message(text="empty clipboard!")

        return []
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionReadNotes(Action):
    def name(self) -> Text:
        return "action_read_notes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Read the notes from the file
        with open("notes.txt", "r") as notes_file:
            notes = notes_file.readlines()
        
        # Send the read notes as a message to the user
        if notes:
            dispatcher.utter_message(text="Here are your notes:")
            for note in notes:
                dispatcher.utter_message(text=note.strip())
        else:
            dispatcher.utter_message(text="You haven't taken any notes yet.")

        return []

from rasa_sdk import Action
import subprocess
import threading

class ExecuteCommandAction(Action):
    def name(self):
        return "action_execute_command"

    def run(self, dispatcher, tracker, domain):
        # Define the command or Python file to execute
        command = "python3 ./Modules/linuxtoolbox.py"

        # Define a function to run the command
        def run_command():
            try:
                subprocess.run(["gnome-terminal", "--", "bash", "-c", command])
                dispatcher.utter_message("Command executed successfully.")
            except subprocess.CalledProcessError as e:
                dispatcher.utter_message(f"Error executing module: {e}")
                dispatcher.utter_message("Failed to execute command.")

        # Create a thread to run the command
        command_thread = threading.Thread(target=run_command)
        command_thread.start()

        return []

