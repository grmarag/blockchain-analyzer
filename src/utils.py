import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network

def plot_clusters(df, x_col, y_col, cluster_col, save_path=None):
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(df[x_col], df[y_col], c=df[cluster_col], cmap='viridis')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title("Address Clusters")
    plt.colorbar(scatter)
    plt.savefig(save_path)

def plot_network(graph, save_path="network.html", max_nodes=200):
    # If the graph is huge, restrict to a subgraph for visualization
    if graph.number_of_nodes() > max_nodes:
        # Extract the largest weakly connected component for a directed graph
        largest_cc = max(nx.weakly_connected_components(graph), key=len)
        subgraph = graph.subgraph(largest_cc).copy()
        # If still too many nodes, select top nodes by degree
        if subgraph.number_of_nodes() > max_nodes:
            sorted_nodes = sorted(subgraph.degree, key=lambda x: x[1], reverse=True)
            top_nodes = [n for n, d in sorted_nodes[:max_nodes]]
            subgraph = subgraph.subgraph(top_nodes).copy()
        graph = subgraph
    # Create a PyVis network
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
    # Add nodes with degree information
    for node in graph.nodes():
        degree = graph.degree[node]
        net.add_node(node, label=str(node), title=f"Degree: {degree}")
    # Add edges with additional info in the tooltip
    for u, v, data in graph.edges(data=True):
        title = f"Amount: {data.get('amount', 'N/A')}<br>Transactions: {data.get('tx_count', 'N/A')}"
        net.add_edge(u, v, title=title)
    # Use a physics layout for better node separation
    net.show_buttons(filter_=['physics'])
    net.show(save_path, notebook=False)
    print(f"Interactive network visualization saved as {save_path}")

def plot_amount_anomalies(transactions, anomalies, save_path=None):
    plt.figure(figsize=(10, 6))
    plt.scatter(transactions.index, transactions['amount'], label='Normal', alpha=0.5)
    plt.scatter(anomalies.index, anomalies['amount'], color='red', label='Anomaly')
    plt.xlabel('Transaction Index')
    plt.ylabel('Amount')
    plt.title('Transaction Amounts with Anomalies')
    plt.legend()
    plt.savefig(save_path)

def plot_activity_anomalies(activity, anomalies, save_path=None):
    plt.figure(figsize=(10, 6))
    # Plot all sender activity in blue
    plt.scatter(activity.index, activity['tx_count'], label='Normal', alpha=0.5)
    # Identify anomalies based on sender IDs
    anomaly_mask = activity['sender'].isin(anomalies['sender'])
    plt.scatter(activity[anomaly_mask].index, activity[anomaly_mask]['tx_count'], color='red', label='Anomaly')
    plt.xlabel('Sender Index')
    plt.ylabel('Transaction Count')
    plt.title('Sender Activity with Anomalies')
    plt.legend()
    plt.savefig(save_path)