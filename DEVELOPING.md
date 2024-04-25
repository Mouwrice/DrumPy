# Development guide

## Project structure

This python project is built using the [poetry](https://python-poetry.org/) dependency manager.
All the project dependencies are defined in the `pyproject.toml` file. The code resides in the `drumpy` folder.

Some tools are used to maintain the code quality and to automate the development process. These tools are defined in the `pyproject.toml` file as well.
These are:
- [ruff](https://docs.astral.sh/ruff/) for code formatting and linting. With optionally the ruff-lsp extension for providing integration in the editor.
- [pyright](https://github.com/microsoft/pyright) for static type checking.
- [deptry](https://deptry.com/) to check for issues with dependencies, such as unused or missing dependencies.
- [pre-commit](https://pre-commit.com/) to run the above tools before committing changes.

## Github actions

The project uses Github actions to automate the release and deployment process. The workflow files are defined in the `.github/workflows` folder.

### Release Please

