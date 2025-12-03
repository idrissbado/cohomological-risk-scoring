"""
Tests for PCRScorer class
==========================

Author: Idriss Bado
"""

import pytest
import numpy as np
import sys
sys.path.insert(0, '../src')

from cohomological_risk_scoring import PCRScorer
from cohomological_risk_scoring.utils import create_example_network


class TestPCRScorer:
    """Test suite for PCRScorer class."""
    
    @pytest.fixture
    def test_network(self):
        """Create a test network."""
        return create_example_network(n_vertices=10, seed=42)
    
    def test_initialization(self):
        """Test scorer initialization."""
        scorer = PCRScorer(max_dim=2, filtration_param='weight')
        assert scorer.sheaf.max_dim == 2
        assert scorer.filtration_param == 'weight'
    
    def test_fit(self, test_network):
        """Test model fitting."""
        G, vertex_features, edge_features = test_network
        scorer = PCRScorer()
        scorer.fit(G, vertex_features, edge_features)
        
        assert hasattr(scorer, 'graph')
        assert hasattr(scorer, 'persistence')
        assert scorer.graph.number_of_nodes() > 0
    
    def test_compute_all_scores(self, test_network):
        """Test score computation."""
        G, vertex_features, edge_features = test_network
        scorer = PCRScorer()
        scorer.fit(G, vertex_features, edge_features)
        
        scores = scorer.compute_all_scores()
        assert len(scores) == G.number_of_nodes()
        assert all(0 <= s <= 1 for s in scores.values())
    
    def test_get_risk_classes(self, test_network):
        """Test risk class retrieval."""
        G, vertex_features, edge_features = test_network
        scorer = PCRScorer()
        scorer.fit(G, vertex_features, edge_features)
        scorer.compute_all_scores()
        
        risk_classes = scorer.get_risk_classes(threshold=0.0)
        assert isinstance(risk_classes, list)
    
    def test_generate_report(self, test_network):
        """Test report generation."""
        G, vertex_features, edge_features = test_network
        scorer = PCRScorer()
        scorer.fit(G, vertex_features, edge_features)
        scorer.compute_all_scores()
        
        report = scorer.generate_report()
        assert isinstance(report, str)
        assert len(report) > 0
        assert "COHOMOLOGICAL RISK SCORING" in report


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
