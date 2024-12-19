# Création et Configuration de l’Infrastructure

Ce document décrit les étapes nécessaires pour créer et configurer votre infrastructure à l’aide de Terraform et Ansible.

## Prérequis

- **Terraform** installé sur votre machine
- **Ansible** installé sur votre machine
- Une clé SSH pour accéder à l’instance distante (fichier `.pem`)

## Étape 1 : Création de l’Infrastructure avec Terraform

1. Initialiser le répertoire Terraform :
   ```bash
   terraform init

Cette commande télécharge et installe les plugins nécessaires.

2. Valider la configuration Terraform
    ```bash
    terraform validate

3. Planifier l’exécution
    bash
    terraform plan

4. Appliquer les changements
    ```bash
    terraform apply -auto-approve
À la fin de cette étape, vous devriez avoir une ou plusieurs instances déployées et prêtes à être configurées.

## Étape 2 : Configuration de l’Infrastructure avec 

## Tester l’inventaire Ansible
Vérifiez que les hôtes dans votre inventaire inventory/hosts sont accessibles :

    ```bash
    ansible -i inventory/hosts all -m ping

**Exemple de sortie**
    '''text
    51.44.166.214 | SUCCESS => {
        "ansible_facts": {
            "discovered_interpreter_python": "/usr/bin/python3"
        },
        "changed": false,
        "ping": "pong"
    }
    '''
Exécution du Playbook Docker
Pour installer et configurer Docker sur vos instances :
    ```bash
    ansible-playbook -i inventory/hosts docker-playbook.yml

Connexion à l’Instance
Pour vous connecter à l’instance (exemple d’adresse IP) :
```bash
ssh -i /root/keys/my-terraform-key.pem ubuntu@13.36.167.142

Vérifiez la version de Docker :
    ```bash
    docker --version

Exemple de sortie
text
Docker version 26.1.3, build 26.1.3-0ubuntu1~24.04.1

Lancement de Scripts Python via Ansible
Pour exécuter un script Python (ex: train.py) sur l’instance :
    ```bash
    ansible all -i inventory/hosts -u ubuntu -b -m command -a "python3 /opt/mlflow/train.py"

Ou avec un playbook :
    ```bash
    ansible-playbook -i inventory/hosts -u ubuntu -b -m command -a "python3 /opt/mlflow/train.py"


