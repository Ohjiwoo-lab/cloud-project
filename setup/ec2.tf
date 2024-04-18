# Amazon Linux 2 AMI
data "aws_ami" "amazon-linux-2" {
    most_recent = true

    filter {
        name   = "owner-alias"
        values = ["amazon"]
    }

    filter {
        name   = "name"
        values = ["amzn2-ami-hvm*"]
    }
}

# Create master instance
resource "aws_instance" "master" {
    ami           = data.aws_ami.amazon-linux-2.id
    instance_type = "t2.micro"

    tags = {
        Name = "master"
    }
}

# Create slave instance
resource "aws_instance" "slave" {
    ami           = data.aws_ami.amazon-linux-2.id
    instance_type = "t2.micro"

    tags = {
        Name = "slave"
    }
}