# README: Clustering & Evaluation Task (Alvin Phan)

## Role in Group Project

This document describes the work completed by **Alvin Phan** as part of a group project on 5G Network Performance Analysis. My task was focused exclusively on **clustering and evaluation**, using a dataset pre-processed by Savindu and Chung. The output of this stage feeds into Maisha’s forecasting task.

The saved directory for this project can be accessed via this link below:
https://drive.google.com/drive/folders/1Y1B1n_ddsYAEVwDBjVrewPzL3_UYevRg?usp=sharing
---

## 💻 How to Run

1. Upload files to Google Drive: `drive/MyDrive/COS40007 Design Project/data/processed/` ⚠️Make sure to change path or modify your own path to match⚠️
2. Open **Clustering & Analysis.ipynb** in Google Colab
3. Use `cluster_ready.csv` as the dataset input
4. Adjust `sample_size` in each method, default = 30,000 rows (most reliable, consistently crashing past 50k)
5. Restart runtime after each method if memory is limited

> Tested on a 10GB RAM session. Agglomerative clustering is the most memory intensive.

---

## 📊 Clustering Results (sample size: 30,000)

| Method            | Silhouette Score (↑) | Davies-Bouldin Index (↓) |
| ----------------- | -------------------- | ------------------------ |
| **K-Means**       | 0.487                | 0.824                    |
| **DBSCAN**        | 0.324                | 1.252                    |
| **Agglomerative** | 0.417                | 0.953                    |

---

## 🔍 Summary

* Optimal number of clusters (`k`) determined using **Elbow Method** → `k=4`
* **K-Means** gave the best overall performance for Silhouette and Davies-Bouldin
* **DBSCAN** was sensitive to density variations; parameters used: `eps=1.2`, `min_samples=7`
* **Agglomerative** produced moderate results but consumed the most memory

**Output CSVs** (with cluster labels) are ready for use in the forecasting stage.

---

## ✅ Future Contribution

* You may expand the analysis by increasing `sample_size` on higher-memory machines
* Forecasting team can reuse saved cluster outputs (e.g., `kmeans_30k.csv`) as inputs

---

## 👤 Author

* **Alvin Phan** — Cluster Modeling & Evaluation
