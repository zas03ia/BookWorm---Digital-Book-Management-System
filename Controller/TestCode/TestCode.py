import unittest
import application as a


class TestPerson(unittest.TestCase):


    def setUp(self):
        self.p1 = a.Person()
        self.p1.username = "zas344"
        self.p1.email = "zasia.zafreen@g.bracu.ac.bd"
        self.p1.password = "zasia#123"
        self.p2 = a.Person()
        self.p2.username = "wizard"
        self.p2.email = "zasia.zafreen@gmail.com"
        self.p2.password = "wizard#123"


    def tearDown(self):

        key_id = a.data("select", "person", "id", None, ["username", self.p2.username])[0][0]
        a.data("delete", "custom", "*", None, ["id", key_id])
        a.data("delete", "person", "*", None, ["username", self.p2.username])


    def test_valid(self):

        self.assertEqual(self.p1.valid, {"username": True, "email": True, "password": True})
        self.assertEqual(self.p2.valid, {"username": False, "email": False, "password": False})

    def test_verify(self):
        self.assertEqual(self.p2.verify, True)
        self.p2.password = "abc"
        self.assertEqual(self.p2.verify, False)

    def test_login(self):
        self.assertEqual(self.p1.login, True)
        self.assertEqual(self.p2.login, False)

    def test_create_account(self):

        self.assertEqual(self.p1.create_account, [False, "Invalid Username"])
        self.p2.email="zasia.zafreen@g.bracu.ac.bd"
        self.assertEqual(self.p2.create_account, [False, "Account already exists with this email address"])
        self.p2.email="zasia.zafreen@gmail.com"
        self.assertEqual(self.p2.create_account, [True])


    def test_reset(self, start, res_code, return_code):
        pass
        ### this part is related to the frontend



###########################################################################################
class BookTest(unittest.TestCase):

    @classmethod
    def Testinfo(cls, user = None):
        pass
        ### this part is related to flask session

    @classmethod
    def Testset_progress(cls, p):
        pass
        ### this part is related to flask session

    def Testopen(self):
        pass
        ### this part is related to flask session

    def Testprogress(self):
        pass
        ### this part is related to flask session

    @classmethod
    def Testmean(cls, q= None):
        pass
        ### this part is related to flask session

class ShelfTest(unittest.TestCase):

    @classmethod
    def Testshow(cls):
        pass
        ### this part is related to flask session

    @classmethod
    def Testadd_book(cls, b_id):
        pass
        ### this part is related to flask session

    @classmethod
    def Testrm_book(cls, b_id):
        pass
        ### this part is related to flask session



class CustomTest(unittest.TestCase):

    @classmethod
    def Testshow(cls):
        pass
        ### this part is related to flask session

    @classmethod
    def Testset_font_size(cls, size):
        pass
        ### this part is related to flask session

    @classmethod
    def Testset_page_color(cls, p_color):
        pass
        ### this part is related to flask session

    @classmethod
    def Testset_text_color(cls, t_color):
        pass
        ### this part is related to flask session


if __name__ == '__main__':
    unittest.main()