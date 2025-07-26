# Graph Neural Networks – Self-Study Projects

After developing an interest in Graph Neural Networks, I read parts of [Graph Representation Learning](https://www.cs.mcgill.ca/~wlh/grl_book/files/GRL_Book.pdf), and experimented with GNNs in two small projects.

---

## 📁 Projects Overview

### 1. **Protein Classification – Enzyme vs Non-Enzyme**
 
**Description:** 
Enzymes are a specific class of proteins that play a central role in cellular metabolism by catalyzing the chemical reactions necessary for proper cell function. Being able to determine whether a protein is an enzyme or not can aid in the search for therapeutic targets for treating certain diseases, and also support the design of biocatalysts. 

I explored the application of GNNs to predict whether a protein functions as an enzyme based solely on its amino acid structure.

**Task:** Graph classification 

---

### 2. **Prediction of trophic relationships**

**Description:**  
The structure of a trophic network is constrained by the species and potential interactions that exist within the regional pool, also known as the trophic meta-network (metaweb). Each local community that makes up the metaweb can exhibit different trophic structures. [Ecological network assembly](https://nadiah.org/wp-content/uploads/2022/02/Saravia22-Metaweb_determines_local_food_webs.pdf)

The goal of this project is to predict potential trophic relationships induced by the introduction of a new species into a given ecosystem. The trophic network can be modeled as a graph where nodes represent species and edges represent trophic interactions.

**Task:** Link prediction  


---

## 🛠 Tools & Libraries

- Python
- Deep Graph Library (DGL), Pytorch
- NetworkX
- MLFlow
- Scikit-learn, NumPy, Pandas, etc.

---

## 📚 What I Learned

- The concept of message passing
- Aggregation functions and update functions
- Differences between node, link, and graph-level prediction tasks
- GNN architectures: GCN, GAT, GraphSAGE, etc.
- Proteins structures
---

Feel free to explore each project folder for notebook, and details about experiments.
