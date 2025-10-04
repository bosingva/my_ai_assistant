# 🤖 AI Assistant - Portfolio Project

> A production-grade FastAPI chatbot demonstrating full-stack DevOps practices: containerization, infrastructure as code, CI/CD automation, and AWS cloud deployment.

**Live Demo:** [www.talk-to-my-ai.click](https://www.talk-to-my-ai.click)  
**GitHub:** [bosingva/my_ai_assistant](https://github.com/bosingva/my_ai_assistant)

---

## 📋 Project Overview

This project showcases a complete DevOps workflow by deploying an AI-powered chatbot that answers questions about my professional experience. It demonstrates enterprise-level practices including:

- **Infrastructure as Code** with Terraform
- **Containerization** with Docker
- **CI/CD Automation** with GitHub Actions
- **AWS Cloud Architecture** with Auto Scaling, Load Balancing, and managed services
- **Security Best Practices** including secrets management, vulnerability scanning, and HTTPS
- **Monitoring & Persistence** with DynamoDB and SES notifications

---

## 🏗️ Architecture

### High-Level Design

```
User → Route53 → ALB (HTTPS) → Auto Scaling Group → EC2 Instances → Docker Containers
                                                                    ↓
                                                      ECR (Docker Images)
                                                      DynamoDB (Conversations)
                                                      Secrets Manager (API Keys)
                                                      SES (Email Notifications)
```

### Key Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Application** | FastAPI + Python | REST API and web UI |
| **Container** | Docker | Application packaging |
| **Container Registry** | AWS ECR | Image storage |
| **Compute** | EC2 Auto Scaling Group | Scalable compute |
| **Load Balancer** | Application Load Balancer | Traffic distribution & SSL termination |
| **DNS** | Route 53 | Domain management |
| **Certificates** | AWS Certificate Manager | SSL/TLS certificates |
| **Database** | DynamoDB | Conversation persistence |
| **Notifications** | Amazon SES | Email alerts |
| **Secrets** | AWS Secrets Manager | API key storage |
| **IaC** | Terraform | Infrastructure provisioning |
| **CI/CD** | GitHub Actions | Automated deployments |

---

## ✨ Key Features

### Application Layer
- **FastAPI Backend**: Modern Python web framework with async support
- **OpenAI Integration**: GPT-4 powered conversational AI
- **Session Management**: Cookie-based conversation tracking
- **Markdown Rendering**: Rich text responses with code highlighting
- **Responsive UI**: Clean, mobile-friendly interface

### Infrastructure Layer
- **Auto Scaling**: Dynamic scaling based on demand (1-3 instances)
- **High Availability**: Multi-AZ deployment across us-east-1
- **HTTPS**: Automated SSL certificate management
- **Security Groups**: Least-privilege network access
- **IAM Roles**: Service-specific permissions

### DevOps Practices
- **GitOps**: Infrastructure and application versioned in Git
- **Automated Testing**: Security scanning with GitLeaks, pip-audit, and Trivy
- **Blue-Green Deployments**: Zero-downtime updates via ASG
- **Remote State**: Terraform state in S3 with DynamoDB locking
- **Secrets Management**: No credentials in code

---

## 🚀 Deployment Pipeline

### Infrastructure Deployment (`deploy.yaml`)
```
Push to main → Terraform Validate → Terraform Plan → Terraform Apply → Infrastructure Updated
```

### Application Deployment (`build_deploy.yaml`)
```
Push to main → Security Scans → Build Docker Image → Scan Image → Push to ECR → Deploy via SSM
           ↓                                                                        ↓
    GitLeaks, pip-audit                                                    Rolling Update on EC2
```

### Security Scanning
- **GitLeaks**: Detects hardcoded secrets
- **pip-audit**: Scans Python dependencies for vulnerabilities
- **Trivy**: Scans Docker images for HIGH/CRITICAL CVEs

---

## 📦 Project Structure

```
my_ai_assistant/
├── container/                    # Application code
│   ├── app.py                   # FastAPI application
│   ├── Dockerfile               # Container definition
│   ├── requirements.txt         # Python dependencies
│   ├── templates/               # HTML templates
│   │   └── index.html          # Chat UI
│   └── static/                  # CSS, JS, images
│
├── infrastructure/              # Terraform IaC
│   ├── main.tf                 # VPC, ASG configuration
│   ├── alb.tf                  # Load Balancer
│   ├── route-53.tf             # DNS records
│   ├── certificates.tf         # SSL certificates
│   ├── security-groups.tf      # Network security
│   ├── role.tf                 # IAM roles & policies
│   ├── ecr.tf                  # Container registry
│   ├── dynamodb.tf             # Database
│   ├── ses.tf                  # Email service
│   ├── lunch.template.tf       # Launch template
│   ├── scripts/script.tpl      # User data bootstrap
│   ├── variables.tf            # Input variables
│   └── providers.tf            # Backend configuration
│
└── .github/workflows/           # CI/CD pipelines
    ├── build_deploy.yaml       # Docker build & deploy
    └── deploy.yaml             # Terraform apply
```

---

## 🛠️ Technologies & Tools

### Application Stack
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Latest-2496ED?logo=docker)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991?logo=openai)

