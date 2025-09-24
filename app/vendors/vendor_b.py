from .base import Vendor

class VendorB(Vendor):
    async def transfer(self, amount: float, txhash: str):
        return {"status": "pending", "vendor": "vendorB", "amount": amount, "txhash": txhash}

