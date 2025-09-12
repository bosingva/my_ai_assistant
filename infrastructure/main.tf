provider "aws" {
  region = var.aws_region
  
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
  filter {
    name   = "availability-zone"
    values = ["us-east-1a", "us-east-1b", "us-east-1c", "us-east-1d", "us-east-1f"]
  }
}

resource "aws_autoscaling_group" "demo" {
  desired_capacity     = var.desired_capacity
  max_size             = var.max_size
  min_size             = var.min_size
  vpc_zone_identifier  = data.aws_subnets.default.ids
  target_group_arns    = [aws_lb_target_group.ai_assistant_tg.arn]

  launch_template {
    id      = aws_launch_template.example.id
    version = "$Latest"
  }

  health_check_type = "EC2"
  health_check_grace_period = 30

tag {
    key   = "Name"
    value = "home-lab"
    propagate_at_launch = true
  }
}
