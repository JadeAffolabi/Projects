import numpy as np
import json, pickle
from collections import OrderedDict

def merge_arrays_with_nan(A, B):
    rows_A, cols_A = A.shape
    rows_B, cols_B = B.shape

    total_rows = rows_A + rows_B
    total_cols = cols_A + cols_B

    merged = np.full((total_rows, total_cols), np.nan)

    # Place A in the top-left
    merged[:rows_A, :cols_A] = A

    # Place B in the bottom-right
    merged[rows_A:, cols_A:] = B

    return merged

if __name__ == "__main__":
    Y_davis = pickle.load(open('./data/' + 'davis' + '/' + 'Y', 'rb'), encoding='latin1')
    Y_binding = pickle.load(open('./data/' + 'binding' + '/' + 'Y', 'rb'), encoding='latin1')

    ligands_davis = json.load(open('./data/' + 'davis' + '/' + 'ligands_can.txt'), object_pairs_hook=OrderedDict)
    proteins_davis = json.load(open('./data/' + 'davis' + '/' + 'proteins.txt'), object_pairs_hook=OrderedDict)

    ligands_binding = json.load(open('./data/' + 'binding' + '/' + 'ligands_can.txt'), object_pairs_hook=OrderedDict)
    proteins_binding = json.load(open('./data/' + 'binding' + '/' + 'proteins.txt'), object_pairs_hook=OrderedDict)

    #Transform affinity from Kd to pKd
    transformed_Y_davis_list = [-np.log10(y / 1e9) for y in Y_davis]
    transformed_Y_davis = np.asarray(transformed_Y_davis_list)
v   #Transform affinity from Kd to pKd
    transformed_Y_binding_list = [-np.log10(y / 1e9) for y in Y_binding]
    transformed_Y_binding = np.asarray(transformed_Y_binding_list)

    #Merged Affinities
    Y_dv_kb = merge_arrays_with_nan(transformed_Y_davis, transformed_Y_binding)
    with open("./data/davis_binding/Y", "wb") as file:
        pickle.dump(Y_dv_kb, file)


    offset = len(np.where(np.isnan(Y_davis)==False)[0])

    #Merge train folds
    train_folds_davis = json.load(open('./data/' + 'davis' + '/'+ 'folds/train_fold_setting1.txt'))
    train_folds_binding = json.load(open('./data/' + 'binding' + '/'+ 'folds/train_fold_setting1.txt'))

    #All the first 2 folds of binding are one element bigger than the other folds
    train_folds_binding[1] = train_folds_binding[1][:-1]
    train_folds_binding[0] = train_folds_binding[0][:-1]

    #Add the offset of (ligand-protein) index to the list of indexes of binding
    new_train_folds_binding = np.array(train_folds_binding) + offset
    new_train_folds_binding_list = new_train_folds_binding.tolist()

    new_train_folds = [dv_list + kb_list for dv_list, kb_list in zip(train_folds_davis, new_train_folds_binding_list)]

    for train_fold in new_train_folds:
    random.shuffle(train_fold)

    with open("data/davis_binding/folds/train_fold_setting1.txt", "w") as file:
        json.dump(new_train_folds, file)
    
    #Merge test folds
    test_folds_davis = json.load(open('./data/' + 'davis' + '/'+ 'folds/test_fold_setting1.txt'))
    test_folds_binding = json.load(open('./data/' + 'binding' + '/'+ 'folds/test_fold_setting1.txt'))

    new_test_folds_binding = np.array(test_folds_binding) + offset
    new_test_folds_binding_list = new_test_folds_binding.tolist()

    new_test_folds = test_folds_davis + new_test_folds_binding_list
    random.shuffle(new_test_folds)

    with open("data/davis_binding/folds/test_fold_setting1.txt", "w") as file:
        json.dump(new_test_folds, file)
        