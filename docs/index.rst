Cohomological Risk Scoring Documentation
==========================================

**Cohomological Risk Scoring** is a Python package for financial risk assessment using algebraic topology and persistent cohomology.

This framework interprets financial risk as a cohomological obstruction to global data coherence in financial networks.

.. image:: https://img.shields.io/pypi/v/cohomological-risk-scoring.svg
   :target: https://pypi.org/project/cohomological-risk-scoring/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/cohomological-risk-scoring.svg
   :target: https://pypi.org/project/cohomological-risk-scoring/
   :alt: Python versions

Installation
------------

Install from PyPI:

.. code-block:: bash

   pip install cohomological-risk-scoring

Quick Start
-----------

.. code-block:: python

   from cohomological_risk_scoring import PCRScorer
   import numpy as np

   # Generate sample data
   np.random.seed(42)
   n_nodes = 20
   features = np.random.randn(n_nodes, 4)
   edges = [(i, j) for i in range(n_nodes) for j in range(i+1, n_nodes) 
            if np.random.random() > 0.7]

   # Create scorer and compute risk
   scorer = PCRScorer()
   scorer.fit(features, edges)
   risk_scores = scorer.compute_all_scores()
   risk_classes = scorer.get_risk_classes()

   print(f"High Risk Entities: {risk_classes['high']}")

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   api
   theory
   examples

Key Features
------------

* **Topological Risk Detection**: Uses persistent cohomology to detect structural anomalies
* **Sheaf Theory**: Models financial networks as sheaves over simplicial complexes
* **Cyclic Fraud Detection**: Guaranteed detection of circular transaction patterns
* **Stability Guarantees**: Robust to data perturbations and noise
* **Interpretable Results**: Provides topological footprints of detected anomalies

API Reference
-------------

.. toctree::
   :maxdepth: 2
   
   api

Theoretical Background
----------------------

The framework is based on:

* **Persistent Homology**: Tracking topological features across filtration scales
* **Sheaf Cohomology**: Measuring global consistency of local data
* **Algebraic Topology**: Detecting structural patterns in financial networks

Mathematical Foundations
~~~~~~~~~~~~~~~~~~~~~~~~

The core concept is modeling financial risk as non-trivial cohomology classes in H¹:

* **Vertices**: Financial entities (users, merchants, accounts)
* **Edges**: Transactions and relationships
* **Sheaf Data**: Local features and relational constraints
* **Cohomology**: Obstruction to global consistency

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
