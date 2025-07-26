# 🧬 Protein Classification – Enzyme vs Non-Enzyme

## 📊 Dataset

**PROTEINS** is a dataset of proteins labeled as either **“enzyme”** or **“non-enzyme.”**  
Each protein is represented as a **graph**, where:

- Nodes = amino acids  
- Edges = pairs of amino acids less than **6 Ångströms** apart

This dataset is accessible via `dgl.data.TUDataset`, which provides access to the **TUDatasets** — a widely used collection of benchmark datasets for **graph classification** and **regression** tasks.

---

## 🧪 Experiments

To address the classification task, the model consists of two main components:

- **🔷 Encoder:** A **Graph Neural Network** (GCN or GAT) that encodes the protein structure into a **latent representation**
- **🔶 Decoder:** A **Multi-Layer Perceptron (MLP)** that maps the latent representation to a binary output: enzyme or non-enzyme

This setup frames the problem as a **graph classification task**.

---

## 💬 Discussion

The final model did **not achieve satisfactory performance**.
The state-of-the-art model, **HGP-SL**, achieves **84.91 ± 1.62% accuracy**  

These results prompt a few important questions:

1. 🧩 **Feasibility** — Can a single model realistically learn shared features across **thousands of enzyme types**?  
2. 🎯 **Relevance** — In practice, knowing whether a protein is an enzyme isn't always enough. We're often more interested in:
   - Its **specific catalytic function**
   - Or its **biological role** in a pathway

Instead of binary classification, more nuanced tasks could be explored.

