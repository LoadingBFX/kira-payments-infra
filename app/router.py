from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from .blockchain_mock import verify_txhash
from .vendors.vendor_a import VendorA
from .vendors.vendor_b import VendorB
import time
from prometheus_client import Counter, Histogram

router = APIRouter()

REQUESTS = Counter("transfer_requests_total", "Number of transfer requests", ["vendor"])
CONFIRMS = Counter("txhash_confirmations_total", "Txhash confirmations", ["result"])
LATENCY = Histogram("transfer_latency_seconds", "Transfer latency per vendor", ["vendor"])
SUCCESSES = Counter("transfer_success_total", "Successful transfers", ["vendor"])
FAILURES = Counter("transfer_failure_total", "Failed transfers", ["vendor"])

class TransferIn(BaseModel):
    amount: float = Field(gt=0)
    vendor: str
    txhash: str

def get_vendor(vendor: str):
    if vendor == "vendorA":
        return VendorA()
    if vendor == "vendorB":
        return VendorB()
    raise HTTPException(status_code=400, detail="Unsupported vendor")

@router.post("/transfer")
async def transfer(req: TransferIn):
    vendor_name = req.vendor
    REQUESTS.labels(vendor_name).inc()

    t0 = time.time()
    result = verify_txhash(req.txhash)
    CONFIRMS.labels(result).inc()
    if result != "confirmed":
        FAILURES.labels(vendor_name).inc()
        raise HTTPException(status_code=404, detail="txhash not found")

    vendor = get_vendor(vendor_name)
    resp = await vendor.transfer(req.amount, req.txhash)

    LATENCY.labels(vendor_name).observe(time.time() - t0)
    if resp.get("status") in ("success", "pending"):
        SUCCESSES.labels(vendor_name).inc()
    else:
        FAILURES.labels(vendor_name).inc()
    return resp

