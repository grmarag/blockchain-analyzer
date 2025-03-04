import pandas as pd
from src.clustering import ClusteringAnalyzer

def test_compute_address_features():
    data = pd.DataFrame([
        {"sender": "A", "recipient": "B", "amount": 100, "token": "token", "height": 1, "tx_hash": "hash"},
        {"sender": "A", "recipient": "C", "amount": 200, "token": "token", "height": 2, "tx_hash": "hash2"},
        {"sender": "B", "recipient": "A", "amount": 150, "token": "token", "height": 3, "tx_hash": "hash3"}
    ])
    clustering = ClusteringAnalyzer(data)
    features = clustering.compute_address_features()
    assert "address" in features.columns
    assert "sent_total" in features.columns

def test_cluster_addresses():
    data = pd.DataFrame([
        {"sender": "A", "recipient": "B", "amount": 100, "token": "token", "height": 1, "tx_hash": "hash"},
        {"sender": "A", "recipient": "C", "amount": 200, "token": "token", "height": 2, "tx_hash": "hash2"},
        {"sender": "B", "recipient": "A", "amount": 150, "token": "token", "height": 3, "tx_hash": "hash3"}
    ])
    clustering = ClusteringAnalyzer(data)
    clusters = clustering.cluster_addresses(method="kmeans", n_clusters=2)
    assert "cluster" in clusters.columns