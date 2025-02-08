from concurrent.futures import ThreadPoolExecutor
import random

from core.client import Client
from config import *


def bridge(acc):
    client = Client(acc)
    for i in range(20):
        status, s2 = client.start_bridge()

        if status or s2:
            if status: client.sleep(delay_actions)
            break

def start_bridge(accounts):
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(bridge, acc) for acc in accounts]

        for future in futures:
            future.result()