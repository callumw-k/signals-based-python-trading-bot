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


if __name__ == '__main__':
    api_key = os.environ['API_KEY']
    api_secret = os.environ['API_SECRET']
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
        newest_message_id = newest_message['id']
        prev_message_exists = True if prev_message != '' else False
        if prev_message_exists and newest_message_id == prev_message['id']:
            print("No change")
        elif prev_message_exists and int(prev_message['id']) + 1 == int(newest_message_id):
            print("One message")
            messages.append(newest_message)
        elif prev_message_exists and int(newest_message_id) - int(prev_message['id']) > 1:
            missed_amount = int(newest_message_id) - int(prev_message['id'])
            missed_messages = message_data[-missed_amount:]
            messages = missed_messages
            print(f'Missed ${missed_amount}. Messages are : ${messages}')

        for message in messages:
            # Checking for new Signal
            message_title = getMessageTitle(message)
            message_body = getMessageBody(message)

            # Check if message contains token.
            coin_alert = checkIfTokenExists(message_title)

            # Check if new signal
            new_signal = isNewSignal(message_body)

            # Checking for target one
            target_one = isTargetOne(message_body)

            # Check for target two

            # Checking if the signal is closed
            signal_closed = isSignalClose(message_body)

            if coin_alert:
                coin = Token(getToken(message_title), getSymbol(message_title), client=client)
                if new_signal and coin.nominal_value < 10:
                    quantity = getBuyQuantity(coin)
                    new_order = placeOrder(client, coin.symbol, quantity, Client)
                    # set_limit_order=placeLimitOrder(client,coin,quantity)
                    print(new_order)
                elif target_one:
                    quantity = getHalfAssetBalance(coin)
                    new_order = placeSellOrder(client, coin.symbol, quantity, Client)
                    print(new_order)
                elif signal_closed and coin.nominal_value > 10:
                    quantity = round_step_size(coin.token_balance - coin.step_size, coin.step_size)
                    new_order = placeSellOrder(client, coin.symbol, quantity, Client)
                    print(new_order)
                else:
                    print("No Orders placed, waiting")
            else:
                print("Waiting")
        prev_message = newest_message
        sleep(60 - time() % 60)
