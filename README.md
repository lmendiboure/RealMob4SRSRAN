# Description

Le dépôt contient l’ensemble des configurations, scripts, et outils nécessaires pour déployer et tester une infrastructure 5G O-RAN, avec des scénarios de mobilité. 
Il a été développé dans le cadre d’un stage au Laboratoire d’Informatique Gaspard-Monge (LIGM).


# Prérequis

Avant d’utiliser ce dépôt, assurez-vous que votre environnement est correctement configuré :

    Systèmes requis : Linux (Ubuntu 22.04 recommandé).
    Dépendances logicielles :
        Docker et Docker Compose
        GNU Radio
        Python 3.11 et les bibliothèques nécessaires (voir requirements.txt).
        Open5GS, srsRAN, et Oran-sc-ric

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
Cet xApp collectera des métriques clés, telles que le CQI, les débits (UL/DL), et la latence etc, et les sauvegardera dans un fichier JSON pour une analyse ultérieure.

## 3 Scripts Réalisés et Comment les Utiliser



