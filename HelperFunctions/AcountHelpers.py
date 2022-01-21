import binance.exceptions
from binance.helpers import round_step_size


def placeOrder(client, symbol, quantity, Client):
    try:
        order = client.create_order(symbol=symbol, side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET,
                                    quantity=quantity)
    except binance.exceptions.BinanceAPIException as e:
        print(f'Status Code = {e.status_code} and Error = {e.message}')
    else:
        return order


def placeLimitOrder(client, token, quantity):
    try:
        order = client.order_limit_sell(symbol=token.symbol, quantity=quantity, price='')
    except binance.exceptions.BinanceAPIException as e:
        print(f'Status Code = {e.status_code} and Error = {e.message}')
    else:
        return order


def placeSellOrder(client, symbol, quantity, Client):
    try:
        order = client.create_order(symbol=symbol, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_MARKET,
                                    quantity=quantity)
    except binance.exceptions.BinanceAPIException as e:
        print(f'Status Code = {e.status_code} and Error = {e.message}')
    else:
        return order


def getHalfAssetBalance(coin):
    token_amount = float(coin.token_balance) / 2
    return round_step_size(token_amount, coin.step_size)


def getTokenBalance(client, coin):
    account_balance = client.get_asset_balance(asset=coin.token_name)
    token_amount = float(account_balance['free'])
    return round_step_size(token_amount, coin.getStepSize()) - coin.getStepSize()


def getBuyQuantity(coin):
    quantity = 25 / coin.bidPrice
    return round_step_size(quantity, coin.step_size)
