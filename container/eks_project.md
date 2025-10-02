# EKS Online Boutique Project

## Project Overview
A production-grade Kubernetes infrastructure on AWS EKS, demonstrating enterprise-level DevOps practices including service mesh, GitOps, secrets management, and policy enforcement.

## Architecture

### Infrastructure Layer (Terraform)
- **VPC**: Custom VPC with public/private subnets across 3 AZs
- **EKS Cluster**: Kubernetes 1.29 with managed node groups
- **Istio Service Mesh**: mTLS, traffic management, observability
- **ArgoCD**: GitOps continuous deployment
- **External Secrets**: AWS Secrets Manager integration
- **OPA Gatekeeper**: Policy enforcement for security compliance

### Application Layer
- **Microservices**: 11-service e-commerce application
- **Languages**: Go, Python, Java, Node.js, C#
- **Security**: Non-root containers, dropped capabilities, read-only filesystems
- **Networking**: Istio Gateway with NLB, authorization policies

## Technical Highlights

### Security Features
1. **Zero-Trust Networking**: Strict mTLS between all services
2. **Admission Control**: OPA policies block privileged containers
3. **Secrets Management**: No secrets in Git, automated rotation
4. **Pod Security**: Hardened containers following best practices

### GitOps Workflow
1. Code pushed to Git repository
2. ArgoCD detects changes automatically
3. Reconciles cluster state with Git
4. Self-healing and automated rollback

### Infrastructure as Code
- Modular Terraform configuration
- Remote state in S3 with DynamoDB locking
- Automated via GitHub Actions
- Separate infrastructure and application repos

## Repositories
- **Infrastructure**: https://github.com/bosingva/eks-online-boutique
- **Application**: https://github.com/bosingva/online-boutique-app

## Cost Considerations
- Estimated monthly cost: $300-400
- Designed for portfolio demonstration
- Can be scaled down for cost optimization

## Skills Demonstrated
- AWS EKS, VPC, IAM, Secrets Manager
- Kubernetes orchestration and operations
- Service mesh (Istio) implementation
- GitOps with ArgoCD
- Infrastructure as Code (Terraform)
- Security and compliance (OPA Gatekeeper)
- CI/CD with GitHub Actions
- Container security best practices

## Status
Currently deployed and demonstrable upon request.
Project showcases production-ready infrastructure suitable for enterprise environments.