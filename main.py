from telethon import TelegramClient, events, Button
from currency_converter import CurrencyConverter
import requests

converter_instance = CurrencyConverter()
api_id = 0
api_hash = ""
token = ""

currenices = ["EUR", "USD","JPY","BGN","CYP","CZK","DKK","EEK","GBP","HUF","LTL","LVL","MTL","PLN","ROL","RON","SEK","SIT","SKK","CHF","ISK","NOK","HRK","RUB","TRL","TRY","AUD","BRL","CAD","CNY","HKD","IDR","ILS","INR","KRW","MXN","MYR","NZD","PHP","SGD","THB","ZAR"]

welcome = """
Howdy. I am the best currency converter in the whole galaxy. I can:

- Show all currencies corresponding to EUR. (Button "Currrencies")

- Convert currencies (Button "Convert")

My capabilities reminder: /help
"""
reminder = "Remind my capabilities: /help"
currency_from = "Choose currency to convert to."
currency_to = "Choose currency to convert from."
chosen_currency_from = ""
chosen_currency_to = ""
enter_value = "Enter amount to convert."
value = 0

bot = TelegramClient('xlconvertbot', api_id, api_hash).start(bot_token=token)
currency_buttons = []
currency_buttons.append([])

main_buttons = [[Button.text("Currencies")], [Button.text("Convert")]]
for button in main_buttons:
    button[0].resize = True
row = 0

def byte_to_string(data):
    data = str(data)
    return data.replace("'", "").replace("b", "")

status = 0
for currency_id in range(len(currenices) - 1):
    if (currency_id % 6 == 0):
        currency_buttons.append([])
        row +=1
    
    currency_buttons[row].append(Button.inline(currenices[currency_id], currenices[currency_id]))
    

@bot.on(events.NewMessage)
async def echo(event):
    global status, chosen_currency_from, chosen_currency_to
    match event.text:
        case "/start":
            await event.respond(welcome, buttons=main_buttons)
        case "Convert":
            status = 1
            await event.respond(currency_from, buttons=currency_buttons)
        case "Currencies":
            pass
    if status == 3:
        value = event.text
        print(chosen_currency_from, chosen_currency_to)
        result = converter_instance.convert(int(value), chosen_currency_from, chosen_currency_to)
        result_message = value + chosen_currency_from + " is " + str(result) + chosen_currency_to
        status = 0
        await event.respond(result_message)

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

if __name__ == '__main__':
    main()



"""



to_convert = int(input("Введите сумму конвертации: "))

print("Доступные валюты:")
for currency in currenices:
    print(currency, end=" ")


#print()
"""