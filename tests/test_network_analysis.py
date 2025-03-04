import pandas as pd
from src.network_analysis import NetworkAnalyzer

def test_build_graph():
    data = pd.DataFrame([
        {"sender": "A", "recipient": "B", "amount": 100, "token": "token", "height": 1, "tx_hash": "hash"},
        {"sender": "B", "recipient": "C", "amount": 150, "token": "token", "height": 2, "tx_hash": "hash2"}
    ])
    analyzer = NetworkAnalyzer(data)
    graph = analyzer.build_graph()
    assert graph.number_of_nodes() >= 3

def test_get_hubs():
    data = pd.DataFrame([
        {"sender": "A", "recipient": "B", "amount": 100, "token": "token", "height": 1, "tx_hash": "hash"},
        {"sender": "A", "recipient": "C", "amount": 150, "token": "token", "height": 2, "tx_hash": "hash2"},
        {"sender": "A", "recipient": "D", "amount": 200, "token": "token", "height": 3, "tx_hash": "hash3"}
    ])
    analyzer = NetworkAnalyzer(data)
    analyzer.build_graph()
    hubs = analyzer.get_hubs(threshold=0.5)
    assert isinstance(hubs, dict)