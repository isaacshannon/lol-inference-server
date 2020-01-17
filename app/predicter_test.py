import unittest

from PIL import Image

from app.predicter import predict_locations


class PredictLocationsTestCase(unittest.TestCase):
    def test_predict_locations(self):
        img = Image.open("./test/hka_isg_4_2019_0000000015.png")
        res = predict_locations(img)
        res.save("./test/predict-test.png")

        self.assertEqual(True, True)
