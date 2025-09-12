resource "aws_launch_template" "example" {
  name_prefix   = "demo-lt-"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  key_name      = var.key_name 

  network_interfaces {
    security_groups = [aws_security_group.asg_sg.id]
  }

  iam_instance_profile  {
    name = data.aws_iam_instance_profile.app-server-role.name
  }

  user_data = base64encode(local.user_data_script)

  tags = {
    Name = "home-lab"
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-*"]
  }

  owners = ["099720109477"] 
}
