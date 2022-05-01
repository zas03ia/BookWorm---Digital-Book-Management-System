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

    def test_valid(self):
        self.assertEqual(self.p1.valid, {"username": True, "email": True, "password": True})
        self.assertEqual(self.p2.valid, {"username": False, "email": False, "password": False})


if __name__ == '__main__':
    unittest.main()
