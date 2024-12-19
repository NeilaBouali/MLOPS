# Création et Configuration de l'Infrastructure

## Étape 1: Création de l'Infrastructure avec Terraform

1. **Initialiser Terraform :**
   ```bash
   terraform init
Valider la configuration :

bash
Copier le code
terraform validate
Vérifier le plan d'exécution :

bash
Copier le code
terraform plan
Appliquer les changements :

bash
Copier le code
terraform apply -auto-approve
Étape 2: Configuration d'Ansible
Tester l'Inventory
Testons la connexion à l'inventaire avec Ansible pour vérifier que tout fonctionne correctement.

bash
Copier le code
ansible -i inventory/hosts all -m ping
Sortie attendue :

ruby
Copier le code
51.44.166.214 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
Exécution du Playbook
Pour exécuter le playbook Ansible, utilisez la commande suivante :

bash
Copier le code
ansible-playbook -i inventory/hosts docker-playbook.yml
Connexion à l'Instance
Pour se connecter à l'instance via SSH, utilisez la commande suivante :

bash
Copier le code
ssh -i /root/keys/my-terraform-key.pem ubuntu@13.36.167.142
Vérification de la Version de Docker
Pour vérifier la version de Docker, utilisez la commande suivante :

bash
Copier le code
docker --version
Sortie attendue :

ruby
Copier le code
ubuntu@ip-172-31-12-77:~$ docker --version
Docker version 26.1.3, build 26.1.3-0ubuntu1~24.04.1
Exécution de Commande via Ansible
Pour exécuter un script Python via Ansible, utilisez la commande suivante :

bash
Copier le code
ansible all -i <votre_inventory> -u ubuntu -b -m command -a "python3 /opt/mlflow/train.py"
Ou, pour exécuter le playbook :

bash
Copier le code
ansible-playbook -i inventory/hosts -u ubuntu -b -m command -a "python3 /opt/

