import sys, os
import torch
import torch.nn as nn
from pathlib import Path
import matplotlib.pyplot as plt
from torch_geometric.data import DataLoader
import pickle
from gnn import GNNNet
from utils import *
from emetrics import *
from data_process import create_dataset_for_5folds
import mlflow

# Fonction pour tracer l'évolution de la loss au cours des epochs
def plot_loss(loss_history, plot_path):
    plt.plot(loss_history["Train"], label="Train loss")
    plt.plot(loss_history["Val"], label="Val loss")
    plt.xlabel("Epoch")
    plt.ylabel("MSE Loss")
    plt.grid()
    plt.legend()
    plt.savefig(plot_path+"/"+"loss.png")
    plt.close()

# Classe pour gérer la sauvegarde du modèle, incluant l'early stopping
class ModelCheckpoint:
    def __init__(self, model_name, model_dir, 
                 earlyStopping=False, patience=5, delta=0, save_last_epoch=False, save_best_model=False):
        self.checkpoint_file = model_dir + "/" + model_name + '.pth'
        self.model_dir = model_dir
        self.saved_score = None
        self._with_earlyStopping = earlyStopping
        self.save_last_epoch = save_last_epoch
        self.save_best_model = save_best_model
        self.delta = delta if earlyStopping else 0
        self.counter = 0 if earlyStopping else None
        self.early_stop = False if earlyStopping else None
        self.patience = patience if earlyStopping else None

    def save_checkpoint(self, model, optimizer):
        torch.save({"model" : model.state_dict(),
                    "optimizer" : optimizer.state_dict(),
                    }, self.checkpoint_file)

    def load_checkpoint(self, model, optimizer):
        checkpoint = torch.load(self.checkpoint_file)
        model.load_state_dict(checkpoint['model'])
        optimizer.load_state_dict(checkpoint['optimizer'])

    def _update_checkpoint(self, model, optimizer, 
                           loss, loss_history, epoch):
        self.saved_score = loss
        if self._with_earlyStopping:
            self.counter = 0
        self.save_checkpoint(model, optimizer)
        if epoch:
            with open(self.model_dir+"/"+"stop.txt", "w") as file:
                file.write(f"Current epoch = {epoch}; Val_loss = {self.saved_score}")
        if loss_history:
            with open(self.model_dir+"/"+"loss_history.pkl", "wb") as file:
                pickle.dump(loss_history, file)
        plot_loss(loss_history, self.model_dir)

    def __call__(self, model, loss, optimizer,
                 epoch=None, loss_history=None):
        score = loss      
        if self.saved_score is None:
            self.saved_score = score
        elif self.saved_score - score < self.delta:
            if self._with_earlyStopping:
                self.counter += 1
                if self.counter >= self.patience:
                    self.early_stop = True
        elif self.save_best_model:
                self._update_checkpoint(model, optimizer, score, loss_history, epoch)

        if self.save_last_epoch:
            self._update_checkpoint(model, optimizer, score, loss_history, epoch)

# Fonction d'entraînement sur un seul fold
def train_process(model_name, train_params):
    fold = [0, 1, 2, 3, 4][int(sys.argv[3])]
    DATASETS = train_params["Datasets"]
    BATCH_SIZE = train_params["Batch size"]
    NUM_EPOCHS = train_params["Epochs"]
    LR = train_params["Learning rate"]
    print('Learning rate: ', LR)
    print('Epochs: ', NUM_EPOCHS)

    model_dir = './models/' + model_name
    figures_dir = "./figures/" + model_name

    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    USE_CUDA = torch.cuda.is_available()
    device = torch.device("cuda:0" if USE_CUDA else 'cpu')
    model = GNNNet()
    model.to(device)

    loss_fn = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)

    checkpoint = ModelCheckpoint(model_name, model_dir, save_last_epoch=True)
    loss_history = {"Train":[], "Val":[]}

    for dataset in DATASETS:
        train_data, valid_data = create_dataset_for_5folds(dataset, fold)
        
        train_loader = torch.utils.data.DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True,
                                                collate_fn=collate)
        valid_loader = torch.utils.data.DataLoader(valid_data, batch_size=BATCH_SIZE, shuffle=False,
                                                collate_fn=collate)

        for epoch in range(NUM_EPOCHS):
            train(model, device, train_loader, optimizer, epoch + 1, loss_history["Train"])
            print('predicting for valid data')
            G, P = predicting(model, device, valid_loader)
            val = get_mse(G, P)
            loss_history["Val"].append(val)
            print('valid mse:', val)
            checkpoint(model, val, optimizer, epoch, loss_history)
            if checkpoint.early_stop:
                print("Ealy stopping.")
                with open(model_dir+"/"+"stop.txt", "a") as file:
                    file.write("Early stopping.")
                break
        print("Training complete.")

    os.remove(model_dir+"/"+"loss.png")
    plot_loss(loss_history, figures_dir)
    return val, figures_dir

