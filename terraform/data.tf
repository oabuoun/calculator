data "aws_ami" "oabu_web_server_ami_linux" {
  most_recent = true
  owners      = ["amazon"]
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*"]
  }
}

data "aws_subnet_ids" "oabu_web_server_subnet_tf" {
  vpc_id = aws_default_vpc.oabu_web_server_vpc_tf.id
}
