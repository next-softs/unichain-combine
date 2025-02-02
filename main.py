from models.accounts import Accounts

from utils.first_message import first_message
from core.client import Client
from utils.logs import logger
from config import *

import threading, time, random

from contracts.Bridge import Bridge
from contracts.Uniswap import Uniswap
from contracts.MintNft import MintNft
from contracts.OwltoDeploy import OwltoDeploy

from models.nfts import nft_list


def start_bridge(clients):
    address_not_eth = []
    for client in clients:
        status, _ = client.start_bridge()
        if status:
            client.sleep(delay_actions)

        if _:
            address_not_eth.append(client.bridge.address)

    logger.info(f"{len(address_not_eth)} кошельков без баланса:")
    for a in address_not_eth: print(a)

def start_wrap_unwrap(clients):
    for client in clients:
        threading.Thread(target=client.wrap_unwrap).start()

        s = random.randint(*delay_actions)
        logger.info(f"ожидаем {s} сек для запуска след. кошелька..")
        time.sleep(s)

def start_deploy_owlto(clients):
    for client in clients:
        client.deploy_owlto()
        client.sleep(delay_actions)

def start_random_transactions(clients):
    for client in clients:
        threading.Thread(target=client.random_transactions).start()

        s = random.randint(*delay_actions)
        logger.info(f"ожидаем {s} сек для запуска след. кошелька..")
        time.sleep(s)

def start_mint_nft(accounts):
    mints = []
    for account in accounts:
        for nft in nft_list:
            mints.append(MintNft(account, nft))

    random.shuffle(mints)

    for mint in mints:
        if mint.mint():
            s = random.randint(*delay_actions)
            logger.info(f"ожидаем {s} сек для запуска след. кошелька..")
            time.sleep(s)

    logger.success("все nft получены")


def main():
    accounts_manager = Accounts()
    accounts_manager.loads_accs()
    accounts = accounts_manager.accounts

    action = input("> 1. Бридж Sepolia > Unichain\n"
                   "> 2. Wrap/Unwrap\n"
                   "> 3. Деплой на owlto\n"
                   "> 4. Случайные транзакции\n"
                   "> 5. Минт нфт\n"
                   ">> ")

    print("-"*50+"\n")

    if action != "5":
        clients = [Client(account) for account in accounts]
        random.shuffle(clients)

    if action == "1":
        start_bridge(clients)
    elif action == "2":
        start_wrap_unwrap(clients)
    elif action == "3":
        start_deploy_owlto(clients)
    elif action == "4":
        start_random_transactions(clients)
    elif action == "5":
        start_mint_nft(accounts)
    else:
        logger.warning(f"Выбран вариант, которого нет!")

if __name__ == '__main__':
    first_message()
    main()
