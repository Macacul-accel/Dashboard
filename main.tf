# Define AWS provider and set the region for resource provisioning
provider "aws" {
  region = "eu-west-3"
}

# Create a Virtual Private Cloud to isolate the infrastructure
resource "aws_vpc" "default" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "Django_EC2_VPC"
  }
}

# Internet Gateway to allow internet access to the VPC
resource "aws_internet_gateway" "default" {
  vpc_id = aws_vpc.default.id
  tags = {
    Name = "Django_EC2_Internet_Gateway"
  }
}

# Route table for controlling traffic leaving the VPC
resource "aws_route_table" "default" {
  vpc_id = aws_vpc.default.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.default.id
  }
  tags = {
    Name = "Django_EC2_Route_Table"
  }
}

# Subnet within VPC for resource allocation, in availability zone eu-west-3a
resource "aws_subnet" "subnet1" {
  vpc_id                  = aws_vpc.default.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = false
  availability_zone       = "eu-west-3a"
  tags = {
    Name = "Django_EC2_Subnet_1"
  }
}

# Another subnet for redundancy, in availability zone eu-west-3b
resource "aws_subnet" "subnet2" {
  vpc_id                  = aws_vpc.default.id
  cidr_block              = "10.0.2.0/24"
  map_public_ip_on_launch = false
  availability_zone       = "eu-west-3b"
  tags = {
    Name = "Django_EC2_Subnet_2"
  }
}

# Associate subnets with route table for internet access
resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.subnet1.id
  route_table_id = aws_route_table.default.id
}
resource "aws_route_table_association" "b" {
  subnet_id      = aws_subnet.subnet2.id
  route_table_id = aws_route_table.default.id
}



# Security group for EC2 instance
resource "aws_security_group" "ec2_sg" {
  vpc_id = aws_vpc.default.id
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Only allow HTTPS traffic from everywhere
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "EC2_Security_Group"
  }
}

# Ensure EC2 instance has access to parameters
resource "aws_iam_role_policy" "ssm_access" {
  name = "SSMAccessPolicy"
  role = aws_iam_role.ec2_role.name

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect   = "Allow",
      Action   = ["ssm:GetParameter", "ssm:GetParameters"],
      Resource = "arn:aws:ssm:eu-west-3:861276092462:parameter/my-app/*"
    }]
  })
}


# EC2 instance for the local web app
resource "aws_instance" "web" {
  ami                    = "ami-03216a20ecc5d72ee" # Amazon Linux
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.subnet1.id # Place this instance in one of the private subnets
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  associate_public_ip_address = true # Assigns a public IP address to your instance
  user_data_replace_on_change = true # Replace the user data when it changes

  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  user_data = <<-EOF
    #!/bin/bash
    set -ex
    yum update -y
    yum install -y yum-utils docker aws-cli

    # Fetch secrets from Parameter Store
    SECRET_KEY=$(aws ssm get-parameter --name "/my-app/SECRET_KEY" --with-decryption --query Parameter.Value --output text)
    ALLOWED_HOSTS=$(aws ssm get-parameter --name "/my-app/ALLOWED_HOSTS" --query Parameter.Value --output text)
    DB_NAME=$(aws ssm get-parameter --name "/my-app/DB_NAME" --query Parameter.Value --output text)
    DB_USER=$(aws ssm get-parameter --name "/my-app/DB_USER" --query Parameter.Value --output text)
    DB_PWD=$(aws ssm get-parameter --name "/my-app/DB_PWD" --with-decryption --query Parameter.Value --output text)
    DB_HOST=$(aws ssm get-parameter --name "/my-app/DB_HOST" --query Parameter.Value --output text)
    DB_PORT=$(aws ssm get-parameter --name "/my-app/DB_PORT" --query Parameter.Value --output text)
    SENDGRID_API_KEY=$(aws ssm get-parameter --name "/my-app/SENDGRID_API_KEY" --with-decryption --query Parameter.Value --output text)
    FROM_EMAIL=$(aws ssm get-parameter --name "/my-app/FROM_EMAIL" --query Parameter.Value --output text)

    # Create the .env file
    cat <<EOT > /home/ec2-user/.env
    SECRET_KEY=$SECRET_KEY
    ALLOWED_HOSTS=$ALLOWED_HOSTS
    DB_NAME=$DB_NAME
    DB_USER=$DB_USER
    DB_PWD=$DB_PWD
    DB_HOST=$DB_HOST
    DB_PORT=$DB_PORT
    SENDGRID_API_KEY=$SENDGRID_API_KEY
    FROM_EMAIL=$FROM_EMAIL
    EOT

    # Authenticate and pull the Docker image from ECR
    aws ecr get-login-password --region eu-west-3 | docker login --username AWS --password-stdin 861276092462.dkr.ecr.eu-west-3.amazonaws.com
    docker pull 861276092462.dkr.ecr.eu-west-3.amazonaws.com/yugi-django:latest

    # Run the Docker container with the .env file
    docker run -d -p 80:80 --env-file /home/ec2-user/.env 861276092462.dkr.ecr.eu-west-3.amazonaws.com/yugi-django:latest
  EOF

  tags = {
    Name = "Django_EC2_Complete_Server"
  }
}

# IAM role for EC2 instance to access ECR
resource "aws_iam_role" "ec2_role" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Principal = {
        Service = "ec2.amazonaws.com",
      },
      Effect = "Allow",
    }],
  })
}

# Attach the AmazonEC2ContainerRegistryReadOnly policy to the role
resource "aws_iam_role_policy_attachment" "ecr_read" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

# IAM instance profile for EC2 instance
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "django_ec2_complete_profile"
  role = aws_iam_role.ec2_role.name
}