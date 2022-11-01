import numpy as np
import cv2

def brightness(image, contrast=1.25, brightness=50):
    """Adjust the brightness of an image.

    :param image: The image to adjust.
    :returns: An image with the brightness adjusted.
    """
    frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    frame[:,:,2] = np.clip(contrast * frame[:,:,2] + brightness, 0, 255)
    frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
    return frame