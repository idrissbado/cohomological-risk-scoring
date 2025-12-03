# Cohomological Risk Scoring - Quick Start Guide

**Author:** Idriss Bado

## Installation

### Quick Install

```bash
cd cohomological_risk_scoring
pip install -e .
```

### Install with Development Tools

```bash
pip install -e ".[dev]"
```

## 5-Minute Tutorial

### 1. Import the Package

```python
from cohomological_risk_scoring import PCRScorer
from cohomological_risk_scoring.utils import create_example_network
```

### 2. Create or Load Your Network

```python
# Create an example network
G, vertex_features, edge_features = create_example_network(n_vertices=30)

# vertex_features: Dict mapping vertex ID to feature vector
# edge_features: Dict mapping (u, v) to transaction amount
```

### 3. Initialize and Fit the Scorer

```python
# Initialize
scorer = PCRScorer(max_dim=2, filtration_param='weight')

# Fit to your data
scorer.fit(G, vertex_features, edge_features)
```

### 4. Compute Risk Scores

```python
# Compute PCR scores for all vertices
scores = scorer.compute_all_scores()

# Get high-risk entities
high_risk = {v: s for v, s in scores.items() if s > 0.7}
print(f"High-risk entities: {high_risk}")
```

### 5. Analyze Results

```python
# Get detailed report
print(scorer.generate_report())

# Visualize persistence diagram and scores
scorer.visualize_persistence(save_path='results.png')

# Get risk classes
risk_classes = scorer.get_risk_classes(threshold=0.1)
print(f"Found {len(risk_classes)} risk classes")
```

## Understanding the Output

### PCR Scores
- **Range:** 0.0 to 1.0 (normalized)
- **Interpretation:**
  - `> 0.7`: High risk - investigate immediately
  - `0.3 - 0.7`: Medium risk - monitor closely
  - `< 0.3`: Low risk - normal behavior

### Risk Classes (CRCs)
Each Cohomological Risk Class represents a persistent topological feature:
- **Persistence:** How long the feature exists across filtration
- **Risk Level:** Normalized risk score for the class
- **Vertices:** Entities involved in this risk pattern

## Advanced Usage

### Custom Restriction Function

```python
def custom_restriction(v_feat, e_feat):
    """Compare transaction to expected behavior."""
    income = v_feat[0]  # Assume first feature is income
    capacity = income / 12 * 0.1  # 10% monthly capacity
    return abs(e_feat - capacity) / capacity

scorer.fit(G, vertex_features, edge_features, 
           restriction_func=custom_restriction)
```

### Adjust Scoring Weights

```python
scores = scorer.compute_all_scores(
    persistence_weight=1.5,  # Emphasize persistent features
    norm_weight=0.2          # De-emphasize local inconsistency
)
```

## Running Examples

```bash
# Basic usage
cd examples
python basic_usage.py

# Advanced analysis
python advanced_analysis.py
```

## Project Structure

```
cohomological_risk_scoring/
├── src/
│   └── cohomological_risk_scoring/
│       ├── __init__.py      # Package initialization
│       ├── sheaf.py          # FinancialSheaf class
│       ├── scorer.py         # PCRScorer class
│       └── utils.py          # Utility functions
├── tests/
│   ├── test_sheaf.py        # Sheaf tests
│   └── test_scorer.py       # Scorer tests
├── examples/
│   ├── basic_usage.py       # Basic example
│   └── advanced_analysis.py # Advanced example
├── docs/                     # Documentation
├── setup.py                  # Setup script
├── requirements.txt          # Dependencies
├── README.md                 # Full documentation
├── LICENSE                   # MIT License
└── pyproject.toml           # Modern Python config
```

## Running Tests

```bash
# Run all tests
pytest tests/

# With coverage
pytest --cov=cohomological_risk_scoring tests/

# Run specific test
pytest tests/test_scorer.py -v
```

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Explore the `examples/` directory for more use cases
3. Check out the mathematical background in the documentation
4. Contribute to the project on GitHub

## Common Issues

### Import Errors
Make sure you've installed the package:
```bash
pip install -e .
```

### GUDHI Installation Issues
GUDHI requires compilation. On Windows, you may need Visual C++ build tools.

### Matplotlib Display Issues
If visualizations don't show:
```python
import matplotlib
matplotlib.use('TkAgg')  # or 'Agg' for saving only
```

## Getting Help

- **Documentation:** Check README.md and docstrings
- **Examples:** Run the example scripts
- **Issues:** Open an issue on GitHub
- **Email:** idrissbadoolivier@gmail.com

## Citation

```bibtex
@software{bado2025cohomological,
  author = {Bado, Idriss},
  title = {Cohomological Risk Scoring},
  year = {2025},
  url = {https://github.com/idrissbado/cohomological-risk-scoring}
}
```

---

**Author: Idriss Bado** | **License: MIT** | **Python: >=3.8**