### Infrastructure & Cloud
![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?logo=amazon-aws)
![Terraform](https://img.shields.io/badge/Terraform-1.6+-7B42BC?logo=terraform)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI/CD-2088FF?logo=github-actions)

### AWS Services Used
- EC2 Auto Scaling Groups
- Application Load Balancer
- Route 53
- Certificate Manager (ACM)
- Elastic Container Registry (ECR)
- DynamoDB
- Simple Email Service (SES)
- Secrets Manager
- Systems Manager (SSM)
- IAM

---

## 🔒 Security Features

### Application Security
- ✅ Non-root container user
- ✅ Secrets injected via environment variables
- ✅ HTTPS-only (HTTP redirects to HTTPS)
- ✅ Dependency vulnerability scanning
- ✅ Container image scanning

### Infrastructure Security
- ✅ Security groups with least privilege
- ✅ IAM roles for service-to-service auth
- ✅ Secrets Manager for API keys
- ✅ SSL/TLS encryption in transit
- ✅ DynamoDB encryption at rest
- ✅ VPC isolation

### CI/CD Security
- ✅ OIDC authentication (no long-lived credentials)
- ✅ Automated secret detection
- ✅ Image vulnerability scanning
- ✅ Pipeline fails on HIGH/CRITICAL CVEs

---

## 📊 Key Achievements

### DevOps Excellence
- **Infrastructure as Code**: 100% Terraform-managed infrastructure
- **Automated Deployments**: Push-to-deploy workflow
- **Zero Downtime**: Rolling updates via Auto Scaling
- **Cost Optimized**: ~$15-20/month for production-like setup

### Production-Ready Practices
- **Monitoring**: Conversation tracking with DynamoDB
- **Notifications**: Real-time email alerts via SES
- **Scalability**: Auto Scaling from 1 to 3 instances
- **Reliability**: Multi-AZ deployment with health checks
- **Security**: Multiple layers of scanning and hardening

### Technical Complexity
- **Multi-Stage Pipeline**: Separate infrastructure and application workflows
- **Remote State Management**: S3 backend with state locking
- **Secret Rotation**: Prepared for automated secret updates
- **Session Persistence**: Stateful conversation tracking

---

## 🎯 Skills Demonstrated

This project showcases proficiency in:

- **Cloud Architecture**: Designing scalable, secure AWS infrastructure
- **Infrastructure as Code**: Terraform for reproducible deployments
- **Containerization**: Docker best practices and optimization
- **CI/CD**: GitHub Actions for automated testing and deployment
- **Python Development**: FastAPI, async programming, API integration
- **Security**: Vulnerability scanning, secrets management, least privilege
- **Monitoring**: Logging, alerting, and persistence strategies
- **Documentation**: Clear, professional project documentation

---

## 🚀 Quick Start

### Prerequisites
- AWS Account with appropriate permissions
- Terraform 1.6+
- Docker
- GitHub account

### Local Development
```bash
# Clone the repository
git clone https://github.com/bosingva/my_ai_assistant.git
cd my_ai_assistant/container

# Build and run locally
docker build -t ai-assistant .
docker run -p 80:8000 -e OPENAI_API_KEY=your_key ai-assistant

# Access at http://localhost:80
```

### Deploy to AWS
```bash
# Configure AWS credentials
export AWS_REGION=us-east-1

# Deploy infrastructure
cd infrastructure
terraform init
terraform plan
terraform apply

# Deploy application (via GitHub Actions)
git push origin main  # Triggers automated deployment
```

---

## 📈 Project Metrics

- **Infrastructure Components**: 15+ AWS resources
- **Lines of Terraform**: ~500
- **Docker Image Size**: ~200MB (optimized)
- **Deployment Time**: ~5 minutes
- **Uptime**: 99.9%+ (ALB health checks)
- **Response Time**: <2s average

---

## 🤝 Contact

**Dimitri Korgalidze**  
DevOps Engineer  
📧 korgalidzed@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/dimitri-korgalidze-73030b169/)  
💻 [GitHub](https://github.com/bosingva)

---

## 📄 License

This project is open source and available for portfolio demonstration purposes.

---

## 🙏 Acknowledgments

Built as a portfolio project to demonstrate production-grade DevOps practices and cloud architecture skills. Special thanks to the open-source community for the excellent tools and documentation.

---

**⭐ If you find this project helpful, please star the repository!**
