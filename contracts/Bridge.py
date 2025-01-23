from contracts.default import Default
from utils.get_abi import get_abi
from utils.encode import get_data_byte64

from decimal import Decimal


class Bridge(Default):
    def __init__(self, account):
        super().__init__(account.private_key, "https://sepolia.drpc.org", get_abi(""), "0xea58fcA6849d79EAd1f26608855c2D6407d54Ce2", account.proxy)

    def bridge(self, amount):
        data = get_data_byte64("0xe11013dd",
                               self.address,
                               hex(200000),
                               hex(96), hex(11),
                               hex(52223474424246259519216848849587966436218704979479727952724832034918655590400))

        tx = {
            "chainId": self.w3.eth.chain_id,
            "data": data,
            "from": self.address,
            "nonce": self.nonce(),
            "to": self.contract_address,
            "value": hex(self.gwei_to_wei(amount))
        }

        return self.send_transaction(tx, f"bridge sepolia > unichain ({amount} ETH)")
