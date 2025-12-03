"""
PCR Scorer Implementation
==========================

Main class for computing Persistence of Cohomological Risk scores.

Author: Idriss Bado
"""

import matplotlib.pyplot as plt
import networkx as nx
from typing import Dict, List, Optional, Callable

from .sheaf import FinancialSheaf


class PCRScorer:
    """Main class for computing Persistence of Cohomological Risk scores."""
    
    def __init__(self, 
                 max_dim: int = 2,
                 filtration_param: str = 'weight'):
        """
        Initialize PCR scorer.
        
        Parameters
        ----------
        max_dim : int, default=2
            Maximum simplex dimension
        filtration_param : str, default='weight'
            Parameter for filtration ('weight', 'time', 'amount')
        """
        self.sheaf = FinancialSheaf(max_simplex_dim=max_dim)
        self.filtration_param = filtration_param
        self.results = {}
        
    def fit(self, 
           graph: nx.Graph,
           vertex_features: Dict,
           edge_features: Dict,
           restriction_func: Optional[Callable] = None):
        """
        Fit the model to financial data.
        
        Parameters
        ----------
        graph : nx.Graph
            Financial transaction graph
        vertex_features : Dict
            Vertex feature vectors
        edge_features : Dict
            Edge feature values
        restriction_func : Callable, optional
            Restriction function for sheaf
        """
        # Build complex
        self.sheaf.build_complex_from_graph(graph)
        
        # Define sheaf data
        self.sheaf.define_sheaf_data(
            vertex_features, 
            edge_features, 
            restriction_func
        )
        
        # Compute persistent cohomology
        self.persistence = self.sheaf.compute_persistent_cohomology(
            self.filtration_param
        )
        
        # Store for reference
        self.graph = graph
        self.vertex_features = vertex_features
        self.edge_features = edge_features
        
    def compute_all_scores(self, 
                          persistence_weight: float = 1.0,
                          norm_weight: float = 0.5) -> Dict:
        """
        Compute PCR scores for all vertices.
        
        Parameters
        ----------
        persistence_weight : float, default=1.0
            Weight for persistence term
        norm_weight : float, default=0.5
            Weight for cocycle norm term
        
        Returns
        -------
        Dict
            Dictionary mapping vertex IDs to PCR scores
        """
        scores = {}
        
        for vertex in self.graph.nodes():
            score = self.sheaf.compute_pcr_score(
                vertex, 
                persistence_weight, 
                norm_weight
            )
            scores[vertex] = score
        
        # Normalize scores to [0, 1]
        max_score = max(scores.values()) if scores else 1
        if max_score > 0:
            scores = {v: s / max_score for v, s in scores.items()}
        
        self.scores = scores
        return scores
    
    def get_risk_classes(self, threshold: float = 0.1) -> List[Dict]:
        """
        Get identified risk classes.
        
        Parameters
        ----------
        threshold : float, default=0.1
            Minimum persistence threshold
            
        Returns
        -------
        List[Dict]
            List of risk class dictionaries
        """
        return self.sheaf.get_risk_classes(threshold)
    
    def visualize_persistence(self, save_path: Optional[str] = None):
        """
        Visualize persistence diagram and PCR scores.
        
        Parameters
        ----------
        save_path : str, optional
            Path to save the figure
        """
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot persistence diagram
        h1_points = [(b, d) for b, d in self.persistence['H1'] if d != float('inf')]
        
        if h1_points:
            births, deaths = zip(*h1_points)
            axes[0].scatter(births, deaths, alpha=0.6, s=100, edgecolors='black', linewidths=1)
            max_val = max(max(births), max(deaths))
            axes[0].plot([0, max_val], [0, max_val], 'k--', alpha=0.3, label='Diagonal')
            axes[0].set_xlabel('Birth', fontsize=12)
            axes[0].set_ylabel('Death', fontsize=12)
            axes[0].set_title('Persistence Diagram (H¹)', fontsize=14, fontweight='bold')
            axes[0].grid(True, alpha=0.3)
            axes[0].legend()
        else:
            axes[0].text(0.5, 0.5, 'No persistent features found', 
                        ha='center', va='center', transform=axes[0].transAxes)
            axes[0].set_title('Persistence Diagram (H¹)', fontsize=14, fontweight='bold')
        
        # Plot PCR scores
        if hasattr(self, 'scores'):
            vertices = list(self.scores.keys())
            scores = list(self.scores.values())
            
            colors = ['red' if s > 0.7 else 'orange' if s > 0.3 else 'green' for s in scores]
            axes[1].bar(range(len(vertices)), scores, alpha=0.7, color=colors, edgecolor='black')
            axes[1].axhline(y=0.7, color='red', linestyle='--', alpha=0.5, label='High Risk')
            axes[1].axhline(y=0.3, color='orange', linestyle='--', alpha=0.5, label='Medium Risk')
            axes[1].set_xlabel('Vertex Index', fontsize=12)
            axes[1].set_ylabel('PCR Score', fontsize=12)
            axes[1].set_title('PCR Scores by Vertex', fontsize=14, fontweight='bold')
            axes[1].grid(True, alpha=0.3, axis='y')
            axes[1].legend()
            axes[1].set_ylim([0, 1.05])
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def generate_report(self) -> str:
        """
        Generate analysis report.
        
        Returns
        -------
        str
            Formatted analysis report
        """
        report = []
        report.append("=" * 60)
        report.append("COHOMOLOGICAL RISK SCORING ANALYSIS")
        report.append("=" * 60)
        report.append(f"Author: Idriss Bado")
        report.append("")
        
        # Basic stats
        report.append("Network Statistics:")
        report.append(f"  Vertices: {self.graph.number_of_nodes()}")
        report.append(f"  Edges: {self.graph.number_of_edges()}")
        report.append(f"  Density: {nx.density(self.graph):.4f}")
        
        # Cohomology info
        h1_dim = len(self.persistence['H1'])
        h0_dim = len(self.persistence['H0'])
        report.append(f"\nCohomological Analysis:")
        report.append(f"  H⁰ classes found: {h0_dim}")
        report.append(f"  H¹ classes found: {h1_dim}")
        
        # PCR scores
        if hasattr(self, 'scores'):
            high_risk = sum(1 for s in self.scores.values() if s > 0.7)
            medium_risk = sum(1 for s in self.scores.values() if 0.3 < s <= 0.7)
            low_risk = len(self.scores) - high_risk - medium_risk
            
            report.append(f"\nPCR Score Distribution:")
            report.append(f"  High risk (score > 0.7): {high_risk} vertices ({100*high_risk/len(self.scores):.1f}%)")
            report.append(f"  Medium risk (0.3 < score ≤ 0.7): {medium_risk} vertices ({100*medium_risk/len(self.scores):.1f}%)")
            report.append(f"  Low risk (score ≤ 0.3): {low_risk} vertices ({100*low_risk/len(self.scores):.1f}%)")
            
            # Top risky vertices
            top_5 = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)[:5]
            report.append(f"\nTop 5 Risky Vertices:")
            for v, score in top_5:
                report.append(f"  Vertex {v}: PCR = {score:.3f}")
        
        # Risk classes
        crcs = self.get_risk_classes(0.1)
        report.append(f"\nCohomological Risk Classes (CRCs) found: {len(crcs)}")
        
        for i, crc in enumerate(crcs[:3]):  # Show top 3
            report.append(f"\n  CRC #{i+1}:")
            report.append(f"    Birth: {crc['birth']:.3f}")
            report.append(f"    Death: {crc['death']:.3f}")
            report.append(f"    Persistence: {crc['persistence']:.3f}")
            report.append(f"    Risk level: {crc['risk_level']:.2f}")
            report.append(f"    Involves vertices: {crc['vertices'][:5]}...")
        
        report.append("\n" + "=" * 60)
        
        return "\n".join(report)
