"""Setup configuration for cohomological-risk-scoring package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
try:
    long_description = (this_directory / "README.md").read_text(encoding='utf-8')
except FileNotFoundError:
    long_description = "A cohomological approach to financial risk scoring using persistent homology and sheaf theory"

setup(
    name="cohomological-risk-scoring",
    version="0.1.0",
    author="Idriss Bado",
    author_email="idrissbadoolivier@gmail.com",
    description="A cohomological approach to financial risk scoring using persistent homology and sheaf theory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idrissbado/cohomological-risk-scoring",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "networkx>=2.6.0",
        "gudhi>=3.5.0",
        "persim>=0.3.0",
        "matplotlib>=3.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "sphinx>=4.5.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    keywords="topology, persistent-homology, sheaf-theory, risk-scoring, financial-analysis, cohomology",
    project_urls={
        "Bug Reports": "https://github.com/idrissbado/cohomological-risk-scoring/issues",
        "Source": "https://github.com/idrissbado/cohomological-risk-scoring",
        "Documentation": "https://cohomological-risk-scoring.readthedocs.io",
        "Research Paper": "https://www.researchgate.net/publication/398275656_Cohomological_Risk_Scoring_A_Topological_Framework_for_Detecting_Structural_Inconsistencies_in_Financial_Networks",
    },
)
