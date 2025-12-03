"""
Utility Functions
=================

Helper functions for creating example networks and data preprocessing.

Author: Idriss Bado
"""

import numpy as np
import networkx as nx
from typing import Tuple, Dict, Optional


def create_example_network(n_vertices: int = 20, 
                          edge_probability: float = 0.3,
                          seed: Optional[int] = None) -> Tuple[nx.Graph, Dict, Dict]:
    """
    Create an example financial network for testing and demonstration.
    
    Parameters
    ----------
    n_vertices : int, default=20
        Number of vertices (entities) in the network
    edge_probability : float, default=0.3
        Probability of edge creation in Erdős-Rényi model
    seed : int, optional
        Random seed for reproducibility
        
    Returns
    -------
    Tuple[nx.Graph, Dict, Dict]
        Graph, vertex features, and edge features
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Create graph with random transactions
    G = nx.erdos_renyi_graph(n_vertices, edge_probability, seed=seed)
    
    # Add random weights (transaction amounts)
    for u, v in G.edges():
        # Normal transactions: mostly small amounts
        if np.random.random() > 0.1:
            amount = np.random.exponential(100)
        else:
            # Suspicious: large circular flows
            amount = np.random.exponential(1000)
        G[u][v]['weight'] = amount
        G[u][v]['time'] = np.random.randint(0, 100)
    
    # Create vertex features (e.g., declared income, KYC score)
    vertex_features = {}
    for v in G.nodes():
        vertex_features[v] = np.array([
            np.random.normal(50000, 20000),  # Declared income
            np.random.beta(2, 5),           # KYC completeness (0-1)
            np.random.exponential(10)       # Account age (months)
        ])
    
    # Create edge features (actual transaction amounts)
    edge_features = {}
    for u, v in G.edges():
        edge_features[(u, v)] = G[u][v]['weight']
    
    return G, vertex_features, edge_features


def create_example_financial_network(n_vertices: int = 20) -> Tuple[nx.Graph, Dict, Dict]:
    """
    Legacy function name for backward compatibility.
    
    Parameters
    ----------
    n_vertices : int, default=20
        Number of vertices in the network
        
    Returns
    -------
    Tuple[nx.Graph, Dict, Dict]
        Graph, vertex features, and edge features
    """
    return create_example_network(n_vertices)


def load_transaction_data(filepath: str) -> Tuple[nx.Graph, Dict, Dict]:
    """
    Load financial transaction data from file.
    
    Parameters
    ----------
    filepath : str
        Path to the data file
        
    Returns
    -------
    Tuple[nx.Graph, Dict, Dict]
        Graph, vertex features, and edge features
        
    Notes
    -----
    Expected file format: CSV with columns: source, target, amount, timestamp
    """
    import pandas as pd
    
    # Load data
    df = pd.read_csv(filepath)
    
    # Create graph
    G = nx.from_pandas_edgelist(
        df, 
        source='source', 
        target='target', 
        edge_attr=['amount', 'timestamp']
    )
    
    # Create basic vertex features
    vertex_features = {}
    for v in G.nodes():
        # Aggregate features from transactions
        incoming = sum(G[u][v].get('amount', 0) for u in G.predecessors(v) if G.has_edge(u, v))
        outgoing = sum(G[v][w].get('amount', 0) for w in G.successors(v) if G.has_edge(v, w))
        
        vertex_features[v] = np.array([
            incoming,
            outgoing,
            len(list(G.neighbors(v)))
        ])
    
    # Create edge features
    edge_features = {}
    for u, v in G.edges():
        edge_features[(u, v)] = G[u][v].get('amount', 0)
    
    return G, vertex_features, edge_features


def normalize_features(features: Dict, method: str = 'standard') -> Dict:
    """
    Normalize feature vectors.
    
    Parameters
    ----------
    features : Dict
        Dictionary of feature vectors
    method : str, default='standard'
        Normalization method: 'standard', 'minmax', or 'l2'
        
    Returns
    -------
    Dict
        Normalized features
    """
    feature_array = np.array(list(features.values()))
    
    if method == 'standard':
        mean = feature_array.mean(axis=0)
        std = feature_array.std(axis=0)
        normalized = (feature_array - mean) / (std + 1e-8)
    elif method == 'minmax':
        min_val = feature_array.min(axis=0)
        max_val = feature_array.max(axis=0)
        normalized = (feature_array - min_val) / (max_val - min_val + 1e-8)
    elif method == 'l2':
        norms = np.linalg.norm(feature_array, axis=1, keepdims=True)
        normalized = feature_array / (norms + 1e-8)
    else:
        raise ValueError(f"Unknown normalization method: {method}")
    
    return {k: normalized[i] for i, k in enumerate(features.keys())}


def compute_network_statistics(G: nx.Graph) -> Dict:
    """
    Compute basic network statistics.
    
    Parameters
    ----------
    G : nx.Graph
        Input graph
        
    Returns
    -------
    Dict
        Dictionary of network statistics
    """
    stats = {
        'num_nodes': G.number_of_nodes(),
        'num_edges': G.number_of_edges(),
        'density': nx.density(G),
        'avg_degree': sum(dict(G.degree()).values()) / G.number_of_nodes(),
        'num_components': nx.number_connected_components(G),
        'avg_clustering': nx.average_clustering(G),
    }
    
    # Add centrality measures for top nodes
    degree_cent = nx.degree_centrality(G)
    betweenness_cent = nx.betweenness_centrality(G)
    
    stats['top_degree_nodes'] = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:5]
    stats['top_betweenness_nodes'] = sorted(betweenness_cent.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return stats
