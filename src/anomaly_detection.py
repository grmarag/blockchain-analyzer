import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

class AnomalyDetector:
    def __init__(self, transactions: pd.DataFrame):
        self.transactions = transactions
        self.anomalies = None

    def detect_amount_anomalies(self, contamination=0.01):
        """Detect anomalies in transaction amounts using Isolation Forest."""
        X = self.transactions[['amount']].values
        clf = IsolationForest(contamination=contamination, random_state=42)
        preds = clf.fit_predict(X)
        self.transactions['anomaly_if'] = preds
        anomalies = self.transactions[self.transactions['anomaly_if'] == -1]
        self.anomalies = anomalies
        return anomalies

    def detect_activity_anomalies(self, contamination=0.01):
        """Detect anomalies in sender activity using Local Outlier Factor."""
        activity = self.transactions.groupby("sender").size().reset_index(name="tx_count")
        X = activity[['tx_count']].values
        lof = LocalOutlierFactor(contamination=contamination)
        preds = lof.fit_predict(X)
        activity['anomaly_lof'] = preds
        anomalies = activity[activity['anomaly_lof'] == -1]
        return anomalies