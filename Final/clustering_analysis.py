import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler

# Output directory (same as script location, or set explicitly)
output_dir = r'G:\Ai Projects\cluster_analysis'
os.makedirs(output_dir, exist_ok=True)


# Load engineered data with composite features
df = pd.read_csv("G:\Ai Projects\original_composite_features.csv")

# Features for Clustering & Forecasting
base_features = [
    'latitude', 'longitude', 'svr1', 'speed',
    'Bitrate', 'Bitrate-RX', 'Retransmissions', 'send_data', 'CWnd'
]
time_features = ['hour', 'day_of_week', 'is_weekend']
extra_features = [
    col for col in df.columns if any(kw in col for kw in ['lag', 'rolling', 'hex_id'])
    and df[col].dtype != 'O'
]
all_features = base_features + time_features + extra_features
features = [f for f in all_features if f in df.columns]
df_clust = df[features].fillna(0)

# Downsample for efficiency
df_clust_sample = df_clust.sample(n=2000, random_state=42)

# Scale features for clustering
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_clust_sample)

# K-means: Elbow Method, Silhouette & Davies-Bouldin
inertia, silhouette_scores, davies_scores = [], [], []
K = range(2, 10)
for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    inertia.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X_scaled, labels))
    davies_scores.append(davies_bouldin_score(X_scaled, labels))

plt.figure(figsize=(15, 4))
plt.subplot(1, 3, 1)
plt.plot(K, inertia, 'o-')
plt.title("KMeans Elbow")
plt.xlabel('k'); plt.ylabel('Inertia')

plt.subplot(1, 3, 2)
plt.plot(K, silhouette_scores, 'o-')
plt.title("Silhouette Score")
plt.xlabel('k'); plt.ylabel('Silhouette')

plt.subplot(1, 3, 3)
plt.plot(K, davies_scores, 'o-')
plt.title("Davies-Bouldin Score")
plt.xlabel('k'); plt.ylabel('Davies-Bouldin')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'kmeans_metrics.png'))
plt.close()

# Fit KMeans with best k
# best_k = K[np.argmax(silhouette_scores)]     <-- This choses best k value from elbow method above, uncomment if you want this method, less accuracy
best_k = 4   #<--- values overide
kmeans = KMeans(n_clusters=best_k, random_state=42)
labels_kmeans = kmeans.fit_predict(X_scaled)
df_clust_sample['kmeans_label'] = labels_kmeans

plt.figure(figsize=(7, 5))
sns.scatterplot(x='longitude', y='latitude', hue='kmeans_label', data=df_clust_sample, palette='tab10')
plt.title(f"KMeans Clustering (k={best_k})")
plt.savefig(os.path.join(output_dir, 'kmeans_clusters.png'))
plt.close()

# Agglomerative Clustering (same k as KMeans)-
agg = AgglomerativeClustering(n_clusters=best_k)
labels_agg = agg.fit_predict(X_scaled)
df_clust_sample['agg_label'] = labels_agg
score_agg_sil = silhouette_score(X_scaled, labels_agg)
score_agg_db = davies_bouldin_score(X_scaled, labels_agg)

plt.figure(figsize=(7, 5))
sns.scatterplot(x='longitude', y='latitude', hue='agg_label', data=df_clust_sample, palette='tab10')
plt.title(f"Agglomerative Clustering (k={best_k})")
plt.savefig(os.path.join(output_dir, 'agglomerative_clusters.png'))
plt.close()

# DBSCAN (parameters may need tuning)
db = DBSCAN(eps=2.0, min_samples=10) #tweak eps values here
labels_db = db.fit_predict(X_scaled)
df_clust_sample['dbscan_label'] = labels_db
if len(set(labels_db)) > 1:
    score_db_sil = silhouette_score(X_scaled, labels_db)
    score_db_db = davies_bouldin_score(X_scaled, labels_db)
else:
    score_db_sil = np.nan
    score_db_db = np.nan

plt.figure(figsize=(7, 5))
sns.scatterplot(x='longitude', y='latitude', hue='dbscan_label', data=df_clust_sample, palette='tab10')
plt.title("DBSCAN Clustering")
plt.savefig(os.path.join(output_dir, 'dbscan_clusters.png'))
plt.close()

# Save all scores to a CSV for reporting
score_table = pd.DataFrame({
    'Method': ['KMeans', 'Agglomerative', 'DBSCAN'],
    'Silhouette': [max(silhouette_scores), score_agg_sil, score_db_sil],
    'DaviesBouldin': [davies_scores[np.argmax(silhouette_scores)], score_agg_db, score_db_db]
})
score_table.to_csv(os.path.join(output_dir, 'clustering_scores.csv'), index=False)
print("\n---- Summary ----")
print(score_table)

# Grouped Bar Chart for Score Comparison
bar_width = 0.35
index = np.arange(len(score_table['Method']))
plt.figure(figsize=(8, 5))
plt.bar(index, score_table['Silhouette'], bar_width, label='Silhouette', color='dodgerblue')
plt.bar(index + bar_width, score_table['DaviesBouldin'], bar_width, label='Davies-Bouldin', color='orange')
plt.xlabel('Clustering Method')
plt.ylabel('Score (Higher Silhouette is better, Lower Davies-Bouldin is better)')
plt.title('Clustering Scores Comparison')
plt.xticks(index + bar_width / 2, score_table['Method'])
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'clustering_scores_comparison.png'))
plt.close()
