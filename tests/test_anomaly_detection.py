import pandas as pd
from src.anomaly_detection import AnomalyDetector

def test_detect_amount_anomalies():
    data = pd.DataFrame([
        {"sender": "A", "recipient": "B", "amount": 100, "token": "token", "height": 1, "tx_hash": "hash"},
        {"sender": "A", "recipient": "C", "amount": 1000000, "token": "token", "height": 2, "tx_hash": "hash2"},
        {"sender": "B", "recipient": "C", "amount": 500, "token": "token", "height": 3, "tx_hash": "hash3"},
        {"sender": "C", "recipient": "D", "amount": 200, "token": "token", "height": 4, "tx_hash": "hash4"},
        {"sender": "D", "recipient": "E", "amount": 100, "token": "token", "height": 5, "tx_hash": "hash5"}
    ])
    detector = AnomalyDetector(data)
    anomalies = detector.detect_amount_anomalies(contamination=0.2)
    assert not anomalies.empty

def test_detect_activity_anomalies():
    data = pd.DataFrame([
        {"sender": "A", "recipient": "B", "amount": 100, "token": "token", "height": 1, "tx_hash": "hash1"},
        {"sender": "A", "recipient": "C", "amount": 200, "token": "token", "height": 2, "tx_hash": "hash2"},
        {"sender": "A", "recipient": "D", "amount": 150, "token": "token", "height": 3, "tx_hash": "hash3"},
        {"sender": "B", "recipient": "C", "amount": 500, "token": "token", "height": 4, "tx_hash": "hash4"},
        {"sender": "B", "recipient": "D", "amount": 300, "token": "token", "height": 5, "tx_hash": "hash5"},
        {"sender": "B", "recipient": "E", "amount": 700, "token": "token", "height": 6, "tx_hash": "hash6"},
        {"sender": "C", "recipient": "F", "amount": 50, "token": "token", "height": 7, "tx_hash": "hash7"},
        {"sender": "C", "recipient": "G", "amount": 90, "token": "token", "height": 8, "tx_hash": "hash8"},
        {"sender": "C", "recipient": "H", "amount": 40, "token": "token", "height": 9, "tx_hash": "hash9"},
        {"sender": "C", "recipient": "I", "amount": 5000, "token": "token", "height": 10, "tx_hash": "hash10"},
        {"sender": "C", "recipient": "J", "amount": 60, "token": "token", "height": 11, "tx_hash": "hash11"},
        {"sender": "C", "recipient": "K", "amount": 30, "token": "token", "height": 12, "tx_hash": "hash12"},
        {"sender": "D", "recipient": "L", "amount": 300, "token": "token", "height": 13, "tx_hash": "hash13"},
        {"sender": "D", "recipient": "M", "amount": 150, "token": "token", "height": 14, "tx_hash": "hash14"},
        {"sender": "D", "recipient": "N", "amount": 100, "token": "token", "height": 15, "tx_hash": "hash15"},
        {"sender": "D", "recipient": "O", "amount": 250, "token": "token", "height": 16, "tx_hash": "hash16"},
        {"sender": "D", "recipient": "P", "amount": 400, "token": "token", "height": 17, "tx_hash": "hash17"},
        {"sender": "E", "recipient": "Q", "amount": 500, "token": "token", "height": 18, "tx_hash": "hash18"},
        {"sender": "E", "recipient": "R", "amount": 600, "token": "token", "height": 19, "tx_hash": "hash19"},
        {"sender": "E", "recipient": "S", "amount": 700, "token": "token", "height": 20, "tx_hash": "hash20"},
    ])
    detector = AnomalyDetector(data)
    anomalies = detector.detect_activity_anomalies(contamination=0.2)
    assert not anomalies.empty