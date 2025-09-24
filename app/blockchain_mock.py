import hashlib

def verify_txhash(txhash: str) -> str:
    if not txhash or not txhash.startswith("0x"):
        return "not found"
    # 简单规则：hash 后偶数开头算 confirmed，否则 not found（可替换更复杂逻辑）
    h = hashlib.sha256(txhash.encode()).hexdigest()
    return "confirmed" if h[0] in "02468abcdef" else "not found"

