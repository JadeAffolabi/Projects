import os
import sys
import torch
import numpy as np
from random import shuffle
import matplotlib.pyplot as plt
from torch_geometric.data import Batch

from emetrics import get_aupr, get_cindex, get_rm2, get_ci, get_mse, get_rmse, get_pearson, get_spearman
from utils import *
from scipy import stats
from gnn import GNNNet  # Modèle de réseau de neurones graphiques 
from data_process import create_dataset_for_test  
from lifelines.utils import concordance_index

def predicting(model, device, loader):
    """Effectue des prédictions sur l'ensemble de test."""
    model.eval()
    total_preds = torch.Tensor()
    total_labels = torch.Tensor()
    print('Make prediction for {} samples...'.format(len(loader.dataset)))
    with torch.no_grad():
        for data in loader:
            data_mol = data[0].to(device)  # Données moléculaires
            data_pro = data[1].to(device)  # Données protéiques
            output = model(data_mol, data_pro)
            total_preds = torch.cat((total_preds, output.cpu()), 0)
            total_labels = torch.cat((total_labels, data_mol.y.view(-1, 1).cpu()), 0)
    return total_labels.numpy().flatten(), total_preds.numpy().flatten()

def calculate_metrics(model_name, Y, P, dataset='davis'):
    """Calcule les métriques de performance et les enregistre dans un fichier."""
    cindex = get_cindex(Y, P)  
    cindex2 = get_ci(Y, P)     
    rm2 = get_rm2(Y, P)
    mse = get_mse(Y, P)
    pearson = get_pearson(Y, P)
    spearman = get_spearman(Y, P)
    rmse = get_rmse(Y, P)

    # Sauvegarde des résultats dans un fichier
    result_file_name = 'models/' + model_name + '/' + 'test_results.txt'
    result_str = 'Dataset : ' + dataset + '\r\n'
    result_str += f'rmse:{rmse} mse:{mse} pearson:{pearson} spearman:{spearman} ci:{cindex} rm2:{rm2}\n'
    with open(result_file_name, 'a') as file:
       file.writelines(result_str)
    
    return cindex2, mse, pearson

def plot_density(plot_path, Y, P, dataset='davis'):
    """Crée un graphique de densité entre les valeurs réelles et prédites."""
    plt.figure(figsize=(10, 5))
    plt.grid(linestyle='--')
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.scatter(P, Y, color='blue', s=40)
    plt.title('density of ' + dataset, fontsize=30, fontweight='bold')
    plt.xlabel('predicted', fontsize=30, fontweight='bold')
    plt.ylabel('measured', fontsize=30, fontweight='bold')

    # Trace une ligne de référence diagonale selon le dataset
    if dataset == 'davis':
        plt.plot([5, 11], [5, 11], color='black')
    else:
        plt.plot([6, 16], [6, 16], color='black')

    plt.legend(loc=0, numpoints=1)
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()
    plt.setp(ltext, fontsize=12, fontweight='bold')
    plt.savefig(plot_path, dpi=500, bbox_inches='tight')

if __name__ == '__main__':
    # Récupération du nom du modèle et du dataset depuis la ligne de commande
    model_name = sys.argv[1]
    print('Model : ', model_name)
    dataset = sys.argv[2]

    # Définition des chemins
    model_file_name = 'models/'+model_name + '/' + model_name + '.pth'
    plot_path = 'figures/' + model_name + '/' + 'density_' + dataset + '.png'

    # Chargement du modèle
    TEST_BATCH_SIZE = 512
    device = torch.device("cuda:0" if torch.cuda.is_available() else 'cpu')
    model = GNNNet()
    model.to(device)

    # Chargement du checkpoint du modèle
    checkpoint = torch.load(model_file_name)
    model.load_state_dict(checkpoint["model"])

    # Création du DataLoader pour le test
    test_data = create_dataset_for_test(dataset)
    test_loader = torch.utils.data.DataLoader(test_data, batch_size=TEST_BATCH_SIZE, shuffle=False,
                                              collate_fn=collate)

    # Initialisation de l’expérience MLflow
    experiment_name = "Tests"
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name=model_name):
        # Prédiction et évaluation
        Y, P = predicting(model, device, test_loader)
        ci, mse, pearson = calculate_metrics(model_name, Y, P, dataset)
        plot_density(plot_path, Y, P, dataset)

        # Log des résultats dans MLflow
        mlflow.set_tag("Test Dataset", dataset)
        mlflow.log_metric("Test CI", float(f"{ci:.3}"))
        mlflow.log_metric("Test mse", float(f"{mse:.3}"))
        mlflow.log_metric("Test pearson", float(f"{pearson:.3}"))
        mlflow.log_artifact(plot_path)

    print("Test complete.")
