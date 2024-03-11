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
import os
import requests
from typing import List, Dict, Any, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

class ActionUpdateNLUData(Action):
    def name(self):
        return "ActionUpdateNLUData"

    def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the user's message
        user_message = tracker.latest_message.get("text")

        # Read API key from the file
        api_key_file = "api_key.txt"
        with open(api_key_file, "r") as f:
            api_key = f.read().strip()

        # Query ChatGPT for a response
        chatgpt_response = self.ask_chatgpt(user_message, api_key)

        if chatgpt_response:
            # Send the response from ChatGPT to the user
            dispatcher.utter_message(text=chatgpt_response)
        else:
            # If ChatGPT couldn't generate a response, revert the last user utterance
            print("return_user_utterance")
            return [UserUtteranceReverted()]

        return []

    def ask_chatgpt(self, question: Text, api_key: str) -> Text:
        # Define your ChatGPT API parameters
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': 'text-davinci-003',
            'messages': [
                {'role': 'system', 'content': 'You are a bot.', 'position': 'end'},
                {'role': 'user', 'content': question, 'position': 'start'}
            ]
        }

        # Send a request to the ChatGPT API
        response = requests.post(url, headers=headers, json=payload)

        # Extract the response text from the API response
        response_data = response.json()
        if 'choices' in response_data:
            return response_data['choices'][0]['message']['content']
        else:
            print("failed")
            return None


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

