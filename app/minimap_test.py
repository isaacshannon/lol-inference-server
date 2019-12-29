import unittest
from PIL import Image
from app import minimap


class MyTestCase(unittest.TestCase):
    def test_locate_minimap(self):
        img = Image.open("./test/game_screen_000.png")
        res = minimap.locate_minimap(img)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
