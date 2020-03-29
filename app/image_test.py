import os
import unittest
from PIL import Image
from app.image import enhance_img

class EnhanceImageTestCase(unittest.TestCase):
    def test_predict_locations(self):
        print(os.listdir())
        img = Image.open("./test/iphone_se_image.png")
        img = enhance_img(img)
        img.save("./test/enhanced.png")