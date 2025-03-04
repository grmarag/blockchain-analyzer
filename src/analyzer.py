import argparse
import os
import pandas as pd
from src.data_loader import DataLoader
from src.clustering import ClusteringAnalyzer
from src.anomaly_detection import AnomalyDetector
from src.network_analysis import NetworkAnalyzer
from src.ai_agent import AIAgent
from fpdf import FPDF
from src.utils import plot_clusters, plot_network, plot_amount_anomalies, plot_activity_anomalies

class BlockchainAnalyzer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.transactions = None
        # Raw results (not aggregated)
        self.raw_clustering_results = None
        self.raw_anomaly_results = None
        self.raw_network_results = None
        # Aggregated results (for AI insights)
        self.clustering_results = None
        self.anomaly_results = None
        self.network_results = None

    def load_data(self):
        loader = DataLoader(self.file_path)
        self.transactions = loader.load_data()

    def run_clustering(self):
        clustering = ClusteringAnalyzer(self.transactions)
        clustering.compute_address_features()
        # Save raw clustering output (unaggregated)
        raw_results = clustering.cluster_addresses(method="hdbscan", min_cluster_size=5)
        self.raw_clustering_results = raw_results.copy()
        
        # Aggregate cluster statistics for AI insights
        aggregated_clustering = raw_results.groupby("cluster").agg(
            size=("address", "count"),
            avg_sent_tx=("sent_count", "mean"),
            avg_received_tx=("received_count", "mean"),
            avg_sent_value=("sent_total", "mean"),
            avg_received_value=("received_total", "mean"),
            total_sent=("sent_total", "sum"),
            total_received=("received_total", "sum"),
        ).reset_index()
        self.clustering_results = aggregated_clustering.head(1000)
        return self.clustering_results

    def run_anomaly_detection(self):
        detector = AnomalyDetector(self.transactions)
        # Save raw anomaly detection results
        raw_amount_anomalies = detector.detect_amount_anomalies(contamination=0.01)
        raw_activity_anomalies = detector.detect_activity_anomalies(contamination=0.01)
        self.raw_anomaly_results = {
            "amount_anomalies": raw_amount_anomalies.copy(),
            "activity_anomalies": raw_activity_anomalies.copy()
        }

        # Aggregated (or selected) anomalies for AI insights (e.g. top n)
        aggregated_amount_anomalies = raw_amount_anomalies.sort_values(by="amount", ascending=False).head(5)
        aggregated_activity_anomalies = raw_activity_anomalies.sort_values(by="tx_count", ascending=False).head(5)
        self.anomaly_results = {
            "amount_anomalies": aggregated_amount_anomalies,
            "activity_anomalies": aggregated_activity_anomalies
        }
        return self.anomaly_results

    def run_network_analysis(self):
        network_analyzer = NetworkAnalyzer(self.transactions)
        graph = network_analyzer.build_graph()
        centrality = network_analyzer.analyze_centrality()
        hubs = network_analyzer.get_hubs(threshold=0.05)

        # Save raw network results without aggregation
        self.raw_network_results = {
            "graph": graph,
            "centrality": centrality.copy(),
            "hubs": hubs.copy()
        }
        
        # Prepare aggregated network data for AI insights
        # Aggregated centrality: convert to DataFrame and select top n nodes
        degree_dict = centrality.get("degree", {})
        betweenness_dict = centrality.get("betweenness", {})
        nodes = set(degree_dict.keys()).union(betweenness_dict.keys())
        data = []
        for node in nodes:
            data.append({
                "node": node,
                "degree": degree_dict.get(node, 0),
                "betweenness": betweenness_dict.get(node, 0)
            })
        df_centrality = pd.DataFrame(data)
        df_centrality = df_centrality.sort_values(by=["betweenness", "degree"], ascending=False).head(5)
        aggregated_centrality = df_centrality.to_dict(orient="records")
        
        # Aggregated hubs: top n by hub value
        aggregated_hubs = dict(sorted(hubs.items(), key=lambda x: x[1], reverse=True)[:5])
        
        # New Aggregated network edges: group by source and count number of unique target nodes (direct_connection)
        edges = []
        for u, v, data in graph.edges(data=True):
            edges.append({"source": u, "target": v})
        if edges:
            df_edges = pd.DataFrame(edges)
            df_direct_connection = df_edges.groupby("source").agg(direct_connection=("target", "nunique")).reset_index()
            aggregated_edges = df_direct_connection.to_dict(orient="records")
        else:
            aggregated_edges = []

        # Include aggregated network edges in the results
        self.network_results = {
            "graph": graph,
            "centrality": aggregated_centrality,
            "hubs": aggregated_hubs,
            "network_edges": aggregated_edges
        }
        return self.network_results

    def save_results_to_filesystem(self, directory="data/final"):
        os.makedirs(directory, exist_ok=True)
        
        # Save raw clustering results (without aggregation)
        if self.raw_clustering_results is not None:
            clustering_csv_path = os.path.join(directory, "clustering_results.csv")
            self.raw_clustering_results.to_csv(clustering_csv_path, index=False)
            print(f"Raw clustering results saved to {clustering_csv_path}")
        
        # Save raw anomaly detection results
        if self.raw_anomaly_results is not None:
            if "amount_anomalies" in self.raw_anomaly_results:
                amount_csv_path = os.path.join(directory, "amount_anomalies.csv")
                self.raw_anomaly_results["amount_anomalies"].to_csv(amount_csv_path, index=False)
                print(f"Raw amount anomalies saved to {amount_csv_path}")
            if "activity_anomalies" in self.raw_anomaly_results:
                activity_csv_path = os.path.join(directory, "activity_anomalies.csv")
                self.raw_anomaly_results["activity_anomalies"].to_csv(activity_csv_path, index=False)
                print(f"Raw activity anomalies saved to {activity_csv_path}")
        
        # Save raw network analysis results
        if self.raw_network_results is not None:
            graph = self.raw_network_results.get("graph")
            if graph is not None:
                edges = []
                for u, v, data in graph.edges(data=True):
                    edge_data = {"source": u, "target": v}
                    if "weight" in data:
                        edge_data["weight"] = data["weight"]
                    edges.append(edge_data)
                if edges:
                    df_edges = pd.DataFrame(edges)
                    edges_csv_path = os.path.join(directory, "network_edges.csv")
                    df_edges.to_csv(edges_csv_path, index=False)
                    print(f"Raw network edges saved to {edges_csv_path}")
            
            # Save raw centrality (convert full dict to DataFrame)
            centrality = self.raw_network_results.get("centrality")
            if centrality is not None:
                degree_dict = centrality.get("degree", {})
                betweenness_dict = centrality.get("betweenness", {})
                nodes = set(degree_dict.keys()).union(betweenness_dict.keys())
                data = []
                for node in nodes:
                    data.append({
                        "node": node,
                        "degree": degree_dict.get(node, 0),
                        "betweenness": betweenness_dict.get(node, 0)
                    })
                df_centrality = pd.DataFrame(data)
                centrality_csv_path = os.path.join(directory, "network_centrality.csv")
                df_centrality.to_csv(centrality_csv_path, index=False)
                print(f"Raw network centrality saved to {centrality_csv_path}")
            
            # Save raw hubs
            hubs = self.raw_network_results.get("hubs")
            if hubs is not None:
                df_hubs = pd.DataFrame(list(hubs.items()), columns=["node", "hub_value"])
                hubs_csv_path = os.path.join(directory, "network_hubs.csv")
                df_hubs.to_csv(hubs_csv_path, index=False)
                print(f"Raw network hubs saved to {hubs_csv_path}")

    def run_ai_insights(self):
        summary = "1. Clustering & Address Profiling:\n"
        summary += "   - Clustering algorithm used: HDBSCAN (min_cluster_size=5).\n"
        summary += "   - Aggregated clustering details: " + str(self.clustering_results.to_dict()) + "\n\n"
        
        summary += "2. Anomaly Detection:\n"
        summary += "   - Amount anomalies detected using Isolation Forest.\n"
        summary += "   - Activity anomalies detected using Local Outlier Factor.\n"
        summary += "   - Aggregated anomaly detection results (row counts): " + str({k: v.shape for k, v in self.anomaly_results.items()}) + "\n\n"
        
        summary += "3. Network Analysis:\n"
        summary += "   - Aggregated network hubs identified: " + str(self.network_results.get('hubs', {})) + "\n"
        summary += "   - Aggregated centrality metrics: " + str(self.network_results.get('centrality', {})) + "\n"
        
        agent = AIAgent()
        report = agent.generate_insight_report(summary)
        return report

