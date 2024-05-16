variable "trail_name" {
  type    = string
  default = "management_events"
}

# 현재 계정 정보를 가져오기
data "aws_caller_identity" "current" {}

# 현재 리전 정보 가져오기
data "aws_region" "current" {}