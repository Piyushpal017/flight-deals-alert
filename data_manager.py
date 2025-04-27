import requests
from dotenv import load_dotenv
load_dotenv()
import os



class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):    
        self.headers = {"Authorization": f"Bearer {os.getenv('TOKEN')}"}
        self.Sheety_endpoint_price = os.environ["SHEETY_ENDPOINT_PRICES"]
        self.Sheety_endpoint_users = os.environ["SHEETY_ENDPOINT_USERS"]
        self.destination_data = {}
        self.customer_data = {} 

    def get_destination_data(self):
        response = requests.get(self.Sheety_endpoint_price, headers=self.headers)
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
            response = requests.put(url=f"{self.Sheety_endpoint_price}/{city['id']}", json=new_data, headers=self.headers)
            print(response.text)

    def get_customer_chat_id(self):
        response = requests.get(self.Sheety_endpoint_users, headers=self.headers)
        result = response.json()
        self.customer_data = result["users"]
        return self.customer_data
