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

## GitHub Actions

The project uses GitHub actions to automate the release and deployment process. The workflow files are defined in the `.github/workflows` folder.

### Release Please (https://github.com/googleapis/release-please)

The [release-please-action](https://github.com/marketplace/actions/release-please-action) is used to automate the release process. It creates a pull request with the changes in the `CHANGELOG.md` file and the version bump in the `pyproject.toml` file.
Based on the commit messages, it determines the type of change and the version bump.

### Docker build and push

The `docker.yml` workflow file builds the docker image and pushes it to the GitHub Container Registry.

### Nuitka build

The `nuitka.yml` workflow file builds the application using [Nuitka](https://nuitka.net/) and uploads the binaries as an artifact.
Note that the nuitka build action installs the dependencies using pip and requires the `requirements.txt` file to be present.
This file is generated using the `poetry export` command.
```shell
poetry export -f requirements.txt --output requirements.txt --without-hashes 
```
This command is executed in the `nuitka.yml` workflow file, so it is not necessary to run it manually.
It is provided by the [Poetry Export Plugin](https://github.com/python-poetry/poetry-plugin-export).


#### Building locally

For testing and debugging purposes, it is possible to build the application locally using Nuitka.
You can find the required nuitka command in the [build_exe.nu](build_exe.nu) file. Or you can run the following command:
```shell
poetry run python -m nuitka
--include-plugin-directory=.venv/Lib/site-packages/pygame_gui/data/
--include-data-files=.venv/Lib/site-packages/pygame_gui/data/*.*=pygame_gui/data/
--include-data-files=.venv/Lib/site-packages/pygame_gui/data/translations/*=pygame_gui/data/translations/
--include-data-files=./*.task=./
--include-data-dir=./DrumSamples=./DrumSamples
--enable-console
--enable-plugin=no-qt
--standalone ./drumpy/cli.py
```
