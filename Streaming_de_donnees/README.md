# Comment prendre en main la démonstration

## Sur votre machine locale

1. Téléchargez l'archive **streaming_demo.tar** sur votre machine locale.  

2. Démarrez votre machine virtuelle.  

3. Utilisez la commande suivante en changeant les éléments entre crochets **<>** :

```
scp -i <path_to_your_pem_file>/data_enginering_machine.pem <path_to_the_archive>/streaming_demo.tar ubuntu@<your_vm_ip_addr>:/home/ubuntu/  
```

## Depuis votre machine virtuelle :  

4. Décompressez l'archive depuis le dossier /home/ubuntu :

```
tar xvf streaming_demo.tar  
```

5. Rendez-vous dans le dossier /home/ubuntu/streaming_demo :

```
cd /home/ubuntu/streaming_demo  
```

6. Installez le package python3.8-venv si vous ne l'avez pas :  

    6.a. Mettez à jour le gestionnaire de paquets apt :
    
    ```
    sudo apt-get update  
    ```

    6.b. Installez le package python3.8-venv :
    
    ```
    sudo apt-get install -y python3.8-venv  
    ```

7. Lancez le script d'initialisation comme ceci en changeant les éléments entre crochets **<>** :

```
bash init.sh <your_vm_ip_addr>  
```

8. Lancez les conteneurs docker à l'aide du fichier **Makefile**:

```
make  
```

9. Lancez les 2 autres brokers kafka :

```
make scale3  
```

10. Depuis l'interface utilisateur de kafka sur le navigateur à l'adresse `<your_vm_ip_addr>:8080`, créez le topic twitter.  

11. Entrez dans votre environnement virtuel python :

```
source venv/bin/activate  
```

12. Dans cet environnement python :

    12.a. Lancez le **producer** :
    
    ```
    python3 producer.py  
    ```

    12.b. Dans une autre fenêtre, lancez le **consumer** :
    
    ```
    python3 consumer.py  
    ```

    12.c. Dans une autre fenêtre, lancez le programme **live_dash.py** :
    
    ```
    python3 live_dash.py  
    ```

13. Rendez-vous à l'adresse `<your_vm_ip_addr>:8050` sur le navigateur pour voir l'évolution du dashboard.
