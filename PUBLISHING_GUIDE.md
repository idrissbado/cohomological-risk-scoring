# Publishing to PyPI - Complete Guide

**Package:** cohomological-risk-scoring  
**Author:** Idriss Bado  
**Email:** idrissbadoolivier@gmail.com  

## Prerequisites

### 1. Install Build Tools

```bash
pip install --upgrade pip setuptools wheel twine build
```

### 2. Create PyPI Account

1. Go to https://pypi.org/account/register/
2. Create an account with your email: idrissbadoolivier@gmail.com
3. Verify your email address
4. Enable 2FA (Two-Factor Authentication) - **Required**

### 3. Create TestPyPI Account (for testing)

1. Go to https://test.pypi.org/account/register/
2. Create a separate account
3. Verify email and enable 2FA

### 4. Create API Tokens

#### For PyPI:
1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Name: "cohomological-risk-scoring"
4. Scope: "Entire account" (or specific to this project after first upload)
5. Copy and save the token securely

#### For TestPyPI:
1. Go to https://test.pypi.org/manage/account/token/
2. Follow same steps as above
3. Save this token separately

### 5. Configure PyPI Credentials

Create `~/.pypirc` file:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR-ACTUAL-TOKEN-HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TEST-TOKEN-HERE
```

**Security Note:** Keep this file private! Add to .gitignore if in a repo.

## Pre-Publication Checklist

### 1. Verify Package Information

- [x] Author email updated: idrissbadoolivier@gmail.com
- [x] Version number set: 0.1.0
- [x] License included: MIT
- [x] README.md is complete
- [x] All dependencies listed in setup.py
- [x] Package metadata in pyproject.toml

### 2. Run Tests

```bash
cd C:\Users\DELL\cohomological_risk_scoring
pytest tests/ -v
```

### 3. Check Code Quality

```bash
# Format code
black src/

# Check for issues
flake8 src/

# Type checking (optional)
mypy src/
```

### 4. Verify Package Structure

```bash
tree /F /A
```

Expected structure:
```
cohomological_risk_scoring/
├── src/cohomological_risk_scoring/
│   ├── __init__.py
│   ├── sheaf.py
│   ├── scorer.py
│   └── utils.py
├── tests/
├── examples/
├── setup.py
├── pyproject.toml
├── README.md
├── LICENSE
└── requirements.txt
```

### 5. Test Local Installation

```bash
# Install in development mode
pip install -e .

# Test import
python -c "from cohomological_risk_scoring import PCRScorer; print('Success!')"

