import unittest
from PIL import Image
from app import minimap
import os


class MinimapTestCase(unittest.TestCase):
    def test_locate_minimap(self):
        images = os.listdir("/home/isaac/dev/league/lol-web-server/app/test/full_map")
        # images = ["league-voice-coms.jpg"]
        # images = ["2.png"]
        # images = ["4.png"]
        images = ["cam-000.JPG"]
        for im in images:
            img = Image.open(f"./app/test/full_map/{im}").convert("RGBA")
            img = img.resize((img.size[0]//8, img.size[1]//8), Image.BICUBIC)
            img.save(f"./app/test/full_result/shrunk.png")
            res, x, y = minimap.locate_minimap(img)
            im = im.split(".")[0]
            res.save(f"/home/isaac/dev/league/lol-web-server/app/test/full_result/{im}.png")
            self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
