"""
Camera Diagnostics & Multi-Backend Initialization Utility
Author: Jean Roy Lastimosa

Probes available OpenCV video capture backends (DirectShow, Media Foundation, V4L2)
to ensure reliable camera initialization across Windows and Linux environments,
and renders a verification frame using Matplotlib.
"""

import cv2
from matplotlib import pyplot as plt


def show_image(img):
    """Display a BGR OpenCV frame in RGB format using Matplotlib."""
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.show()


def initialize_camera(index=0):
    """
    Attempt to open the specified camera index across multiple video backends.

    Args:
        index (int): Hardware camera index (default: 0).

    Returns:
        cv2.VideoCapture: Initialized video capture object.

    Raises:
        ValueError: If the camera cannot be opened with any supported backend.
    """
    backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_V4L2]
    for backend in backends:
        cap = cv2.VideoCapture(index, backend)
        if cap.isOpened():
            print(f"Camera {index} opened successfully with backend: {backend}")
            return cap
    raise ValueError(f"Failed to open camera {index} with any backend")


if __name__ == "__main__":
    try:
        cap = initialize_camera(0)
        ret, frame = cap.read()
        if ret:
            show_image(frame)
        else:
            print("Failed to read frame from camera.")
        cap.release()
    except Exception as e:
        print(f"Camera initialization error: {e}")
