# 🕸️ Prediction of Trophic Relationships

## 📊 Dataset

The dataset consists of **three essential files**:

- **📋 list edges.csv**  
  Contains all trophic relationships (graph edges) between species.  
  Includes columns for **source nodes** and **target nodes**.

- **📋 clean species and taxo.csv**  
  Provides metadata for each species in the metaweb, such as: dentifier, class, order, family, and scientific name.

- **📦 data species.pickle**  
  Contains species characteristics (e.g: 🌙 nocturnal, ☀️ diurnal, 🦴 vertebrate, 🐁 small mammal).  
  Each characteristic is encoded as **1** if present, **0** otherwise.

The resulting trophic network graph includes **1,151 nodes** and **83,568 edges**, spanning amphibians, reptiles, birds, and mammals.

---

## 🧪 Experiments

This project uses an **encoder-decoder architecture**:

- **Encoder:** Generates a new embedding for each species by incorporating its own features and those of its neighbors.  
- **Decoder:** Predicts the presence of an edge between two species based on their embeddings.

The edge prediction task is framed as a **binary classification problem**, following the **SEAL method**:  
- ✅ Existing edges are treated as **positive samples**  
- ❌ Non-existing edges are sampled as **negative samples**


The encoder chose is a **GraphSAGE** GNN.  
For the decoder, two options are considered:

- **Dot product** between the embeddings of two nodes  
- **MLP (Multi-Layer Perceptron)**

---

## 💬 Discussion

- **Batch training** is not suitable, as the model overfits from the start. Dropout does not alleviate this issue.  
- **GraphSAGE** and **GCN** show similar performance, suggesting that the chosen architectures were not sufficiently optimized to leverage each model’s strengths.  
- Typically, **GraphSAGE** is expected to outperform GCN in link prediction due to its inductive learning capability and neighborhood subsampling.  
- The **GAT** model performs poorly and also overfits.

A detailed analysis of the **GraphSAGE model's** 10 largest errors on the test set reveals:

- ❗ For **non-existent links**, the model most often misclassifies relationships involving **mammals**.  
- ❗ For **existent links**, the majority of errors involve **birds**.

---
