from telethon import TelegramClient, events, Button
import requests
from datetime import datetime
import os
import json

welcome = """
⚙️ Howdy. I am the best currency converter in the whole galaxy. I can:

- Show currency rates to EUR (Button "Rates")

- Convert currencies (Button "Convert")

- Conversion history (Button "History")

My capabilities reminder: /help
"""
value_bounds = "❌ Value must be a number between 0.01 and 1000000!"
reminder = "🔧 Remind my capabilities: /help"
currency_from = "💱 Choose currency to convert to."
currency_to = "💱 Choose currency to convert from."
chosen_currency_from = ""
chosen_currency_to = ""
enter_value = "💲 Enter amount to convert."
value = 0
rate_header = "📌 Current exchange rates: \n\n"
rate_format = "1 {} = {} EUR\n"
history_header = "🔍 History of {}: \n\n"
history_format = "{} {} => {} {}\n"
history_empty = "❌ Your history is empty!"
result_message = "💵 {} {} is {} {}"
same_currency = "❗️ You cannot choose same currency twice!"

class MenuButton:
    rates = "📊 Rates"
    convert = "💳 Convert"
    history = "📎 History"

api_id = 0
api_hash = ""
token = ""

userdata = {}
def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def byte_to_string(data):
    data = str(data)
    return data.replace("'", "").replace("b", "")

def convert_currency(amount, currency_from, currency_to):
    request = ("https://www.frankfurter.app/latest?amount={}&from={}&to={}").format(amount, currency_from, currency_to)
    response = requests.get(request)
    response = response.json()
    if (not "rates" in response.keys()): # Checks if required data is in data
        return None
    return response["rates"].get(currency_to)

def get_current_rates():
    request = "https://api.frankfurter.app/latest"
    response = requests.get(request)
    return response.json()["rates"]

def get_currencies():
    request = "https://api.frankfurter.app/latest"
    response = requests.get(request)
    return list(response.json()["rates"].keys())

def add_conversion(username, currency_from, currency_to, amount, result):
    timestamp = datetime.timestamp(datetime.now())
    conversion_data = {}
    conversion_data["from"] = currency_from
    conversion_data["to"] = currency_to
    conversion_data["amount"] = str(amount)
    conversion_data["result"] = str(result)
    
    conversions = {}
    if (username in list(userdata.keys())): # Checks if current users username is in history
        conversions = userdata.get(username)["conversions"]
    conversions[str(timestamp)] = conversion_data
    conversions_interface = {}
    conversions_interface["conversions"] = conversions
    userdata[username] = conversions_interface

def load_userdata():
    if (os.path.isfile("userdata.json")): # Checks if file exists
        with open("userdata.json", 'r') as json_file:
            global userdata
            userdata = dict(json.load(json_file))

def save_userdata():
    with open("userdata.json", 'w') as json_file:
        json.dump(userdata, json_file, indent=2, separators=(',',': '))

def get_history(username):
    if (userdata.get(username) == None): # Checks if userdata for a specific user is empty
        return history_empty
    result = ""
    result += history_header.format(username)
    conversions = userdata.get(username)["conversions"]
    for conversion_timestamp in conversions.keys(): # For every time in all available data
        current_conversion = conversions.get(conversion_timestamp)
        result += history_format.format(current_conversion.get("amount"), current_conversion.get("from"), current_conversion.get("result"), current_conversion.get("to"))
    return result

load_userdata()
currenices = get_currencies()
currenices.append("EUR")

bot = TelegramClient('xlconvertbot', api_id, api_hash).start(bot_token=token)

currency_buttons = []
currency_buttons.append([])
main_buttons = [[Button.text(MenuButton.rates)], [Button.text(MenuButton.convert)],  [Button.text(MenuButton.history)]]
for button in main_buttons: # For every button
    button[0].resize = True
row = 0
status = 0
for currency_id in range(len(currenices)): # For number in range currency count
    if (currency_id % 6 == 0): # Checks if currency id can be devided by 6 without remainder
        currency_buttons.append([])
        row +=1
    currency_buttons[row].append(Button.inline(currenices[currency_id], currenices[currency_id]))

@bot.on(events.NewMessage)
async def echo(event):
    sender = await event.get_sender()
    global status, chosen_currency_from, chosen_currency_to

    if status == 3: 
        value = event.text
        status = 0
        if (chosen_currency_from == chosen_currency_to): # Checks if currencies to and from are the same
            await event.respond(same_currency)
            return
        if not is_float(value) or float(value) > 10000000 or float(value) < 0.01: #Checks if entered value is within required bounds
            status = 0
            await event.respond(value_bounds)
            return
        result = convert_currency(float(value), chosen_currency_from, chosen_currency_to)
        response = result_message.format(value, chosen_currency_from, str(result), chosen_currency_to)
        add_conversion(sender.username, chosen_currency_from, chosen_currency_from, float(value), result)
        save_userdata()
        await event.respond(response)
        return
    
    match event.text:
        case "/start":
            await event.respond(welcome, buttons=main_buttons)
            return
        case "/help":
            await event.respond(welcome, buttons=main_buttons)
            return
        case MenuButton.convert:
            status = 1
            await event.respond(currency_from, buttons=currency_buttons)
            return
        case MenuButton.rates:
            response = ""
            response += rate_header
            current_rates = get_current_rates()
            for rate_name in current_rates.keys(): # For every name of rate in available rates
                response += rate_format.format(rate_name, current_rates.get(rate_name))
            await event.respond(response)
            return
            
        case MenuButton.history:
            await event.respond(get_history(sender.username))
            return
        case _:
            await event.respond(reminder)
            return

@bot.on(events.CallbackQuery)
async def echo(event):
    global status, chosen_currency_from, chosen_currency_to
    match status:
        case 0:
            await event.respond(reminder)
        case 1:
            chosen_currency_from = byte_to_string(event.data)
            status = 2
            await event.respond(currency_to, buttons=currency_buttons)
        case 2:
            chosen_currency_to = byte_to_string(event.data)
            status = 3
            await event.respond(enter_value)


def main():
    bot.run_until_disconnected()

if __name__ == '__main__': # Check if programa strāda galvena faila
    main()