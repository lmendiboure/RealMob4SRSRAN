"""

Description : Ce script surveille un fichier CSV spécifié et ajoute un horodatage pour chaque nouvelle ligne ajoutée. 
Les données avec horodatage sont écrites dans un fichier de sortie. Cela est utile pour suivre les modifications 
en temps réel sur le fichier d'entrée.

Fonctionnalités principales :
- Surveillance des modifications d'un fichier CSV en utilisant la bibliothèque `watchdog`.
- Ajout automatique d'un horodatage (timestamp) pour chaque nouvelle ligne détectée.

Prérequis :
- La bibliothèque `watchdog` installée (`pip install watchdog`).
- Chemins d'accès valides pour les fichiers d'entrée et de sortie.

"""



import time
import os
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

class ObservateurFichier(FileSystemEventHandler):
    def __init__(self, chemin_fichier, fichier_sortie):
        # Initialisation de l'observateur pour surveiller un fichier spécifique.
        self.chemin_fichier = chemin_fichier
        self.fichier_sortie = fichier_sortie
        self.derniere_position = 0  # Position pour continuer la lecture du fichier
        self.premiere_ligne = True  # Indicateur pour la première ligne

    def on_modified(self, event):
        """
        Méthode appelée lorsque le fichier surveillé est modifié.
        :param event: Événement de modification détecté par watchdog.
        """
        if event.src_path == self.chemin_fichier:
            with open(self.chemin_fichier, 'r') as fichier:
                fichier.seek(self.derniere_position)
                lignes = fichier.readlines()
                self.derniere_position = fichier.tell()

            if lignes:
                for ligne in lignes:
                    # Vérifier si c'est la première ligne écrite dans le fichier de sortie
                    if self.premiere_ligne:
                        contenu = f"timestampss;{ligne.strip()}\n"
                        self.premiere_ligne = False  # Marquer que la première ligne a été écrite
                    else:
                        # Utiliser l'horodatage réel pour les lignes suivantes
                        horodatage = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                        contenu = f"{horodatage};{ligne.strip()}\n"

                    with open(self.fichier_sortie, 'a') as fichier_sortie:
                        fichier_sortie.write(contenu)

if __name__ == "__main__":
    chemin_fichier = "/tmp/ue1_metrics.csv"
    fichier_sortie = "/home/ligm/metrics_timestamp.csv"

    # Supprimer le fichier de sortie s'il existe déjà
    if os.path.exists(fichier_sortie):
        os.remove(fichier_sortie)

    # Vérifier que le fichier d'entrée existe
    if os.path.exists(chemin_fichier):
        gestionnaire_evenement = ObservateurFichier(chemin_fichier, fichier_sortie)
        observateur = Observer()
        observateur.schedule(gestionnaire_evenement, path=chemin_fichier, recursive=False)
        observateur.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observateur.stop()
        observateur.join()
    else:
        print(f"Erreur : Le fichier {chemin_fichier} n'existe pas.")

