import json
import pickle
import numpy as np
import pandas as pd
import os

dataset_path = "./data/pdbbind/"

# Charger la matrice Y réduite
with open(os.path.join(dataset_path, "Y"), "rb") as f:
    Y = pickle.load(f)

# Charger les protéines conservées
with open(os.path.join(dataset_path, "proteins.txt")) as f:
    proteins = json.load(f)
protein_ids = list(proteins.keys())

# Charger les ligands
with open(os.path.join(dataset_path, "ligands_can.txt")) as f:
    ligands = json.load(f)
ligand_ids = list(ligands.keys())

# Vérifier dimensions cohérentes
assert Y.shape == (len(ligand_ids), len(protein_ids)), f"Shape mismatch: Y = {Y.shape}, ligands = {len(ligand_ids)}, proteins = {len(protein_ids)}"

# Construire dataframe avec triplets
rows = []
for i, ligand_id in enumerate(ligand_ids):
    for j, protein_id in enumerate(protein_ids):
        value = Y[i, j]
        if not np.isnan(value):
            rows.append({
                "Ligand_ID": ligand_id,
                "Protein_ID": protein_id,
                "Affinity_pKd": value
            })

df = pd.DataFrame(rows)

# Sauvegarder en CSV
output_path = os.path.join(dataset_path, "ligand_protein_affinities.csv")
df.to_csv(output_path, index=False)

print(f"{len(df)} entrées enregistrées dans {output_path}")
