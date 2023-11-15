import cv2
from libs.images.image_utils import brightness, extract_objects

class ImageTransformer:
    def __init__(self):
        pass

    def transform(self, image):
        img = image
        # rotate 180 degree
        img = cv2.rotate(img, cv2.ROTATE_180)

        # extract objects
        img = extract_objects(img)

        # brightness
        img = brightness(img)

        return img
