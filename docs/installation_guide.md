Etape1: Création de l'infrastructure 
terraform init #Initialiser Terraform 
terraform validate #Valider la configuration   
terraform plan #Vérifier le plan d'exécution 
terraform apply -auto-approve #Pour appliquer les changements 

Configuration de Ansible ------------------------
Tester inventory
ansible -i inventory/hosts all -m ping
en sortie -
51.44.166.214 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
} - 

Exécution
ansible-playbook -i inventory/hosts docker-playbook.yml

Connection à l'instance:
ssh -i /root/keys/my-terraform-key.pem ubuntu@13.36.167.142

Vérification de la version docker:
docker --version
 En sortie:
 ubuntu@ip-172-31-12-77:~$ docker --version
Docker version 26.1.3, build 26.1.3-0ubuntu1~24.04.1


ansible all -i <votre_inventory> -u ubuntu -b -m command -a "python3 /opt/mlflow/train.py"

ansible-playbook -i inventory/hosts -u ubuntu -b -m command -a "python3 /opt/mlflow/train.py"

