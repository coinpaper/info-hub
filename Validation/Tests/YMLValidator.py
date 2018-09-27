import unittest
from Validation.YMLValidator import YMLValidator


class TestValueValidator(unittest.TestCase):

    def test_end_2_end(self):
        v = YMLValidator("test-testing-coin")
        self.assertTrue(v.validate())


if __name__ == "__main__":
    unittest.main()
