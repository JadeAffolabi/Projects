from tdc.multi_pred import DTI
import json
import pandas as pd
import numpy as np
import os
import pickle
from collections import OrderedDict

# Créer le dossier
dataset = "binding1"
dataset_path = f"./data/{dataset}/"
os.makedirs(dataset_path, exist_ok=True)

# Charger le dataset
data_obj = DTI(name='BindingDB_Kd')
data_obj.harmonize_affinities(mode = 'max_affinity')
data = data_obj.get_data()
# Nettoyer les données (enlever les Kd <= 0)
data = data[data['Y'] > 0]
print(data[5:])
# Construire dictionnaire des ligands
ligand_ids = OrderedDict()
for row in data.itertuples():
    ligand_ids[row.Drug_ID] = row.Drug

with open(dataset_path + "ligands_can.txt", "w") as f:
    json.dump(ligand_ids, f)

# Construire dictionnaire des protéines
protein_ids = OrderedDict()
for row in data.itertuples():
    protein_ids[row.Target_ID] = row.Target

with open(dataset_path + "proteins.txt", "w") as f:
    json.dump(protein_ids, f)

# Indices
ligand_list = list(ligand_ids.keys())
protein_list = list(protein_ids.keys())
ligand_index = {k: i for i, k in enumerate(ligand_list)}
protein_index = {k: i for i, k in enumerate(protein_list)}

# Initialiser la matrice avec des NaN
Y = np.full((len(ligand_list), len(protein_list)), np.nan)

# Remplir la matrice d'affinité avec pKd
for row in data.itertuples():
    l_idx = ligand_index.get(row.Drug_ID)
    p_idx = protein_index.get(row.Target_ID)
    if l_idx is not None and p_idx is not None:
        Y[l_idx, p_idx] = row.Y

# Sauvegarder au format pickle
with open(dataset_path + "Y", "wb") as f:
    pickle.dump(Y, f)
