# DrumPy

Air drumming using MediaPipe Pose Landmarker. 

https://github.com/Mouwrice/DrumPy/assets/56763273/36107c48-a916-4dba-ab1e-c4f9960ca7ed

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


## Usage

The application uses the body pose estimation model from mediapipe to detect the position of the hands and the face.
What you need to do is stand in front of the camera and start moving your hands as if you are playing the drums.
The application will detect your hands and play the corresponding drum sound.
At first, there is a calibration phase where the application will ask you to hit the drums in a specific order.
This is to calibrate the position of the drums in the camera view.
After the calibration phase, you can start playing the drums freely.
This calibration phase is only done once when the application is started and progress is shown in the console.
Keep this console visible to see the progress and the drum sounds that are being calibrated.

The currently enabled drum elements are: Snare Drum, High Hat Closed, Kick Drum and Cymbal.
They are calibrated in that order.

The application also has a small CLI interface that can be used to tweaks some parameters or choose a different camera.
Open a terminal in the same directory as the application to access the CLI.

```shell
cli.exe --help
```
Which will show the following help message:

```
Usage: cli.exe [OPTIONS]

Options:
  --source [camera|file]          Source of video, camera or file
  --file TEXT                     Path to video file, should be provided if
                                  source is file
  --running-mode [live_stream|blocking]
                                  Running mode for pose estimation, either
                                  dropping frames with the live stream or
                                  blocking
  --model [lite|full|heavy]       Model to use for pose estimation
  --delegate [cpu|gpu]            Delegate to use for pose estimation
  --camera-index INTEGER          Index of the camera to use
  --help                          Show this message and exit.
```
