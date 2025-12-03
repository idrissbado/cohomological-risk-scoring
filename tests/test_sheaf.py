"""
Tests for FinancialSheaf class
===============================

Author: Idriss Bado
"""

import pytest
import numpy as np
import networkx as nx
import sys
sys.path.insert(0, '../src')

from cohomological_risk_scoring.sheaf import FinancialSheaf


class TestFinancialSheaf:
    """Test suite for FinancialSheaf class."""
    
    @pytest.fixture
    def simple_graph(self):
        """Create a simple test graph."""
        G = nx.Graph()
        G.add_edges_from([(0, 1), (1, 2), (2, 0)])
        for u, v in G.edges():
            G[u][v]['weight'] = 1.0
        return G
    
    @pytest.fixture
    def vertex_features(self):
        """Create simple vertex features."""
        return {
            0: np.array([1.0, 2.0, 3.0]),
            1: np.array([1.5, 2.5, 3.5]),
            2: np.array([2.0, 3.0, 4.0])
        }
    
    @pytest.fixture
    def edge_features(self):
        """Create simple edge features."""
        return {
            (0, 1): 1.0,
            (1, 2): 1.0,
            (2, 0): 1.0
        }
    
    def test_initialization(self):
        """Test sheaf initialization."""
        sheaf = FinancialSheaf(max_simplex_dim=2)
        assert sheaf.max_dim == 2
        assert sheaf.complex == {}
        assert sheaf.sheaf_data == {}
    
    def test_build_complex(self, simple_graph):
        """Test complex building."""
        sheaf = FinancialSheaf(max_simplex_dim=2)
        complex = sheaf.build_complex_from_graph(simple_graph)
        
        assert 0 in complex
        assert 1 in complex
        assert len(complex[0]) == 3  # 3 vertices
        assert len(complex[1]) == 3  # 3 edges
    
    def test_define_sheaf_data(self, simple_graph, vertex_features, edge_features):
        """Test sheaf data definition."""
        sheaf = FinancialSheaf()
        sheaf.build_complex_from_graph(simple_graph)
        sheaf.define_sheaf_data(vertex_features, edge_features)
        
        assert 'vertices' in sheaf.sheaf_data
        assert 'edges' in sheaf.sheaf_data
        assert len(sheaf.vertex_features) == 3
    
    def test_compute_coboundary_matrix(self, simple_graph, vertex_features, edge_features):
        """Test coboundary matrix computation."""
        sheaf = FinancialSheaf()
        sheaf.build_complex_from_graph(simple_graph)
        sheaf.define_sheaf_data(vertex_features, edge_features)
        
        delta = sheaf.compute_coboundary_matrix(0)
        assert delta.shape[0] > 0  # Has rows
        assert delta.shape[1] > 0  # Has columns
    
    def test_persistent_cohomology(self, simple_graph, vertex_features, edge_features):
        """Test persistent cohomology computation."""
        sheaf = FinancialSheaf()
        sheaf.build_complex_from_graph(simple_graph)
        sheaf.define_sheaf_data(vertex_features, edge_features)
        
        persistence = sheaf.compute_persistent_cohomology()
        assert 'H0' in persistence
        assert 'H1' in persistence
        assert isinstance(persistence['H0'], list)
        assert isinstance(persistence['H1'], list)
    
    def test_pcr_score_computation(self, simple_graph, vertex_features, edge_features):
        """Test PCR score computation."""
        sheaf = FinancialSheaf()
        sheaf.build_complex_from_graph(simple_graph)
        sheaf.define_sheaf_data(vertex_features, edge_features)
        sheaf.compute_persistent_cohomology()
        
        score = sheaf.compute_pcr_score(0)
        assert isinstance(score, float)
        assert score >= 0
    
    def test_get_risk_classes(self, simple_graph, vertex_features, edge_features):
        """Test risk class identification."""
        sheaf = FinancialSheaf()
        sheaf.build_complex_from_graph(simple_graph)
        sheaf.define_sheaf_data(vertex_features, edge_features)
        sheaf.compute_persistent_cohomology()
        
        crcs = sheaf.get_risk_classes(threshold=0.0)
        assert isinstance(crcs, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
