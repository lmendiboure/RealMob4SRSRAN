# Description

Le dépôt contient l’ensemble des configurations, scripts, et outils nécessaires pour déployer et tester une infrastructure 5G O-RAN, avec des scénarios de mobilité. 
Il a été développé dans le cadre d’un stage au Laboratoire d’Informatique Gaspard-Monge (LIGM).


# Prérequis

Avant d’utiliser ce dépôt, assurez-vous que votre environnement est correctement configuré :

    Systèmes requis : Linux (Ubuntu 22.04 recommandé).
    Dépendances logicielles :
        Docker et Docker Compose
        GNU Radio
        Python 3.11 et les bibliothèques nécessaires.
        Open5GS, srsRAN, et Oran-sc-ric

# Fichiers Disponibles dans le Dépôt
Ce dépôt contient plusieurs fichiers essentiels pour la configuration et l’exécution des différents scénarios de mobilité. Voici une description détaillée des fichiers et de leur utilisation :

### Fichiers yaml (amf, upf et smf)
Les fichiers ```amf.yaml```, ```upf.yaml``` et ```smf.yaml``` sont des fichiers essentiels à la configuration du cœur de réseau Open5GS. Ils définissent les paramètres nécessaires pour le bon fonctionnement de chaque composant du réseau et leur interconnexion avec le gNB.

Ces fichiers sont situés dans le répertoire suivant : ```/etc/open5gs/ ```

Il est impératif de maintenir une cohérence entre ces fichiers YAML et le fichier de configuration du gNB. Les paramètres à vérifier incluent notamment :
- Les adresses IP utilisées pour les interfaces du cœur de réseau (AMF, UPF et SMF) et leur correspondance avec les adresses IP configurées dans le fichier YAML du gNB.
- Les ports spécifiés pour les communications entre les composants du cœur et le gNB.

### Fichiers de Configuration des UEs et gNBs
- Des fichiers de configuration sont disponibles pour 4 UEs fonctionnant à des largeurs de bande de 10 Hz et 20 Hz.
- Des fichiers de configuration sont également fournis pour un gNB configuré pour des bandes passantes de 10 Hz et 20 Hz.
- Pour le cas d’un déploiement avec deux gNBs, des fichiers spécifiques sont fournis : ```gnb1.yaml``` et ```gnb2.yaml```, chacun configuré pour un gNB distinct.

### Fichiers GNU Radio (GRC)
Plusieurs fichiers GNU Radio Companion (GRC) sont disponibles pour simuler différents scénarios.
Les fichiers GRC sont nommés en suivant une convention claire : ngnb_scenariom.grc, où :
- n représente le nombre de gNBs.
- m représente le nombre d’UEs.
- Par exemple :
    - 1gnb_scenario4.grc correspond à une simulation avec 1 gNB et 4 UEs.
    - 2gnb_scenario3.grc correspond à une simulation avec 2 gNBs et 3 UEs.
      
### Fichiers JSON pour les Datasets
Les fichiers JSON générés représentent les datasets produits pour les cinq scénarios de mobilité, grâce au script ```subband.py```.

Voici une description de chaque scénario :

#### Scenario 1 :
Ce scénario implique quatre UEs se déplaçant à une vitesse de 60 km/h. L’UE1 reste fixe à une distance constante de 500m par rapport au gNB, tandis que les trois autres UEs (UE2, UE3, et UE4) se déplacent dans le sens positif, avec des positions initiales respectives de X0=100, −900, et 700.

#### Scenario 2 :
Ce scénario est similaire au précédent, sauf que les UEs se déplacent dans le sens négatif.

#### Scenario 3 :
Dans ce scénario, l’UE1 n’est plus fixe et commence à X0=−300, se déplaçant dans le sens positif avec UE2. Les UE3 et UE4, quant à eux, se déplacent dans le sens négatif.

