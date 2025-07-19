import numpy as np
import random
import json
import os
import pickle

# Config
dataset = "pdbbind"
folds_dir = f'./data/{dataset}/folds/'
os.makedirs(folds_dir, exist_ok=True)
random.seed(42)

# Charger la matrice Y
Y = pickle.load(open(f'./data/{dataset}/Y', 'rb'))

label_row_inds, label_col_inds = np.where(np.isnan(Y) == False)
n_folds=5

folds = [[] for _ in range(n_folds)]

# Mélanger les indices des données
indices = list(range(len(label_row_inds)))  # Utilise les indices des données valides (non-NaN)
random.shuffle(indices)

# Diviser les indices en folds
for i, idx in enumerate(indices):
    folds[i % n_folds].append(idx)

# Créer le fichier test_fold_setting1.txt (1/3)
test_fold = folds[0]  # Le premier fold comme test
with open(folds_dir + "test_fold_setting1.txt", "w") as f:
    json.dump(test_fold, f)

# Créer le fichier train_fold_setting1.txt (2/3)
train_folds = [folds[i] for i in range(1, n_folds)]  # Les autres folds comme train
with open(folds_dir + "train_fold_setting1.txt", "w") as f:
    json.dump(train_folds, f)

