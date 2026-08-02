---
name: new-python-project
description: Scaffold a new Python project under D:\MyWork\Python\ClaudeCoding following workspace conventions (venv_1, reusable package layout, README, git). Use when the user asks to start/create a new Python project in this workspace.
user-invokable: true
---

# /new-python-project — scaffold a new project

Arguments passed: `$ARGUMENTS` (optional project name)

This performs the deterministic scaffolding described in the workspace's
`CLAUDE.md` (rules 1-3, 5, 7, 8) so a new project starts in a consistent,
reusable shape. It does **not** write any feature logic — after scaffolding,
follow rule 6 (plan the actual feature, get approval, then code it).

## Steps

1. **Get the project name.** If `$ARGUMENTS` is empty or not a clear
   PascalCase name, ask the user for one with `AskUserQuestion`. Confirm it
   describes what the project does (per CLAUDE.md rule 1). Derive:
   - `ProjectFolder` = PascalCase name, e.g. `WeatherFetcher`
   - `package_name` = snake_case version, e.g. `weather_fetcher`

2. **Check for collisions.** Confirm `D:\MyWork\Python\ClaudeCoding\<ProjectFolder>`
   does not already exist. If it does, stop and ask the user how to proceed.

3. **Create the structure:**
   ```
   <ProjectFolder>/
     <package_name>/
       __init__.py
     main.py
     README.md
     .vscode/
       settings.json
   ```

   No per-project `.gitignore` needed — the workspace-root `.gitignore`
   already excludes `__pycache__/`, `*.pyc`, and `.claude/settings.local.json`
   for every project.

   - `<package_name>/__init__.py` — empty, or a one-line module docstring
     naming the package. This is where real logic modules go later, one
     small single-responsibility module per concern (see `SimpleCalculator/operations/`
     for the pattern already used in this workspace).
   - `main.py` — a thin entry point, e.g.:
     ```python
     """Entry point for <ProjectFolder>. Wires the package together; no logic here."""
     from <package_name> import ...

     def main():
         ...

     if __name__ == "__main__":
         main()
     ```
   - `README.md` — use this skeleton, filled in:
     ```markdown
     # <ProjectFolder>

     ## Purpose
     <one paragraph — what this project does and why>

     ## Structure
     - `<package_name>/` — importable library code
     - `main.py` — entry point / CLI

     ## How to run
     D:\Software\Python_venv\venv_1\Scripts\python.exe main.py

     ## How to import & reuse
     ```python
     from <package_name>.<module> import <function>
     ```

     ## Features / Changelog
     - <date>: initial scaffold
     ```
   - `.vscode/settings.json` — copy the working pattern from
     `Practice/.vscode/settings.json`:
     ```json
     {
         "code-runner.runInTerminal": true,
         "python.defaultInterpreterPath": "D:\\Software\\Python_venv\\venv_1\\Scripts\\python.exe",
         "code-runner.executorMap": {
             "python": "D:\\Software\\Python_venv\\venv_1\\Scripts\\python.exe -u"
         }
     }
     ```

4. **Commit.** The workspace root (`D:\MyWork\Python\ClaudeCoding`) is
   already the `chavanskc/Python` git repo (branch `dev-1`) — don't `git
   init` inside the new project folder. From the workspace root:
   ```
   git add <ProjectFolder>
   git commit -m "Scaffold <ProjectFolder>"
   ```
   Ask the user before pushing (`git push`) — don't push automatically.

5. **Report next steps to the user:**
   - The scaffold and commit are done.
   - Per CLAUDE.md rule 6: now stop and plan the actual feature/logic with
     the user before writing any code into the package.
