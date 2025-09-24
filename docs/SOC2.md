# SOC 2 Alignment

## Security
- **IAM/RBAC**: Principle of least privilege in CI; protected branches in the repository; in cloud environments use IAM roles and separation of duties.  
- **Network isolation**: Local runs use a dedicated Docker network; in cloud, use VPC, subnets, and security groups.  
- **Minimal exposure**: Only ports 8000 (API) and 9090 (Prometheus) are exposed.  

## Availability
- **Health checks**: Defined in Terraform and container health configuration.  
- **Deployment validation**: CI runs health checks after deployment; failures trigger rollback/failed pipeline.  

## Processing Integrity
- **Input validation**: `/transfer` requests validated with Pydantic (e.g., amount > 0, vendor required).  
- **Vendor architecture**: Vendor modules follow a stable interface; adding a new vendor does not affect existing flows.  

## Confidentiality
- **Logs**: Do not store sensitive data; logs capture only path, method, and status code.  
- **Future-proofing**: Plan to enforce TLS and encrypted secret storage (e.g., AWS SSM, Vault, or KMS).  

## Privacy
- **No PII**: This demo setup does not process personal identifiable information.  
- **If handling real data**: Apply data minimization and access auditing.  

## Audit Logging
- **Structured logs**: JSON-formatted logs include transaction hash validation results.  
- **Metrics**: Prometheus counters and histograms provide operational evidence (requests, confirmations, failures, latency).  

## Incident Response
- **CI/CD alerts**: Pipeline failures are surfaced immediately (e.g., Slack or GitHub notifications).  
- **MTTR tracking**: Measured via pipeline data — record time from failure to recovery (see DORA metrics).  