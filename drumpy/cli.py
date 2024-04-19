import click
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import RunningMode

from drumpy.app.main import App
from drumpy.app.video_source import Source
from drumpy.mediapipe_pose.landmarker_model import LandmarkerModel


def parse_running_mode(mode: str) -> RunningMode:
    match mode.lower():
        case "live_stream":
            return RunningMode.LIVE_STREAM
        case "blocking":
            return RunningMode.VIDEO
        case _:
            raise ValueError(f"Invalid running mode: {mode}")


def parse_model(model: str) -> LandmarkerModel:
    match model.lower():
        case "lite":
            return LandmarkerModel.LITE
        case "full":
            return LandmarkerModel.FULL
        case "heavy":
            return LandmarkerModel.HEAVY
        case _:
            raise ValueError(f"Invalid model: {model}")


def parse_delegate(delegate: str) -> BaseOptions.Delegate:
    match delegate.lower():
        case "cpu":
            return BaseOptions.Delegate.CPU
        case "gpu":
            return BaseOptions.Delegate.GPU
        case _:
            raise ValueError(f"Invalid delegate: {delegate}")


@click.command()
@click.option(
    "--source",
    type=click.Choice(["camera", "file"], case_sensitive=False),
    default="camera",
    help="Source of video, camera or file",
)
@click.option(
    "--file", type=str, help="Path to video file, should be provided if source is file"
)
@click.option(
    "--running-mode",
    type=click.Choice(["live_stream", "blocking"], case_sensitive=False),
    default="live_stream",
    help="Running mode for pose estimation, either dropping frames with the live stream or blocking",
)
@click.option(
    "--model",
    type=click.Choice(["lite", "full", "heavy"], case_sensitive=False),
    default="full",
    help="Model to use for pose estimation",
)
@click.option(
    "--delegate",
    type=click.Choice(["cpu", "gpu"], case_sensitive=False),
    default="cpu",
    help="Delegate to use for pose estimation",
)
@click.option("--camera-index", type=int, default=0, help="Index of the camera to use")
def cli(
    source: str,
    file: str | None,
    running_mode: str,
    model: str,
    delegate: str,
    camera_index: int,
):
    print("Starting Drumpy...")

    print(f"Using source: {source}")
    source = Source.from_str(source)

    if source == Source.FILE:
        assert file is not None, "File path must be provided, use --file option"
        print(f"Using file: {file}")

    print(f"Using running mode: {running_mode}")
    running_mode = parse_running_mode(running_mode)

    print(f"Using model: {model}")
    model = parse_model(model)

    print(f"Using delegate: {delegate}")
    delegate = parse_delegate(delegate)

    print(f"Using camera index: {camera_index}")

    app = App(
        source=source,
        file_path=file,
        running_mode=running_mode,
        model=model,
        delegate=delegate,
        camera_index=camera_index,
    )
    app.start()


if __name__ == "__main__":
    cli()
