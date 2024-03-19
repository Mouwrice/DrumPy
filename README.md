# DrumPy

Air drumming using body pose estimation.

## Installation

### Using python 3.11 and poetry

1. Have a working python 3.11 environment.
2. Install poetry to install the dependencies and create a virtual environment. https://python-poetry.org/

It might be that poetry is not added to PATH when installing with pip. In that case execute `python -m poetry` instead
in the following commands.

```shell
poetry install --no-dev # Installs the project and dependencies in a virtual environment. Omitting the --no-dev flag will install development dependencies as well.
poetry run python -m drumpy.app.main # Run the application
```

### Docker

A docker image is available on this repositories GitHub Container
Registry. https://github.com/Mouwrice/DrumPy/pkgs/container/drumpy

```shell
docker run ghcr.io/mouwrice/drumpy:main
```

The docker image can also be built locally using regular `docker build`.

The image requires a webcam and display to be made available to the container.

On Arch Linux I was able to get it running using the following
steps: https://wiki.archlinux.org/title/Docker#Run_graphical_programs_inside_a_container

```shell
sudo docker run --device "/dev/video0" -e "DISPLAY=:0" --mount type=bind,src=/tmp/.X11-unix,dst=/tmp/.X11-unix --device=/dev/dri:/dev/dri  ghcr.io/mouwrice/drumpy:main
```

Windows yet to be tested.
