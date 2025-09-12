# AI Assistant – Home Lab Project

A simple **FastAPI** app with a chat UI, containerized with **Docker**, and deployed to **AWS** using **Terraform** and **GitHub Actions**.

---

## 🚀 Features
- FastAPI backend with a minimal web UI.
- Containerized app (Docker).
- Deployment to AWS via Auto Scaling Group + Load Balancer.
- CI/CD pipeline with GitHub Actions (build, push, deploy).
- Terraform-managed infrastructure.

---

## 📦 Project Structure
```
my_ai_assistant/
├─ container/        # FastAPI app + Dockerfile
├─ infrastructure/   # Terraform config for AWS
└─ .github/workflows # CI/CD pipelines
```

---

## 🐳 Run Locally
```bash
cd my_ai_assistant/container
docker build -t ai-assistant .
docker run -p 80:8000 -e OPENAI_API_KEY=sk-... ai-assistant
```

👉 Open [http://localhost:80](http://localhost:80)

---

## ☁️ Deploy with Terraform
```bash
cd my_ai_assistant/infrastructure
terraform init
terraform apply
```

> Terraform backend uses **S3 + DynamoDB** (see `providers.tf`).

---

## 🔄 CI/CD (GitHub Actions)
- **build_deploy.yaml** → builds & pushes Docker image to ECR, updates EC2 via SSM.  
- **deploy.yaml** → runs Terraform to provision/update infra.  

---

## 🌐 Demo
Live instance: [www.talk-to-my-ai.click](http://www.talk-to-my-ai.click)

---

## ✅ Prerequisites
- AWS account with:
  - **ECR repository** (for container images).
  - **S3 bucket** + **DynamoDB table** (for Terraform state & locking).
  - **EC2 Auto Scaling Group** with SSM agent enabled.
- GitHub repo configured with:
  - **Variables**: `AWS_REGION`, `ECR_REPOSITORY`
  - **Secrets**: `AWS_ACCOUNT_ID`, `AWS_ROLE_TO_ASSUME`, `OPENAI_API_KEY`
- Terraform CLI installed locally (if running outside CI/CD).