# Fonction de cross-validation pour évaluer la robustesse du modèle
def cross_validation_process(model_name, train_params):
    DATASETS = train_params["Datasets"]
    BATCH_SIZE = train_params["Batch size"]
    NUM_EPOCHS = train_params["Epochs"]
    LR = train_params["Learning rate"]
    print('Learning rate: ', LR)
    print('Epochs: ', NUM_EPOCHS)

    model_dir = './models/' + model_name
    figures_dir = "./figures/" + model_name
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    USE_CUDA = torch.cuda.is_available()
    device = torch.device("cuda:0" if USE_CUDA else 'cpu')
    
    fold_results = []  # Liste des scores pour chaque fold
    
    for fold in range(5):
        print(f"\n=== Starting Fold {fold} ===")
        model = GNNNet()
        model.to(device)
        
        loss_fn = nn.MSELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=LR)
        
        fold_model_dir = f"{model_dir}/fold_{fold}"
        fold_figures_dir = f"{figures_dir}/fold_{fold}"
        os.makedirs(fold_model_dir, exist_ok=True)
        os.makedirs(fold_figures_dir, exist_ok=True)
            
        checkpoint = ModelCheckpoint(model_name, fold_model_dir, save_last_epoch=True)
        loss_history = {"Train":[], "Val":[]}

        for dataset in DATASETS:
            train_data, valid_data = create_dataset_for_5folds(dataset, fold)
            train_loader = torch.utils.data.DataLoader(train_data, batch_size=BATCH_SIZE, 
                                                     shuffle=True, collate_fn=collate)
            valid_loader = torch.utils.data.DataLoader(valid_data, batch_size=BATCH_SIZE, 
                                                     shuffle=False, collate_fn=collate)

            for epoch in range(NUM_EPOCHS):
                train(model, device, train_loader, optimizer, epoch + 1, loss_history["Train"])
                print('predicting for valid data')
                G, P = predicting(model, device, valid_loader)
                val = get_mse(G, P)
                loss_history["Val"].append(val)
                print(f'Fold {fold} Epoch {epoch+1} valid mse:', val)
                checkpoint(model, val, optimizer, epoch, loss_history)
                if hasattr(checkpoint, 'early_stop') and checkpoint.early_stop:
                    print("Early stopping.")
                    with open(fold_model_dir+"/"+"stop.txt", "a") as file:
                        file.write("Early stopping.")
                    break
        
        fold_results.append(val)
        plot_loss(loss_history, fold_figures_dir)
    
    avg_val = sum(fold_results) / len(fold_results)
    print(f"\n=== Cross Validation Results ===")
    print(f"Average Validation MSE: {avg_val:.4f}")
    print("Individual fold results:", fold_results)
    
    return avg_val, figures_dir, fold_results

# Exécution d'un run mlflow avec log des métriques et paramètres
def mlflow_run(experiment_name, run_name, tag, train_params, model_params = None):
    mlflow.set_experiment(experiment_name)
    with mlflow.start_run(run_name=run_name):
        if model_params is not None:
            mlflow.log_params(model_params)
        mlflow.log_params(train_params)
        mlflow.set_tag(tag["key"], tag["value"])

        # Cross validation # à commenter si non utilisée
        # avg_loss, artifact_path, fold_results = cross_validation_process(model_name, train_params)
        # mlflow.log_metric("Avg Val loss mse", float(f"{avg_loss:.3}"))
        # for i, loss in enumerate(fold_results):
        #     mlflow.log_metric(f"Fold {i} Val loss", float(f"{loss:.3}"))

        # Entraînement standard
        loss, artifact_path = train_process(model_name, train_params)
        mlflow.log_metric("Val loss mse", float(f"{loss:.3}"))
        mlflow.log_artifact(artifact_path)

# Point d'entrée principal
if __name__ == "__main__":
    model_name = sys.argv[1]
    datasets = [sys.argv[i] for i in range(2, len(sys.argv)-1)]
    BATCH_SIZE = 512
    NUM_EPOCHS = 500
    LR = 0.001
    train_params = {
        "Batch size" : BATCH_SIZE,
        "Epochs" : NUM_EPOCHS,
        "Learning rate" : LR,
        "Datasets" : datasets
    }
    tag = {"key":"Origin", "value":"DGraphDTA"}

    experiment_name = "Cross Validation"
    mlflow_run(experiment_name, model_name, tag, train_params)
