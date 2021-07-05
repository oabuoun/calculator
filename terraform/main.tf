terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"
}

resource "aws_default_vpc" "oabu_web_server_vpc_tf"{

}

resource "aws_security_group" "oabu_web_server_security_group_tf" {
  name = "oabu_web_server_security_group"

  vpc_id = aws_default_vpc.oabu_web_server_vpc_tf.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port    = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "oabu_web_server_instance_tf" {
  ami                         = data.aws_ami.oabu_web_server_ami_linux.id //"ami-0f89681a05a3a9de7"
  instance_type               = "t2.micro"
  subnet_id                   = tolist(data.aws_subnet_ids.oabu_web_server_subnet_tf.ids)[0]
  associate_public_ip_address = true
  key_name                    =  "cyber-oabu-key"
  vpc_security_group_ids      = [aws_security_group.oabu_web_server_security_group_tf.id]

  tags = {
      Name = "Oabu Web Server"
  }

  connection {
    type = "ssh"
    host = self.public_ip
    user = "ec2-user"
    private_key = file("/home/kali/.ssh/cyber-oabu-key.pem")
  }

  provisioner "file" {
    source = "../init-scripts"
    destination = "/tmp/init-scripts"
  }

  provisioner "file" {
    source = "../.mysql_password"
    destination = "/tmp/.mysql_password"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/init-scripts/docker_install.sh",
      "/tmp/init-scripts/docker_install.sh",
    ]
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/init-scripts/mysql_install.sh",
      "/tmp/init-scripts/mysql_install.sh",
    ]
  }

  provisioner "file" {
    source = "../init-sql"
    destination = "/tmp"
  }

  provisioner "remote-exec" {
    when = destroy
    inline = [
      "chmod +x /tmp/init-scripts/stop.sh",
      "/tmp/init-scripts/stop.sh",
    ]
  }

}

resource "aws_volume_attachment" "oabu_web_server_db_volume_attachment_tf" {
  device_name = "/dev/xvdz"
  volume_id   = "vol-0e32e0dd6a7e660f4"
  instance_id = aws_instance.oabu_web_server_instance_tf.id
  skip_destroy = true

  connection {
    type = "ssh"
    host = aws_instance.oabu_web_server_instance_tf.public_ip
    user = "ec2-user"
    private_key = file(var.aws_private_key)
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/init-scripts/mount.sh",
      "/tmp/init-scripts/mount.sh",
    ]
  }

  provisioner "remote-exec" {
    inline = [
      "cd /tmp/init-scripts/",
      "chmod +x launch.sh",
      "./launch.sh",
    ]
  }
}