def save_report_to_pdf(report: str, filename: str = "reports/report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Blockchain Analysis Insight Report", ln=True, align='C')
    pdf.ln(10)
    
    for line in report.split('\n'):
        if line.strip().startswith(("1.", "2.", "3.")) or line.strip().endswith(":"):
            pdf.set_font("Arial", 'B', 12)
        else:
            pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, txt=line)
    pdf.output(filename)

def main():
    parser = argparse.ArgumentParser(description="Blockchain Analyzer")
    parser.add_argument("--input", required=True, help="Path to dataset JSONL file")
    args = parser.parse_args()

    analyzer = BlockchainAnalyzer(args.input)
    analyzer.load_data()
    print("Data Loaded.")
    analyzer.run_clustering()
    print("Clustering completed.")
    analyzer.run_anomaly_detection()
    print("Anomaly detection completed.")
    analyzer.run_network_analysis()
    print("Network analysis completed.")
    analyzer.save_results_to_filesystem()
    
    # Visualization using aggregated results
    if analyzer.clustering_results is not None:
        print("Generating clustering visualization...")
        plot_clusters(analyzer.raw_clustering_results, x_col='sent_total', y_col='received_total', cluster_col='cluster', save_path="figures/clustering.png")
    if analyzer.anomaly_results is not None and "amount_anomalies" in analyzer.anomaly_results:
        print("Generating amount anomaly visualization...")
        plot_amount_anomalies(analyzer.transactions, analyzer.raw_anomaly_results["amount_anomalies"], save_path="figures/amount_anomalies.png")
    activity = analyzer.transactions.groupby("sender").size().reset_index(name="tx_count")
    if analyzer.anomaly_results is not None and "activity_anomalies" in analyzer.anomaly_results:
        print("Generating activity anomaly visualization...")
        plot_activity_anomalies(activity, analyzer.raw_anomaly_results["activity_anomalies"], save_path="figures/activity_anomalies.png")
    if analyzer.raw_network_results is not None and "graph" in analyzer.raw_network_results:
        print("Generating network visualization...")
        plot_network(analyzer.raw_network_results["graph"], save_path="figures/transaction_network.html")

    report = analyzer.run_ai_insights()
    print("AI Generated Report:")
    print(report)
    save_report_to_pdf(report)
    print("Report saved as 'report.pdf'.")

if __name__ == "__main__":
    main()