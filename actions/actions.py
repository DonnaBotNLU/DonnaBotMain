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
import discord
from discord.ext import commands
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

class ActionSendToDiscord(Action):
    def name(self) -> Text:
        return "action_send_to_discord"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Check if the channel ID slot is set
        channel_id = tracker.get_slot("channel_id")
        dispatcher.utter_message("getting ID")
        if not channel_id:
            # If channel ID is not set, prompt the user to provide it
            dispatcher.utter_message("Please provide the Discord channel ID where you want to send the message.")
            return []

        # Extract the user's message
        user_message = tracker.latest_message.get("text")

        # Read API key from the file
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

        return []


class ActionSetChannelID(Action):
    def name(self) -> Text:
        return "action_set_channel_id"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the channel ID from the user's message
        channel_id = tracker.latest_message.get("text")

        # Save the channel ID as a slot
        return [SlotSet("channel_id", channel_id)]


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

