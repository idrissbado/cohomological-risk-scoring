Examples
========

This page provides practical examples of using Cohomological Risk Scoring.

Example 1: Fraud Ring Detection
--------------------------------

Detecting a circular transaction pattern (money laundering loop):

.. code-block:: python

   import numpy as np
   from cohomological_risk_scoring import PCRScorer
   
   # Create a network with a fraud ring (5-cycle)
   n_nodes = 20
   features = np.random.randn(n_nodes, 4)
   
   # Add normal transactions
   edges = [(i, j) for i in range(n_nodes) 
            for j in range(i+1, n_nodes) 
            if np.random.random() > 0.8]
   
   # Add fraud ring: nodes 0->5->10->15->19->0
   fraud_ring = [(0, 5), (5, 10), (10, 15), (15, 19), (19, 0)]
   edges.extend(fraud_ring)
   
   # Manipulate features to create inconsistency
   features[fraud_ring[0][0]] *= 2  # Inconsistent profiles
   
   # Detect fraud
   scorer = PCRScorer()
   scorer.fit(features, edges)
   risk_scores = scorer.compute_all_scores()
   
   # Fraud ring members should have high scores
   print("Risk scores for fraud ring:")
   for node in [0, 5, 10, 15, 19]:
       print(f"Node {node}: {risk_scores[node]:.3f}")

Example 2: Transaction Network Analysis
----------------------------------------

Analyzing a transaction network from CSV data:

.. code-block:: python

   import pandas as pd
   from cohomological_risk_scoring import PCRScorer
   
   # Load transaction data
   df = pd.read_csv('transactions.csv')
   
   # Build adjacency and features
   entities = pd.concat([df['sender'], df['receiver']]).unique()
   entity_to_id = {e: i for i, e in enumerate(entities)}
   
   edges = [(entity_to_id[row['sender']], 
             entity_to_id[row['receiver']]) 
            for _, row in df.iterrows()]
   
   # Extract features per entity
   features = []
   for entity in entities:
       sent = df[df['sender'] == entity]['amount'].sum()
       received = df[df['receiver'] == entity]['amount'].sum()
       count = len(df[(df['sender'] == entity) | 
                      (df['receiver'] == entity)])
       features.append([sent, received, count, sent - received])
   
   features = np.array(features)
   
   # Compute risk
   scorer = PCRScorer()
   scorer.fit(features, edges)
   scores = scorer.compute_all_scores()
   classes = scorer.get_risk_classes()
   
   # Report high-risk entities
   print("High-risk entities:")
   for idx in classes['high']:
       print(f"{entities[idx]}: {scores[idx]:.3f}")

Example 3: Visualization and Reporting
---------------------------------------

.. code-block:: python

   from cohomological_risk_scoring import PCRScorer
   import matplotlib.pyplot as plt
   
   # Fit model (using data from previous examples)
   scorer = PCRScorer()
   scorer.fit(features, edges)
   
   # Visualize persistence diagram
   scorer.visualize_persistence()
   plt.savefig('persistence_diagram.png')
   
   # Generate detailed report
   report = scorer.generate_report()
   print(report)
   
   # Extract specific cohomology classes
   sheaf = scorer.sheaf
   cohomology = sheaf.compute_cohomology()
   
   print(f"Dimension of H^1: {cohomology['rank']}")
   print(f"Number of risk classes: {len(cohomology['generators'])}")

Example 4: Advanced Configuration
----------------------------------

Customizing the financial sheaf and filtration:

.. code-block:: python

   from cohomological_risk_scoring import FinancialSheaf
   import networkx as nx
   
   # Create custom graph
   G = nx.karate_club_graph()
   
   # Define custom vertex features
   features = np.array([[G.degree(n), 
                         nx.clustering(G, n), 
                         nx.betweenness_centrality(G)[n]] 
                        for n in G.nodes()])
   
   # Create sheaf with custom parameters
   sheaf = FinancialSheaf(
       vertex_features=features,
       edges=list(G.edges()),
       max_filtration=2.0
   )
   
   # Build and analyze
   sheaf.build_complex_from_graph()
   sheaf.define_sheaf_data()
   cohomology = sheaf.compute_persistent_cohomology()
   scores = sheaf.compute_pcr_score()
   
   print(f"PCR Scores: {scores}")

Example 5: Real-Time Monitoring
--------------------------------

Streaming risk assessment for incoming transactions:

.. code-block:: python

   class RiskMonitor:
       def __init__(self):
           self.scorer = PCRScorer()
           self.features = None
           self.edges = []
       
       def update(self, new_transaction):
           """Add new transaction and recompute risks"""
           sender, receiver, amount = new_transaction
           self.edges.append((sender, receiver))
           
           # Update features (simplified)
           if self.features is None:
               n = max(sender, receiver) + 1
               self.features = np.zeros((n, 4))
           
           self.features[sender][0] += amount  # total sent
           self.features[receiver][1] += amount  # total received
           
           # Refit (in production, use incremental updates)
           self.scorer.fit(self.features, self.edges)
           
           return self.scorer.compute_all_scores()
   
   # Usage
   monitor = RiskMonitor()
   for transaction in incoming_stream:
       scores = monitor.update(transaction)
       # Alert if high risk detected
       if max(scores) > threshold:
           alert_compliance_team(scores)
