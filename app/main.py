from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .router import router
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import json
import logging
import sys

# 结构化 JSON 日志
logger = logging.getLogger("uvicorn")
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.handlers = [handler]
logger.setLevel(logging.INFO)

app = FastAPI(title="Kira Payments API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request, call_next):
    response = await call_next(request)
    log = {
        "path": request.url.path,
        "method": request.method,
        "status_code": response.status_code,
    }
    logger.info(json.dumps(log))
    return response

@app.get("/healthz")
async def health():
    return {"status": "ok"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

app.include_router(router)

