import time, random, logging

from models.accounts import Accounts
from utils.first_message import first_message
from utils.logs import logger
from config import *

from src.random_transactions import start_random_transaction
from src.deploy_owlto import start_deploy_owlto
from src.wrap_unwrap import start_wrap_unwrap
from src.check_balance import start_balance
from src.mint_nft import start_mint_nft
from src.bridge import start_bridge


def main():
    logging.getLogger("web3").setLevel(logging.CRITICAL)
    logging.getLogger("urllib3").setLevel(logging.CRITICAL)

    accounts_manager = Accounts()
    accounts_manager.loads_accs()
    accounts = accounts_manager.accounts
    random.shuffle(accounts)

    action = input("> 1. Бридж Sepolia > Unichain\n"
                   "> 2. Wrap/Unwrap\n"
                   "> 3. Деплой на owlto\n"
                   "> 4. Случайные транзакции\n"
                   "> 5. Минт нфт\n"
                   "> 6. Баланс UNICHAIN ETH\n"
                   ">> ")

    print("-"*50+"\n")
    
    if action == "1":
        start_bridge(accounts)
    elif action == "2":
        start_wrap_unwrap(accounts)
    elif action == "3":
        start_deploy_owlto(accounts)
    elif action == "4":
        start_random_transaction(accounts)
    elif action == "5":
        start_mint_nft(accounts)
    elif action == "6":
        start_balance(accounts)
    else:
        logger.warning(f"Выбран вариант, которого нет!")


if __name__ == '__main__':
    first_message()
    main()
