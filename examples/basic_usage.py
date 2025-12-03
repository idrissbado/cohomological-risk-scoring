"""
Basic Usage Example
===================

This example demonstrates basic usage of the cohomological risk scoring package.

Author: Idriss Bado
"""

import sys
sys.path.insert(0, '../src')

from cohomological_risk_scoring import PCRScorer
from cohomological_risk_scoring.utils import create_example_network


def main():
    """Demonstrate basic usage of the package."""
    
    print("=" * 70)
    print("COHOMOLOGICAL RISK SCORING - BASIC USAGE EXAMPLE")
    print("Author: Idriss Bado")
    print("=" * 70)
    
    # Step 1: Create example financial network
    print("\n1. Creating example financial network...")
    G, vertex_features, edge_features = create_example_network(n_vertices=30, seed=42)
    print(f"   Created network with {G.number_of_nodes()} vertices and {G.number_of_edges()} edges")
    
    # Step 2: Initialize the PCR scorer
    print("\n2. Initializing PCR scorer...")
    scorer = PCRScorer(max_dim=2, filtration_param='weight')
    print("   PCR scorer initialized with max_dim=2")
    
    # Step 3: Fit the model
    print("\n3. Fitting model to financial data...")
    scorer.fit(G, vertex_features, edge_features)
    print("   Model fitted successfully")
    
    # Step 4: Compute PCR scores
    print("\n4. Computing PCR scores for all vertices...")
    scores = scorer.compute_all_scores(
        persistence_weight=1.0,
        norm_weight=0.3
    )
    print(f"   Computed scores for {len(scores)} vertices")
    
    # Step 5: Analyze results
    print("\n5. Analyzing results...")
    
    # Get top risky vertices
    top_risky = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]
    print("\n   Top 5 risky vertices:")
    for v, score in top_risky:
        print(f"     • Vertex {v}: PCR score = {score:.3f}")
    
    # Get risk classes
    risk_classes = scorer.get_risk_classes(threshold=0.1)
    print(f"\n   Found {len(risk_classes)} Cohomological Risk Classes (CRCs)")
    
    # Step 6: Generate comprehensive report
    print("\n6. Generating comprehensive analysis report...\n")
    print(scorer.generate_report())
    
    # Step 7: Visualize results
    print("\n7. Generating visualizations...")
    scorer.visualize_persistence(save_path='basic_example_results.png')
    print("   Visualization saved to 'basic_example_results.png'")
    
    print("\n" + "=" * 70)
    print("EXAMPLE COMPLETED SUCCESSFULLY")
    print("=" * 70)
    
    return scorer, scores


if __name__ == "__main__":
    scorer, scores = main()
