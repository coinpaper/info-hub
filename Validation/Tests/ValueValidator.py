import unittest

from Validation.ValueValidator import ValueValidator

context = {
    "coin_id": "test-testing-coin"
}

TEXT_100 = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut l"
TEXT_600 = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ip"


class TestValueValidator(unittest.TestCase):

    def test_id(self):
        """
        Tests the YMLs ID property
        :return:
        """
        # Valid input
        validation = "text|max(50)|lowercase"
        validator = ValueValidator("test-testing-coin", validation, context)
        self.assertTrue(validator.validate())

        # Invalid input
        validator = ValueValidator("TEST-testing-coin", validation, context)
        self.assertRaises(ValueError, validator.validate)

    def test_symbol(self):
        """
        Tests the YMLs symbol property
        :return:
        """
        # Valid input
        validation = "text|max(10)|uppercase"
        validator = ValueValidator("TEST", validation, context)
        self.assertTrue(validator.validate())

        # Invalid input
        validator = ValueValidator("test", validation, context)
        self.assertRaises(ValueError, validator.validate)

    def test_name(self):
        """
        Tests the YMLs name property
        :return:
        """
        # Valid input
        validation = "text|max(50)"
        validator = ValueValidator("Testing Coin", validation, context)
        self.assertTrue(validator.validate())

        # Invalid input
        validator = ValueValidator(TEXT_100, validation, context)
        self.assertRaises(ValueError, validator.validate)

    def test_logo(self):
        """
        Tests the YMLs name property
        :return:
        """
        # Valid input
        validation = "image|png"
        validator = ValueValidator("test-testing-coin_logo@512x512.png", validation, context)
        self.assertTrue(validator.validate())

        # Invalid input
        validator = ValueValidator("invalid@128x128.png", validation, context)
        self.assertRaises(ValueError, validator.validate)

    def test_founded(self):
        """
        Tests the YMLs name property
        :return:
        """
        # Valid input
        validation = "date"
        validator = ValueValidator("1997-11-01", validation, context)
        self.assertTrue(validator.validate())

        # Invalid input
        validator = ValueValidator("01-11-1997", validation, context)
        self.assertRaises(ValueError, validator.validate)


if __name__ == '__main__':
    unittest.main()
