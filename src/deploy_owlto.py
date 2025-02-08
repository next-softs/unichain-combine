from concurrent.futures import ThreadPoolExecutor
import random

from core.client import Client
from config import *


def deploy(acc):
    client = Client(acc)
    client.deploy_owlto()

def start_deploy_owlto(accounts):
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(deploy, acc) for acc in accounts]

        for future in futures:
            future.result()