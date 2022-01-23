import os
import numpy as np

import binance.exceptions
from binance.helpers import round_step_size


def placeOrder(client, coin, quantity, Client):
    try:
        order = client.create_order(symbol=coin.symbol, side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET,
                                    quantity=quantity)
    except binance.exceptions.BinanceAPIException as e:
        print(f'Status Code = {e.status_code} and Error = {e.message}')
    else:
        return order


def placeLimitOrder(client, coin, quantity, Client):
    stop_price = round_step_size(coin.bidPrice * 0.93, coin.tick_size)
    try:
        order = client.create_order(symbol=coin.symbol, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_STOP_LOSS_LIMIT,
                                    timeInForce=Client.TIME_IN_FORCE_GTC, quantity=quantity,
                                    stopPrice=getNonScientificValue(stop_price),
                                    price=getNonScientificValue(
                                        round_step_size(stop_price * 0.99, coin.tick_size)))
    except binance.exceptions.BinanceAPIException as e:
        print('Place Limit Order Function', f'Status Code = {e.status_code} and Error = {e.message}')
    else:
        return order


def getRoundedQuantity(coin):
    return round_step_size(coin.token_balance - coin.step_size, step_size=coin.step_size)


def getNonScientificValue(value):
    return np.format_float_positional(value, trim='-')


def cancelAllOrders(client, coin):
    open_orders = client.get_open_orders(symbol=coin.symbol)
    for order in open_orders:
        result = client.cancel_order(symbol=coin.symbol, orderId=order['orderId'])
        print(result)
    coin.updateTokenBalance()


def placeSellOrder(client, symbol, quantity, Client):
    try:
        order = client.create_order(symbol=symbol, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_MARKET,
                                    quantity=quantity)
    except binance.exceptions.BinanceAPIException as e:
        print(f'Status Code = {e.status_code} and Error = {e.message}')
    else:
        return order


def getFirstSellAmount(coin):
    token_amount = float(coin.token_balance) * 0.6
    return round_step_size(token_amount, coin.step_size)


def getHalfAssetBalance(coin):
    token_amount = float(coin.token_balance) / 2
    return round_step_size(token_amount, coin.step_size)


def getTokenBalance(client, coin):
    account_balance = client.get_asset_balance(asset=coin.token_name)
    token_amount = float(account_balance['free'])
    return round_step_size(token_amount, coin.getStepSize()) - coin.getStepSize()


def getNewOrderQuantity(coin):
    # quantity = 50 / coin.bidPrice
    quantity = float(os.environ['AMOUNT']) / coin.bidPrice
    return round_step_size(quantity, coin.step_size)
