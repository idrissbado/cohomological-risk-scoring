# Cohomological Risk Scoring

[![PyPI version](https://img.shields.io/pypi/v/cohomological-risk-scoring.svg)](https://pypi.org/project/cohomological-risk-scoring/)
[![Python versions](https://img.shields.io/pypi/pyversions/cohomological-risk-scoring.svg)](https://pypi.org/project/cohomological-risk-scoring/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/cohomological-risk-scoring/badge/?version=latest)](https://cohomological-risk-scoring.readthedocs.io/en/latest/?badge=latest)

**Author:** Idriss Bado

A sophisticated Python package for financial risk assessment using cohomological methods, persistent homology, and sheaf theory. This framework provides a mathematically rigorous approach to identifying systemic risks and anomalies in financial transaction networks.

## Overview

This package implements the **Persistence of Cohomological Risk (PCR)** scoring methodology, which uses algebraic topology to detect structural inconsistencies in financial networks. Unlike traditional graph-based methods, this approach captures higher-order relationships and cyclic dependencies that often indicate fraudulent behavior or systemic risk.

## Key Features

- **Sheaf-Theoretic Framework**: Model financial data as sheaves over simplicial complexes
- **Persistent Cohomology**: Compute topological features across multiple scales
- **Risk Scoring**: Assign cohomological risk scores to entities based on structural inconsistencies
- **Risk Class Identification**: Automatically identify Cohomological Risk Classes (CRCs)
- **Visualization Tools**: Generate persistence diagrams and risk score distributions
- **Network Analysis**: Build and analyze financial transaction networks

## Mathematical Foundation

The package is built on three key mathematical concepts:

1. **Simplicial Complexes**: Financial networks are modeled as simplicial complexes where vertices represent entities, edges represent transactions, and higher-dimensional simplices capture multi-party relationships.

2. **Sheaf Theory**: Data is organized as a sheaf, with stalks at each simplex and restriction maps encoding consistency conditions.

3. **Persistent Cohomology**: Cohomological features are tracked across a filtration, revealing persistent structural anomalies that indicate risk.

## Installation

### From PyPI (when published)

```bash
pip install cohomological-risk-scoring
```

### From Source

```bash
git clone https://github.com/idrissbado/cohomological-risk-scoring.git
cd cohomological-risk-scoring
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
import networkx as nx
from cohomological_risk_scoring import PCRScorer
from cohomological_risk_scoring.utils import create_example_network

# Create or load your financial network
G, vertex_features, edge_features = create_example_network(n_vertices=30)

# Initialize the scorer
scorer = PCRScorer(max_dim=2, filtration_param='weight')

# Fit the model
scorer.fit(G, vertex_features, edge_features)

# Compute risk scores
scores = scorer.compute_all_scores()

# Identify high-risk entities
high_risk = {v: s for v, s in scores.items() if s > 0.7}
print(f"High-risk entities: {high_risk}")

# Get risk classes
risk_classes = scorer.get_risk_classes(threshold=0.1)

# Visualize results
scorer.visualize_persistence(save_path='persistence_diagram.png')

# Generate detailed report
print(scorer.generate_report())
```

## Core Components

### FinancialSheaf

The `FinancialSheaf` class implements the mathematical foundation:

- **Complex Construction**: Build simplicial complexes from financial graphs
- **Sheaf Data**: Define vertex and edge stalks with restriction maps
- **Cohomology Computation**: Calculate coboundary matrices and cohomology groups
- **Persistent Cohomology**: Track cohomological features across filtrations

### PCRScorer

The `PCRScorer` class provides the main interface:

- **Fit**: Build the sheaf model from financial data
- **Score Computation**: Calculate PCR scores for all entities
- **Risk Classification**: Identify Cohomological Risk Classes
- **Visualization**: Generate persistence diagrams and score distributions
- **Reporting**: Create comprehensive analysis reports

## Use Cases

- **Anti-Money Laundering (AML)**: Detect circular transaction patterns
- **Fraud Detection**: Identify inconsistent financial behavior
- **Credit Risk**: Assess systemic risk in lending networks
- **Market Manipulation**: Detect coordinated trading schemes
- **Regulatory Compliance**: Monitor for suspicious activity patterns

## Requirements

- Python >= 3.8
- NumPy >= 1.20.0
- SciPy >= 1.7.0
- NetworkX >= 2.6.0
- GUDHI >= 3.5.0
- Persim >= 0.3.0
- Matplotlib >= 3.4.0

## Documentation

Full documentation is available at [https://cohomological-risk-scoring.readthedocs.io](https://cohomological-risk-scoring.readthedocs.io)

## Examples

See the `examples/` directory for detailed usage examples:

- `basic_usage.py`: Introduction to the package
- `advanced_analysis.py`: Custom restriction functions and advanced features
- `real_world_data.py`: Working with real financial datasets

## Testing

Run the test suite:

```bash
pytest tests/
```

With coverage:

```bash
pytest --cov=cohomological_risk_scoring tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Citation

If you use this package in your research, please cite:

```bibtex
@software{bado2025cohomological,
  author = {Bado, Idriss},
  title = {Cohomological Risk Scoring: A Topological Approach to Financial Risk Assessment},
  year = {2025},
  url = {https://github.com/idrissbado/cohomological-risk-scoring}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Idriss Bado**

- GitHub: [@idrissbado](https://github.com/idrissbado)
- Email: idrissbadoolivier@gmail.com

## Acknowledgments

- The GUDHI library team for persistent homology tools
- The NetworkX community for graph analysis capabilities
- Researchers in topological data analysis and financial mathematics

## Roadmap

- [ ] Support for directed graphs
- [ ] GPU acceleration for large-scale networks
- [ ] Integration with popular fraud detection frameworks
- [ ] Real-time monitoring capabilities
- [ ] Interactive web-based visualization
- [ ] Extended documentation with tutorials
- [ ] Benchmark datasets for evaluation

## References

1. Carlsson, G. (2009). "Topology and data." Bulletin of the American Mathematical Society, 46(2), 255-308.
2. Ghrist, R. (2014). "Elementary Applied Topology." Createspace.
3. Hansen, J., & Ghrist, R. (2019). "Toward a spectral theory of cellular sheaves." Journal of Applied and Computational Topology, 3(4), 315-358.
