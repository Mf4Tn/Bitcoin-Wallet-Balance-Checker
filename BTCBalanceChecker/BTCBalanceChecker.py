import requests

WALLETS_PATH = "wallet.txt"
BTC_WALLETS = []
BTC_PRICE_API = "http://api.bitcoincharts.com/v1/weighted_prices.json"
BLOCKCHAIN_API = "https://api.blockchain.info/haskoin-store/btc/address/[ADDRESS]/balance"

class btc_info():
    def last_24h():
        try:
            return requests.get(BTC_PRICE_API).json()["USD"]["24h"]
        except:
            return None
    def to_usd(amount):
        amount = float(amount)
        price = amount*float(btc_info.last_24h())
        return round(price)
    def get_balance(wallet):
        try:
            info = {
                "balance":0,
                "transactions":0,
                "total":0
            }
            get_info = requests.get(BLOCKCHAIN_API.replace('[ADDRESS]',wallet))
            if "error" not in get_info.text:
                get_info = get_info.json()
                balance = int(get_info["confirmed"])/100000000
                txs = int(get_info["txs"])
                total = int(get_info["received"])/100000000
            else:
                balance,txs,total = None,None,None
            info["balance"] = balance
            info["transactions"] = txs
            info["total"] = total
            return info
        except:
            return None

if __name__ == "__main__":
    wallets = open(WALLETS_PATH,"r").read().splitlines()
    for _ in wallets:
        if _ not in BTC_WALLETS:
            BTC_WALLETS.append(_)
    for wallet in BTC_WALLETS:
        wallet_info = btc_info.get_balance(wallet)
        if(wallet_info["balance"] != None):
            wallet_info["balance"] = btc_info.to_usd(wallet_info["balance"])
            wallet_info["total"] = btc_info.to_usd(wallet_info["total"])
            log = f"{wallet} | Current Balance ${wallet_info['balance']} | Total Balance ${wallet_info['total']} | Transactions {wallet_info['transactions']}"
            print(log)
            open(
                'wallets-balance.txt','a'
            ).write(log+'\n')
