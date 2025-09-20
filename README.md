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

# 📖 Detailed Breakdown

This section provides a **deeper dive** into the project for developers who want to understand the internals.

---

## Part 1: Container (FastAPI App)

### 📂 Contents
- **app.py** – FastAPI app with routes, static files, templates, and OpenAI integration.  
- **dimitri_profile.md** – Profile text used inside the app.  
- **infrastructure.md** – Infra description text used inside the app.  
- **templates/index.html** – HTML template rendered by FastAPI (chat UI).  
- **static/** – Static assets (CSS, JS, images).  
- **requirements.txt** – Python dependencies.  
- **Dockerfile** – Container image definition.  

### 🐳 Docker Build & Run
```bash
docker build -t ai-assistant:latest .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key ai-assistant:latest
```

### 📦 Push to ECR (example)
```bash
docker tag ai-assistant:latest <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/ai-assistant:latest
docker push <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/ai-assistant:latest
```

---

## Part 2: Infrastructure (Terraform on AWS)

### 📂 Contents
- **main.tf** – AWS provider and VPC/subnet data sources.  
- **alb.tf** – Application Load Balancer, Target Groups, Listeners.  
- **route-53.tf** – DNS records for apex + www.  
- **certificates.tf** – ACM certificate for HTTPS.  
- **role.tf** – IAM roles for EC2 / services.  
- **security-groups.tf** – Security group definitions.  
- **ecr.tf** – Elastic Container Registry.  
- **lunch.tempalte.tf** – EC2 Launch Template for Auto Scaling Group.  
- **scripts/script.tpl** – EC2 bootstrap/user-data script.  
- **variables.tf / locals.tf** – Variables and configs.  

`.terraform/` and `.terraform.lock.hcl` are auto-generated.

### 🌍 Resources Created
- VPC & Subnets (default).  
- ALB with Target Group + Listener.  
- Auto Scaling Group with EC2.  
- Route 53 DNS records (apex + www).  
- ACM Certificates for SSL.  
- ECR repo for Docker images.  
- Security Groups.  
- IAM roles.  

### 🚀 Terraform Workflow
```bash
terraform init
terraform validate
terraform plan
terraform apply --auto-approve
```

### 🔗 Domain Setup
- `talk-to-my-ai.click` → ALB  
- `www.talk-to-my-ai.click` → ALB  

---

# ✅ Deployment Flow
1. Build & push Docker image from `container/`.  
2. Provision infra with Terraform from `infrastructure/`.  
3. ASG launches EC2 instances.  
4. Instances pull image from ECR and run the app.  
5. ALB + Route53 serve public traffic.  
