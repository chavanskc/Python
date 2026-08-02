# ClaudeCoding workspace conventions

This folder hosts many independent Python projects, each built with Claude Code. These rules apply to every project created or edited anywhere under this directory.

## 1. Project naming
Each project lives in its own folder with a meaningful **PascalCase** name that describes what it does (e.g. `SimpleCalculator`). One project = one folder = one git repo.

## 2. Python environment
Always use the virtual environment at `D:\Software\Python_venv\venv_1`. Never use a system or Microsoft Store Python install.
- Interpreter: `D:\Software\Python_venv\venv_1\Scripts\python.exe`
- Package installs: `D:\Software\Python_venv\venv_1\Scripts\pip.exe`
- Every project's `.vscode/settings.json` should set `python.defaultInterpreterPath` and `code-runner.executorMap.python` to that interpreter (see `new-python-project` skill, or `Practice/.vscode/settings.json` for a working example).

## 3. Reusable library structure
Structure each project so its logic can be imported by other projects, not just run standalone:
- `<project_name>/` — an importable package (snake_case, has `__init__.py`), with small, single-responsibility modules grouped by what they do.
- `main.py` (or `cli.py`) — a thin entry point at the project root that only wires the package together (parses args, calls functions, prints results). No real logic here.

Example already in this workspace: `SimpleCalculator/operations/` holds one module per operation (`addition.py`, `subtraction.py`, ...), and `SimpleCalculator/cli.py` / `expression_evaluator.py` just call into it.

## 4. Simplicity
Write simple, readable code a developer can walk through without effort. PEP8 style. No speculative abstractions, no features beyond what's asked, no half-finished code paths.

## 5. Function documentation
Every function gets a docstring covering:
- What it does (one line)
- Parameters and return value
- A short example of how to import and call it from elsewhere, e.g.:
  ```python
  """
  Add two numbers.

  Args:
      a (float): first number
      b (float): second number
  Returns:
      float: a + b

  Example:
      from simple_calculator.operations.addition import add
      add(2, 3)  # -> 5
  """
  ```

## 6. Plan before coding
For any new project or non-trivial feature, propose a plan and get explicit approval before writing code (use Plan Mode). Skip this only for trivial, single-step changes.

## 7. Project documentation
Every project has its own `README.md`, created when the project is started and updated whenever features are added or changed. Cover: purpose, folder structure, how to run it, and how to import/reuse its functions from another project.

## 8. Version control
The whole workspace (`D:\MyWork\Python\ClaudeCoding`) is one git repository, pushed to `chavanskc/Python` on GitHub, with each project as a subfolder — not a repo per project. Work happens on the `dev-1` branch. Commit as features land.

## Tooling available in this workspace
- **Skill `new-python-project`** (`.claude/skills/new-python-project/`) — scaffolds a new project following rules 1-3, 5, 7, 8 in one step.
- **Agent `python-conventions-reviewer`** (`.claude/agents/`) — read-only check of a project against these rules; reports findings, does not edit. Apply fixes yourself only after the user approves them.
