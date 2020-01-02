import time
import unittest

from PIL import Image, ImageDraw
from app import locator


def draw_grid(draw, labels):
    fill = (0, 255, 255, 96)
    for l in labels:
        x = l[0] * 10
        y = l[1] * 10
        draw.rectangle((x, y, x + 10, y + 10), fill=fill)


class LocatorTestCase(unittest.TestCase):
    def test_locate_players(self):
        img = Image.open("./test/dwg_lk_4_worlds_2019_0000000939.png")

        start = time.time()
        res = locator.locate_players(img)
        print(time.time() - start)

        overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        tags = res.split(" ")
        grids = [(int(t.split("-")[0]), int(t.split("-")[1])) for t in tags]
        draw_grid(draw, grids)
        out = Image.alpha_composite(img, overlay)
        out.save("./test/locator-test.png")

        self.assertEqual(True, True)


class AugmentMapTestCase(unittest.TestCase):
    def test_augment_map(self):
        previous_positions = ["10-9 12-10 12-11 3-2 3-3 6-7 7-6 7-7 8-5 8-6 9-4",
                              "11-11 11-12 12-10 12-11 12-12 2-3 3-2 3-3 7-5 7-6 7-7 8-5 8-6 8-7",
                              "10-9 11-11 12-10 12-11 2-2 2-3 3-1 3-2 3-3 8-4 8-6 8-7",
                              "11-12 12-10 12-11 12-12 2-2 2-3 3-2 3-3 8-4 8-5 8-7",
                              "11-11 12-10 12-11 2-2 2-3 6-4 7-4 7-7 8-6 8-7",
                              "12-11 12-12 2-3 3-3 3-4 7-4 8-7 8-8 12-11 12-12 3-3 7-4 8-7",
                              "12-10 12-11 12-12 2-3 2-4 3-3 3-4 7-4 7-7 8-7",
                              "12-10 12-11 2-2 2-3 3-3 6-7 7-3 7-4 7-6 7-7 8-6",
                              "1-3 11-11 11-12 12-10 12-11 12-12 2-3 2-4 6-4 7-4 7-6 7-7 8-6",
                              "1-2 1-3 11-10 11-11 12-10 12-11 2-2 2-3 6-3 6-4 6-7 7-3 7-6 7-7",
                              "12-10 12-11 12-12 2-3 2-4 6-4 7-3 7-4 7-6 7-7 8-6 8-7",
                              "11-10 11-11 12-10 12-11 2-3 2-4 6-3 7-3 7-4 7-6 7-7 8-6",
                              "1-3 1-4 11-10 11-11 11-12 12-10 12-11 2-3 2-4 6-4 6-7 7-7",
                              "1-3 1-4 11-11 12-10 12-11 2-3 2-4 6-3 6-4 6-7 7-6 7-7",
                              "11-11 12-10 12-11 2-3 2-4 6-3 6-4 7-3 7-4 7-7 8-6 8-7"]

        img = Image.open("./test/hka_isg_4_2019_0000000015.png")
        res = locator.create_composite(previous_positions, img)
        res.save("./test/augment-test.png")

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
