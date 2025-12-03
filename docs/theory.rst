Theoretical Background
======================

**Full Theoretical Treatment:** For complete mathematical proofs and detailed theoretical foundations, see the research paper:

`Bado, I. O. (2025). "Cohomological Risk Scoring: A Topological Framework for Detecting Structural Inconsistencies in Financial Networks." <https://www.researchgate.net/publication/398275656_Cohomological_Risk_Scoring_A_Topological_Framework_for_Detecting_Structural_Inconsistencies_in_Financial_Networks>`_

Mathematical Foundations
------------------------

Cohomological Risk Scoring is based on the mathematical framework of algebraic topology applied to financial networks.

Core Concepts
~~~~~~~~~~~~~

1. **Simplicial Complexes**
   
   Financial networks are modeled as simplicial complexes:
   
   - **Vertices (0-simplices)**: Financial entities
   - **Edges (1-simplices)**: Transactions/relationships
   - **Triangles (2-simplices)**: Higher-order interactions

2. **Sheaf Theory**
   
   A financial sheaf F assigns:
   
   - Data spaces to each simplex
   - Restriction maps encoding consistency constraints
   
3. **Persistent Cohomology**
   
   Tracks cohomological features across filtration scales to identify robust risk signals.

Key Theorems
------------

Theorem 1: Stability
~~~~~~~~~~~~~~~~~~~~

The persistence diagram of Cohomological Risk Classes (CRCs) is stable under data perturbations:

.. math::

   d_B(\text{Dgm}_1, \text{Dgm}_2) \leq C \cdot d_{GH}((K_1, F_1), (K_2, F_2))

**Implication**: Small errors in data lead to small changes in risk scores.

Theorem 2: Detection
~~~~~~~~~~~~~~~~~~~~

The framework guarantees detection of cyclic fraud patterns satisfying:

.. math::

   \left\| \sum_{i=1}^k \left( g(v_i, v_{i+1}) - \rho_{v_i \to e_i}(\mathbf{v}_i) \right) \right\| > \epsilon

**Implication**: Money laundering loops and circular trading are always detected.

Theorem 3: Locality
~~~~~~~~~~~~~~~~~~~

PCR scores can be computed efficiently from local neighborhoods:

.. math::

   r = O(\log(1/\epsilon))

**Implication**: Scalable to large networks with millions of nodes.

PCR Score Definition
--------------------

The Persistence of Cohomological Risk (PCR) score for vertex v:

.. math::

   \text{PCR}(v) = \sum_{[\omega] \in \mathcal{P}} \mathbb{1}_{v \in \text{supp}([\omega])} \cdot \text{pers}([\omega]) \cdot \|[\omega]\|

Where:

- P: Set of persistent CRCs
- pers([ω]): Persistence (lifetime) of cohomology class
- ||[ω]||: Norm of representative cocycle

Interpretation
--------------

High PCR Score Indicates
~~~~~~~~~~~~~~~~~~~~~~~~

1. **Cyclic Inconsistencies**: Entity participates in transaction loops inconsistent with declared profiles
2. **Structural Anomalies**: Part of fraud rings or laundering networks
3. **Global Risk**: Risk emerges from network structure, not local features alone

Advantages
~~~~~~~~~~

- **Global Perspective**: Detects relational risks invisible to local models
- **Interpretability**: Provides specific cycles/structures causing risk
- **Robustness**: Stable under noise and missing data
- **Mathematical Rigor**: Backed by theorems with formal guarantees

For the complete mathematical treatment, see the accompanying paper:
**"Cohomological Risk Scoring: A Topological Framework for Detecting Structural Inconsistencies in Financial Networks"**
