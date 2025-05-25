# ## Prep
# ### Import
import glob
import pandas as pd
import numpy as np
import h3
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import KNNImputer
from sklearn.preprocessing import RobustScaler, MinMaxScaler, FunctionTransformer
from sklearn.feature_selection import mutual_info_regression


# ### Data Cleaning
# - removes rows with invalid GPS coord (999)
# - filter preset bounds that approximate the Brimbank area, this ensures that the truck's speed is nonnegative
# - svr columns are converted into numeric values
# - EDA showed high correlation of svr series, thus svr1 only was kept
# - reduces noise and filtering to more realistic geographic area eliminates extreme noise that distort clustering, especially when mapping zones for performance
# - LightGBM, SGBoost, and RandomForest require clean input without dummy or outlier values
# - Missing or inconsistent latency leads time-series models to poor learning
# - Keeping only svr1 reduces model complexity and risk of overfitting, while keeping essential latency information needed
def clean_data(df):
    df = df.copy()
    # remove invalid GPS (999 values)
    df = df[(df['latitude'] != 999) & (df['longitude'] != 999)]
    # filter valid geographical range (example values for Brimbank)
    df = df[
        df['latitude'].between(-38, -10) &
        df['longitude'].between(110, 155) &
        (df['speed'] >= 0)
    ]
    # convert svr1-4 to numeric and replace dummy 1000 with NaN
    svr_cols = ['svr1', 'svr2', 'svr3', 'svr4']
    df[svr_cols] = df[svr_cols].apply(pd.to_numeric, errors='coerce').replace(1000, np.nan)
    # drop redundant svr columns: keep only svr1 (this is justified by their high correlation)
    df = df.drop(columns=['svr2', 'svr3', 'svr4'])
    return df


# ### Geospatial Features using H3
# - computes H3 hexagon ID for each data point at resolution 9 (which approx. 1km^2 area)
# - they are then stored in new column, standardising spatial bins
# - unlike arbitrary square bins, hexagons offer uniformity and reduced edge effects
# - KMeans and DBSCAN need standardised spatial groupings to improve identification of zones
# - hexagon zones act as spatial "buckets" that allow aggregated network performance metrics per area calculation
# - LightGBM, SGBoost can utilise hex_id to explain regional performance differences
def add_hex_zones(df, resolution=9):
    df = df.copy()
    # compute H3 hexagon ID for each row, resolution 9 ~1km² per hexagon
    df['hex_id'] = df.apply(
        lambda row: h3.geo_to_h3(row['latitude'], row['longitude'], resolution),
        axis=1
    )
    return df


# ### Temporal Features
# - raw Unix timestamp converted to proper datetime object with timezone conversion to Australia/Melbourne
# - adds time-series-essential columns to the data frame
# - allow forecasting models to learn periodic trends
# - extraction of discrete and meaningful features avoid ordinal traps (weekend)
# - time-based features are essential in ensemble models to capture time-dependent variations
def add_time_features(df):
    df = df.copy()
    # create proper datetime from the Unix timestamp in 'time'
    df['datetime'] = pd.to_datetime(df['time'], unit='s', utc=True).dt.tz_convert('Australia/Melbourne')
    # extract additional features
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5,6]).astype(int)
    return df


# ### Composite Feature Engineering (Lag and Rolling Stats)
# - calculates lag features like previous time step's latency and three time steps prior
# - rolling (time-aware) stats like mean and std od svr1 over a window (6 samples roughly representing an hour if data is sampled every 10 mins)
# - rolling drops missing values indirectly
# - temporal dependancies are captured to indicate how network performance evolves with time
# - summarise current performance and provide historical context, good for forecasting accuracy and enrich tree-based regressors
# - richer feature set and allow distinguishing between zones with stable versus volatile performance
def engineer_features(df):
    df = df.copy()
    df['lag1_svr1'] = df['svr1'].shift(1)
    df['lag3_svr1'] = df['svr1'].shift(3)
    # rolling statistics with a window of 6 samples (~1 hour, if data is roughly 10-min intervals)
    df['rolling_mean_svr1'] = df['svr1'].rolling(6, min_periods=1).mean()
    df['rolling_std_svr1'] = df['svr1'].rolling(6, min_periods=1).std()
    return df.dropna()


# ### Normalisation Preprocessor
# - applies two separate scalers to groups of features
#   - robust: numerical that may contain outliers
#   - minmax: geographic features to map into [0, 1] range
# - others not changed
# - models sensitive to feature scales are solved by normalisation (no single variable unduly influence)
# - mitigate impact of outliers
# - essential to clustering, since they yield more consistent and comparable distance metrics across features
def get_preprocessor(cols_numeric, cols_geo):
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', RobustScaler(), cols_numeric),
            ('geo', MinMaxScaler(), cols_geo)
        ],
        remainder='passthrough'
    )
    return preprocessor


