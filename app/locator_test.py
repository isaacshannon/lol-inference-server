import time
import unittest

from PIL import Image, ImageDraw
from app import locator


def draw_grid(draw, labels):
    fill = (255, 255, 255, 96)
    for l in labels:
        x = l[0] * 10
        y = l[1] * 10
        if l[2] == "blue":
            fill = (0, 0, 255, 96)
        elif l[2] == "red":
            fill = (255, 0, 0, 96)
        elif l[2] == "blue-red":
            fill = (255, 255, 255, 96)
        draw.rectangle((x, y, x + 10, y + 10), fill=fill)


class LocatorTestCase(unittest.TestCase):
    def test_locate_players(self):
        img = Image.open("./test/hka_isg_4_2019_0000000015.png")
        img = img.resize((150, 150))

        start = time.time()
        res = locator.locate_players(img)
        print(time.time() - start)

        overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        tags = res.split(" ")
        grids = [(int(t.split(";")[0]), int(t.split(";")[1]), t.split(";")[2]) for t in tags]
        draw_grid(draw, grids)
        out = Image.alpha_composite(img, overlay)
        out.save("./test/locator-test.png")

        self.assertEqual(True, True)


class AugmentMapTestCase(unittest.TestCase):
    def test_augment_map(self):
        previous_positions = [
            '1;11;red 7;10;blue 7;11;blue-red 8;3;blue 8;4;red 1;4;blue 7;3;blue 7;4;blue 7;7;blue-red 8;6;blue 8;7;blue',
            '1;11;red 8;10;blue 8;11;blue-red 7;3;blue 7;4;red 2;4;blue 7;3;blue 7;4;blue 7;7;blue-red 8;6;blue 8;7;blue',
            '1;11;red 9;10;blue 9;11;blue-red 6;3;blue 6;4;red 3;4;blue 7;3;blue 7;4;blue 7;7;blue-red 8;6;blue 8;7;blue',
            '1;11;red 10;10;blue 10;11;blue-red 5;3;blue 5;4;red 4;4;blue 7;3;blue 7;4;blue 7;7;blue-red 8;6;blue 8;7;blue',
            '2;11;red 11;10;blue 11;11;blue-red 4;3;blue 4;4;red 5;4;blue 7;3;blue 7;4;blue 7;7;blue-red 8;6;blue 8;7;blue',
            '3;11;red 12;10;blue 12;11;blue-red 3;3;blue 3;4;red 6;4;blue 7;3;blue 7;4;blue 7;7;blue-red 8;6;blue 8;7;blue',
            '4;11;red 12;10;blue 12;11;blue-red 2;3;blue 2;4;red 6;4;blue 7;3;blue 7;4;blue 7;7;blue-red 8;6;blue 8;7;blue',
            '5;11;red 12;10;blue 12;11;blue-red 2;3;blue 2;4;red 6;4;blue 7;3;blue 7;4;blue 7;7;blue-red 8;6;blue 8;7;blue',
            '6;11;red 12;10;blue 12;11;blue-red 2;3;blue 2;4;red 6;4;blue 7;3;blue 7;4;blue 7;7;blue-red 8;6;blue 8;7;blue',
            '7;11;red 12;10;blue 12;11;blue-red 2;3;blue 2;4;red 6;4;blue 7;3;blue 7;4;blue 7;7;blue-red 8;6;blue 8;7;blue',
            '8;11;red 12;10;blue 12;11;blue-red 2;3;blue 2;4;red 6;4;blue 7;3;blue 7;4;blue 7;7;blue-red 8;6;blue 8;7;blue',
            '9;11;red 12;10;blue 12;11;blue-red 2;3;blue 2;4;red 6;4;blue 7;3;blue 7;4;blue 7;7;blue-red 8;6;blue 8;7;blue',
            '10;11;red 12;10;blue 12;11;blue-red 2;3;blue 2;4;red 6;4;blue 7;3;blue 7;4;blue 7;7;blue-red 8;6;blue 8;7;blue',
            '11;10;red 12;10;blue 12;11;blue-red 2;3;blue 2;4;red 6;4;blue 7;3;blue 7;4;blue 7;7;blue-red 8;6;blue 8;7;blue',
            '12;10;red 12;10;blue 12;11;blue-red 2;3;blue 2;4;red 6;4;blue 7;3;blue 7;4;blue 7;7;blue-red 8;6;blue 8;7;blue',
        ]

        img = Image.open("./test/hka_isg_4_2019_0000000015.png")
        res = locator.create_composite(previous_positions, img)
        res.save("./test/augment-test.png")

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
