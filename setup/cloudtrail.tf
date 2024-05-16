# S3 버킷 생성
resource "aws_s3_bucket" "trail_log_bucket" {
  bucket        = "trail-event-logs"
  force_destroy = true
}

# 버킷 정책 생성
resource "aws_s3_bucket_policy" "trail_log_bucket_policy" {
  bucket = aws_s3_bucket.trail_log_bucket.id
  
  policy = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
              "Service": "cloudtrail.amazonaws.com"
            },
            "Action": "s3:GetBucketAcl",
            "Resource": "${aws_s3_bucket.trail_log_bucket.arn}"
        },
        {
            "Effect": "Allow",
            "Principal": {
              "Service": "cloudtrail.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": "${aws_s3_bucket.trail_log_bucket.arn}/AWSLogs/${data.aws_caller_identity.current.account_id}/*",
            "Condition": {
                "StringEquals": {
                    "s3:x-amz-acl": "bucket-owner-full-control",
                    "AWS:SourceArn": "arn:aws:cloudtrail:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:trail/${var.trail_name}"
                }
            }
        }
    ]
}
POLICY
}

# 추적 생성
resource "aws_cloudtrail" "management_event" {
  name = var.trail_name
  s3_bucket_name = aws_s3_bucket.trail_log_bucket.id
  enable_log_file_validation = true
  is_multi_region_trail = true
  enable_logging = false

  event_selector {
    read_write_type = "All"
  }

  depends_on = [
    aws_s3_bucket_policy.trail_log_bucket_policy
  ]
}