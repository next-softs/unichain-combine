from config import *
from utils.file_manager import append_to_txt
from utils.logs import logger

from decimal import Decimal
import time, random

from contracts.Bridge import Bridge
from contracts.Uniswap import Uniswap
from contracts.OwltoDeploy import OwltoDeploy

class Client:
    def __init__(self, account):
        self.account = account

        self.bridge = Bridge(self.account)
        self.uniswap = Uniswap(self.account)
        self.owlto = OwltoDeploy(self.account)

        self.acc_name = self.bridge.acc_name

    def sleep(self, delay):
        s = random.randint(*delay)
        logger.info(f"{self.acc_name} ожидаем {s} сек..")
        time.sleep(s)

    def start_bridge(self):
        try:
            amount = round(random.uniform(*bridge_amount), random.randint(*precision))

            balance_eth = float(self.uniswap.balance())
            balance_weth = float(self.uniswap.balance_weth())

            if balance_eth + balance_weth >= min_bridge_amount:
                logger.warning(f"{self.acc_name} в unichain уже есть {round(balance_eth + balance_weth, 6)} ETH, бриджить не будем")
                return False, False

            balance_eth = float(self.bridge.balance())
            if amount >= balance_eth:
                if bridge_amount[0] > balance_eth:
                    logger.warning(f"{self.acc_name} недостаточно eth для бриджа {amount}ETH")
                    return False, True

                amount = bridge_amount[0]

            self.bridge.bridge(amount)
            return True, False

        except Exception as err:
            logger.error(f"{self.acc_name} {err}")

        return False, False

    def start_wrap_unwrap(self):
        while True:
            self.wrap_unwrap()
            self.sleep(delay_actions)

    def wrap_unwrap(self):
        try:
            amount = round(random.uniform(*wrap_amount), random.randint(*precision))

            balance_eth = float(self.uniswap.balance()) - 0.001
            balance_eth = balance_eth if balance_eth > 0 else 0

            balance_weth = round(float(self.uniswap.balance_weth()) * 0.99, 6)

            if amount > balance_eth and balance_weth != 0:
                self.uniswap.unwrap(balance_weth)
            else:
                action = random.choice(["wrap", "unwrap"])
                if action == "wrap" or balance_weth == 0:
                    amount = amount if amount < balance_eth else balance_weth
                    self.uniswap.wrap(amount)
                else:
                    amount = amount if amount < balance_weth else balance_weth
                    self.uniswap.unwrap(amount)

        except Exception as err:
            logger.error(f"{self.acc_name} {err}")

    def deploy_owlto(self):
        try:
            self.owlto.deploy()
        except Exception as err:
            logger.error(f"{self.acc_name} {err}")

    def random_transactions(self):
        actions = ["wrap_unwrap", "deploy"]
        weights = list(weights_transactions.values())

        while True:
            try:
                action = random.choices(actions, weights=weights, k=1)[0]
                if action == "wrap_unwrap":
                    self.wrap_unwrap()
                elif action == "deploy":
                    self.deploy_owlto()

            except Exception as err:
                logger.error(f"{self.acc_name} {err}")

            self.sleep(delay_actions)
