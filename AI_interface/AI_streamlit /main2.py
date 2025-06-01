import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import h3
import folium
from streamlit_folium import st_folium
from sklearn.decomposition import PCA
from PIL import Image
import pickle
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import joblib
import plotly.graph_objects as go
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
from datetime import timedelta

# Configure Streamlit page
st.set_page_config(
    page_title="5G Forecasting Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)
# Custom CSS for clean styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #000000;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #4a4a4a;
        margin-bottom: 2rem;
    }
    
    /* Impact Metrics */
    .impact-metric {
        background: #2a2a2a;
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .impact-number {
        font-size: 2.5rem;
        font-weight: 900;
        line-height: 1;
    }
    .impact-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Key Insight Badges */
    .insight-badge {
        display: inline-block;
        background: white;
        color: black;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    /* Critical Finding - Butter Yellow Highlight */
    .critical-finding {
        background: #fd6d05;
        color: #000000;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        margin: 1rem 0;
        border-left: 4px solid #d4c373;
    }
    
    /* Success Story */
    .success-story {
        background: white;
        border: 2px solid  #ff8b37;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    /* Process Steps */
    .process-step {
        background: #f5f5f5;
        border: px solid  #ff8b37;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        position: relative;
        color: #2a2a2a;
    }
    .process-step h4 {
        color: #000000 !important;
        margin-top: 0 !important;
    }
    .process-step::before {
        content: "✓";
        position: absolute;
        top: -10px;
        left: 15px;
        background:#ff8b37;
        color: white;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: bold;
    }
    
    /* Stats Grid */
    .stat-item {
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 8px;
        border: 2px solid  #ff8b37;
    }
    .stat-number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #000000;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #4a4a4a;
        margin-top: 0.3rem;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.6rem;
        font-weight: 700;
        color: #000000;
        margin: 2rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Butter yellow highlight box */
    .highlight-box {
        background: #f4e4a6;
        color: #000000;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #d4c373;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">5G Network Performance Analysis</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transforming 150K network records into actionable intelligence</p>', unsafe_allow_html=True)

# Impact Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="impact-metric">
        <div class="impact-number">99.2%</div>
        <div class="impact-label">SVR Correlation Found</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="impact-metric">
        <div class="impact-number">75%</div>
        <div class="impact-label">Complexity Reduction</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="impact-metric">
        <div class="impact-number">6</div>
        <div class="impact-label">ML-Ready Datasets</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="impact-metric">
        <div class="impact-number">1km²</div>
        <div class="impact-label">Spatial Resolution</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Critical Finding - Yellow Highlight
st.markdown("""
<div class="critical-finding">
<strong>Critical Discovery:</strong> SVR1-4 metrics showed 99.2% correlation, enabling 75% feature reduction without accuracy loss
</div>
""", unsafe_allow_html=True)

# Key Insights Badges
st.markdown('<h2 class="section-header">Key Achievements</h2>', unsafe_allow_html=True)

st.markdown("""
<span class="insight-badge">Invalid GPS Removed</span>
<span class="insight-badge">Geographic Bounds Applied</span>
<span class="insight-badge">H3 Hexagon Mapping</span>
<span class="insight-badge">Temporal Features Added</span>
<span class="insight-badge">Rolling Statistics</span>
<span class="insight-badge">Data Leakage Prevented</span>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Side-by-side: Correlation + Success Story
col1, col2 = st.columns([1, 1])

with col1:
    # Enhanced SVR Correlation - Colorful
    fig = go.Figure(data=go.Heatmap(
        z=[[1.0, 0.992, 0.994, 0.991],
           [0.992, 1.0, 0.998, 0.989],
           [0.994, 0.998, 1.0, 0.987],
           [0.991, 0.989, 0.987, 1.0]],
        x=['SVR1', 'SVR2', 'SVR3', 'SVR4'],
        y=['SVR1', 'SVR2', 'SVR3', 'SVR4'],
        colorscale='RdYlBu_r',
        text=[[1.0, 0.992, 0.994, 0.991],
              [0.992, 1.0, 0.998, 0.989],
              [0.994, 0.998, 1.0, 0.987],
              [0.991, 0.989, 0.987, 1.0]],
        texttemplate="%{text:.3f}",
        textfont={"size": 14, "color": "white"},
        showscale=True,
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title="<b>SVR Metrics: Extreme Correlation</b>",
        height=300,
        margin=dict(l=0, r=0, t=40, b=0),
        font=dict(size=12, color='#000000')
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("""
    <div class="success-story">
    <h3 style="color: #000000; margin-top: 0;"> Summary</h3>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
        <div class="stat-item">
            <div class="stat-number">150K</div>
            <div class="stat-label">Records Cleaned</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">85%</div>
            <div class="stat-label">Quality Improvement</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">4→1</div>
            <div class="stat-label">SVR Optimization</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">6</div>
            <div class="stat-label">Output Datasets</div>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

# Processing Pipeline - Compact
st.markdown('<h2 class="section-header">Optimized Pipeline</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="process-step">
    <h4 style="margin-top: 0;">Data Cleaning</h4>
    <p style="margin-bottom: 0;"><strong>Removed:</strong> Invalid GPS (999), geographic outliers<br>
    <strong>Result:</strong> 150K clean records</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="process-step">
    <h4 style="margin-top: 0;">Spatial Mapping</h4>
    <p style="margin-bottom: 0;"><strong>Applied:</strong> H3 hexagon zones (1km²)<br>
    <strong>Result:</strong> Standardized spatial features</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="process-step">
    <h4 style="margin-top: 0;">Feature Engineering</h4>
    <p style="margin-bottom: 0;"><strong>Added:</strong> Lag, rolling stats, temporal<br>
    <strong>Result:</strong> ML-ready datasets</p>
    </div>
    """, unsafe_allow_html=True)

# Feature Importance - Compact
st.markdown('<h2 class="section-header">Feature Impact</h2>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    # Streamlined feature importance - Grayscale with butter yellow highlight
    features = ['SVR1 Latency', 'Vehicle Speed', 'Location (Lat)', 'Location (Lon)', 'Time (Hour)', 'Bitrate']
    importance = [0.35, 0.18, 0.12, 0.11, 0.10, 0.08]
    colors = ['#ff8b37', '#f4e4a6', '#f4e4a6', '#f4e4a6', '#f4e4a6', '#f4e4a6']
    
    fig = go.Figure(go.Bar(
        y=features,
        x=importance,
        orientation='h',
        marker_color=colors,
        text=[f'{x:.0%}' for x in importance],
        textposition='inside',
        textfont=dict(color='black', size=12)
    ))
    
    fig.update_layout(
        title="<b>Top Features by Importance</b>",
        xaxis_title="Impact Score",
        height=300,
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=False,
        font=dict(color='#000000')
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("""
    <div class="highlight-box">
    <h4 style="color: #000000; margin-top: 0;">Ready for ML</h4>
    <ul style="margin-bottom: 0; color: #000000;">
        <li><strong>Clustering:</strong> Different algorithms</li>
        <li><strong>Forecasting:</strong> Time-series forecasting</li>
        <li><strong>Train the model:</strong> Multiple approaches</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)


# Custom CSS for better styling
st.markdown("""
<style>
.main {
    padding-top: 2rem;
}
.stSelectbox > div > div > select {
    background-color: #f0f2f6;
}
.metric-container {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #1f77b4;
}
.cluster-info {
    background-color: #e8f4fd;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

st.title("5G Network Dashboard with Time-Series Forecasting")
st.markdown("---")

# Sidebar for algorithm and cluster selection
with st.sidebar:
    st.markdown("### 5G Network Configuration")
    st.markdown("---")
    
    # Navigation - FIXED with unique key
    page_selection = st.radio(
        "Select Dashboard View:",
        ["Network Clustering", "Time-Series Forecasting"],
        help="Choose between network visualization and forecasting analysis",
        key="main_page_selection"  # UNIQUE KEY ADDED
    )
    
    if page_selection == "Network Clustering":
        algorithm = st.selectbox(
            "Select Clustering Algorithm", 
            ["K-means", "DBscan", "Agglomerative"],
            help="Choose the clustering algorithm to analyze",
            key="clustering_algorithm_select"  # UNIQUE KEY ADDED
        )
        

    
    else:  # Time-Series Forecasting
        st.markdown("### Forecasting Configuration")
        selected_cluster = st.selectbox(
            "Cluster ID:", 
            [f'cluster_{i}' for i in range(1, 5)],
            key="forecasting_cluster_select"  # UNIQUE KEY ADDED
        )
        selected_metric = st.selectbox(
            "Metric:", 
            ['latency', 'throughput'],
            key="forecasting_metric_select"  # UNIQUE KEY ADDED
        )
        
        # Time period selection
        time_period = st.selectbox(
            "Time Period:",
            ['All Hours', 'Peak Hours Only', 'Off-Peak Hours Only', 'Custom Range'],
            key="time_period_select"  # UNIQUE KEY ADDED
        )
        
        # Custom time range (only show if Custom Range is selected)
        if time_period == 'Custom Range':
            start_hour = st.slider("Start Hour:", 0, 23, 9, key="start_hour_slider")
            end_hour = st.slider("End Hour:", 0, 23, 17, key="end_hour_slider")
            if start_hour >= end_hour:
                st.warning("End hour must be after start hour!")
        
        forecast_window = st.slider("Forecast Hours:", 1, 48, 24, key="forecast_window_slider")
    
    st.markdown("---")
    st.markdown("### Dashboard Info")
    st.info("This dashboard analyzes 5G network performance using clustering algorithms and provides time-series forecasting capabilities.")

# Time-series forecasting functions
@st.cache_data
def generate_data(cluster_id, metric_type, days=14):
    """Generate sample time series data"""
    np.random.seed(hash(cluster_id) % 1000)
    
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    timestamps = pd.date_range(start=start_time, end=end_time, freq='H')
    
    base_value = 120 if metric_type == 'latency' else 800
    data = []
    
    for i, ts in enumerate(timestamps):
        hour = ts.hour
        is_rush = (ts.weekday() < 5) and ((7 <= hour <= 9) or (17 <= hour <= 19))
        
        # Seasonal pattern + rush hour effect + noise
        seasonal = 30 * np.sin(2 * np.pi * hour / 24)
        rush_factor = 1.6 if (is_rush and metric_type == 'latency') else (0.7 if is_rush else 1.0)
        noise = np.random.normal(0, base_value * 0.1)
        
        value = max(0, (base_value + seasonal + noise) * rush_factor)
        
        data.append({
            'datetime': ts,
            'value': value,
            'is_rush_hour': is_rush,
            'hour': hour
        })
    
    return pd.DataFrame(data)

def filter_data_by_time_period(data, time_period, start_hour=None, end_hour=None):
    """Filter data based on selected time period"""
    if time_period == 'Peak Hours Only':
        return data[data['is_rush_hour']]
    elif time_period == 'Off-Peak Hours Only':
        return data[~data['is_rush_hour']]
    elif time_period == 'Custom Range' and start_hour is not None and end_hour is not None:
        if start_hour < end_hour:
            return data[(data['hour'] >= start_hour) & (data['hour'] <= end_hour)]
        else:
            return data  # Return all if invalid range
    else:  # All Hours
        return data

def generate_forecast(historical_data, hours=24):
    """Generate simple forecast"""
    last_timestamp = historical_data['datetime'].iloc[-1]
    forecasts = []
    
    for i in range(1, hours + 1):
        future_time = last_timestamp + timedelta(hours=i)
        hour = future_time.hour
        is_rush = (future_time.weekday() < 5) and ((7 <= hour <= 9) or (17 <= hour <= 19))
        
        # Simple forecast based on hourly patterns
        hourly_avg = historical_data[historical_data['datetime'].dt.hour == hour]['value'].mean()
        base_forecast = hourly_avg if not pd.isna(hourly_avg) else historical_data['value'].mean()
        
        rush_factor = 1.3 if is_rush else 0.9
        noise = np.random.normal(1, 0.05)
        
        forecast_value = max(0, base_forecast * rush_factor * noise)
        
        forecasts.append({
            'datetime': future_time,
            'predicted_value': forecast_value,
            'is_rush_hour': is_rush
        })
    
    return pd.DataFrame(forecasts)

# Network clustering functions (from your original code)
file_map = {
    "K-means": "kmeans_30k.csv",
    "DBscan": "dbscan_30k.csv",
    "Agglomerative": "agglo_30k.csv"
}

@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        st.sidebar.success(f"✅ Loaded {len(df)} records from {file_path}")
    except FileNotFoundError:
        st.error(f"❌ File not found: {file_path}")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()

    # If agglo, rename columns to standard format and inject synthetic coords
    if "latency_avg" in df.columns and "throughput" in df.columns:
        df = df.rename(columns={
            "latency_avg": "svr_avg",
            "throughput": "Bitrate"
        })
        # Create more realistic synthetic coordinates for Melbourne area
        np.random.seed(42)
        df["latitude"] = -37.8136 + np.random.normal(0, 0.05, len(df))
        df["longitude"] = 144.9631 + np.random.normal(0, 0.05, len(df))
        df["truck"] = np.random.randint(1, 5, len(df))
        df["square_id"] = [f"zone_{i//100}" for i in range(len(df))]

    required_cols = ["latitude", "longitude"]
    if not all(col in df.columns for col in required_cols):
        st.error(f"❌ Missing required columns in {file_path}. Columns found: {df.columns.tolist()}")
        st.stop()

    # Filter out invalid coordinates with better validation
    initial_count = len(df)
    df = df[
        (df["latitude"] != 99.999) & 
        (df["longitude"] != 99.999) &
        (df["latitude"].notna()) & 
        (df["longitude"].notna()) &
        (df["latitude"] >= -90) & 
        (df["latitude"] <= 90) &
        (df["longitude"] >= -180) & 
        (df["longitude"] <= 180)
    ]
    
    if len(df) < initial_count:
        st.sidebar.warning(f"⚠️ Filtered out {initial_count - len(df)} invalid coordinates")

    if "svr_avg" not in df.columns:
        if all(col in df.columns for col in ["svr1", "svr2", "svr3", "svr4"]):
            df["svr_avg"] = df[["svr1", "svr2", "svr3", "svr4"]].mean(axis=1)
        else:
            # Create synthetic latency data if columns don't exist
            df["svr_avg"] = np.random.normal(50, 15, len(df))

    # Generate hex_id for valid coordinates with error handling
    def safe_h3_conversion(lat, lon):
        try:
            return h3.geo_to_h3(lat, lon, 8)
        except:
            return None

    df["hex_id"] = df.apply(lambda row: safe_h3_conversion(row["latitude"], row["longitude"]), axis=1)
    df = df[df["hex_id"].notna()]  # Remove rows where H3 conversion failed
    df["hex_id"] = df["hex_id"].astype(str)

    # Find cluster column more robustly
    cluster_col = None
    possible_cluster_cols = [
        'label', 'labels', 'cluster', 'clusters', 'cluster_id', 'cluster_label',
        'dbscan_label', 'kmeans_label', 'agglo_label'
    ]
    
    for col in df.columns:
        if any(keyword in col.lower() for keyword in possible_cluster_cols):
            cluster_col = col
            break
    
    if cluster_col:
        df["cluster_id"] = df[cluster_col]
        # Handle DBSCAN outliers (-1) and ensure proper data types
        df["cluster_id"] = pd.to_numeric(df["cluster_id"], errors='coerce').fillna(-1).astype(int)
    else:
        # Fallback: create clusters based on svr_avg quartiles
        df["cluster_id"] = pd.qcut(df["svr_avg"], q=4, labels=[0, 1, 2, 3], duplicates='drop').astype(int)

    # Add Bitrate if missing
    if "Bitrate" not in df.columns:
        # Create inverse relationship with latency
        df["Bitrate"] = 100 - (df["svr_avg"] - 30) * 0.8 + np.random.normal(0, 5, len(df))
        df["Bitrate"] = np.maximum(df["Bitrate"], 10)  # Ensure positive values

    # Remove duplicates more carefully
    df = df.drop_duplicates(subset=["hex_id"])
    
    return df

# Page routing based on selection
if page_selection == "Network Clustering":
    # Load data with progress indicator
    with st.spinner(f"Loading {algorithm} clustering data..."):
        df = load_data(file_map[algorithm])

   

    # Aggregate data by hex_id
    agg = df.groupby("hex_id").agg({
        "latitude": "mean",
        "longitude": "mean",
        "svr_avg": "mean",
        "Bitrate": "mean",
        "truck": pd.Series.nunique if "truck" in df.columns else lambda x: 1,
        "square_id": "first" if "square_id" in df.columns else lambda x: "unknown",
        "cluster_id": "first"
    }).reset_index()

    # Show preview of processed data
    with st.expander("View Data Preview", expanded=False):
        st.dataframe(agg.head(10), use_container_width=True)

    # Define consistent cluster colors
    cluster_colors = {
        0: "#1f77b4",  # blue - Excellent
        1: "#2ca02c",  # green - Good  
        2: "#ff7f0e",  # orange - Fair
        3: "#d62728",  # red - Poor
        -1: "#7f7f7f"  # gray - Outliers (DBSCAN)
    }

    cluster_names = {
        0: "Excellent Performance",
        1: "Good Performance", 
        2: "Fair Performance",
        3: "Poor Performance",
        -1: "Outliers (DBSCAN)"
    }

    # Get unique clusters in the current data
    unique_clusters = sorted(agg['cluster_id'].unique()) if len(agg) > 0 else []

    # Calculate map center with better bounds checking
    if len(agg) > 0:
        center_lat = agg['latitude'].median()  # Use median for better center
        center_lon = agg['longitude'].median()
        
        # Calculate appropriate zoom level based on data spread
        lat_span = agg['latitude'].max() - agg['latitude'].min()
        lon_span = agg['longitude'].max() - agg['longitude'].min()
        max_span = max(lat_span, lon_span)
        
        if max_span > 1:
            zoom_level = 8
        elif max_span > 0.1:
            zoom_level = 10
        elif max_span > 0.01:
            zoom_level = 12
        else:
            zoom_level = 14
    else:
        # Default to Melbourne coordinates
        center_lat, center_lon = -37.8136, 144.9631
        zoom_level = 10

    # Improved hexagon drawing function
    def draw_hexagons_improved(agg_data, fmap):
        """Draw hexagons on the map with improved error handling and styling"""
        successful_hexagons = 0
        failed_hexagons = 0
        
        for _, row in agg_data.iterrows():
            try:
                hex_id = str(row["hex_id"])
                
                # More robust hex_id validation
                if not hex_id or len(hex_id) < 15 or hex_id == 'nan':
                    failed_hexagons += 1
                    continue
                
                # Get hexagon boundary with error handling
                try:
                    hex_boundary_coords = h3.h3_to_geo_boundary(hex_id, geo_json=True)
                    hex_boundary = [[lat, lon] for lon, lat in hex_boundary_coords]
                except Exception as e:
                    failed_hexagons += 1
                    continue
                    
                if len(hex_boundary) < 3:  # Need at least 3 points for a polygon
                    failed_hexagons += 1
                    continue
                    
                hex_boundary.append(hex_boundary[0])  # Close polygon
                cluster = int(row["cluster_id"])
                color = cluster_colors.get(cluster, "#808080")
                
                # Create more informative popup
                popup_content = f"""
                <div style='font-family: Arial; font-size: 14px; line-height: 1.6; max-width: 250px;'>
                    <h4 style='margin: 0 0 10px 0; color: {color}; border-bottom: 2px solid {color}; padding-bottom: 5px;'>
                         Network Cell Details
                    </h4>
                    <p><strong> Cluster:</strong> {cluster} ({cluster_names.get(cluster, 'Unknown')})</p>
                    <p><strong> Latency:</strong> {row['svr_avg']:.1f} ms</p>
                    <p><strong> Throughput:</strong> {row['Bitrate']:.1f} Mbps</p>
                    <p><strong> Connections:</strong> {row['truck']}</p>
                    <p><strong> Zone:</strong> {row['square_id']}</p>
                    <p><strong> Hex ID:</strong> <code>{hex_id[:12]}...</code></p>
                    <hr style='margin: 10px 0;'>
                </div>
                """
                
                # Determine fill opacity based on performance
                fill_opacity = 0.7
                if cluster == 0:  # Excellent
                    fill_opacity = 0.8
                elif cluster == 3 or cluster == -1:  # Poor or Outlier
                    fill_opacity = 0.6
                
                folium.Polygon(
                    locations=hex_boundary,
                    color="#2c3e50",  # Darker border
                    weight=1.5,
                    opacity=0.8,
                    fill=True,
                    fill_color=color,
                    fill_opacity=fill_opacity,
                    popup=folium.Popup(popup_content, max_width=300),
                    tooltip=f"Cluster {cluster}: {row['svr_avg']:.1f}ms, {row['Bitrate']:.1f}Mbps"
                ).add_to(fmap)
                
                successful_hexagons += 1
                
            except Exception as e:
                failed_hexagons += 1
        
        return successful_hexagons, failed_hexagons

    # Create improved legend
    def create_improved_legend(unique_clusters, cluster_colors, algorithm):
        """Create an enhanced legend with better styling"""
        legend_items = []
        
        for cluster_id in unique_clusters:
            color = cluster_colors.get(cluster_id, "#808080")
            name = cluster_names.get(cluster_id, f"Cluster {cluster_id}")
            count = len(agg[agg['cluster_id'] == cluster_id])
            
            legend_items.append(f'''
                <div style="display: flex; align-items: center; margin-bottom: 8px; padding: 4px 8px; border-radius: 4px; background: rgba(255,255,255,0.1);">
                    <div style="width: 16px; height: 16px; background-color: {color}; border-radius: 3px; margin-right: 10px; border: 1px solid rgba(0,0,0,0.2);"></div>
                    <span style="font-weight: 500;">{name}</span>
                    <span style="margin-left: auto; color: #666; font-size: 12px;">({count})</span>
                </div>
            ''')
        
        legend_html = f"""
        <div style="position: fixed; 
             bottom: 20px; left: 20px; 
             width: 280px; height: auto; 
             background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
             z-index: 9999; 
             font-size: 13px;
             border: none;
             padding: 20px; 
             border-radius: 12px;
             box-shadow: 0 8px 25px rgba(0,0,0,0.15);
             backdrop-filter: blur(10px);">
             
            <div style="display: flex; align-items: center; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #e9ecef;">
                <span style="font-size: 18px; margin-right: 8px;"></span>
                <span style="font-size: 16px; font-weight: bold; color: #2c3e50;">Cluster Legend</span>
            </div>
            
            {''.join(legend_items)}
            
            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #dee2e6;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <small style="color: #6c757d;"><strong>Algorithm:</strong> {algorithm}</small>
                    <small style="color: #6c757d;"><strong>Total:</strong> {len(agg)} cells</small>
                </div>
            </div>
        </div>
        """
        return legend_html



    # Algorithm comparison section
    st.markdown("---")
    st.markdown("## Algorithm Performance Comparison")

    col1, col2 = st.columns(2)

    with col1:
        # Show image based on selected algorithm
        image_paths = {
            "K-means": "images/k_means.png",
            "DBscan": "images/dbscan.png", 
            "Agglomerative": "images/agglo.png"
        }

        if algorithm in image_paths:
            try:
                image = Image.open(image_paths[algorithm])
                st.image(image, use_container_width=True, caption=f"{algorithm} Clustering Results")
            except FileNotFoundError:
                st.warning(f"⚠️ Image file not found: {image_paths[algorithm]}")
                st.info("Please ensure the images directory exists with the clustering result images.")

    with col2:
        algorithm_descriptions = {
            "K-means": """
            ###  K-means Clustering
            
            **Characteristics:**
            - Partitions data into k spherical clusters
            - Fast and efficient for large datasets  
            - Works well with evenly distributed data
            -   Requires pre-defining number of clusters
            -   Sensitive to outliers
            
            **Best for:** General network optimization and resource allocation
            """,
            "DBscan": """
            ###  DBSCAN Clustering
            
            **Characteristics:**
            -  Finds clusters of arbitrary shape
            -  Automatically determines cluster count
            -  Excellent outlier detection
            -  Sensitive to density variations
            -  Requires parameter tuning
            
            **Best for:** Anomaly detection and irregular network patterns
            """,
            "Agglomerative": """
            ###  Agglomerative Clustering
            
            **Characteristics:**
            -  Hierarchical cluster structure
            -  Works with any distance metric
            -  Provides cluster dendrogram
            -  Computationally expensive
            -  Memory intensive for large datasets
           
            **Best for:** Understanding hierarchical network relationships
            """
        }
        
        st.markdown(algorithm_descriptions.get(algorithm, "No description available."))

    # Performance metrics visualization
    st.markdown("### Clustering Evaluation Metrics")
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Silhouette Score (Higher is Better)**")
        fig, ax = plt.subplots()
        sns.barplot(x=["KMeans", "DBSCAN", "Agglomerative"], y=[0.58, 0.33, 0.42], ax=ax)
        ax.set_ylim(0, 1)
        st.pyplot(fig)

    with col4:
        st.markdown("**Davies-Bouldin Index (Lower is Better)**")
        fig, ax = plt.subplots()
        sns.barplot(x=["KMeans", "DBSCAN", "Agglomerative"], y=[0.62, 1.35, 0.97], ax=ax)
        ax.set_ylim(0, 2)
        st.pyplot(fig)

else:  # Time-Series Forecasting Page
    st.title(" Time-Series Forecasting Dashboard")

    # Load data and model
    try:
        data = pd.read_csv("time_series_forecasting_data_2.csv")
       
        data['datetime'] = pd.to_datetime(data['datetime'])
        data = data.dropna()
    except FileNotFoundError:
        st.error("❌ Time series data file not found. Please ensure 'time_series_forecasting_data_2.csv' exists.")
        st.stop()

    # Load pretrained model
    try:
        model = joblib.load("random_forest_model_20250531_020257.joblib")
    except FileNotFoundError:
        st.error("❌ Model file not found. Please ensure 'random_forest_model_20250531_020257.joblib' exists.")
        st.stop()

    # Cluster IDs (placeholder)
    cluster_ids = ['cluster_1']

    # Metric-to-column mapping
    target_map = {
        "latency": "latency_avg",
        "throughput": "Bitrate"
    }
    target_col = target_map[selected_metric]

    # Check if target column exists
    if target_col not in data.columns:
        st.error(f"❌ Column '{target_col}' not found in data. Available columns: {list(data.columns)}")
        st.stop()

    # Time filtering
    data['hour'] = data['datetime'].dt.hour
    if time_period == "Peak Hours Only":
        data = data[data['hour'].between(8, 19)]
    elif time_period == "Off-Peak Hours Only":
        data = data[(data['hour'] < 8) | (data['hour'] > 19)]

    # Define features and target
    X = data.drop(columns=["datetime", target_col])
    y = data[[target_col]]

    # Fit scalers on current data
    scaler_X = StandardScaler()
    scaler_y = StandardScaler()
    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y)

    # Predict using pretrained model
    preds_scaled = model.predict(X_scaled).reshape(-1, 1)
    preds = scaler_y.inverse_transform(preds_scaled)

    data['Predicted'] = preds

    # Future prediction placeholder
    last_time = data['datetime'].iloc[-1]
    future_times = [last_time + timedelta(hours=i) for i in range(1, forecast_window + 1)]
    future_preds = preds[-forecast_window:]

    # Forecast visualization
    title_map = {
        "latency": "Latency (ms)",
        "throughput": "Throughput (Mbps)"
    }

    st.title(f"{selected_metric.capitalize()} Forecast - {selected_cluster} ({time_period})")
    st.caption(f"Showing {len(data)} data points from {data['datetime'].min()} to {data['datetime'].max()}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['datetime'], y=data[target_col], mode='lines', name='Historical', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=data['datetime'], y=data['Predicted'], mode='lines', name='Forecast', line=dict(dash='dash', color='orange')))
    fig.add_trace(go.Scatter(x=future_times, y=future_preds.flatten(), mode='lines+markers', name='Future Forecast', line=dict(dash='dot', color='gold')))
    fig.update_layout(height=400, xaxis_title='Time', yaxis_title=title_map[selected_metric])
    st.plotly_chart(fig, use_container_width=True)

    # Insights and summary
    st.subheader(" Insights")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Time Period Analysis ({time_period}) - {selected_metric.capitalize()}**:")
        rush_hour_values = data[data['hour'].between(8, 19)][target_col].mean()
        all_hour_values = data[target_col].mean()
        rush_hour_factor = round(rush_hour_values / all_hour_values, 2)
        st.write(f"- Rush hour {selected_metric} is {rush_hour_factor}x higher than average")
        if rush_hour_factor > 1.1:
            st.write("- Impact: High load periods require scaling")
        else:
            st.write("- Impact: Load variation is minimal")
    with col2:
        st.markdown("**Forecast Summary:**")
        st.write(f"- Next {forecast_window}h: {sum(data['hour'].iloc[-forecast_window:].between(8, 19))} rush hour(s)")
        st.write(f"- Based on: {selected_metric} patterns")
        st.write("- Recommendation: Monitor resource allocation")

    # Forecast table
    st.subheader("Next 12 Hours Forecast")
    forecast_table = pd.DataFrame({
        "Time": future_times,
        "Predicted": future_preds.flatten(),
        "Period": ["Rush Hour" if t.hour in range(8, 20) else "Normal" for t in future_times]
    })
    st.dataframe(forecast_table.head(12), use_container_width=True)

    # Model performance metrics
    st.subheader(" Model Performance Metrics")
    mse = mean_squared_error(y, preds)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y, preds)
    r2 = r2_score(y, preds)
    mape = np.mean(np.abs((y.values - preds) / (y.values + 1e-10))) * 100
    accuracy = 100 - mape

    metric_names = ["Accuracy (%)", "R² Score", "MAE", "RMSE"]
    metric_values = [accuracy, r2 * 100, mae, rmse]
    bar_colors = ["blue", "orange", "green", "red"]

    bar_fig = go.Figure(data=[
        go.Bar(name=metric_names[i], x=[metric_names[i]], y=[metric_values[i]], marker_color=bar_colors[i])
        for i in range(4)
    ])
    bar_fig.update_layout(yaxis_title='Value', height=300)
    st.plotly_chart(bar_fig, use_container_width=True)

    st.markdown(f"""
    **Accuracy:** {accuracy:.1f}%  
    **R² Score:** {r2:.3f}  
    **MAE:** {mae:.2f}  
    **RMSE:** {rmse:.2f}
    """)
