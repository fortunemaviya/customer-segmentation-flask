import pandas as pd
import joblib
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def preprocess_data(df):
    # Handle different column name cases
    income_col = next(col for col in df.columns if 'income' in col.lower())
    score_col = next(col for col in df.columns if 'score' in col.lower())
    
    X = df[[income_col, score_col]]
    scaler = StandardScaler()
    return scaler.fit_transform(X), income_col, score_col

def train_kmeans(X_scaled, n_clusters=5):
    kmeans = KMeans(
        n_clusters=n_clusters,
        init='k-means++',
        random_state=42,
        n_init=10  # Explicitly set to avoid warning
    )
    kmeans.fit(X_scaled)
    return kmeans

def save_model(model, path='kmeans_model.pkl'):
    joblib.dump(model, path)

def load_model(path='kmeans_model.pkl'):
    return joblib.load(path)