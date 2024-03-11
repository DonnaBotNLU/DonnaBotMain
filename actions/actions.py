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
import requests
from typing import Text, Dict, Any, Tuple
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionUpdateNLUData(Action):
    def name(self) -> Text:
        return "action_update_nlu_data"

    def run(self, dispatcher, tracker, domain):
        print("not implemented yet")
        return []


from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class PreTrain1Action(Action):
    def name(self):
        return "pre_train1"

    def run(self, dispatcher, tracker, domain):
        from rasa_denerator import RasaDenerator

        nlu_file = "data/nlu.md"
        actions_dir = "actions/"
        tag_dict = {"templates": "domain", "slots": "domain",
                    "entities": "domain"}
        output_file = "domain.yml"

        denerator = RasaDenerator(nlu_file=nlu_file,
                                  actions_dir=actions_dir,
                                  tag_dict=tag_dict,
                                  output=output_file)
        denerator.generate_domain()

        return [SlotSet("domain_generated", True)]

        
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

