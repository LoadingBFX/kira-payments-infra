# ARCHITECTURE
```
kira-payments-infra
├─ api/
│  ├─ Dockerfile
│  └─ requirements.txt
├─ app/
│  ├─ main.py
│  ├─ blockchain_mock.py
│  ├─ router.py
│  └─ vendors/
│     ├─ __init__.py
│     ├─ base.py
│     ├─ vendor_a.py
│     └─ vendor_b.py
├─ tests/
│  └─ test_transfer.py
├─ observability/
│  └─ prometheus.yml
├─ infra/terraform/
│  ├─ main.tf
│  ├─ providers.tf
│  ├─ variables.tf
│  └─ outputs.tf
├─ .github/workflows/
│  └─ ci.yml
└─ docs/
   ├─ ARCHITECTURE.md
   └─ SOC2.md


```
## Overview
- API: FastAPI, /transfer, /healthz, /metrics
- Vendors: base interface + vendorA (success), vendorB (pending)
- Blockchain mock: verify_txhash()

## Request Flow
Client -> /transfer -> txhash verify -> vendor module -> response -> metrics+logs

## Vendor Extensibility
- New vendorC: add `vendors/vendor_c.py` implementing `Vendor`
- Register in `get_vendor()` or用简单的映射表（可改为依赖注入/插件扫描）

## Observability
- Prometheus metrics:
  - transfer_requests_total{vendor}
  - transfer_latency_seconds{vendor}
  - transfer_success_total{vendor}, transfer_failure_total{vendor}
  - txhash_confirmations_total{result}
- Structured logs (JSON), stdout，可接 Loki/ELK

## IaC
- Terraform docker provider: network, api container, prometheus container
- 输出 API/Prometheus URL

## CI/CD
- Build -> Terraform apply -> Health check -> Post-deploy tests -> Artifact DORA
- Fail-fast on tests
