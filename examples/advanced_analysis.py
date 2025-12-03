"""
Advanced Analysis Example
==========================

This example demonstrates advanced features including custom restriction functions
and detailed risk analysis.

Author: Idriss Bado
"""

import sys
import numpy as np
sys.path.insert(0, '../src')

from cohomological_risk_scoring import PCRScorer
from cohomological_risk_scoring.utils import create_example_network


def custom_restriction_function(v_feat, e_feat):
    """
    Custom restriction function comparing transaction to income capacity.
    
    Parameters
    ----------
    v_feat : np.ndarray
        Vertex feature vector [income, kyc_score, account_age]
    e_feat : float
        Edge feature (transaction amount)
        
    Returns
    -------
    float
        Discrepancy measure
    """
    if isinstance(v_feat, np.ndarray) and len(v_feat) >= 1:
        income = v_feat[0]  # First component is income
        # Assume 10% of monthly income as normal transaction capacity
        monthly_capacity = income / 12 * 0.1
        discrepancy = abs(e_feat - monthly_capacity) / (monthly_capacity + 1e-8)
        return discrepancy
    else:
        return abs(v_feat - e_feat) if isinstance(v_feat, (int, float)) else 1.0


def analyze_vertex_details(scorer, vertex_id):
    """Analyze details for a specific vertex."""
    print(f"\n{'='*60}")
    print(f"DETAILED ANALYSIS FOR VERTEX {vertex_id}")
    print(f"{'='*60}")
    
    # Get PCR score
    pcr_score = scorer.scores.get(vertex_id, 0)
    print(f"\nPCR Score: {pcr_score:.4f}")
    
    # Get vertex features
    v_feat = scorer.vertex_features[vertex_id]
    print(f"\nVertex Features:")
    print(f"  Income: ${v_feat[0]:,.2f}")
    print(f"  KYC Score: {v_feat[1]:.3f}")
    print(f"  Account Age: {v_feat[2]:.1f} months")
    
    # Get connected edges
    neighbors = list(scorer.graph.neighbors(vertex_id))
    print(f"\nConnections: {len(neighbors)} edges")
    
    # Analyze top transactions
    transactions = []
    for neighbor in neighbors:
        if (vertex_id, neighbor) in scorer.edge_features:
            amount = scorer.edge_features[(vertex_id, neighbor)]
            transactions.append((neighbor, amount))
    
    if transactions:
        transactions.sort(key=lambda x: x[1], reverse=True)
        print(f"\nTop 5 Transactions:")
        for i, (target, amount) in enumerate(transactions[:5], 1):
            print(f"  {i}. To vertex {target}: ${amount:,.2f}")
    
    # Get associated risk classes
    risk_classes = scorer.get_risk_classes(0.05)
    associated_crcs = [crc for crc in risk_classes if vertex_id in crc['vertices']]
    
    print(f"\nAssociated Risk Classes: {len(associated_crcs)}")
    for i, crc in enumerate(associated_crcs[:3], 1):
        print(f"  CRC #{crc['id']}: Persistence={crc['persistence']:.3f}, Risk={crc['risk_level']:.2f}")


def main():
    """Demonstrate advanced analysis features."""
    
    print("=" * 70)
    print("COHOMOLOGICAL RISK SCORING - ADVANCED ANALYSIS")
    print("Author: Idriss Bado")
    print("=" * 70)
    
    # Create larger network for more interesting analysis
    print("\n1. Creating financial network (50 vertices)...")
    G, vertex_features, edge_features = create_example_network(n_vertices=50, seed=123)
    
    # Initialize scorer
    print("\n2. Initializing PCR scorer with custom settings...")
    scorer = PCRScorer(max_dim=2, filtration_param='weight')
    
    # Fit with custom restriction function
    print("\n3. Fitting model with custom restriction function...")
    scorer.fit(
        G, 
        vertex_features, 
        edge_features, 
        restriction_func=custom_restriction_function
    )
    
    # Compute scores with different weights
    print("\n4. Computing PCR scores with adjusted weights...")
    scores = scorer.compute_all_scores(
        persistence_weight=1.5,  # Emphasize persistence
        norm_weight=0.2          # De-emphasize local inconsistency
    )
    
    # Comprehensive analysis
    print("\n5. Performing comprehensive risk analysis...")
    
    # Risk distribution
    high_risk = [v for v, s in scores.items() if s > 0.7]
    medium_risk = [v for v, s in scores.items() if 0.3 < s <= 0.7]
    low_risk = [v for v, s in scores.items() if s <= 0.3]
    
    print(f"\n   Risk Distribution:")
    print(f"     High Risk:   {len(high_risk)} vertices ({100*len(high_risk)/len(scores):.1f}%)")
    print(f"     Medium Risk: {len(medium_risk)} vertices ({100*len(medium_risk)/len(scores):.1f}%)")
    print(f"     Low Risk:    {len(low_risk)} vertices ({100*len(low_risk)/len(scores):.1f}%)")
    
    # Identify critical vertices
    print("\n6. Identifying critical high-risk vertices...")
    top_10 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]
    print("\n   Top 10 Risky Vertices:")
    for rank, (v, score) in enumerate(top_10, 1):
        degree = scorer.graph.degree(v)
        print(f"     {rank:2d}. Vertex {v:2d}: Score={score:.4f}, Connections={degree}")
    
    # Analyze specific vertices
    print("\n7. Detailed vertex analysis...")
    if top_10:
        analyze_vertex_details(scorer, top_10[0][0])
        if len(top_10) > 4:
            analyze_vertex_details(scorer, top_10[4][0])
    
    # Risk class analysis
    print(f"\n8. Analyzing Cohomological Risk Classes...")
    risk_classes = scorer.get_risk_classes(threshold=0.05)
    print(f"\n   Found {len(risk_classes)} CRCs with persistence > 0.05")
    
    if risk_classes:
        print("\n   Top 3 Risk Classes:")
        for i, crc in enumerate(sorted(risk_classes, key=lambda x: x['persistence'], reverse=True)[:3], 1):
            print(f"\n   CRC #{i}:")
            print(f"     ID: {crc['id']}")
            print(f"     Birth: {crc['birth']:.3f}")
            print(f"     Death: {crc['death']:.3f}")
            print(f"     Persistence: {crc['persistence']:.3f}")
            print(f"     Risk Level: {crc['risk_level']:.2f}")
            print(f"     Involves {len(crc['vertices'])} vertices")
    
    # Generate full report
    print("\n9. Generating comprehensive report...\n")
    print(scorer.generate_report())
    
    # Visualize
    print("\n10. Creating visualizations...")
    scorer.visualize_persistence(save_path='advanced_example_results.png')
    print("    Visualization saved to 'advanced_example_results.png'")
    
    print("\n" + "=" * 70)
    print("ADVANCED ANALYSIS COMPLETED")
    print("=" * 70)
    
    return scorer, scores


if __name__ == "__main__":
    scorer, scores = main()
