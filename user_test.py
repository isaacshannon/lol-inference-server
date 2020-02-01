import unittest
from app import user


class UserTestCase(unittest.TestCase):
    def test_get_user(self):
        res = user.get_user("5")
        self.assertIsNotNone(res)

    def test_update_user(self):
        user.update_user((0, 5), (0, 5), "5")
        res = user.get_user("5")
        self.assertIs(0, res["mapX"], "User not updated")


if __name__ == '__main__':
    unittest.main()
