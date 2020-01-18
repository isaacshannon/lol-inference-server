import unittest

from PIL import Image

from app.predicter import predict_locations


class PredictLocationsTestCase(unittest.TestCase):
    def test_predict_locations(self):
        aug_img = Image.open("./test/augment-test.png")
        og_img = Image.open("./test/hd_mini_map.png")
        res = predict_locations(aug_img, og_img)
        res.save("./test/predict-test.png")

        self.assertEqual(True, True)
