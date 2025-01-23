from contracts.default import Default
from utils.get_abi import get_abi
from utils.encode import get_data_byte64

from decimal import Decimal


class Uniswap(Default):
    def __init__(self, account):
        super().__init__(account.private_key, "https://unichain-sepolia-rpc.publicnode.com", get_abi(""), "0x4200000000000000000000000000000000000006", account.proxy)

    def wrap(self, amount):
        tx = {
            "chainId": self.w3.eth.chain_id,
            "data": "0xd0e30db0",
            "from": self.address,
            "nonce": self.nonce(),
            "to": self.contract_address,
            "value": hex(self.gwei_to_wei(amount))
        }

        return self.send_transaction(tx, f"wrap eth > weth ({amount} ETH)")

    def unwrap(self, amount):
        data = get_data_byte64("0x2e1a7d4d",
                               hex(self.gwei_to_wei(amount)))

        tx = {
            "chainId": self.w3.eth.chain_id,
            "data": data,
            "from": self.address,
            "nonce": self.nonce(),
            "to": self.contract_address
        }

        return self.send_transaction(tx, f"unwrap weth > eth ({amount} WETH)")

    def balance_weth(self):
        return float(self.token_balance(self.contract_address))
