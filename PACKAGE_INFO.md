# Package Information

## Cohomological Risk Scoring

**Version:** 0.1.0  
**Author:** Idriss Bado  
**License:** MIT  
**Python:** >= 3.8  

### Description

A sophisticated Python package for financial risk assessment using cohomological methods, persistent homology, and sheaf theory. This framework provides a mathematically rigorous approach to identifying systemic risks and anomalies in financial transaction networks.

### Core Modules

#### 1. `sheaf.py` - FinancialSheaf Class
The mathematical foundation implementing sheaf theory over simplicial complexes:
- Simplicial complex construction from graphs
- Sheaf data definition with restriction maps
- Coboundary matrix computation
- Cohomology group calculation
- Persistent cohomology tracking
- PCR score computation
- Risk class identification

**Key Methods:**
- `build_complex_from_graph()` - Construct simplicial complex
- `define_sheaf_data()` - Set up sheaf stalks and restrictions
- `compute_coboundary_matrix()` - Calculate δ^p operators
- `compute_cohomology()` - Compute H^p groups
- `compute_persistent_cohomology()` - Track features across filtration
- `compute_pcr_score()` - Calculate vertex risk score
- `get_risk_classes()` - Identify CRCs

#### 2. `scorer.py` - PCRScorer Class
The main user-facing interface for risk scoring:
- Model fitting to financial data
- Batch score computation
- Visualization generation
- Report creation
- Risk class retrieval

**Key Methods:**
- `fit()` - Fit model to transaction network
- `compute_all_scores()` - Compute all vertex scores
- `get_risk_classes()` - Get identified risk classes
- `visualize_persistence()` - Create visualizations
- `generate_report()` - Generate analysis report

#### 3. `utils.py` - Utility Functions
Helper functions for data handling and preprocessing:
- Example network creation
- Transaction data loading
- Feature normalization
- Network statistics computation

**Key Functions:**
- `create_example_network()` - Generate test networks
- `load_transaction_data()` - Load from CSV
- `normalize_features()` - Normalize feature vectors
- `compute_network_statistics()` - Network metrics

### Mathematical Concepts

#### Simplicial Complexes
Financial networks are represented as simplicial complexes where:
- **0-simplices (vertices):** Financial entities
- **1-simplices (edges):** Transactions between entities
- **2-simplices (triangles):** Cyclic transaction patterns
- **Higher simplices:** Multi-party relationships

#### Sheaf Theory
Data is organized as a sheaf F over the complex:
- **Stalks F(σ):** Feature vectors at each simplex
- **Restriction maps ρ:** Consistency conditions
- **Cocycles:** Globally consistent configurations
- **Coboundaries:** Locally derived data

#### Persistent Cohomology
Features are tracked across a filtration:
- **Birth:** When a feature appears
- **Death:** When a feature disappears
- **Persistence:** Death - Birth (lifetime)
- **Persistence Diagram:** Visual representation

#### PCR Score
The Persistence of Cohomological Risk score combines:
- **Persistence term:** Weighted by feature lifetime
- **Cocycle norm:** Local inconsistency measure
- **Final score:** Normalized to [0, 1]

### Usage Patterns

#### Basic Pattern
```python
from cohomological_risk_scoring import PCRScorer
from cohomological_risk_scoring.utils import create_example_network

# Create/load network
G, v_feat, e_feat = create_example_network()

# Initialize and fit
scorer = PCRScorer()
scorer.fit(G, v_feat, e_feat)

# Compute scores
scores = scorer.compute_all_scores()

# Analyze
print(scorer.generate_report())
scorer.visualize_persistence()
```

#### Advanced Pattern
```python
# Custom restriction function
def custom_restriction(v, e):
    return abs(v[0] - e) / v[0]  # Relative difference

# Fit with custom function
scorer.fit(G, v_feat, e_feat, restriction_func=custom_restriction)

# Adjusted scoring weights
scores = scorer.compute_all_scores(
    persistence_weight=1.5,
    norm_weight=0.2
)

# Detailed analysis
for v, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"Vertex {v}: {score:.3f}")
    # Analyze this vertex...
```

### Dependencies

**Required:**
- `numpy` - Numerical computations
- `scipy` - Sparse matrices and linear algebra
- `networkx` - Graph operations
- `gudhi` - Persistent homology
- `persim` - Persistence diagram utilities
- `matplotlib` - Visualization

**Development:**
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `black` - Code formatting
- `flake8` - Linting
- `mypy` - Type checking
- `sphinx` - Documentation generation

### File Structure

```
cohomological_risk_scoring/
├── src/cohomological_risk_scoring/
│   ├── __init__.py           # Package exports
│   ├── sheaf.py              # FinancialSheaf class
│   ├── scorer.py             # PCRScorer class
│   └── utils.py              # Utilities
├── tests/
│   ├── __init__.py           # Test setup
│   ├── test_sheaf.py         # Sheaf tests
│   └── test_scorer.py        # Scorer tests
├── examples/
│   ├── basic_usage.py        # Basic demo
│   └── advanced_analysis.py  # Advanced demo
├── docs/                     # Documentation
├── setup.py                  # Installation
├── pyproject.toml            # Modern config
├── requirements.txt          # Dependencies
├── README.md                 # Main docs
├── QUICKSTART.md             # Quick guide
├── CONTRIBUTING.md           # Contribution guide
├── CHANGELOG.md              # Version history
├── LICENSE                   # MIT license
└── .gitignore               # Git exclusions
```

### Installation Methods

**From source (editable):**
```bash
git clone https://github.com/idrissbado/cohomological-risk-scoring.git
cd cohomological-risk-scoring
pip install -e .
```

**With development tools:**
```bash
pip install -e ".[dev]"
```

**From PyPI (when published):**
```bash
pip install cohomological-risk-scoring
```

### Testing

```bash
# All tests
pytest tests/

# With coverage
pytest --cov=cohomological_risk_scoring tests/

# Specific test file
pytest tests/test_scorer.py -v
```

### Configuration

The package can be configured via:
- Constructor parameters
- Method arguments
- Custom restriction functions
- Scoring weights

See examples for detailed configuration options.

### Performance Considerations

- **Network Size:** Tested up to 1000 vertices
- **Max Dimension:** Default max_dim=2 (triangles)
- **Filtration:** Parameter choice affects computation
- **Memory:** Scales with complex size

For large networks (>1000 vertices), consider:
- Reducing max_dim
- Filtering edges by threshold
- Using sparser networks

### Known Limitations

- Currently supports undirected graphs only
- Requires edge weights for filtration
- Computational complexity increases with max_dim
- Visualization may be slow for large networks

### Future Development

See CHANGELOG.md for planned features and enhancements.

### Support

- **Documentation:** README.md and docstrings
- **Examples:** `examples/` directory
- **Issues:** GitHub issue tracker
- **Email:** idrissbadoolivier@gmail.com

### Citation

When using this package in research, please cite:

```bibtex
@software{bado2025cohomological,
  author = {Bado, Idriss},
  title = {Cohomological Risk Scoring: A Topological Approach to Financial Risk Assessment},
  year = {2025},
  version = {0.1.0},
  url = {https://github.com/idrissbado/cohomological-risk-scoring},
  license = {MIT}
}
```

### License

MIT License - see LICENSE file for details.

---

**Author:** Idriss Bado  
**Created:** December 3, 2025  
**Last Updated:** December 3, 2025  
**Version:** 0.1.0
