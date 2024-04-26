# The nuitka command to package the application for windows
# Can only be run on windows
# Expected to be run in the root of the project

(poetry run python -m nuitka
--include-plugin-directory=.venv/Lib/site-packages/pygame_gui/data/
--include-data-files=.venv/Lib/site-packages/pygame_gui/data/*.*=pygame_gui/data/
--include-data-files=.venv/Lib/site-packages/pygame_gui/data/translations/*=pygame_gui/data/translations/
--include-data-files=./*.task=./
--include-data-dir=./DrumSamples=./DrumSamples
--enable-console
--enable-plugin=no-qt
--standalone ./drumpy/cli.py
)
