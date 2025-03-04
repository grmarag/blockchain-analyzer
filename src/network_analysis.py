import networkx as nx
import pandas as pd

class NetworkAnalyzer:
    def __init__(self, transactions: pd.DataFrame):
        self.transactions = transactions
        self.graph = None
        self.centrality = {}

    def build_graph(self):
        # Aggregate transactions: sum of amounts and count per (sender, recipient) pair
        aggregated = self.transactions.groupby(['sender', 'recipient'], as_index=False).agg(
            amount=('amount', 'sum'),
            tx_count=('amount', 'count')
        )
        # Create a directed graph from the aggregated DataFrame
        self.graph = nx.from_pandas_edgelist(
            aggregated,
            source='sender',
            target='recipient',
            edge_attr=['amount', 'tx_count'],
            create_using=nx.DiGraph()
        )
        return self.graph

    def analyze_centrality(self, approximate=True, k=100):
        if self.graph is None:
            self.build_graph()
        # Compute degree centrality
        degree_centrality = nx.degree_centrality(self.graph)
        
        # Compute betweenness centrality (approximate if specified and graph is large)
        if approximate and len(self.graph) > k:
            betweenness_centrality = nx.betweenness_centrality(self.graph, k=k, normalized=True)
        else:
            betweenness_centrality = nx.betweenness_centrality(self.graph, normalized=True)
        
        self.centrality = {
            "degree": degree_centrality,
            "betweenness": betweenness_centrality
        }
        return self.centrality

    def get_hubs(self, threshold=0.1):
        # Use cached degree centrality if available
        if "degree" in self.centrality:
            degree_centrality = self.centrality["degree"]
        else:
            if self.graph is None:
                self.build_graph()
            degree_centrality = nx.degree_centrality(self.graph)
            self.centrality["degree"] = degree_centrality
        
        hubs = {node: cent for node, cent in degree_centrality.items() if cent >= threshold}
        return hubs