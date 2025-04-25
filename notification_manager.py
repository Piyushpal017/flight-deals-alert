import requests
from dotenv import load_dotenv
import os
load_dotenv()


def telegram_bot_sendtext(bot_message):
    
    bot_token = os.getenv("BOT_TOKEN")
    bot_chatID = os.getenv("BOT_CHATID")
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()





