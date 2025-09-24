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

# tweak
