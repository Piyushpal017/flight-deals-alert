#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from datetime import datetime, timedelta
import time
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import telegram_bot_sendtext

data_manager = DataManager()
flight_search = FlightSearch()

sheet_data = data_manager.get_destination_data()

ORIGIN_CITY_IATA = "DEL"

for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        time.sleep(2)
print(f"sheet_data:\n {sheet_data}")

data_manager.destination_data = sheet_data
data_manager.update_destination_data()

# retrieve customer chat id

customer_data = data_manager.get_customer_chat_id()

customer_chat_id = [row["whatIsYourTelegramChatId ?"] for row in customer_data]
    
# Search for flights

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6*30))

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}....")
    flights = flight_search.get_flight_price(ORIGIN_CITY_IATA, destination["iataCode"], from_time=tomorrow, to_time=six_month_from_today)
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: Rs. {cheapest_flight.price}")
    time.sleep(2)

    if cheapest_flight.price == "N/A":
        print(f"No direct flight to {destination['city']}. Looking for indirect flights....")
        stopover_flights = flight_search.get_flight_price(ORIGIN_CITY_IATA, destination["iataCode"], from_time=tomorrow, to_time=six_month_from_today, is_direct=False)
        cheapest_flight = find_cheapest_flight(stopover_flights)
        print(f"Cheapest indirect flight price is : Rs. {cheapest_flight.price}")


    # send notification on telegram
    if cheapest_flight.price != "N/A" and cheapest_flight.price <destination["lowestPrice"]:
        if cheapest_flight.stops == 0:
            telegram_bot_sendtext(f"Low price alert! Only Rs.{cheapest_flight.price} to fly direct "
                        f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                        f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}.")
        else:
             telegram_bot_sendtext(f"Low price alert! Only Rs.{cheapest_flight.price} to fly "
                        f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                        f"with {cheapest_flight.stops} stops"
                        f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}.")
        
        print(f"Check your email. Lower price flight found to {destination['city']}")


    



