import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import lightgbm as lgb
import matplotlib.pyplot as plt

# Settings
data_path = r"G:\Ai Projects\original_composite_features.csv"
clustered_dir = r"G:\Ai Projects\lgbm"
os.makedirs(clustered_dir, exist_ok=True)
kmeans_clusters = 4
sample_size = 60000
clustered_csv = os.path.join(clustered_dir, f'kmeans_{sample_size//1000}k.csv')

# Load and sample data
df = pd.read_csv(data_path)
if len(df) > sample_size:
    df = df.sample(n=sample_size, random_state=42)

# Preprocess common: datetime and feature engineering
df['datetime'] = pd.to_datetime(df['datetime'])
df = df.sort_values('datetime')
df['svr1_lag1'] = df['svr1'].shift(1)
df['svr1_lag2'] = df['svr1'].shift(2)
df['svr1_rollmean_3'] = df['svr1'].rolling(3).mean()
df['svr1_rollmean_6'] = df['svr1'].rolling(6).mean()
df['svr1_rollstd_3'] = df['svr1'].rolling(3).std()
df['hour'] = df['datetime'].dt.hour
df.dropna(inplace=True)

# Common variables
target = 'svr1'
exclude_cols = [target, 'latitude', 'longitude', 'datetime', 'hex_id']

# Evaluation metrics
def accuracy_20pct(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred) <= 0.2 * np.abs(y_true))

def eval_scores(y_true, y_pred):
    r2 = r2_score(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / np.where(y_true == 0, 1, y_true))) * 100
    acc20 = accuracy_20pct(y_true, y_pred) * 100
    return {"R2": r2, "RMSE": rmse, "MAE": mae, "MAPE (%)": mape, "Accuracy20 (%)": acc20}

params = {
    'objective': 'regression',
    'metric': 'rmse',
    'boosting_type': 'gbdt',
    'device': 'gpu',
    'verbosity': -1,
    'random_state': 42
}

# ---- Iteration 1: WITHOUT cluster label ----
df1 = df.copy()
train1 = df1.iloc[:int(len(df1)*0.8)]
test1 = df1.iloc[int(len(df1)*0.8):]
features1 = [c for c in df1.columns if c not in exclude_cols and df1[c].dtype in [np.float64, np.int64, np.float32, np.int32] and c != 'cluster_label']
X1_train, y1_train = train1[features1], train1[target]
X1_test, y1_test = test1[features1], test1[target]

lgb_train1 = lgb.Dataset(X1_train, y1_train)
lgb_test1 = lgb.Dataset(X1_test, y1_test, reference=lgb_train1)
print("\n--- Training LightGBM WITHOUT cluster label ---")
gbm1 = lgb.train(params, lgb_train1, num_boost_round=200, valid_sets=[lgb_test1],
                 callbacks=[lgb.early_stopping(stopping_rounds=20), lgb.log_evaluation(period=20)])
y1_pred = gbm1.predict(X1_test)
scores1 = eval_scores(y1_test, y1_pred)
print("\nScores WITHOUT cluster:", scores1)

pd.DataFrame([scores1]).to_csv(os.path.join(clustered_dir, "scores_without_cluster.csv"))
plt.figure(figsize=(12, 5))
plt.plot(test1['datetime'], y1_test, label='Actual', color='blue')
plt.plot(test1['datetime'], y1_pred, label='Predicted', color='red', linestyle='--')
plt.title("Actual vs. Predicted svr1 (Without Cluster)")
plt.xlabel("Datetime")
plt.ylabel("svr1")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(clustered_dir, "forecast_actual_vs_predicted_without_cluster.png"))
plt.show()

error_pct1 = np.abs((y1_test - y1_pred) / np.where(y1_test == 0, 1, y1_test)) * 100
plt.figure(figsize=(7, 4))
plt.hist(error_pct1, bins=30)
plt.title("Forecast Percentage Error Distribution (No Cluster)")
plt.xlabel("Error %")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(os.path.join(clustered_dir, "error_distribution_no_cluster.png"))
plt.show()

