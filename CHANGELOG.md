# Changelog

All notable changes to the Cohomological Risk Scoring package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-12-03

### Added
- Initial release of cohomological-risk-scoring package
- `FinancialSheaf` class for sheaf-theoretic modeling of financial networks
- `PCRScorer` class for computing Persistence of Cohomological Risk scores
- Simplicial complex construction from financial transaction graphs
- Persistent cohomology computation using GUDHI
- PCR score computation for individual vertices
- Cohomological Risk Class (CRC) identification
- Visualization tools for persistence diagrams and risk scores
- Comprehensive report generation
- Utility functions for creating example networks
- Support for custom restriction functions
- Basic test suite with pytest
- Documentation and examples
- MIT License

### Features
- Build simplicial complexes from graphs via clique expansion
- Define sheaf data with vertex and edge stalks
- Compute coboundary matrices and cohomology groups
- Track persistent features across filtrations
- Identify high-risk entities and risk classes
- Visualize results with matplotlib
- Generate detailed analysis reports

### Documentation
- Comprehensive README with mathematical background
- Quick start guide (QUICKSTART.md)
- Contributing guidelines (CONTRIBUTING.md)
- API documentation in docstrings
- Two example scripts demonstrating usage
- MIT License file

### Testing
- Unit tests for FinancialSheaf class
- Unit tests for PCRScorer class
- Test fixtures for common scenarios
- pytest configuration

### Infrastructure
- Python package structure following best practices
- setup.py and pyproject.toml for installation
- requirements.txt for dependencies
- .gitignore for version control
- MANIFEST.in for package distribution
- setup.cfg for tool configurations

### Dependencies
- numpy >= 1.20.0
- scipy >= 1.7.0
- networkx >= 2.6.0
- gudhi >= 3.5.0
- persim >= 0.3.0
- matplotlib >= 3.4.0

### Author
- Idriss Bado - Initial work and package development

## [Unreleased]

### Planned Features
- [ ] Support for directed graphs
- [ ] GPU acceleration for large-scale networks
- [ ] Integration with fraud detection frameworks
- [ ] Real-time monitoring capabilities
- [ ] Interactive web-based visualization
- [ ] Extended documentation with tutorials
- [ ] Benchmark datasets
- [ ] Additional test coverage
- [ ] Performance optimizations
- [ ] CLI interface
- [ ] Docker container support
- [ ] Cloud deployment guides

### Potential Enhancements
- [ ] Multi-dimensional persistence
- [ ] Zigzag persistence
- [ ] Time-series analysis
- [ ] Anomaly detection algorithms
- [ ] Risk prediction models
- [ ] Export to various formats (JSON, CSV, etc.)
- [ ] Database integration
- [ ] API endpoints for web services

---

**Format:** [Version] - YYYY-MM-DD
**Author:** Idriss Bado
**License:** MIT
