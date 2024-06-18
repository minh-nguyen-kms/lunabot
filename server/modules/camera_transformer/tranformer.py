import cv2
from libs.images.image_utils import brightness, extract_objects, checkGround

class ImageTransformer:
    def __init__(self):
        self.extract_objects_count = 1

    def transform(self, image):
        img = image
        # rotate 180 degree
        img = cv2.rotate(img, cv2.ROTATE_180)
        
        # # check ground
        # img = checkGround(img)

        # extract objects
        # if (self.extract_objects_count % 2 == 0):
        #     img = extract_objects(img)
        #     self.extract_objects_count = 1
        # else:
        #     self.extract_objects_count += 1

        # brightness
        # img = brightness(img)

        return img
