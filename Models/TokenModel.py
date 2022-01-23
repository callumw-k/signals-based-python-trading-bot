class Token:
    def __init__(self, token_name, symbol, client):
        self.token_name = token_name
        self.symbol = symbol
        self.client = client
        self.bidPrice = float(self.client.get_orderbook_ticker(symbol=self.symbol)['bidPrice'])
        self.token_balance = float(self.client.get_asset_balance(asset=self.token_name)['free'])
        self.nominal_value = self.token_balance * self.bidPrice
        self.step_size = float(self.client.get_symbol_info(self.symbol)['filters'][2]['stepSize'])
        self.tick_size = float(self.client.get_symbol_info(self.symbol)['filters'][0]['tickSize'])

    def updateTokenBalance(self):
        self.token_balance = float(self.client.get_asset_balance(asset=self.token_name)['free'])
