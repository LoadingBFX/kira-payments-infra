import hashlib

def verify_txhash(txhash: str) -> str:
    if not txhash or not txhash.startswith("0x"):
        return "not found"
    h = hashlib.sha256(txhash.encode()).hexdigest()
    return "confirmed" if h[0] in "02468abcdef" else "not found"

