variable "aws_region" {
  description  = "value for aws region"
  type         = string
  default      = "us-east-1"

}

variable "instance_type" {
  description = "value for instance type"
  type        = string
  default     = "t3.micro"

}

variable "key_name" {
  description = "The name of the key pair to use for the instance"
  type        = string
  default     = "us-east-1"

}

variable "instance_profile_name" {
  description = "The name of the instance profile to use for the instance"
  type        = string
  default     = "app-server-role"

}

variable "alb_name" {
  description = "The name of the Application Load Balancer"
  type        = string
  default     = "alb-for-ai-assistant"
  
}

variable "alb_type" {
  description = "The type of the Application Load Balancer"
  type        = string
  default     = "application"
  
}

variable "alb_target_group_name" {
  description = "The name of the Application Load Balancer Target Group"
  type        = string
  default     = "ai-assistant-tg"
  
}


variable "desired_capacity" {
  description = "The number of EC2 instances to launch in the Auto Scaling group"
  type        = number
  default     = 2
  
}

variable "max_size" {
  description = "The maximum size of the Auto Scaling group"
  type        = number
  default     = 3
  
}
variable "min_size" {
  description = "The minimum size of the Auto Scaling group"
  type        = number
  default     = 2
  
}

variable "domain_name" {
  description = "The domain name for the SSL certificate"
  type        = string
  default     = "talk-to-my-ai.click"
  
}

variable "hosted_zone_id" {
  description = "The ID of your Route 53 hosted zone"
  type        = string
  default = "Z0403436M1TDUKH2S15Z"
}

variable "ecr_repository" {
  description = "Your ECR Repository Name"
  type        = string
  default     = "ai-assistant" 
}

