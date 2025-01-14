"""


Description : 
Ce script analyse un fichier JSON contenant des métriques de station de base (gNB) pour chaque utilisateur (UE). 
Il génère un fichier JSON de sortie contenant des informations enrichies, notamment la répartition des sous-bandes 
(subbands) pour chaque UE, calculée en fonction de la qualité de canal (CQI).

Fonctionnalités principales :
- Lecture d'un fichier JSON d'entrée contenant les métriques gNB.
- Génération de nombres pseudo-aléatoires représentant la répartition des sous-bandes pour chaque UE.
- Écriture des données enrichies dans un fichier JSON de sortie.

"""


import random
import json

# Fonction pour générer une liste de nombres répartissant la valeur CQI sur les subbands
def generate_numbers(c, s):
    """
    Génère une liste de nombres représentant la répartition du CQI sur les sous-bandes.
    :param c: Valeur CQI totale.
    :param s: Nombre de sous-bandes.
    :return: Liste de longueurs `s` contenant les valeurs réparties.
    """
    
    if c == 0:
        return [0] * s  # Retourne s fois 0 si cqi est égal à 0
    c -= s  # Réduire c de s pour garantir que chaque nombre soit au moins 1
    numbers = []
    for i in range(s):
        if i == s - 1:
            numbers.append(c + 1)  # Ajouter 1 pour compenser la réduction initiale
        else:
            x = random.randint(0, c)
            numbers.append(x + 1)  # Ajouter 1 pour garantir que le nombre soit au moins 1
            c -= x
    return numbers

def main():
    # Demander à l'utilisateur le nombre de subbands
    subband = int(input("Entrez le subband (un entier positif): "))
    if subband <= 0:
        raise ValueError("Le subband doit être un entier positif")

    input_filename = 'gnb_metrics.json'  # Nom du fichier d'entrée
    output_filename = 'scenario1.json'  # Nom du fichier de sortie

    try:
        with open(input_filename, 'r') as f:
            data = [json.loads(line) for line in f]

        output_data = []  # Liste pour stocker les données enrichies

        for entry in data:
            timestamp = entry["timestamp"]
            average_latency = entry["cell_metrics"]["average_latency"]
            ue_list = entry["ue_list"]
            
            for ue_index, ue in enumerate(ue_list):
                ue_data = ue["ue_container"]
                cqi = ue_data["cqi"]
                dl_mcs = ue_data["dl_mcs"]
                ul_mcs = ue_data["ul_mcs"]
                dl_brate = ue_data["dl_brate"]
                ul_brate = ue_data["ul_brate"]
                
                # Générer les subbands réparties en fonction du CQI
                numbers = generate_numbers(cqi, subband)
                
                output_entry = {
                    "timestamp": timestamp,
                    "ue": f"UE{ue_index + 1}",
                    "cqi": cqi,
                    "subbands": numbers,
                    "dl_mcs": dl_mcs,
                    "ul_mcs": ul_mcs,
                    "average_latency": average_latency,
                    "dl_brate": dl_brate,
                    "ul_brate": ul_brate
                }
                
                output_data.append(output_entry)
        
        # Écriture des données enrichies dans le fichier JSON de sortie
        with open(output_filename, 'w') as f:
            json.dump(output_data, f, indent=4) # Enregistrer avec une indentation pour la lisibilité
        
        print(f"Données écrites dans {output_filename}")

    except ValueError as e:
        print("Erreur:", e)
    except FileNotFoundError:
        print(f"Le fichier {input_filename} est introuvable.")
    except json.JSONDecodeError:
        print("Erreur lors de la lecture du fichier JSON.")

if __name__ == "__main__":
    main()

