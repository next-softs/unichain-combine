from contracts.default import Default
from utils.get_abi import get_abi
from utils.encode import get_data_byte64

from decimal import Decimal


class MintNft(Default):
    def __init__(self, account, nft):
        super().__init__(account.private_key, "https://unichain-sepolia-rpc.publicnode.com", get_abi(""), nft.address, account.proxy)
        self.nft = nft


    def mint(self):
        data = self.nft.data.format(address=self.address[2:])

        tx = {
            "chainId": self.w3.eth.chain_id,
            "data": data,
            "from": self.address,
            "nonce": self.nonce(),
            "to": self.contract_address
        }

        return self.send_transaction(tx, f"mint {self.nft.title}")
