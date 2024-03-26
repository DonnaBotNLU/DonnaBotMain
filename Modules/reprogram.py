import csv
import json
from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionReprogram(Action):

    def name(self) -> Text:
        return "action_reprogram"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the latest user message from rasa
        latest_message = tracker.latest_message.get('text')
        
        # Or load the latest user message from stores.csv
        with open('stores.csv', 'r') as f:
            reader = csv.reader(f)
            latest_message = next(reader)[0]
        
        # Load the intents mapping
        with open('intents_mapping.json', 'r') as f:
            intents_mapping = json.load(f)
        
        # Lookup the intent for the user message
        intent = intents_mapping.get(latest_message, 'fallback')
        
        # Dispatch the intent to Rasa
        dispatcher.utter_message(intent)


        try:
            # Get the user's question
            question = tracker.latest_message.get("text")

            # Read API key from file
            api_key_file = "actions/keys.txt"

            try:
                with open(api_key_file, "r") as f:
                    api_key = f.read().strip()
            except FileNotFoundError:
                return[]
            
            try:
                with open(training_file, "r") as f:
                    training_file = f.read().strip()
            except FileNotFoundError:
                return[]

            url = "https://api.deepseek.com/v1/chat/completions"
            user_message1 = tracker.latest_message.get("text")
            payload = json.dumps({
                "messages": [
                    {
                        "content": "you are designed to train another chatbot; be simple and specific.",
                        "role": "system"
                    },
                    {
                        "content": "below is the chat logs between our bot and the user, i need you to make a nlu.yml file for rasa using this data. provide only the code and no talking." + training_file,
                        "role": "user"
                    }
                ],
                "model": "deepseek-coder",
                "frequency_penalty": 0,
                "max_tokens": 2000,
                "presence_penalty": 0,
                "stop": None,
                "stream": False,
                "temperature": 1,
                "top_p": 1
            })
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + api_key

            }

            response = requests.request("POST", url, headers=headers, data=payload)
            with open('../test_nlu.yml', 'w') as f:
                json.dump(response.text(), f)
            print("saving test_nlu.yml")                       
            print(response.text)

            # Process response and send back answer
            if response.status_code == 200:
                data = response.json()
                if "choices" in data and data["choices"]:
                    answer = data["choices"][0].get("message", {}).get("content", "No answer found.")
                    dispatcher.utter_message(text=answer)
                    user_message = tracker.latest_message.get("text")
                    with open('stores.csv', 'a') as f:
                        f.write(f"User: {user_message}\n")
                        f.write(f"Bot: {answer}\n")
                else:
                    dispatcher.utter_message(text="No results found.")
            else:
                dispatcher.utter_message(text="Sorry, I don't have an answer for that right now.")
        except Exception as e:
            dispatcher.utter_message(text="An error occurred while processing your request.")
            print(f"Error: {e}")



        return []

