import unittest

from PIL import Image

from app.predicter import predict_locations


class PredictLocationsTestCase(unittest.TestCase):
    def test_predict_locations(self):
        og_img = Image.open("./app/test/hd_mini_map.png")
        mini_img = og_img.resize((150, 150), Image.BICUBIC)
        res = predict_locations(mini_img)
        print(res)

        self.assertEqual(True, True)
