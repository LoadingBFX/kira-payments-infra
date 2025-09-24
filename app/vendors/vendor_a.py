from .base import Vendor

class VendorA(Vendor):
    async def transfer(self, amount: float, txhash: str):
        return {"status": "success", "vendor": "vendorA", "amount": amount, "txhash": txhash}

