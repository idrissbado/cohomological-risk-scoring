# Contributing to Cohomological Risk Scoring

Thank you for your interest in contributing to this project!

## Author

**Idriss Bado**

## How to Contribute

### Reporting Bugs

- Use the GitHub issue tracker
- Include Python version, OS, and error messages
- Provide a minimal reproducible example

### Suggesting Enhancements

- Open an issue with the `enhancement` label
- Describe the use case and expected behavior
- Discuss before implementing large changes

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest tests/`)
6. Format code with Black (`black src/`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use Black for formatting (line length: 100)
- Add docstrings to all public functions
- Include type hints where appropriate

### Testing

- Write tests for all new features
- Maintain test coverage above 80%
- Run tests before submitting PR

```bash
pytest tests/ --cov=cohomological_risk_scoring
```

### Documentation

- Update README.md if adding features
- Add docstrings in NumPy style
- Include examples in docstrings

## Development Setup

```bash
# Clone the repository
git clone https://github.com/idrissbado/cohomological-risk-scoring.git
cd cohomological-risk-scoring

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/
```

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow

## Questions?

Contact Idriss Bado at idrissbadoolivier@gmail.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
