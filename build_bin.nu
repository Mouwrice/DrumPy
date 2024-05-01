# The nuitka command to package the application for linux
# Can only be run on linux
# Expected to be run from the root of the project

(poetry run python -m nuitka
--include-plugin-directory=.venv/lib/python3.11/site-packages/pygame_gui/data/
--include-data-files=./.venv/lib/python3.11/site-packages/pygame_gui/data/*.*=pygame_gui/data/
--include-data-files=./.venv/lib/python3.11/site-packages/pygame_gui/data/translations/*=pygame_gui/data/translations/
--include-data-files=./*.task=./
--include-data-dir=./DrumSamples=./DrumSamples
--enable-console
--enable-plugin=no-qt
--standalone ./drumpy/cli.py
)
