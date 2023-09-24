import json
import random
from time import sleep, time
from tqdm import tqdm
from web3 import Web3, HTTPProvider
from termcolor import cprint, colored

MANTLE_RPC_URL = "https://rpc.mantle.xyz"
ETH_RPC_URL = "https://eth.llamarpc.com"
PRIVATE_KEY = ""  # private-key кошелька
ADDRESS = ""  # вставляем адрес кошелька
ADDRESS_TO = ""  # оставляем пустым, будет отправлятся на рандом адрес
WORK_GWEI = 14  # максимальный газ для работы
web3 = Web3(HTTPProvider(MANTLE_RPC_URL))
ethw3 = Web3(HTTPProvider(ETH_RPC_URL))


def make_tx(address_from, address_to, amount):
    balance = web3.eth.get_balance(address_from)
    balance_eth = web3.from_wei(balance, 'ether')
    print(f"Баланс отправителя: {balance_eth} $MNT")

    transaction = {
        'nonce': web3.eth.get_transaction_count(address_from),
        'gasPrice': web3.to_wei('0.05', 'gwei'),
        'to': address_to,
        'value': web3.to_wei(amount, 'ether'),
        'gas': 210000,
    }

    signed_tx = web3.eth.account.sign_transaction(transaction, PRIVATE_KEY)

    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print(f"Хэш транзакции: {web3.to_hex(tx_hash)}")


def sleeping(from_sleep, to_sleep):
    x = random.randint(from_sleep, to_sleep)
    for i in tqdm(range(x), desc='sleep ', bar_format='{desc}: {n_fmt}/{total_fmt}'):
        sleep(1)

if __name__ == "__main__":
    nonce = 0
    while ethw3.eth.gas_price * (10 ** -9) <= WORK_GWEI:
        if nonce == 0:
            txn_number = web3.eth.get_transaction_count(ADDRESS)
            nonce = txn_number
        print(f'TX#{nonce}')
        print(f'gwei: {ethw3.eth.gas_price * (10 ** -9)}')
        amount = 0.0000001  # количество MNT для отправки
        make_tx(ADDRESS, ADDRESS_TO, amount)
        nonce += 1
        print(colored('---------------------------------------', 'red'))
        sleep(1)


        sleeping(5, 10)  # задержка между транзакциями
        print(colored('---------------------------------------', 'red'))