# Run example
python examples/basic_usage.py
```

## Building the Package

### 1. Clean Previous Builds

```bash
# Remove old build artifacts
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue
```

### 2. Build Distribution Files

```bash
# Build source distribution and wheel
python -m build
```

This creates:
- `dist/cohomological-risk-scoring-0.1.0.tar.gz` (source distribution)
- `dist/cohomological_risk_scoring-0.1.0-py3-none-any.whl` (wheel)

### 3. Verify Build

```bash
# Check package contents
twine check dist/*
```

Should show: `PASSED` for all checks.

## Publishing to TestPyPI (Practice Run)

### 1. Upload to TestPyPI

```bash
twine upload --repository testpypi dist/*
```

Or with explicit token:
```bash
twine upload --repository testpypi dist/* --username __token__ --password pypi-YOUR-TEST-TOKEN
```

### 2. Test Installation from TestPyPI

```bash
# Create fresh virtual environment
python -m venv test_env
test_env\Scripts\activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ cohomological-risk-scoring

# Test it works
python -c "from cohomological_risk_scoring import PCRScorer; print('TestPyPI Success!')"

# Deactivate and remove test environment
deactivate
Remove-Item -Recurse -Force test_env
```

**Note:** `--extra-index-url https://pypi.org/simple/` is needed because TestPyPI doesn't have all dependencies.

## Publishing to PyPI (Official Release)

### 1. Final Pre-Upload Checks

- [ ] All tests pass
- [ ] Documentation is complete
- [ ] Version number is correct
- [ ] CHANGELOG.md is updated
- [ ] Git repository is clean (if using git)
- [ ] TestPyPI upload was successful

### 2. Upload to PyPI

```bash
twine upload dist/*
```

Or with explicit token:
```bash
twine upload dist/* --username __token__ --password pypi-YOUR-ACTUAL-TOKEN
```

### 3. Verify on PyPI

1. Visit https://pypi.org/project/cohomological-risk-scoring/
2. Check that all information displays correctly
3. Verify README renders properly
4. Check that all links work

### 4. Test Installation from PyPI

```bash
# Create fresh virtual environment
python -m venv verify_env
verify_env\Scripts\activate

# Install from PyPI
pip install cohomological-risk-scoring

# Verify installation
python -c "from cohomological_risk_scoring import PCRScorer; print('PyPI Success!')"

# Run quick test
python
>>> from cohomological_risk_scoring.utils import create_example_network
>>> G, v, e = create_example_network(10)
>>> print(f"Created network with {G.number_of_nodes()} nodes")
>>> exit()

# Deactivate
deactivate
```

## Post-Publication Steps

### 1. Create Git Tag (if using Git)

```bash
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

### 2. Create GitHub Release

1. Go to your GitHub repository
2. Click "Releases" → "Create a new release"
3. Tag: v0.1.0
4. Title: "cohomological-risk-scoring v0.1.0"
5. Description: Copy from CHANGELOG.md
6. Attach distribution files (optional)
7. Publish release

### 3. Update Documentation

- [ ] Add PyPI badge to README.md
- [ ] Update installation instructions
- [ ] Announce release (optional)

### 4. Add PyPI Badge to README

```markdown
[![PyPI version](https://badge.fury.io/py/cohomological-risk-scoring.svg)](https://badge.fury.io/py/cohomological-risk-scoring)
[![Python versions](https://img.shields.io/pypi/pyversions/cohomological-risk-scoring.svg)](https://pypi.org/project/cohomological-risk-scoring/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
```

## Publishing Updates (Future Versions)

### 1. Update Version Number

Update in all these files:
- `setup.py` → version="0.1.1"
- `pyproject.toml` → version = "0.1.1"
- `src/cohomological_risk_scoring/__init__.py` → __version__ = "0.1.1"

### 2. Update CHANGELOG.md

Add new version section with changes.

### 3. Rebuild and Upload

```bash
# Clean old builds
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue

# Build new version
python -m build

# Check
twine check dist/*

# Upload to PyPI
twine upload dist/*
```

## Troubleshooting

### Common Issues

#### 1. "File already exists"
- You cannot re-upload the same version
- Increment version number and rebuild

#### 2. "Invalid credentials"
- Check your API token
- Ensure you're using `__token__` as username
- Verify token hasn't expired

#### 3. "Package name already taken"
- Choose a different package name
- Add prefix/suffix to make it unique

#### 4. "Description rendering failed"
- Check README.md syntax
- Use `twine check dist/*` to validate
- Test locally with `python -m readme_renderer README.md`

#### 5. Dependencies not found
- Ensure all dependencies are available on PyPI
- Check spelling of package names in setup.py

### Getting Help

- PyPI Help: https://pypi.org/help/
- Packaging Guide: https://packaging.python.org/
- Email: idrissbadoolivier@gmail.com

## Quick Reference Commands

```bash
# Install build tools
pip install --upgrade pip setuptools wheel twine build

# Clean previous builds
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue

# Build package
python -m build

# Check build
twine check dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*

# Install from PyPI
pip install cohomological-risk-scoring
```

## Security Best Practices

1. **Never commit API tokens** to version control
2. **Use API tokens**, not passwords
3. **Enable 2FA** on PyPI account
4. **Scope tokens** to specific projects when possible
5. **Rotate tokens** periodically
6. **Keep .pypirc private** (chmod 600 on Unix/Linux)

## Resources

- **PyPI:** https://pypi.org/
- **TestPyPI:** https://test.pypi.org/
- **Packaging Guide:** https://packaging.python.org/
- **Twine Docs:** https://twine.readthedocs.io/
- **Build Docs:** https://build.pypa.io/

---

**Author:** Idriss Bado  
**Email:** idrissbadoolivier@gmail.com  
**Package:** cohomological-risk-scoring  
**Version:** 0.1.0  
**License:** MIT
