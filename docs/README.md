###MLOps Project: End-to-End Deployment with CI/CD and IaC

Introduction

Ce projet a pour objectif de mettre en place une chaîne complète MLOps, en intégrant les meilleures pratiques de DevOps et les outils spécifiques au Machine Learning (ML). Nous avons choisi une approche d'Infrastructure as Code (IaC) et un pipeline CI/CD automatisé afin de garantir la scalabilité, la fiabilité et l'efficacité des déploiements.

Technologies Utilisées

1. Infrastructure Cloud

AWS : Nous avons choisi AWS comme fournisseur cloud pour sa robustesse, sa documentation exhaustive et sa grande compatibilité avec les outils d'automatisation.

Instances EC2 : Utilisation d'instances EC2 pour déployer nos services (API, MLflow, monitoring).

S3 : Stockage des modèles ML versionnés avec MLflow.

2. Infrastructure as Code (IaC)

Terraform : Utilisé pour créer, configurer et gérer les ressources AWS de manière automatisée. Voici un exemple de configuration utilisée dans notre fichier main.tf :

provider "aws" {
  region = "eu-west-3" # Région AWS
}

resource "aws_instance" "app_server" {
  ami           = "ami-045a8ab02aadf4f88"
  instance_type = "t2.micro"
  subnet_id     = data.aws_subnet.existing_subnet.id
  key_name      = "my-terraform-key"

  tags = {
    Name = "AppServer"
  }
}

3. Configuration des Serveurs

Ansible : Automatisation de la configuration des instances EC2 (installation de Docker, déploiement des applications, configuration des services comme Prometheus, Grafana, et MLflow).

4. Conteneurisation

Docker : Chaque composant (API ML, MLflow, Monitoring) est encapsulé dans un conteneur Docker pour garantir l'isolation et la portabilité.

5. Machine Learning Tracking

MLflow : Utilisé pour le suivi des expériences et la gestion du versionnement des modèles ML.

6. CI/CD

GitHub Actions : Mise en place d'un pipeline CI/CD pour :

Exécuter des tests automatisés.

Créer des images Docker.

Déployer automatiquement les services sur AWS.

7. Monitoring

Prometheus : Collecte des métriques d'infrastructure et d'application.

Grafana : Visualisation des métriques pour faciliter le monitoring et la détection des problèmes.

Structure du Projet

MLOps/
├── .github/workflows/
│   └── ci-cd.yml
├── docs/
│   ├── api_documentation.md
│   ├── installation_guide.md
│   └── README.md
├── infra/
│   ├── ansible/
│   │   ├── inventory/
│   │   │   └── hosts
│   │   └── roles/
│   │       ├── api/
│   │       │   ├── files/
│   │       │   │   ├── api.py
│   │       │   │   ├── Dockerfile
│   │       │   │   └── requirements.txt
│   │       │   └── tasks/
│   │       │       └── main.yml
│   │       ├── docker/
│   │       │   ├── handlers/
│   │       │   │   └── main.yml
│   │       │   └── tasks/
│   │       │       └── main.yml
│   │       ├── mlflow/
│   │       │   ├── files/
│   │       │   │   ├── Dockerfile
│   │       │   │   └── train.py
│   │       │   └── tasks/
│   │       │       └── main.yml
│   │       └── monitoring/
│   │           └── tasks/
│   │               └── main.yml
│   └── docker-playbook.yml
├── train.py
└── main.tf

Fonctionnalités

Infrastructure Cloud Automatisée

Provisionnement des ressources via Terraform (EC2, S3, groupes de sécurité).

Application ML

API pour les prédictions, développée en Python.

Versionnement des modèles ML avec MLflow.

CI/CD

Pipeline GitHub Actions incluant :

Lancement de tests unitaires.

Build et push des images Docker.

Déploiement automatique sur EC2.

Monitoring

Suivi des métriques d'infrastructure et de performance des modèles.

Visualisation des métriques dans Grafana.

Tests

Pour garantir la qualité et la stabilité du projet, nous avons effectué :

Tests unitaires : Couverture des principales fonctionnalités de l'API.

Tests de charge : Simulation de requêtes massives sur l'API pour évaluer les performances.

Tests d'intégration : Validation des interactions entre les différents composants (API, MLflow, monitoring).

Documentation

Le répertoire contient :

Un README détaillé avec la structure du projet et les choix techniques.

Un guide d'installation pas à pas pour répliquer l'infrastructure.

Une documentation API incluant les endpoints et exemples de requêtes.