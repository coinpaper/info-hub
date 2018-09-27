import unittest

import Validation.Validate as Validate


class TestValidate(unittest.TestCase):

    def test_text(self):
        """
        Test for text validation
        """
        # Valid inputs
        self.assertTrue(Validate.text("test"))
        self.assertTrue(Validate.text("Only <br> tags are fine"))
        self.assertTrue(Validate.text("Only <br/> tags are fine"))
        self.assertTrue(Validate.text("This is longer text"))
        self.assertTrue(Validate.text("!?-+ç%&/()=?"))
        self.assertTrue(Validate.text("öüäéèà"))

        # Invalid inptus
        self.assertRaises(ValueError, Validate.text, "<p>This is false</p>")
        self.assertRaises(ValueError, Validate.text, 3)
        self.assertRaises(ValueError, Validate.text, None)

    def test_number(self):
        """
        Test for type number
        """
        # Valid inputs
        self.assertTrue(Validate.number(2))
        self.assertTrue(Validate.number(5.4))

        # Invalid inptus
        self.assertRaises(ValueError, Validate.number, "2")
        self.assertRaises(ValueError, Validate.number, "5.4")

    def test_boolean(self):
        """
        Test for type boolean
        """
        # Valid inputs
        self.assertTrue(Validate.boolean(True))
        self.assertTrue(Validate.boolean(False))

        # Invalid inptus
        self.assertRaises(ValueError, Validate.boolean, "True")
        self.assertRaises(ValueError, Validate.boolean, "False")

    def test_lowercase(self):
        """
        Test for lowercase text
        """
        # Valid inputs
        self.assertTrue(Validate.lowercase("thisislowercase"))
        self.assertTrue(Validate.lowercase("this is lowercase"))
        self.assertTrue(Validate.lowercase(""))
        self.assertTrue(Validate.lowercase("this contains numbers like 1 or 2"))
        self.assertTrue(Validate.lowercase("this contains special characters!!"))

        # Invalid inptus
        self.assertRaises(ValueError, Validate.lowercase, "This is not all lowercase")
        self.assertRaises(ValueError, Validate.lowercase, "thiscontainsOneuppercase")
        self.assertRaises(ValueError, Validate.lowercase, "ALL UPPERCASE")

    def test_uppercase(self):
        """
        Test for uppercase text
        """
        # Valid inputs
        self.assertTrue(Validate.uppercase("THISISUPPERCASE"))
        self.assertTrue(Validate.uppercase("THIS IS UPPER CASE"))
        self.assertTrue(Validate.uppercase(""))
        self.assertTrue(Validate.uppercase("THIS CONTAINS NUMBERS LIKE 1 OR 2"))
        self.assertTrue(Validate.uppercase("THIS CONTAINS SPECIAL CHARACTERS!!"))

        # Invalid inptus
        self.assertRaises(ValueError, Validate.uppercase, "THIS IS not ALL UPPERCASE")
        self.assertRaises(ValueError, Validate.uppercase, "THISCONTAINSoNELOWERCASE")
        self.assertRaises(ValueError, Validate.uppercase, "all lowercase")

    def test_max(self):
        """
        Test for max value/length
        """
        # Valid inputs
        self.assertTrue(Validate.max("abc", argument=5))
        self.assertTrue(Validate.max("abc", argument=3))
        self.assertTrue(Validate.max(5, argument=10))
        self.assertTrue(Validate.max(10, argument=10))
        self.assertTrue(Validate.max(10.0, argument=10))
        self.assertTrue(Validate.max(10, argument=10.0))
        self.assertTrue(Validate.max(-100, argument=10.0))

        # Invalid inptus
        self.assertRaises(ValueError, Validate.max, "abcdef", argument=5)
        self.assertRaises(ValueError, Validate.max, "abcd", argument=3)
        self.assertRaises(ValueError, Validate.max, 15, argument=10)
        self.assertRaises(ValueError, Validate.max, 10.001, argument=10)
        self.assertRaises(ValueError, Validate.max, 0, argument=-10.0)

    def test_min(self):
        """
        Test for min value/length
        """
        # Valid inputs
        self.assertTrue(Validate.min("abcde", argument=3))
        self.assertTrue(Validate.min("abcde", argument=5))
        self.assertTrue(Validate.min(10, argument=5))
        self.assertTrue(Validate.min(10, argument=10))
        self.assertTrue(Validate.min(10.0, argument=10))
        self.assertTrue(Validate.min(10, argument=10.0))
        self.assertTrue(Validate.min(0, argument=-10.0))

        # Invalid inptus
        self.assertRaises(ValueError, Validate.min, "abcdef", argument=10)
        self.assertRaises(ValueError, Validate.min, "abcd", argument=5)
        self.assertRaises(ValueError, Validate.min, 5, argument=10)
        self.assertRaises(ValueError, Validate.min, 10, argument=10.00001)
        self.assertRaises(ValueError, Validate.min, -10, argument=0)

    def test_date(self):
        """
        Test for date text
        """
        # Valid inputs
        self.assertTrue(Validate.date("2020-01-01"))
        self.assertTrue(Validate.date("2020-1-1"))
        self.assertTrue(Validate.date("2020-12-31"))
        self.assertTrue(Validate.date("1970-02-16"))
        self.assertTrue(Validate.date("1970-2-16"))
        self.assertTrue(Validate.date("1291-09-12"))
        self.assertTrue(Validate.date("1291-9-12"))
        self.assertTrue(Validate.date("1997-11-1"))

        # Invalid inptus
        self.assertRaises(ValueError, Validate.date, "2020-11-31")
        self.assertRaises(ValueError, Validate.date, "2020-02-30")
        self.assertRaises(ValueError, Validate.date, "2020-31-31")
        self.assertRaises(ValueError, Validate.date, "1970-0-0")
        self.assertRaises(ValueError, Validate.date, "2020-31-12")

    def test_oneof(self):
        """
        Test whether value is one of selection
        """
        # Valid inputs
        self.assertTrue(Validate.oneof("a", arguments="a,b,c"))
        self.assertTrue(Validate.oneof("abc", arguments="abc,def,ghi"))

        # Invalid inptus
        self.assertRaises(ValueError, Validate.oneof, "d", arguments="a,b,c")
        self.assertRaises(ValueError, Validate.oneof, "jkl", arguments="abc,def,ghi")

    def test_url(self):
        """
        Test for correct url
        """
        # Valid inputs
        self.assertTrue(Validate.url("https://coinpaper.io"))
        self.assertTrue(Validate.url("https://polygon-software.ch/"))
        self.assertTrue(Validate.url("https://polygon-software.ch/#/team"))

        # Invalid inptus
        self.assertRaises(ValueError, Validate.url, "https://polygon-/.ch")
        self.assertRaises(ValueError, Validate.url, "https://polygon-design.ch")

    def test_foreach(self):
        """
        Test for each repetition on test inputs
        """
        # Valid inputs
        self.assertTrue(Validate.foreach([1, 2, 3], arguments=["number"]))
        self.assertTrue(Validate.foreach(["a", "b", "c"], arguments=["text"]))
        self.assertTrue(Validate.foreach([True, False, True], arguments=["boolean"]))

        # Invalid inptus
        self.assertRaises(ValueError, Validate.foreach, [1, "b", 3], arguments=["number"])
        self.assertRaises(ValueError, Validate.foreach, ["a", "b", 3], arguments=["text"])
        self.assertRaises(ValueError, Validate.foreach, [True, False, "True"], arguments=["boolean"])

    def test_startswith(self):
        """
        Test for prefix
        """
        # Valid inputs
        self.assertTrue(Validate.startswith("prefixtest", argument="prefix"))
        self.assertTrue(Validate.startswith("prefixtest", argument="p"))

        # Invalid inptus
        self.assertRaises(ValueError, Validate.startswith, "prefixtest", argument="postfix")
        self.assertRaises(ValueError, Validate.startswith, "prefixtest", argument="post")

    def test_endswith(self):
        """
        Test for postfix
        """
        # Valid inputs
        self.assertTrue(Validate.endswith("testpostfix", argument="postfix"))
        self.assertTrue(Validate.endswith("testpostfix", argument="x"))

        # Invalid inptus
        self.assertRaises(ValueError, Validate.endswith, "testpostfix", argument="prefix")
        self.assertRaises(ValueError, Validate.endswith, "testpostfix", argument="pre")

    def test_file(self):
        """
        Test for file existance
        """
        context = {
            "coin_id": "test-testing-coin"
        }
        # Valid inputs
        self.assertTrue(Validate.file("test-testing-coin_whitepaper.pdf", context=context))

        # Invalid inptus
        self.assertRaises(ValueError, Validate.file, "nonexisting-file_whitepaper.pdf", context=context)

    def test_pdf(self):
        """
        Test for pdf filetype
        """
        # Valid inputs
        self.assertTrue(Validate.pdf("test-testing-coin_whitepaper.pdf"))

        # Invalid inptus
        self.assertRaises(ValueError, Validate.pdf, "test-testing-coin_whitepaper.PDF")
        self.assertRaises(ValueError, Validate.pdf, "test-testing-coin_whitepaper.docx")

    def test_image(self):
        """
        Test for each repetition on test inputs
        """
        context = {
            "coin_id": "test-testing-coin"
        }
        # Valid inputs
        self.assertTrue(Validate.image("test-testing-coin_logo@512x512.png", context=context))
        self.assertTrue(Validate.image("gwynne-shotwell@512x512.png", context=context))

        # Invalid inptus
        self.assertRaises(ValueError, Validate.image, "invalid@128x128.png", context=context)

    def test_png(self):
        """
        Test for png filetype
        """
        # Valid inputs
        self.assertTrue(Validate.png("test-testing-coin_logo@512x512.png"))
        self.assertTrue(Validate.png("gwynne-shotwell@512x512.png"))
        self.assertTrue(Validate.png("invalid@128x128.png"))

        # Invalid inptus
        self.assertRaises(ValueError, Validate.png, "invalid@128x128.jpg")

    def test_opposite(self):
        """
        Test opposite values
        :return:
        """
        #Valid inputs
        self.assertTrue(Validate.opposite(True, context={"opposite": False}))
        self.assertTrue(Validate.opposite(False, context={"opposite": True}))

        # Invalid inputs
        self.assertRaises(ValueError, Validate.opposite, True, context={"opposite": True})
        self.assertRaises(ValueError, Validate.opposite, False, context={"opposite": False})
        self.assertRaises(ValueError, Validate.opposite, False, context={"opposite": "False"})
        self.assertRaises(ValueError, Validate.opposite, False, context={"opposite": 0})

    def test_youtube(self):
        """
        Test youtube url
        :return:
        """
        # Valid inputs
        self.assertTrue(Validate.youtube("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
        self.assertTrue(Validate.youtube("https://www.youtube.com/watch?v=P027oGJy2n4"))
        self.assertTrue(Validate.youtube("https://www.youtube.com/watch?v=kHzF_4gW78g"))
        self.assertTrue(Validate.youtube("https://www.youtube.com/watch?v=9QfpUg-UutA"))

        # Invalid inputs
        self.assertRaises(ValueError, Validate.youtube, "https://youtu.be/dQw4w9WgXcQ")
        self.assertRaises(ValueError, Validate.youtube, "https://www.youtube.com/watch?v=dQw4w9WgXcQ?t=33")
        self.assertRaises(ValueError, Validate.youtube, "https://youtu.be/dQw4w9WgXcQ?t=33")

    def test_githubuser(self):
        """
        Test github user
        :return:
        """
        # Valid inputs
        self.assertTrue(Validate.githubuser("joelbarmettlerUZH"))
        self.assertTrue(Validate.githubuser("coinpaper"))
        self.assertTrue(Validate.githubuser("polygon-software"))
        self.assertTrue(Validate.githubuser("bitcoin"))

        # Invalid inputs
        self.assertRaises(ValueError, Validate.githubuser, "coinpaper/info-hub")
        self.assertRaises(ValueError, Validate.githubuser, "")
        self.assertRaises(ValueError, Validate.githubuser, "jdfuidjkfjkddfdffjd")

    def test_githubrepo(self):
        """
        Test github repo
        :return:
        """
        # Valid inputs
        self.assertTrue(Validate.githubrepo("joelbarmettlerUZH/auto-tinder"))
        self.assertTrue(Validate.githubrepo("coinpaper/info-hub"))
        self.assertTrue(Validate.githubrepo("polygon-software/PyVisualOdometry"))
        self.assertTrue(Validate.githubrepo("bitcoin/bitcoin"))

        # Invalid inputs
        self.assertRaises(ValueError, Validate.githubrepo, "coinpaper")
        self.assertRaises(ValueError, Validate.githubrepo, "coinpaper/nonexisting-repo")
        self.assertRaises(ValueError, Validate.githubrepo, "jdfuidjkfj/kddfdffjd")

if __name__ == '__main__':
    unittest.main()
