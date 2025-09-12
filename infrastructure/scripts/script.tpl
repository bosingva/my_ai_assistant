#!/bin/bash

# wait 60 seconds until instance fully initialised
sleep 60

# update package repos
sudo apt update

# Install docker on Ubuntu 22.04
sudo apt  install docker.io -y

# Add gitlab-runner & ubuntu users to docker group
# sudo usermod -aG docker gitlab-runner
sudo usermod -aG docker ubuntu

# Start docker to apply the above change
systemctl restart docker

# Install AWS CLI 
sudo apt install awscli -y

OPENAI_API_KEY=$(aws secretsmanager get-secret-value \
  --secret-id OPENAI_API_KEY \
  --query SecretString \
  --output text \
  --region ${AWS_REGION} | tr -d '\n\r')

aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
docker pull ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/ai-assistant:latest
docker run -d --name my-container -p 80:8000 -e OPENAI_API_KEY="$${OPENAI_API_KEY}" ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/ai-assistant:latest
