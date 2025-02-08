from concurrent.futures import ThreadPoolExecutor
import random, time

from core.client import Client
from config import *


def random_transaction(acc):
    client = Client(acc)
    client.random_transaction()

def start_random_transaction(accounts):
    accs = {}
    for acc in accounts: accs[acc.name] = acc

    accounts_timeout = {}
    stime = time.time()

    for i, acc in enumerate(accounts):
        accounts_timeout[acc.name] = int(time.time() + random.randint(*delay_start) * (int(i / threads)))

    while True:
        time.sleep(5)

        start_accounts = []
        for acc, timeout in accounts_timeout.copy().items():
            if time.time() >= timeout:
                start_accounts.append(accs[acc])
                accounts_timeout[acc] = int(time.time() + random.randint(*delay_actions))

        if start_accounts:
            with ThreadPoolExecutor(max_workers=threads) as executor:
                futures = [executor.submit(random_transaction, acc) for acc in start_accounts]

                for future in futures:
                    future.result()
