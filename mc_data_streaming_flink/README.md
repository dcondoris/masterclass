# MC Data Streaming
![alt text](https://www.startdataengineering.com/images/stream_de_project/system_design.png)
## Première Partie : Slides + Script

Présenter les notions du streaming de Données, Kafka et Flink avec ces [slides](https://github.com/DataScientest/dst_masterclass/blob/main/mc_data_streaming_flink/Streaming%20des%20donn%C3%A9es.pptx)

[Script texte](https://github.com/DataScientest/dst_masterclass/blob/main/mc_data_streaming_flink/Script_MC.txt) qui guide le contenu de chaque slide et explique un peu le déroulement de la démo technique.

## Deuxième Partie Démo avec `Kafka` et `Flink`
![alt text](https://www.openlogic.com/sites/default/files/image/2022-11/image-blog-ol-kafka-vs-flink.png)

- Changer `IP_VM` dans le fichier docker-compose.yaml

- Créer une dossier comme mc_datastreaming 
```
mkdir mc_datastreaming
cd mc_datastreaming
```shell
- Create a virtual environement et l'activer
```shell
python -m venv mc_venv
source  mc_venv/bin/activate
```
- Installer les packages 
pip install -r requirements.txt

- Lancement des conteneurs avec `docker compose` (avec 3 brokers pour scalabilité)
docker-compose up --scale kafka=3 -d

- Vérification conteneur (you should see only 1)
```shell
docker ps
```
- Ouvrir Kafka UI dans son navigateur à l'adresse <VM-ip-adress>:8080

- Créer les topics Kafka `Twitter` et  `Consumer`
  
- Executer le Producteur Kafka pour envoyer de la donnée au Topic Kafka `Twitter`

```shell
 python producer.py
```

![alt text](https://miro.medium.com/v2/resize:fit:604/1*crc4eMmIFJ3uqY848r6SQg.png)

 - Lancer script Flink `demo_flink_kafka.py` qui va aller lire les tweets dans le topic `Twitter`, faire des calculs à la volée et envoyer les nouvelles données au topic `Consumer` :
 
  ```shell
 python3 demo_flink_kafka.py
```

- Consommer la donnée avec un dashboard :

```shell
python producer.py
```
```shell
python dashboard.py
```
