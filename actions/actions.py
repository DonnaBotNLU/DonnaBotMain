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

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> None:

        # Get the user's message
        user_message = tracker.latest_message.get("text")

        # Query ChatGPT API for a response to the user's message
        suggested_intent = self.ask_chatgpt(user_message)

        if suggested_intent:
            # Format the NLU data
            formatted_nlu_data = f"""- intent: {suggested_intent}
  examples: |
    - {user_message}
"""
            # Append NLU data to the NLU file
            with open("data/nlu.yml", "a") as nlu_file:
                nlu_file.write(formatted_nlu_data)

            # Format the domain data
            formatted_domain_data = f"""- {suggested_intent}
"""
            # Append domain data to the domain file
            with open("domain.yml", "a") as domain_file:
                domain_file.write(formatted_domain_data)

            # Format the stories data
            formatted_stories_data = f"""- story: {suggested_intent} path
  steps:
  - intent: {suggested_intent}
  - action: utter_{suggested_intent}
"""
            # Append stories data to the stories file
            with open("data/stories.yml", "a") as stories_file:
                stories_file.write(formatted_stories_data)

            # Provide feedback to the user
            dispatcher.utter_message(text=f"I've added your question to my knowledge base under the intent '{suggested_intent}'. Thank you!")
        else:
            dispatcher.utter_message(text="I couldn't determine the intent for this response.")

        return []

    def ask_chatgpt(self, question: Text) -> Tuple[Text, Text, Text]:
        api_key = ''
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
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        # Check if the response contains the 'choices' key
        if 'choices' in response_data:
            # Access the first choice and extract the response text
            response_text = response_data['choices'][0]['message']['content']
            # Extract the suggested intent
            suggested_intent = response_data['choices'][0]['message']['metadata']['intent']['name']
            # Generate a story based on the user's message and GPT response
            story_text = f"utter_{suggested_intent}: {response_text}"
            # Generate a rule based on the suggested intent
            rule_text = f"\n- rule: {suggested_intent}_rule\n  steps:\n  - intent: {suggested_intent}\n  - action: utter_{suggested_intent}\n"
            return suggested_intent, story_text, rule_text
        else:
            # Handle the case when the 'choices' key is not present
            return None, "Sorry, I couldn't understand your question.", ""


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
from rasa_sdk.events import SlotSet
import subprocess

class ExecuteCommandAction(Action):
    def name(self):
        return "action_execute_command"

    def run(self, dispatcher, tracker, domain):
        # Define the command or Python file to execute
        command = "/Modules/linuxtoolbox.py"

        # Execute the command or Python file
        try:
            subprocess.run(command, shell=True, check=True)
            dispatcher.utter_message("Command executed successfully.")
        except subprocess.CalledProcessError as e:
            dispatcher.utter_message(f"Error executing module: {e}")
        
        return []


