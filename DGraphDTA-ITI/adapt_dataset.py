import os
import json
import pickle
import numpy as np
from tdc.multi_pred import DTI

# ---------- Nettoyage des datasets ----------

base_path = "./data/pdbbind/"
pcons4_path = os.path.join(base_path, "pconsc4")
#data = DTI(name='BindingDB_Kd').get_data()
#np.savetxt(os.path.join(base_path, "Y_avant_avant.txt"), data['Y'], fmt="%.5f", delimiter="\t")


# ---------- Étape 1 : Récupérer les protéines à garder ----------
proteins_to_keep = set(
    os.path.splitext(f)[0]
    for f in os.listdir(pcons4_path)
    if os.path.isfile(os.path.join(pcons4_path, f))
)

# ---------- Étape 2 : Charger proteins.txt et filtrer ----------
with open(os.path.join(base_path, "proteins.txt")) as f:
    protein_dict = json.load(f)

all_protein_ids = list(protein_dict.keys())
id_to_index = {k: i for i, k in enumerate(all_protein_ids)}

# Garder uniquement les protéines présentes dans pconsc4 (triées pour cohérence)
kept_protein_ids = sorted(pid for pid in all_protein_ids if pid in proteins_to_keep)
kept_indices = [id_to_index[pid] for pid in kept_protein_ids]
kept_proteins = {pid: protein_dict[pid] for pid in kept_protein_ids}

# ---------- Étape 3 : Charger Y ----------
with open(os.path.join(base_path, "Y"), "rb") as f:
    Y = pickle.load(f)

# Sauvegarder Y avant réduction dans un fichier texte
#np.savetxt(os.path.join(base_path, "Y_avant.txt"), Y, fmt="%.5f", delimiter="\t")

# ---------- Étape 4 : Réduire Y aux colonnes (protéines) conservées ----------
Y_reduced = Y[:, kept_indices]

# ---------- Étape 5 : Supprimer les lignes (ligands) qui n'ont plus d'affinité connue ----------
valid_ligands_mask = ~np.isnan(Y_reduced).all(axis=1)
Y_final = Y_reduced[valid_ligands_mask]

# Sauvegarder Y_final après réduction dans un fichier texte
np.savetxt(os.path.join(base_path, "Y_apres.txt"), Y_final, fmt="%.5f", delimiter="\t")

# ---------- Étape 6 : Mettre à jour ligands_can.txt ----------
with open(os.path.join(base_path, "ligands_can.txt")) as f:
    ligand_dict = json.load(f)

ligand_ids = list(ligand_dict.keys())  # ordre initial
filtered_ligand_ids = [ligand_ids[i] for i, valid in enumerate(valid_ligands_mask) if valid]
filtered_ligand_dict = {lid: ligand_dict[lid] for lid in filtered_ligand_ids}

# ---------- Étape 7 : Sauvegardes ----------
# Sauver Y final
with open(os.path.join(base_path, "Y"), "wb") as f:
    pickle.dump(Y_final, f)

# Sauver proteins.txt mis à jour
with open(os.path.join(base_path, "proteins.txt"), "w") as f:
    json.dump(kept_proteins, f)

# Sauver ligands_can.txt mis à jour
with open(os.path.join(base_path, "ligands_can.txt"), "w") as f:
    json.dump(filtered_ligand_dict, f)

print(f"{len(kept_proteins)} protéines conservées.")
print(f"{len(filtered_ligand_dict)} ligands conservés.")
print("Les fichiers Y_avant.txt et Y_apres.txt ont été générés.")
