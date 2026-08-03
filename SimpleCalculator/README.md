# SimpleCalculator

## Purpose
A command-line calculator: basic arithmetic (add/subtract/multiply/divide)
plus a small expression evaluator that understands `+ - * / ()` with
standard operator precedence (e.g. `5+3*(2-1)`).

## Structure
- `math_lib/` — this project's library package. Everything math-related
  lives here; add future features as new sibling modules/subpackages.
  - `operations/` — one module per arithmetic operation (`addition.py`,
    `subtraction.py`, `multiplication.py`, `division.py`), re-exported from
    `operations/__init__.py`.
  - `expression_evaluator.py` — tokenizer + recursive-descent parser that
    evaluates a math expression string using the `operations` functions.
  - `__init__.py` — re-exports the public API (`add`, `subtract`,
    `multiply`, `divide`, `evaluate_expression`) so callers don't need to
    know the internal layout.
- `cli.py` — entry point: interactive menu that calls into `math_lib`. No
  logic of its own.

## How to run
```
D:\Software\Python_venv\venv_1\Scripts\python.exe cli.py
```

## How to import & reuse
```python
from math_lib import add, subtract, multiply, divide, evaluate_expression

add(2, 3)                      # -> 5
evaluate_expression("5+3*(2-1)")  # -> 8.0
```

## Features / Changelog
- 2026-08-01: initial CLI with four operations
- 2026-08-01: added expression evaluator (`+ - * / ()`, operator precedence)
- 2026-08-01: added README, `.vscode` venv_1 wiring
- 2026-08-02: reverted an accidental restructure (`cli.py` moved into a `Cli/`
  subfolder, `expression_evaluator.py` moved into `operations/`) that broke
  the `operations` import — both were put back at the project root
- 2026-08-02: consolidated `operations/` and `expression_evaluator.py` under
  a single `math_lib/` package (room for future math features), `cli.py`
  stays at the project root and now imports from `math_lib`
