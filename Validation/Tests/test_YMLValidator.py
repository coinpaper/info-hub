import unittest
from Validation.YMLValidator import YMLValidator


class TestValueValidator(unittest.TestCase):

    def test_validate_no_unnecessary_files(self):
        """
        Test for no unecessary files
        """
        v = YMLValidator("test-testing-coin")
        v.validate_no_unnecessary_files()
        self.assertEquals(len(v.file_errors), 2)

        test_images = [
            "invalid@128x128.png",
            "invalid@128x128.jpg"
        ]
        test_files = []
        v = YMLValidator("test-testing-coin")
        v.validate_no_unnecessary_files(test_images=test_images, test_files=test_files)
        self.assertEquals(len(v.file_errors), 0)

    def test_validate_structure(self):
        """
        Test for minimal substructure
        """
        v = YMLValidator("test-testing-coin")
        v.validate_structure()
        self.assertEquals(len(v.structure_errors), 0)

    def test_validate_fields(self):
        """
        Test validity of all fields
        """
        v = YMLValidator("test-testing-coin")
        v.validate_fields()
        self.assertEquals(len(v.field_errors), 0)

    def test_end_2_end(self):
        """
        End-2-End test, supposed to fail since we have unecessary files
        """
        v = YMLValidator("test-testing-coin")
        self.assertRaises(ValueError, v.validate)


if __name__ == "__main__":
    unittest.main()