test1 = test1.copy()
test1['error_pct1'] = error_pct1.values
hourly_error1 = test1.groupby('hour')['error_pct1'].mean()
plt.figure(figsize=(8, 5))
hourly_error1.plot(kind='bar')
plt.title("Forecast Error by Hour (No Cluster)")
plt.ylabel("Mean Absolute Percentage Error")
plt.tight_layout()
plt.savefig(os.path.join(clustered_dir, "hourly_error_no_cluster.png"))
plt.show()

# ---- KMeans clustering for Iteration 2 ----
df2 = df.copy()
kmeans_features = ['latitude', 'longitude', 'Bitrate', 'Retransmissions']
kmeans_data = df2[kmeans_features].fillna(0)
kmeans = KMeans(n_clusters=kmeans_clusters, random_state=42)
df2['cluster_label'] = kmeans.fit_predict(kmeans_data)
df2.to_csv(clustered_csv, index=False)
print(f"\nClustered data saved to: {clustered_csv}")

# ---- Iteration 2: WITH cluster label ----
train2 = df2.iloc[:int(len(df2)*0.8)]
test2 = df2.iloc[int(len(df2)*0.8):]
features2 = [c for c in df2.columns if c not in exclude_cols and df2[c].dtype in [np.float64, np.int64, np.float32, np.int32]]
X2_train, y2_train = train2[features2], train2[target]
X2_test, y2_test = test2[features2], test2[target]

lgb_train2 = lgb.Dataset(X2_train, y2_train)
lgb_test2 = lgb.Dataset(X2_test, y2_test, reference=lgb_train2)
print("\n--- Training LightGBM WITH cluster label ---")
gbm2 = lgb.train(params, lgb_train2, num_boost_round=200, valid_sets=[lgb_test2],
                 callbacks=[lgb.early_stopping(stopping_rounds=20), lgb.log_evaluation(period=20)])
y2_pred = gbm2.predict(X2_test)
scores2 = eval_scores(y2_test, y2_pred)
print("\nScores WITH cluster:", scores2)

pd.DataFrame([scores2]).to_csv(os.path.join(clustered_dir, "scores_with_cluster.csv"))
plt.figure(figsize=(12, 5))
plt.plot(test2['datetime'], y2_test, label='Actual', color='blue')
plt.plot(test2['datetime'], y2_pred, label='Predicted', color='red', linestyle='--')
plt.title("Actual vs. Predicted svr1 (With Cluster)")
plt.xlabel("Datetime")
plt.ylabel("svr1")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(clustered_dir, "forecast_actual_vs_predicted_with_cluster.png"))
plt.show()

error_pct2 = np.abs((y2_test - y2_pred) / np.where(y2_test == 0, 1, y2_test)) * 100
plt.figure(figsize=(7, 4))
plt.hist(error_pct2, bins=30)
plt.title("Forecast Percentage Error Distribution (With Cluster)")
plt.xlabel("Error %")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(os.path.join(clustered_dir, "error_distribution_with_cluster.png"))
plt.show()

test2 = test2.copy()
test2['error_pct2'] = error_pct2.values
hourly_error2 = test2.groupby('hour')['error_pct2'].mean()
plt.figure(figsize=(8, 5))
hourly_error2.plot(kind='bar')
plt.title("Forecast Error by Hour (With Cluster)")
plt.ylabel("Mean Absolute Percentage Error")
plt.tight_layout()
plt.savefig(os.path.join(clustered_dir, "hourly_error_with_cluster.png"))
plt.show()

# Compare both
scores_df = pd.DataFrame([scores1, scores2], index=['Without_Cluster', 'With_Cluster'])
scores_df.to_csv(os.path.join(clustered_dir, "lgbm_comparison_both_iterations.csv"))
print("\nModel Comparison Table:\n", scores_df)
