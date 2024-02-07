import cv2


def overlay(frame, source_fps, fps, frame_count, video_time_ms, model, width, height):
    # Visualization parameters
    row_size = 20  # pixels
    left_margin = 24  # pixels
    text_color = (0, 255, 0)  # green
    font_size = 1
    font_thickness = 1

    # Show the source FPS
    source_fps_text = "Source FPS {:.1f}".format(source_fps)
    text_location = (left_margin, row_size)
    cv2.putText(
        frame,
        source_fps_text,
        text_location,
        cv2.FONT_HERSHEY_PLAIN,
        font_size,
        text_color,
        font_thickness,
    )

    # Show the FPS
    fps_text = "FPS {:.1f}".format(fps)
    text_location = (left_margin, row_size * 2)
    cv2.putText(
        frame,
        fps_text,
        text_location,
        cv2.FONT_HERSHEY_PLAIN,
        font_size,
        text_color,
        font_thickness,
    )

    # Show the frame count
    frame_count_text = "Frame {}".format(frame_count)
    text_location = (left_margin, row_size * 3)
    cv2.putText(
        frame,
        frame_count_text,
        text_location,
        cv2.FONT_HERSHEY_PLAIN,
        font_size,
        text_color,
        font_thickness,
    )

    # Show the time
    time_text = "Time {:.1f}s".format(video_time_ms / 1000)
    text_location = (left_margin, row_size * 4)
    cv2.putText(
        frame,
        time_text,
        text_location,
        cv2.FONT_HERSHEY_PLAIN,
        font_size,
        text_color,
        font_thickness,
    )

    # Show resolution
    resolution_text = "Resolution {}x{}".format(width, height)
    text_location = (left_margin, row_size * 5)
    cv2.putText(
        frame,
        resolution_text,
        text_location,
        cv2.FONT_HERSHEY_PLAIN,
        font_size,
        text_color,
        font_thickness,
    )

    # Show mediapipe model
    model_text = "Model {}".format(model.name)
    text_location = (left_margin, row_size * 6)
    cv2.putText(
        frame,
        model_text,
        text_location,
        cv2.FONT_HERSHEY_PLAIN,
        font_size,
        text_color,
        font_thickness,
    )
