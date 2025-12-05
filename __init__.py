"""
Schema Analyzer Package
A package to analyze JSON schemas and compute statistics about database structures,
document distributions, and storage sizes.
"""

from .schema_analyzer import SchemaAnalyzer
from .size_calculator import SizeCalculator
from .statistics_calculator import StatisticsCalculator

__version__ = "1.0.0"
__all__ = ["SchemaAnalyzer", "SizeCalculator", "StatisticsCalculator"]
