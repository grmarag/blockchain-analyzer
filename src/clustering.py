import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import hdbscan

class ClusteringAnalyzer:
    def __init__(self, transactions: pd.DataFrame):
        self.transactions = transactions
        self.address_features = None
        self.clusters = None

    def compute_address_features(self):
        """Compute features per address from transactions."""
        senders = self.transactions.groupby("sender").agg(
            sent_count=("amount", "count"),
            sent_total=("amount", "sum")
        ).reset_index().rename(columns={"sender": "address"})
        
        recipients = self.transactions.groupby("recipient").agg(
            received_count=("amount", "count"),
            received_total=("amount", "sum")
        ).reset_index().rename(columns={"recipient": "address"})

        features = senders.merge(recipients, on="address", how="outer").fillna(0)
        self.address_features = features
        return features

    def cluster_addresses(self, method="hdbscan", **kwargs):
        """Cluster addresses based on computed features.
        
        Args:
            method: 'hdbscan' or 'kmeans'
        """
        if self.address_features is None:
            self.compute_address_features()
        
        X = self.address_features.drop("address", axis=1).values
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        if method == "hdbscan":
            clusterer = hdbscan.HDBSCAN(**kwargs)
            labels = clusterer.fit_predict(X_scaled)
        elif method == "kmeans":
            n_clusters = kwargs.get("n_clusters", 5)
            clusterer = KMeans(n_clusters=n_clusters, random_state=42)
            labels = clusterer.fit_predict(X_scaled)
        else:
            raise ValueError("Unsupported clustering method")
        
        self.address_features["cluster"] = labels
        self.clusters = self.address_features
        return self.clusters