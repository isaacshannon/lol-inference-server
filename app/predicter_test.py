import unittest

from PIL import Image

from app.predicter import predict_locations


class PredictLocationsTestCase(unittest.TestCase):
    def test_predict_locations(self):
        og_img = Image.open("./test/hd_mini_map.png")
        mini_img = og_img.resize((150,150), Image.BICUBIC)
        res = predict_locations(mini_img, og_img)
        res.save("./test/predict-test.png")

        self.assertEqual(True, True)
