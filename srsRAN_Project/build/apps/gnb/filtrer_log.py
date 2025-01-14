"""
Description :
Ce script analyse un fichier de journal (`gnb.log`) pour filtrer uniquement les lignes contenant certains mots-clés, 
tels que `pusch:`, `pdsch:`, `rb=`, ou `prb=`, tout en excluant celles qui commencent par un trait d'union (`-`).
Les lignes correspondantes sont ensuite sauvegardées dans un fichier de sortie (`gnb_filtre.log`).

Objectif :
- Faciliter l'analyse des fichiers de journal en conservant uniquement les informations pertinentes.

Prérequis :
- Un fichier d'entrée `gnb.log` avec un format contenant les mots-clés à rechercher.

"""



import re

# Nom des fichiers avec chemins complets
input_filename = '/home/ligm/gnb.log'
output_filename = 'gnb_filtre.log'  # Fichier dans le répertoire de l'exécution

# Compilons une regex pour correspondre à 'pusch:', 'pdsch:', 'rb=' et 'prb=' avec des espaces avant
pattern = re.compile(r'\s+(pusch:|pdsch:|prb=)')
exclude_pattern = re.compile(r'^\s*-')  # Regex pour exclure les lignes commençant par '-'

# Lire le fichier d'entrée et écrire les lignes filtrées dans le fichier de sortie
with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
    for line in infile:
        if exclude_pattern.match(line):
            continue  # Passer les lignes commençant par '-'
        if pattern.search(line):
            outfile.write(line)

print(f"Toutes les lignes contenant 'pusch:', 'pdsch:', 'rb=' ou 'prb=' (sans commencer par '-') ont été enregistrées dans {output_filename}.")

