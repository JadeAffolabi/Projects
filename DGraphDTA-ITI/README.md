# DGraphDTA-ITI (Generalization Analysis)

## Overview
This repository hosts an academic deep learning project that aims to analyze the generalization capabilities of the DGraphDTA architecture.

DGraphDTA (Double Graph DTA predictor) is a method for predicting the affinity between drug compounds and proteins using graph neural networks (GNNs). The original model and methodology are described in the following research paper: ["DGraphDTA: A graph neural network-based drug–target affinity prediction method"](https://pubs.rsc.org/en/content/articlelanding/2020/ra/d0ra02297g).

This repository is based on the original implementation available at: [https://github.com/595693085/DGraphDTA](https://github.com/595693085/DGraphDTA).

## Objectives
- **Evaluate Generalization**: Investigate how well the DGraphDTA model generalizes across different datasets.
- **Hands-on Deep Learning**: Gain practical experience with deep learning challenges such as training, optimization, and scalability.
- **High-Performance Computing (HPC) Training**: Utilize the Mesonet HPC cluster for large-scale training and evaluation.

## Project Structure
```
DGraphDTA-Generalization
│── data/               # Datasets used for training and evaluation
│── figures/            # Saved loss and prediction plot on test set
│── mlruns/             # MLFlow tracking informations
│── *.py                # Python files
│── README.md           # Project documentation
```

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- PyTorch
- CUDA (if using GPU)

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/DGraphDTA-ITI.git
   cd dgraphdta
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
### Training the Model
To train the DGraphDTA model, run:
```sh
python training.py MODEL_NAME DATASET_NAME FOLD_NUMBER
```

### Evaluating the Model
To evaluate the trained model:
```sh
python test.py MODEL_NAME DATASET_NAME FOLD_NUMBER
```

## HPC Training on Mesonet
```sh
sbatch train_script.sh MODEL_NAME DATASET_NAME FOLD_NUMBER
```
## HPC Testing on Mesonet
```sh
sbatch test_script.sh MODEL_NAME DATASET_NAME FOLD_NUMBER
```

## Generate dataset on Mesonet
```sh
sbatch exec_scripts.sh
```
## Dataset Generation Guide

Due to storage limits, the datasets are not hosted directly in this repository.

- To get the davis dataset we invite you to go on the original [repository](https://github.com/595693085/DGraphDTA?tab=readme-ov-file)

- To get the bindingDB dataset, please follow this guide. 

This guide details the steps required to prepare and generate the dataset used by DGraphDTA. In our project, we use it for BindingDB_Kd (to create protein.txt, ligands_can.txt and Y, use binding.py and pip install PyTDC) and pdbBind.

Download and extract the **UniClust30** database (required for HHblits):

```sh
wget https://wwwuser.gwdguser.de/~compbiol/uniclust/2018_08/uniclust30_2018_08_hhsuite.tar.gz
mkdir -p dataset/uniclust
tar -xzf uniclust30_2018_08_hhsuite.tar.gz -C dataset/uniclust/
```

Install anaconda (https://www.anaconda.com/docs/getting-started/miniconda/install#linux-terminal-installer)
```sh
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

Set Up the Conda Environment

Create and activate the environment using the provided environment.yml file:

```sh
conda env create -f environment.yml
conda activate dgraphdta
```

Install these dependencies :

```sh
pip install pconsc4
conda install -c conda-forge -c bioconda hhsuite
conda install -c conda-forge biopython
```

Modify these paths in scripts.py :

```sh
HHblits_bin_path = '..'  # HHblits bin path
HHblits_db_path = '..'  # uniclust path
HHfilter_bin_path = '..' # HHfilter bin path
reformat_bin_path = '..' # in scripts/reformat.pl of your environment
convertAlignment_bin_path = '..' # ./scripts/convert_alignment.py
```
You can find the HHblits(resp. HHfilter) bin path with : which hhblits (resp. hhfilter)

convert_align comes from ccmpred (https://github.com/soedinglab/CCMpred) 


Don't forget in the end, use adapt_dataset.py to remove untraited proteins and create_folds.py.  
## Major changes made to the files

For the generation of the new datasets:

- binding.py
- create_folds.py
- adapt_dataset.py
- merge_davis_binding.py

For modifications related to training and testing:

- training.py
- test.py

## Acknowledgments
- The original [DGraphDTA repository](https://github.com/595693085/DGraphDTA)
- The research paper: [DGraphDTA](https://pubs.rsc.org/en/content/articlelanding/2020/ra/d0ra02297g)

## License
This project is for academic use only. Refer to the original repository for licensing details.




