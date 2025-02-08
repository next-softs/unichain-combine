from concurrent.futures import ThreadPoolExecutor
import random

from core.client import Client
from config import *


def wrap_unwrap(acc):
    client = Client(acc)
    client.wrap_unwrap()

def start_wrap_unwrap(accounts):
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(wrap_unwrap, acc) for acc in accounts]

        for future in futures:
            future.result()