# ## Execution
# ### Load Raw Data
raw_files = glob.glob("G:\Ai Projects\data\*-combined-kml.csv")
df_raw = pd.concat([pd.read_csv(f) for f in raw_files], ignore_index=True)
# Encode all object-type (categorical) columns to avoid 'could not convert string to float' errors
from sklearn.preprocessing import LabelEncoder

obj_cols = df_raw.select_dtypes(include=['object']).columns
df_raw[obj_cols] = df_raw[obj_cols].fillna("missing")

for col in obj_cols:
    le = LabelEncoder()
    df_raw[col] = le.fit_transform(df_raw[col].astype(str))


# ### Original All Features (Cleaned)
# - cleaned dataset with all core features
# - broadest set of information
# - base from which composite or specialised datasets are derived
df_cleaned_all = clean_data(df_raw)
df_cleaned_all = add_time_features(df_cleaned_all)
df_cleaned_all = add_hex_zones(df_cleaned_all)
df_cleaned_all.to_csv("original_all_features.csv", index=False)


# ### Original w/ Composite Features
# - dataset after composite engineering
# - augmented features with information specifications provide more context (trends for forecasting, predictors for tree-based models)
df_composite = engineer_features(df_cleaned_all.copy())
df_composite.to_csv("original_composite_features.csv", index=False)


# ### Original w/ Normalisation
# - dataset with normalisation on selected numeric and geographic feature
# - provide feature scale insensitivity
num_cols = ['svr1', 'Bitrate', 'Retransmissions']
geo_cols = ['latitude', 'longitude']
preprocessor = get_preprocessor(num_cols, geo_cols)
df_norm = df_cleaned_all.copy()
norm_array = preprocessor.fit_transform(df_norm[num_cols + geo_cols])
df_norm_scaled = pd.DataFrame(norm_array, columns=[f'{col}_norm' for col in num_cols+geo_cols])
df_norm_final = pd.concat([df_norm.reset_index(drop=True), df_norm_scaled], axis=1)
df_norm_final.to_csv("original_normalisation.csv", index=False)


# ### Strict Temporal Split (avoid leakage)
# - split dataset via temporal cutoff (80th percentile of datetime)
# - create forecasting training and testing sets, normalisation applied separately
# - prevents future information leakage, best practice for time-series forecasting
cutoff_date = df_cleaned_all['datetime'].quantile(0.8)
print("Cutoff Date for forecasting split:", cutoff_date)
forecast_train = df_cleaned_all[df_cleaned_all['datetime'] < cutoff_date].copy()
forecast_test  = df_cleaned_all[df_cleaned_all['datetime'] >= cutoff_date].copy()

# ### Original w/ Composite Features & Normalisation
# - combination of all OR restricted to key var
# - beneficial for models needing both additional context and scaling insensitivity
df_comp_norm = df_composite.copy()
norm_array2 = preprocessor.fit_transform(df_comp_norm[num_cols + geo_cols])
df_comp_norm_scaled = pd.DataFrame(norm_array2, columns=[f'{col}_norm' for col in num_cols+geo_cols])
df_comp_norm_final = pd.concat([df_comp_norm.reset_index(drop=True), df_comp_norm_scaled], axis=1)

# Original
df_comp_norm_final.to_csv("original_composite_normalisation.csv", index=False)
# Restricted to Composite Columns
comp_cols = ['hex_id', 'datetime', 'svr1', 'speed'] + [col for col in df_comp_norm_final.columns if 'rolling' in col]
df_comp_norm_final = df_comp_norm_final[comp_cols + list(df_comp_norm_scaled.columns)]
df_comp_norm_final.to_csv("original_composite_normalisation.csv", index=False)


# ### Original Important Features
# - filtered dataset (top 10 features via MI and SHAP)
# - additional essential identifiers
# - this dataset serves as an attempt to reduce overfitting, speeds up model training
features_for_mi = df_cleaned_all[['svr1', 'Bitrate', 'Retransmissions', 'speed', 'latitude', 'longitude', 'hour', 'day_of_week', 'is_weekend']]
target = df_cleaned_all['svr1']
mi = mutual_info_regression(features_for_mi.fillna(0), target.fillna(0))
mi_series = pd.Series(mi, index=features_for_mi.columns).sort_values(ascending=False)
print("Mutual Information values:\n", mi_series)
important_features = mi_series[mi_series > 0.01].index.tolist()
df_important = df_cleaned_all[important_features + ['hex_id', 'datetime']]
df_important.to_csv("original_important_features.csv", index=False)
