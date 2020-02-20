import unittest
from PIL import Image
from app import minimap
import os


class MinimapTestCase(unittest.TestCase):
    def test_locate_minimap(self):
        img = Image.open(f"/home/isaac/dev/league/lol-web-server/app/test/phone-map.jpg").convert("RGBA")
        res = minimap.locate_minimap(img)
        res.save(f"/home/isaac/dev/league/lol-web-server/app/test/map-find.png")
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
