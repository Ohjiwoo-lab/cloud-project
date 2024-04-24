# 생성한 키 페어를 등록
resource "aws_key_pair" "make_keypair" {
  key_name   = "ansible_keypair"
  public_key = file("./key/ansible_keypair.pub")
}