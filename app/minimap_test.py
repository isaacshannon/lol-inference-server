import unittest
from PIL import Image
from app import minimap


class MinimapTestCase(unittest.TestCase):
    def test_locate_minimap(self):
        img = Image.open("./app/test/last-img.png")
        res, x, y = minimap.locate_minimap(img)
        res.save("/home/isaac/dev/league/lol-web-server/app/test/minimap_test.png")
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
