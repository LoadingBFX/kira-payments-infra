from abc import ABC, abstractmethod
from typing import Dict

class Vendor(ABC):
    @abstractmethod
    async def transfer(self, amount: float, txhash: str) -> Dict:
        pass

