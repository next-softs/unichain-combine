from concurrent.futures import ThreadPoolExecutor
import random, time

from contracts.MintNft import MintNft
from models.nfts import nft_list
from config import *
from utils.logs import logger


def mint_nft(acc):
    mint = MintNft(*acc)
    for i in range(20):
        balance = mint.balance_nft()
        if balance > 0:
            logger.info(f"{mint.acc_name} уже есть {mint.nft.title}")
            break

        status = mint.mint()
        if status:
            s = random.randint(*delay_actions)
            logger.info(f"ожидаем {s} сек для запуска след. кошелька..")
            time.sleep(s)
            break

def start_mint_nft(accounts):
    mints = []
    for account in accounts:
        for nft in nft_list:
            mints.append([account, nft])
    random.shuffle(mints)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(mint_nft, mint) for mint in mints]

        for future in futures:
            future.result()