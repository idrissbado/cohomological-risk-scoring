Quick Start Guide
=================

This guide will help you get started with Cohomological Risk Scoring in 5 minutes.

Installation
------------

.. code-block:: bash

   pip install cohomological-risk-scoring

Basic Usage
-----------

1. Import the Package
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from cohomological_risk_scoring import PCRScorer, FinancialSheaf
   import numpy as np

2. Prepare Your Data
~~~~~~~~~~~~~~~~~~~~

You need:
- **Node features**: A matrix where each row represents features of a financial entity
- **Edges**: List of tuples representing connections (transactions)

.. code-block:: python

   # Example: 20 financial entities with 4 features each
   n_nodes = 20
   features = np.random.randn(n_nodes, 4)
   
   # Example: Random transaction network
   edges = [(i, j) for i in range(n_nodes) 
            for j in range(i+1, n_nodes) 
            if np.random.random() > 0.7]

3. Compute Risk Scores
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Initialize scorer
   scorer = PCRScorer()
   
   # Fit the model
   scorer.fit(features, edges)
   
   # Get risk scores for all nodes
   risk_scores = scorer.compute_all_scores()
   
   # Classify entities by risk level
   risk_classes = scorer.get_risk_classes()
   
   print(f"High Risk: {risk_classes['high']}")
   print(f"Medium Risk: {risk_classes['medium']}")
   print(f"Low Risk: {risk_classes['low']}")

4. Visualize Results
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Visualize persistence diagram
   scorer.visualize_persistence()
   
   # Generate full report
   report = scorer.generate_report()
   print(report)

Advanced Usage
--------------

Working with Real Financial Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   from cohomological_risk_scoring.utils import load_transaction_data
   
   # Load your transaction data
   transactions = pd.read_csv('transactions.csv')
   
   # Convert to graph format
   edges = list(zip(transactions['from'], transactions['to']))
   
   # Extract features per entity
   features = extract_features(transactions)  # Your feature extraction
   
   # Compute risk
   scorer = PCRScorer()
   scorer.fit(features, edges)
   scores = scorer.compute_all_scores()

Customizing Filtration
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Use custom filtration values
   filtration_values = np.linspace(0, 1, 20)
   
   scorer = PCRScorer()
   scorer.fit(features, edges, filtration=filtration_values)

What's Next?
------------

- Explore the :doc:`api` for detailed documentation
- Read the :doc:`theory` for mathematical background
- Check out :doc:`examples` for real-world applications
