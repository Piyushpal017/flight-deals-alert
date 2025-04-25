import requests
from dotenv import load_dotenv
load_dotenv()
import os

Sheety_endpoint = os.environ["SHEETY_ENDPOINT"]

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):    
        self.headers = {"Authorization": f"Bearer {os.getenv('TOKEN')}"}
        self.destination_data = {} 

    def get_destination_data(self):
        response = requests.get(Sheety_endpoint, headers=self.headers)
        result = response.json()
        self.destination_data = result["prices"]
        return self.destination_data
        
    def update_destination_data(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{Sheety_endpoint}/{city['id']}", json=new_data, headers=self.headers)
            print(response.text)
