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

# Create Security Group
resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"
  description = "Allow ssh inbound traffic and all outbound traffic"

  tags = {
    Name = "allow_ssh"
  }
}

# Add inbound rule
resource "aws_vpc_security_group_ingress_rule" "allow_ssh_ipv4" {
  security_group_id = aws_security_group.allow_ssh.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 22
  ip_protocol       = "tcp"
  to_port           = 22
}

resource "aws_vpc_security_group_ingress_rule" "allow_self_security_group" {
  security_group_id = aws_security_group.allow_ssh.id
  referenced_security_group_id = aws_security_group.allow_ssh.id
  from_port         = -1
  ip_protocol       = -1
  to_port           = -1
}

# Add outbound rule
resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv4" {
  security_group_id = aws_security_group.allow_ssh.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

resource "aws_iam_instance_profile" "ssm_profile" {
  name = "ssm_profile"
  role = aws_iam_role.instance_profile.name
}

# Create master instance
resource "aws_instance" "master" {
  ami           = data.aws_ami.amazon-linux-2.id
  instance_type = "t2.micro"
  key_name      = aws_key_pair.make_keypair.key_name
  vpc_security_group_ids = [aws_security_group.allow_ssh.id]
  iam_instance_profile   = aws_iam_instance_profile.ssm_profile.name

  tags = {
    Name = "master"
  }
}

# Create slave instance
resource "aws_instance" "slave" {
  ami           = data.aws_ami.amazon-linux-2.id
  instance_type = "t2.micro"
  key_name      = aws_key_pair.make_keypair.key_name
  vpc_security_group_ids = [aws_security_group.allow_ssh.id]

  tags = {
    Name = "slave"
  }
}

# SSH 원격 접속과 Ansible 설정 (provisioner)
resource "null_resource" "master_connet_and_configuration" {
  depends_on = [aws_instance.master]

  connection {
    user = "ec2-user"
    type = "ssh"
    host = aws_instance.master.public_ip

    private_key = "${file("./key/ansible_keypair")}"
    timeout     = "1m"
  }
  
  provisioner "remote-exec" {
    inline = [
        "sudo yum update",
        "sudo yum install -y python3"
    ]
  }
}

resource "null_resource" "slave_connet_and_configuration" {
  depends_on = [aws_instance.slave]

  connection {
    user = "ec2-user"
    type = "ssh"
    host = aws_instance.slave.public_ip

    private_key = "${file("./key/ansible_keypair")}"
    timeout     = "1m"
  }
  
  provisioner "remote-exec" {
    inline = [
        "sudo yum update",
        "sudo yum install -y python3"
    ]
  }
}

resource "null_resource" "ansible_playbook" {
  depends_on = [aws_instance.master, aws_instance.slave]

  provisioner "local-exec" {
    command = <<EOF
      echo "[demo]" > inventory
      echo "${aws_instance.master.public_ip} ansible_ssh_user=ec2-user ansible_ssh_private_key_file=./key/ansible_keypair" >> inventory
      echo "${aws_instance.slave.public_ip} ansible_ssh_user=ec2-user ansible_ssh_private_key_file=./key/ansible_keypair" >> inventory
      
      echo "[master]" >> inventory
      echo "${aws_instance.master.public_ip} ansible_ssh_user=ec2-user ansible_ssh_private_key_file=./key/ansible_keypair" >> inventory

      echo "[slave]" >> inventory
      echo "${aws_instance.slave.public_ip} ansible_ssh_user=ec2-user ansible_ssh_private_key_file=./key/ansible_keypair" >> inventory

      echo "[master:vars]" >> inventory
      echo "hostname=${aws_instance.master.private_dns}" >> inventory

      echo "[slave:vars]" >> inventory
      echo "hostname=${aws_instance.master.private_dns}" >> inventory
    EOF
  }

  provisioner "local-exec" {
    command = <<EOF
      ANSIBLE_HOST_KEY_CHECKING=False \
      ansible-playbook -i inventory playbook.yml
    EOF
  }
}