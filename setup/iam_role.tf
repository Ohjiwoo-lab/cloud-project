# 역할 생성
resource "aws_iam_role" "instance_profile" {
  name = "instance-ssm-agent"

  # 이 역할을 맡을 수 있는 서비스 명시(EC2 인스턴스)
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow",
        Principal = {
            Service = "ec2.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# SSM이 EC2 인스턴스에 작업을 수행할 수 있도록 허용하는 `AmazonSSMManagedInstanceCore` 관리형 정책을 추가
resource "aws_iam_role_policy_attachment" "attach_ssm_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
  role = aws_iam_role.instance_profile.name
}