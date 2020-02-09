import unittest
from PIL import Image
from app import minimap
import os


class MinimapTestCase(unittest.TestCase):
    def test_locate_minimap(self):
        # images = os.listdir("/home/isaac/dev/league/lol-web-server/app/test/full_map")
        images = ["league-voice-coms.jpg"]
        for im in images:
            img = Image.open(f"./app/test/full_map/{im}")
            res, x, y = minimap.locate_minimap(img)
            res.save(f"/home/isaac/dev/league/lol-web-server/app/test/full_result/{im}")
            self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
