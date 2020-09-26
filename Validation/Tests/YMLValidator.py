import unittest
from Validation.YMLValidator import YMLValidator


class TestValueValidator(unittest.TestCase):

    def test_validate_no_unnecessary_files(self):
        v = YMLValidator("test-testing-coin")
        self.assertRaises(ValueError, v.validate_no_unnecessary_files)

        test_images = [
            "invalid@128x128.png",
            "invalid@128x128.jpg"
        ]
        test_files = []
        v = YMLValidator("test-testing-coin")
        self.assertTrue(v.validate_no_unnecessary_files(
            test_images=test_images,
            test_files=test_files
        ))

    def test_validate_structure(self):
        v = YMLValidator("test-testing-coin")
        self.assertTrue(v.validate_structure())

    def test_validate_fields(self):
        v = YMLValidator("test-testing-coin")
        self.assertTrue(v.validate_fields())

    def test_end_2_end(self):
        v = YMLValidator("test-testing-coin")
        self.assertRaises(ValueError, v.validate)


if __name__ == "__main__":
    unittest.main()
