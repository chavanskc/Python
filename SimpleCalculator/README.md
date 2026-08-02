# SimpleCalculator

## Purpose
A command-line calculator: basic arithmetic (add/subtract/multiply/divide)
plus a small expression evaluator that understands `+ - * / ()` with
standard operator precedence (e.g. `5+3*(2-1)`).

## Structure
- `operations/` — importable library: one module per arithmetic operation
  (`addition.py`, `subtraction.py`, `multiplication.py`, `division.py`),
  re-exported from `operations/__init__.py`.
- `expression_evaluator.py` — tokenizer + recursive-descent parser that
  evaluates a math expression string using the `operations` functions.
- `cli.py` — entry point: interactive menu that calls into `operations` and
  `expression_evaluator`. No logic of its own.

## How to run
```
D:\Software\Python_venv\venv_1\Scripts\python.exe cli.py
```

## How to import & reuse
```python
from operations import add, subtract, multiply, divide
from expression_evaluator import evaluate_expression

add(2, 3)                      # -> 5
evaluate_expression("5+3*(2-1)")  # -> 8.0
```

## Features / Changelog
- 2026-08-01: initial CLI with four operations
- 2026-08-01: added expression evaluator (`+ - * / ()`, operator precedence)
- 2026-08-01: added README, `.vscode` venv_1 wiring
- 2026-08-02: reverted an accidental restructure (`cli.py` moved into a `Cli/`
  subfolder, `expression_evaluator.py` moved into `operations/`) that broke
  the `operations` import — both are back at the project root
