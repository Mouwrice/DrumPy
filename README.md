# DrumPy

Air drumming using body pose estimation.

## Installation

### Download the DrumPy binary from the latest release

Find the latest release on the releases page and download the binary for your platform.
For windows, download the `DrumPy` folder with the `.exe` file inside.
After downloading, extract the folder and run the `.exe` file.

### Using python 3.11 and poetry

For local development or running the application other than the binary, the following steps can be followed:

1. Have a working python 3.11 environment.
2. Install poetry to install the dependencies and create a virtual environment. https://python-poetry.org/

It might be that poetry is not added to PATH when installing with pip. In that case execute `python -m poetry` instead
in the following commands.

```shell
poetry install --no-dev # Installs the project and dependencies in a virtual environment. Omitting the --no-dev flag will install development dependencies as well.
poetry run python -m drumpy.cli # Run the application
```

### Docker

A docker image is available on this repositories GitHub Container
Registry. https://github.com/Mouwrice/DrumPy/pkgs/container/drumpy

> [!NOTE]
> Although the docker image is available, it requires some additional steps to be able to run it properly.
> As It requires a webcam and display to be made available to the container. This seems to be especially difficult
> on Windows.

```shell
docker run ghcr.io/mouwrice/drumpy:main
```

The docker image can also be built locally using regular `docker build`.

On Arch Linux I was able to get it running using the following
steps: https://wiki.archlinux.org/title/Docker#Run_graphical_programs_inside_a_container

```shell
sudo docker run --device "/dev/video0" -e "DISPLAY=:0" --mount type=bind,src=/tmp/.X11-unix,dst=/tmp/.X11-unix --device=/dev/dri:/dev/dri  ghcr.io/mouwrice/drumpy:main
```

Your mileage may vary.


### For more insight into the project setup and development, read the [development guide](DEVELOPING.md).
