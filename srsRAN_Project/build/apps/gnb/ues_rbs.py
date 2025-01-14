"""

Description :
Ce script analyse un fichier de journal (`gnb.log`) pour extraire des informations relatives aux utilisateurs 
équipés (UE) en fonction de leur RNTI. Les informations extraites comprennent :
- L'horodatage (timestamp),
- Les indices de ressources physiques (PRB) et leur étendue,
- Le type de canal (DL ou UL),
- Le calcul des blocs de ressources (RB) utilisés.

Les informations sont écrites dans un fichier de sortie (`ue_rb.log`) pour chaque UE identifié, avec les directions 
descendantes (DL) et montantes (UL) indiquées.

Prérequis :
- Un fichier d'entrée `gnb.log` contenant des lignes formatées avec des champs spécifiques.


"""

import re

# Nom des fichiers
input_filename = '/tmp/gnb.log'
output_filename = 'ue_rb.log'

# Regex pour extraire le timestamp et les valeurs spécifiques
timestamp_pattern = re.compile(r'T([\d:.]+)')
rnti_pattern = re.compile(r'rnti=0x(\d{4})')
prb_pattern = re.compile(r'prb=\[(\d+), (\d+)\)')

# Fonction pour déterminer l'UE en fonction du RNTI
def determine_ue(rnti):
    if rnti == '4601':
        return 'ue0'
    elif rnti == '4602':
        return 'ue1'
    elif rnti == '4603':
        return 'ue2'
    else:
        return None

# Fonction pour déterminer si c'est du DL ou UL en fonction du type de canal
def determine_direction(line):
    if 'PDSCH' in line or 'PDCCH' in line:
        return 'dl'
    elif 'PUSCH' in line or 'PUCCH' in line:
        return 'ul'
    else:
        return None

# Lire le fichier d'entrée et traiter les lignes
with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
    for line in infile:
        print(f"Traitement de la ligne : {line.strip()}")  # Log de chaque ligne traitée

        # Vérifier si la ligne commence par un '-'
        if line.strip().startswith('-'):
            print("Ligne ignorée, commence par '-'.")
            continue

        # Extraire le timestamp
        timestamp_match = timestamp_pattern.search(line)
        if not timestamp_match:
            print("Timestamp non trouvé.")
            continue  # Passer cette ligne si aucun timestamp trouvé
        timestamp = timestamp_match.group(1)
        print(f"Timestamp trouvé : {timestamp}")

        # Extraire le RNTI
        rnti_match = rnti_pattern.search(line)
        if not rnti_match:
            print("RNTI non trouvé.")
            continue  # Passer cette ligne si aucun RNTI trouvé
        rnti = rnti_match.group(1)
        print(f"RNTI trouvé : {rnti}")

        # Déterminer l'UE
        ue = determine_ue(rnti)
        if not ue:
            print("RNTI ne correspond pas aux UEs définis, ligne ignorée.")
            continue  # Passer cette ligne si le RNTI ne correspond pas aux UEs définis
        print(f"UE déterminé : {ue}")

        # Extraire la valeur du PRB
        prb_match = prb_pattern.search(line)
        if not prb_match:
            print("Valeur PRB non trouvée.")
            continue  # Passer cette ligne si aucune valeur PRB trouvée
        prb_start = int(prb_match.group(1))  # Extraire la valeur de 'a'
        prb_end = int(prb_match.group(2))    # Extraire la valeur de 'b'
        prb_value = f"prb=[{prb_start}, {prb_end})"
        print(f"Valeur PRB trouvée : {prb_value}")

        # Calculer la valeur du RB
        rb_value = prb_end - prb_start
        print(f"Valeur RB calculée : {rb_value}")

        # Déterminer le type de canal (DL ou UL)
        direction = determine_direction(line)
        if direction:
            print(f"Direction déterminée : {direction}")
        else:
            print("Aucune direction déterminée (ni DL ni UL), ligne ignorée.")
            continue  # Passer cette ligne si aucune direction (DL ou UL) n'est trouvée

        # Écrire les informations extraites dans le fichier de sortie avec RB et direction ajoutés
        outfile.write(f"{ue} timestamp: {timestamp} {prb_value} rb={rb_value} {direction}\n")

print(f"Toutes les lignes valides ont été enregistrées dans {output_filename}.")

