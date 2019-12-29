import unittest
import cv2
import numpy as np
import os
from PIL import Image


class TestMaskFind(unittest.TestCase):
    image = cv2.imread("./test/map2.jpg")
    edges = cv2.Canny(image, 50, 200)
    template = cv2.imread("./test/map-template.jpg")
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(edges, template, cv2.TM_CCOEFF)
    y, x = np.unravel_index(result.argmax(), result.shape)

    img = Image.open("./test/map2.jpg")
    size_x, size_y = img.size
    print(img.size)
    img = img.crop((x-75, y-75, x+220, y+220))
    img.save("./test/cropped.jpg")


# class TestCrop(unittest.TestCase):
#     img = Image.open("./test/mini-map.png")
#     img = img.resize((150,150), Image.ANTIALIAS)
#     img.save("./test/cropped.png")



if __name__ == '__main__':
    unittest.main()