#### Scenario 4 :
Ce scénario met en scène deux UEs se déplaçant dans des directions opposées.
L’UE1 commence à X0=1500 et se déplace dans le sens négatif.
L’UE2 commence à X0=−1300 et se déplace dans le sens positif.

#### Scenario 5 :
Ce dernier scénario reprend les positions initiales du scénario 4, mais cette fois, les deux UEs se déplacent tous les deux dans le sens positif.


# Instructions d’Utilisation

## 1 Lancement des Composants de Base
Pour lancer les composants de base nécessaires au déploiement de la plateforme (comme le gNB, le cœur de réseau (5GC), et le Near-RT-RIC etc), vous pouvez suivre le guide détaillé
disponible sur la documentation officielle de srsRAN : https://docs.srsran.com/projects/project/en/latest/tutorials/source/near-rt-ric/source/index.html 

Pour le lancement de Grafana, qui permet la visualisation des métriques, vous pouvez consulter la documentation ici : https://docs.srsran.com/projects/project/en/latest/user_manuals/source/grafana_gui.html


## 2 Lancement de l'xApp pour la Remontée des Métriques
L’xApp personnalisé, qui collecte et centralise les métriques des UEs et du gNB, doit être lancé dans le conteneur Docker du RIC. Voici comment le démarrer :
```bash
cd ./oran-sc-ric
sudo docker compose exec python_xapp_runner2 ./simple_mon_xapp.py
```
L'éxécuteur python ```python_xapp_runner2``` a été ajouté (docker-compose.yml du ric) pour répondre aux besoins de l'xApp crée. Cependant l'exécuteur ```python_xapp_runner``` donné par ORAN est conservé et doit etre utilisé les xApps fourni par ORAN SC RIC.
Cet xApp crée collectera des métriques clés, telles que le CQI, les débits (UL/DL), et la latence etc, et les sauvegardera dans un fichier JSON pour une analyse ultérieure.

## 3 Scripts Réalisés(7 Python et 1 Shell), et Comment les Utiliser
Ce dépôt contient huit scripts principaux (sept en Python et un en Shell) qui permettent de gérer, déployer et analyser l’infrastructure mise en place. Chaque script est conçu pour répondre à un besoin spécifique et peut être exécuté depuis le répertoire où il est placé dans le dépôt Git.

### Lancer les Scripts
Pour exécuter un script Python, utilisez la commande suivante :
```bash
python3.11 nom_du_script.py  
```
Le script Shell, nommé lancement.sh, se lance avec la commande suivante :

```bash
./lancement.sh <nombre_gnb> <nombre_ue> <nombre_ric>  
```
Par exemple, pour déployer 1 gNB, 4 UEs, et 1 RIC :
```bash
./lancement.sh 1 4 1  
```

### Limites Actuelles

Pour l’instant, le script lancement.sh permet de lancer jusqu’à 2 gNBs sans intégrer de RIC. Cependant, il est facile de rajouter des gNBs ou de configurer le lancement du RIC. Il suffit de :

- Ajouter une nouvelle boucle ou commande dans le fichier lancement.sh pour gérer les gNBs supplémentaires.
- Modifier les configurations associées (adresses IP, ports, etc.) dans les fichiers neceessaires.

NB: Pour intégrer ORAN SC RIC dans cet environnement, il faudra autant de RIC que de gNB ( un ric pour un gNB).

Le script est conçu pour être flexible et extensible, permettant ainsi de gérer des architectures plus complexes avec peu d’effort.

### Personnalisation et Flexibilité
Le script ```lancement.sh``` est conçu pour être flexible. Avant de l’exécuter, certaines modifications peuvent être nécessaires pour l’adapter à votre environnement :
- Répertoires : Réajustez les chemins des répertoires en fonction de l’endroit où les fichiers sont placés.
- Comptes utilisateurs : Modifiez les mots de passe ou identifiants utilisés dans le script pour qu’ils correspondent à votre configuration.
- Ajouts personnalisés : Ce script est suffisamment flexible pour permettre l’ajout de nouvelles fonctionnalités ou de composants supplémentaires si besoin.

