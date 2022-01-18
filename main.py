import requests
from time import time, sleep
import os
from HelperFunctions.MessageHelpers import *
from HelperFunctions.AcountHelpers import *
from Models.TokenModel import Token

from binance import Client
from binance.helpers import round_step_size


def getMessageData():
    res = requests.get("https://cryptosignalsapi.azurewebsites.net/api/Messages")
    res.headers['content-type'] = 'application/json; charset=utf8'
    data = res.json()
    return data


def getPrecision(symbol):
    return client.get_symbol_info(symbol=symbol)['baseAssetPrecision']


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # api_key = os.environ['API_KEY']
    # api_secret = os.environ['API_SECRET']
    api_key = '***REMOVED***'
    api_secret = '***REMOVED***'
    client = Client(api_key, api_secret)
    prev_message = ''
    while True:
        messages = []
        # Get the lastest last message.
        message_data = getMessageData()
        newest_message = message_data[-1]
        # Check if the latest message id is 1 greater than the previous message id

        # If yes, perform actions
        # If greater than one, loop over each message and perform tasks

        # Get the message title and the message body
        # print(newest_message)
        message_id = newest_message['id']
        if prev_message != '' and message_id == prev_message['id']:
            print("No change")
        elif prev_message != '' and int(prev_message['id']) + 1 == int(message_id):
            messages.append(newest_message)
        elif prev_message != '' and int(message_id) - int(prev_message['id']) > 1:
            missed_amount = int(message_id) - int(prev_message['id'])
            print(missed_amount)
            missed_messages = message_data[-missed_amount:]
            print(missed_messages)
            messages = missed_messages

        print(messages)
        for message in messages:
            # Checking for new Signal
            message_title = getMessageTitle(message)
            message_body = getMessageBody(message)
            coin_alert = checkIfTokenExists(message_title)
            messaged_changed = checkIfChange(prev_message, newest_message)
            new_signal = isNewSignal(message_body)

            # Checking for target one
            target_one = isTargetOne(message_body)
            # Checking if the signal is closed
            signal_closed = isSignalClose(message_body)

            if coin_alert and messaged_changed:
                coin = Token(getToken(message_title), getSymbol(message_title), client=client)
                print(coin.nominal_value, coin.step_size, coin.token_balance)

                if new_signal and coin.nominal_value < 10:
                    quantity = getBuyQuantity(client, coin)
                    new_order = placeOrder(client, coin.symbol, quantity, Client)
                    print(new_order)
                elif target_one:
                    quantity = getHalfAssetBalance(client, coin)
                    new_order = placeSellOrder(client, coin.symbol, quantity, Client)
                    print(new_order)
                elif signal_closed and coin.nominal_value > 10:
                    quantity = round_step_size(coin.token_balance - coin.step_size, coin.step_size)
                    new_order = placeSellOrder(client, coin.symbol, quantity, Client)
                    print(new_order)
                else:
                    print("Order Route, waiting")
            else:
                print("Waiting")
        prev_message = newest_message
        sleep(30 - time() % 30)
