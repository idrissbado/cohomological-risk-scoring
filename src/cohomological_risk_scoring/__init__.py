"""
Cohomological Risk Scoring Package
===================================

A sophisticated Python package for financial risk assessment using cohomological 
methods, persistent homology, and sheaf theory.

Author: Idriss Bado
"""

from .sheaf import FinancialSheaf
from .scorer import PCRScorer

__version__ = "0.1.0"
__author__ = "Idriss Bado"
__email__ = "idrissbadoolivier@gmail.com"

__all__ = [
    "FinancialSheaf",
    "PCRScorer",
]