### Emplacement des Scripts
Certains scripts Python sont situés dans :
```bash
/srsRAN_Project/build/apps/gnb/    
```
Les autres scripts Python et le script Shell se trouvent dans le même répertoire que le dossier ```srsRAN_Project```.

### Descriptions des Scripts
Chaque script contient une description en tête de fichier pour expliquer :
- Son objectif : Ce que le script accomplit (ex. collecte de métriques, génération de datasets).
- Les prérequis : Ce dont vous avez besoin pour l’exécuter correctement (ex. bibliothèques Python, configurations spécifiques).

### Envoie des metrics à influxDB
Un autre conteneur ``` influxdb1``` a été ajouté dans le docker-compose.yml (celui dans /srsRAN_Project/docker/) pour ajouter une autre instance d'InfluxDB. 
Ce conteneur devrait créer un compte utilisateur influxdb qui sera donc accessible sur http://localhost:8087/.
Cependant ce compte peut ne pas être crée, et pourra donc être crée avec ceci:
```bash
sudo docker exec -it influxdb1 influx setup \
--username admin1 \
--password admin12345 \
--org srs1 \
--bucket srsran1 \
--token 605bc59413b7d5457d181ccf20f9fda15693f81b068d70396cc183081b264fbb \
--host http://localhost:8087
```
Si vous changez un de ces paramétres lors de la création du compte, Faites de même sur le script ```envoie_influxdb.py```!
L’envoi des métriques à la base de données InfluxDB est réalisé grâce au script ```envoie_influxdb.py```. Ce script permet de transférer en temps réel les métriques générées par les UEs vers InfluxDB, facilitant leur visualisation et leur analyse ultérieure.

Lors du premier déploiement, il est nécessaire de s’assurer que les fichiers nécessaires existent avant de lancer le script. Pour cela, il faut d’abord démarrer les UEs (sans lancer GNU Radio), puis les arrêter immédiatement après. Cette étape permet aux UEs de créer les fichiers nécessaires pour le fonctionnement du script.

Une fois les fichiers générés, le script ```envoie_influxdb.py``` doit être lancé avant de relancer les UEs pour que les métriques puissent être surveillées et envoyées en temps réel à InfluxDB.

### Génération des Datasets
La génération des datasets repose sur deux scripts principaux : ```metrics_udp_receiver.py``` et ```subband.py```. Le premier est utilisé pour collecter en temps réel les métriques réseau transmises par le gNB via le protocole UDP. Ce script doit être lancé après le démarrage du gNB et peut être lancé avant ou après le lancement des UEs. Une fois les métriques collectées, le script subband.py est utilisé pour les traiter et les enrichir. Ce dernier, exécuté à la fin de l’expérience après l’arrêt de metrics_udp_receiver.py, calcule notamment les subbands CQI en décomposant le CQI global en plusieurs sous-valeurs. Les données finales sont ensuite sauvegardées dans des fichiers JSON, constituant les datasets nécessaires pour les analyses ou les expérimentations futures.

### Récupération des dashboards de grafana en image (png)
Un contenneur renderer(nom à conserver) a été ajouté sur le fichier docker-compose.yml (celui dans /srsRAN_Project/docker/) et lié à grafana. 
Voici les étapes à faire pour récupérer les limages depuis l'interface grafana:
- Sur tableau de bord à exporter, en haut à droite, cliquez sur les trois points verticaux pour ouvrir un menu supplémentaire.
- Dans ce menu, cliquez sur l'option "Share".
- Une fois dans l'interface Share, vous verrez plusieurs options de personnalisation pour l'exportation :
  - Vous pouvez choisir le thème de l'image : soit le thème par défaut (noir), dark, ou light. Si vous voulez que le fond de l'image soit blanc, choisissez light.

