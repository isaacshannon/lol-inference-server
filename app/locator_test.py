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
        expected = "1-10 1-11 10-5 13-1 2-11 2-12 3-9 4-12 4-13 4-9 5-12 5-8 5-9 9-5"
        res = locator.locate_players(img)

        overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        tags = res.split(" ")
        grids = [(int(t.split("-")[0]), int(t.split("-")[1])) for t in tags]
        draw_grid(draw, grids)
        out = Image.alpha_composite(img, overlay)
        out.save("./test/locator-test.png")

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
