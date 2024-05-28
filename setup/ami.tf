resource "aws_ami_from_instance" "create_ami" {
  name               = "slave-image"
  source_instance_id = aws_instance.slave.id

  depends_on = [aws_instance.master, aws_instance.slave]
}