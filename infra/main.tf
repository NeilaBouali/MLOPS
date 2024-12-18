provider "aws" {
  region = "eu-west-3" # Région AWS
}

# Référencement d'un groupe de sécurité existant
data "aws_security_group" "existing_sg" {
  name = "default" 
}

# Référencement d'un sous-réseau existant
data "aws_subnet" "existing_subnet" {
  id = "subnet-010f84a7f317ca2b7" # ID du sous-réseau existant
}

# Instance EC2
resource "aws_instance" "app_server" {
  ami           = "ami-045a8ab02aadf4f88" # AMI valide
  instance_type = "t2.micro"
  subnet_id     = data.aws_subnet.existing_subnet.id

  # Associer le groupe de sécurité existant
  vpc_security_group_ids = [data.aws_security_group.existing_sg.id]

  # Associer une clé SSH existante
  key_name = "my-terraform-key" # Remplacez par le nom exact de votre Key Pair sur AWS

  tags = {
    Name = "AppServer"
  }
}

# Créer un nouveau groupe de sécurité avec des règles spécifiques
resource "aws_security_group" "app_sg" {
  name        = "app-sg"
  description = "Group for App Server"
  vpc_id      = data.aws_subnet.existing_subnet.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5000 # Pour MLflow
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Remplacez par votre IP publique
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# S3 Bucket
resource "aws_s3_bucket" "ml_models" {
  bucket = "mlflow-model-storage"

  tags = {
    Name        = "MLFlow Model Storage"
    Environment = "Dev"
  }
}



