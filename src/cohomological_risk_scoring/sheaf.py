"""
Financial Sheaf Implementation
===============================

This module implements the financial sheaf model for cohomological risk scoring.

Author: Idriss Bado
"""

import numpy as np
import networkx as nx
from itertools import combinations
from scipy import sparse
from scipy.sparse import linalg
import gudhi as gd
from typing import List, Dict, Tuple, Optional, Callable


class FinancialSheaf:
    """Implements the financial sheaf model for cohomological risk scoring."""
    
    def __init__(self, max_simplex_dim: int = 2):
        """
        Initialize the financial sheaf.
        
        Parameters
        ----------
        max_simplex_dim : int, default=2
            Maximum dimension of simplices to consider (2 for triangles, 3 for tetrahedra, etc.)
        """
        self.max_dim = max_simplex_dim
        self.complex = {}
        self.sheaf_data = {}
        self.filtration_values = {}
        
    def build_complex_from_graph(self, 
                                 graph: nx.Graph,
                                 threshold: float = 0.0) -> Dict[int, List]:
        """
        Build simplicial complex from financial graph using clique expansion.
        
        Parameters
        ----------
        graph : nx.Graph
            Financial transaction graph with nodes as entities and edges as transactions
        threshold : float, default=0.0
            Minimum edge weight to include in the complex
            
        Returns
        -------
        Dict[int, List]
            Dictionary mapping dimension to list of simplices
        """
        self.graph = graph
        
        # Filter edges by threshold
        filtered_edges = [(u, v) for u, v, d in graph.edges(data=True) 
                         if d.get('weight', 1) >= threshold]
        
        # Build 0-simplices (vertices)
        vertices = list(graph.nodes())
        self.complex[0] = [[v] for v in vertices]
        
        # Build 1-simplices (edges)
        edges = filtered_edges
        self.complex[1] = [[u, v] for u, v in edges]
        
        # Build higher-dimensional simplices (cliques)
        for dim in range(2, self.max_dim + 1):
            simplices = []
            # Find all cliques of size dim+1
            for clique in nx.enumerate_all_cliques(graph.subgraph(vertices)):
                if len(clique) == dim + 1:
                    # Check if all edges in clique meet threshold
                    edges_ok = all(graph.has_edge(u, v) and 
                                  graph[u][v].get('weight', 1) >= threshold 
                                  for u, v in combinations(clique, 2))
                    if edges_ok:
                        simplices.append(sorted(clique))
            self.complex[dim] = simplices
            
        return self.complex
    
    def define_sheaf_data(self, 
                         vertex_features: Dict,
                         edge_features: Dict,
                         restriction_func: Optional[Callable] = None):
        """
        Define sheaf data with vertex and edge stalks and restriction maps.
        
        Parameters
        ----------
        vertex_features : Dict
            Dictionary mapping vertex IDs to feature vectors
        edge_features : Dict
            Dictionary mapping edge tuples (u, v) to feature values
        restriction_func : Callable, optional
            Function defining restriction maps ρ: F(v) → F(e)
            Default: projection to first component
        """
        self.vertex_features = vertex_features
        self.edge_features = edge_features
        
        # Default restriction: project vertex feature to edge via difference
        if restriction_func is None:
            def restriction_func(v_feat, e_feat):
                # Simple difference-based restriction
                return np.linalg.norm(v_feat - e_feat) if isinstance(v_feat, np.ndarray) else v_feat - e_feat
        
        self.restriction_func = restriction_func
        
        # Store sheaf data
        self.sheaf_data['vertices'] = vertex_features
        self.sheaf_data['edges'] = edge_features
        
    def compute_coboundary_matrix(self, dim: int) -> sparse.csr_matrix:
        """
        Compute coboundary matrix δ^p: C^p → C^{p+1}.
        
        Parameters
        ----------
        dim : int
            Dimension p for cochains
            
        Returns
        -------
        sparse.csr_matrix
            Coboundary matrix
        """
        if dim not in self.complex or dim + 1 not in self.complex:
            return sparse.csr_matrix((0, 0))
        
        p_simplices = self.complex[dim]
        p1_simplices = self.complex[dim + 1]
        
        n_p = len(p_simplices)
        n_p1 = len(p1_simplices)
        
        rows, cols, data = [], [], []
        
        for j, sigma in enumerate(p1_simplices):
            for i, tau in enumerate(p_simplices):
                # Check if tau is a face of sigma
                if set(tau).issubset(set(sigma)):
                    sign = self._orientation_sign(sigma, tau)
                    rows.append(j)
                    cols.append(i)
                    data.append(sign)
        
        return sparse.csr_matrix((data, (rows, cols)), shape=(n_p1, n_p))
    
    def _orientation_sign(self, sigma: List, tau: List) -> int:
        """
        Compute orientation sign for coboundary operator.
        
        Parameters
        ----------
        sigma : List
            Higher-dimensional simplex
        tau : List
            Face of sigma
            
        Returns
        -------
        int
            Orientation sign (+1 or -1)
        """
        # Find index of tau in sigma
        indices = [sigma.index(v) for v in tau]
        # Sign is (-1)^k where k is sum of indices
        return (-1) ** sum(indices)
    
    def compute_cohomology(self, dim: int) -> Dict:
        """
        Compute cohomology group H^p for given dimension.
        
        Parameters
        ----------
        dim : int
            Dimension p
            
        Returns
        -------
        Dict
            Dictionary with basis of H^p, cocycles, and coboundaries
        """
        if dim == 0:
            delta_prev = None
        else:
            delta_prev = self.compute_coboundary_matrix(dim - 1)
        
        delta = self.compute_coboundary_matrix(dim)
        
        # Compute kernels and images
        if delta_prev is not None:
            # For QR decomposition to find image
            Q, R = linalg.qr(delta_prev.todense(), mode='economic')
            im_delta_prev = Q
        else:
            im_delta_prev = None
        
        # Compute kernel of delta (cocycles)
        if delta.shape[1] > 0:
            # Use SVD to find null space
            U, s, Vh = linalg.svds(delta, k=min(delta.shape) - 1)
            kernel_basis = Vh.T[:, np.where(s < 1e-10)[0]]
        else:
            kernel_basis = np.eye(delta.shape[1])
        
        # Compute cohomology basis
        if im_delta_prev is not None and kernel_basis.size > 0:
            # Project kernel basis orthogonal to image
            proj = im_delta_prev @ (im_delta_prev.T @ kernel_basis)
            cohomology_basis = kernel_basis - proj
            
            # Orthogonalize
            Q, R = np.linalg.qr(cohomology_basis, mode='reduced')
            cohomology_basis = Q
        else:
            cohomology_basis = kernel_basis
        
        return {
            'dimension': dim,
            'basis': cohomology_basis,
            'kernel_dim': kernel_basis.shape[1] if kernel_basis.ndim > 1 else 1,
            'image_dim': im_delta_prev.shape[1] if im_delta_prev is not None else 0,
            'cohomology_dim': cohomology_basis.shape[1] if cohomology_basis.ndim > 1 else 1
        }
    
    def compute_persistent_cohomology(self, 
                                     filtration_param: str = 'weight',
                                     max_filtration: Optional[float] = None) -> Dict:
        """
        Compute persistent cohomology across filtration.
        
        Parameters
        ----------
        filtration_param : str, default='weight'
            Parameter to use for filtration ('weight', 'time', 'amount')
        max_filtration : float, optional
            Maximum filtration value
            
        Returns
        -------
        Dict
            Dictionary with persistence diagrams and intervals
        """
        if not hasattr(self, 'graph'):
            raise ValueError("Build complex first using build_complex_from_graph()")
        
        # Create Gudhi simplex tree
        st = gd.SimplexTree()
        
        # Add vertices
        for v in self.graph.nodes():
            st.insert([v], filtration=0)
        
        # Add edges with filtration values
        for u, v, data in self.graph.edges(data=True):
            filtration = data.get(filtration_param, 1.0)
            st.insert([u, v], filtration=filtration)
        
        # Add higher-dimensional simplices
        for dim in range(2, self.max_dim + 1):
            for simplex in self.complex.get(dim, []):
                # Filtration value is max of edge filtrations
                edge_filtrations = []
                for u, v in combinations(simplex, 2):
                    if self.graph.has_edge(u, v):
                        edge_filtrations.append(
                            self.graph[u][v].get(filtration_param, 1.0)
                        )
                if edge_filtrations:
                    filtration = max(edge_filtrations)
                    st.insert(simplex, filtration=filtration)
        
        # Compute persistent cohomology
        persistence = st.persistence(
            homology_coeff_field=2,  # Use Z/2Z coefficients for efficiency
            min_persistence=0,
            persistence_dim_max=True
        )
        
        # Filter for H^1 (dimension 1)
        h1_persistence = [(birth, death) for dim, (birth, death) in persistence 
                         if dim == 1]
        
        # Store persistence intervals
        self.persistence_intervals = {
            'H0': [(b, d) for dim, (b, d) in persistence if dim == 0],
            'H1': h1_persistence
        }
        
        return self.persistence_intervals
    
    def compute_pcr_score(self, 
                         vertex: int,
                         persistence_weight: float = 1.0,
                         norm_weight: float = 0.5) -> float:
        """
        Compute PCR score for a vertex.
        
        Parameters
        ----------
        vertex : int
            Vertex ID
        persistence_weight : float, default=1.0
            Weight for persistence term
        norm_weight : float, default=0.5
            Weight for cocycle norm term
            
        Returns
        -------
        float
            PCR score
        """
        if not hasattr(self, 'persistence_intervals'):
            raise ValueError("Compute persistent cohomology first")
        
        # Get H1 persistence intervals
        h1_intervals = self.persistence_intervals['H1']
        
        # Find cycles involving this vertex
        vertex_pcr = 0.0
        
        for birth, death in h1_intervals:
            # Calculate persistence
            persistence = death - birth if death != float('inf') else birth
            
            # Calculate cocycle norm
            cocycle_norm = self._estimate_cocycle_norm(vertex, birth, death)
            
            # Weighted PCR contribution
            contribution = persistence_weight * persistence + norm_weight * cocycle_norm
            vertex_pcr += contribution
        
        return vertex_pcr
    
    def _estimate_cocycle_norm(self, vertex: int, birth: float, death: float) -> float:
        """
        Estimate norm of cocycle involving vertex.
        
        Parameters
        ----------
        vertex : int
            Vertex ID
        birth : float
            Birth time in filtration
        death : float
            Death time in filtration
            
        Returns
        -------
        float
            Estimated cocycle norm
        """
        # Simplified estimation based on edge inconsistencies
        inconsistencies = []
        
        for neighbor in self.graph.neighbors(vertex):
            edge_data = self.graph[vertex][neighbor]
            
            # Calculate inconsistency
            if vertex in self.vertex_features and (vertex, neighbor) in self.edge_features:
                v_feat = self.vertex_features[vertex]
                e_feat = self.edge_features[(vertex, neighbor)]
                
                if isinstance(v_feat, np.ndarray) and isinstance(e_feat, (int, float)):
                    inconsistency = np.linalg.norm(v_feat) - abs(e_feat)
                else:
                    inconsistency = abs(v_feat - e_feat) if isinstance(v_feat, (int, float)) else 1.0
                
                # Weight by edge filtration if in persistence interval
                edge_filtration = edge_data.get('weight', 1.0)
                if birth <= edge_filtration <= (death if death != float('inf') else birth * 2):
                    inconsistency *= 2  # Double weight if in persistence interval
                
                inconsistencies.append(inconsistency)
        
        return np.mean(inconsistencies) if inconsistencies else 0.0
    
    def get_risk_classes(self, threshold: float = 0.1) -> List[Dict]:
        """
        Identify Cohomological Risk Classes (CRCs) above threshold.
        
        Parameters
        ----------
        threshold : float, default=0.1
            Minimum persistence threshold
            
        Returns
        -------
        List[Dict]
            List of CRC dictionaries
        """
        crcs = []
        
        for i, (birth, death) in enumerate(self.persistence_intervals['H1']):
            persistence = death - birth if death != float('inf') else birth
            
            if persistence >= threshold:
                # Find vertices involved (simplified)
                involved_vertices = self._find_vertices_in_cycle(i)
                
                crcs.append({
                    'id': i,
                    'birth': birth,
                    'death': death,
                    'persistence': persistence,
                    'vertices': involved_vertices,
                    'risk_level': min(persistence * 10, 1.0)  # Normalized to [0, 1]
                })
        
        return crcs
    
    def _find_vertices_in_cycle(self, cycle_idx: int) -> List:
        """
        Find vertices involved in a persistent cycle (simplified).
        
        Parameters
        ----------
        cycle_idx : int
            Index of the cycle
            
        Returns
        -------
        List
            List of vertices involved in the cycle
        """
        # In a full implementation, this would trace back through the
        # persistent homology computation to get the cycle representative
        # Here we return vertices with high PCR scores as approximation
        
        vertices = []
        for v in self.graph.nodes():
            pcr = self.compute_pcr_score(v)
            if pcr > 0.5:  # Threshold
                vertices.append((v, pcr))
        
        # Sort by PCR score
        vertices.sort(key=lambda x: x[1], reverse=True)
        return [v for v, _ in vertices[:10]]  # Top 10 vertices
