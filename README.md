# DrumPy

Air drumming using body pose estimation.

## Installation

### Using python 3.11 and poetry

1. Have a working python 3.11 environment.
2. Install poetry to install the dependencies and create a virtual environment. https://python-poetry.org/

```shell
poetry install
poetry run python -m drumpy.app.main
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

Windows yet to be tested.
