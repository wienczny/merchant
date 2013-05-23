import json
import bitcoinrpc

from decimal import Decimal

from merchant import Gateway, GatewayNotConfigured


class BitcoinGateway(Gateway):

    display_name = "Bitcoin"
    homepage_url = "http://bitcoin.org/"
    default_currency = "BTC"

    def __init__(self, settings):
        self.rpcuser = settings["RPCUSER"]
        self.rpcpassword = settings["RPCPASSWORD"]
        self.host = settings.get("HOST", "127.0.0.1")
        self.port = settings.get("PORT", "8332")
        self.account = settings["ACCOUNT"]
        self.minconf = settings.get("MINCONF", 1)

        self.connection = bitcoinrpc.connect_to_remote(
            self.rpcuser,
            self.rpcpassword,
            self.host,
            self.port
        )

    def get_new_address(self):
        return self.connection.getnewaddress(self.account)

    def get_transactions(self):
        return self.connection.listtransactions(self.account)

    def get_transactions_by_address(self, address):
        all_txns = self.get_transactions()
        return filter(lambda txn: txn.address == address, all_txns)

    def get_txns_sum(self, txns):
        return sum(txn.amount for txn in txns)

    def purchase(self, money, address, options=None):
        options = options or {}
        money = Decimal(str(money))
        txns = self.get_transactions_by_address(address)
        received = self.get_txns_sum(txns)
        response = [txn.__dict__ for txn in txns]
        if received == money:
            return {'status': 'SUCCESS', 'response': response}
        return {'status': 'FAILURE', 'response': response}
