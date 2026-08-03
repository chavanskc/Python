"""
math_lib — this project's math library.

Holds the arithmetic building blocks (operations/) and anything built on
top of them (expression_evaluator.py today; future math features go here
as new sibling modules/subpackages). Re-exports the public API so callers
can do `from math_lib import add, evaluate_expression` without knowing
the internal layout.
"""
from .operations import add, subtract, multiply, divide
from .expression_evaluator import evaluate_expression

__all__ = ["add", "subtract", "multiply", "divide", "evaluate_expression"]
