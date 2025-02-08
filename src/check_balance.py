from concurrent.futures import ThreadPoolExecutor
import random

from utils.logs import logger
from contracts.Uniswap import Uniswap
from config import *


def balance(acc):
    for i in range(10):
        try:
            client = Uniswap(acc)
            balance = float(client.balance()) + float(client.balance_weth())
            logger.info(f"{client.address} {round(balance, 6)} ETH")
            return balance
        except:
            return 0

def start_balance(accounts):
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(balance, acc) for acc in accounts]

        results = []
        for future in futures:
            results.append(future.result())

        balances_accs = 0
        for b in results:
            if b > 0: balances_accs += 1

        logger.info(f"Кошельки с балансом: {balances_accs} | Кошельки без баланса: {len(results) - balances_accs} | Всего проверенных: {len(results)}")