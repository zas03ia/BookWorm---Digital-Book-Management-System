import unittest
from flask import Flask
from application import app

class appTest(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        try:
            response = tester.get('/')
            self.assertEqual(response.status_code, 200)
        except:
            response = tester.post('/')
            self.assertEqual(response.status_code, 200)

    def test_login(self):
        tester = app.test_client(self)
        try:
            response = tester.get('/login')
            self.assertEqual(response.status_code, 200)
        except:
            response = tester.post('/login')
            self.assertEqual(response.status_code, 200)

    def test_create(self):
        tester = app.test_client(self)
        try:
            response = tester.get('/create')
            self.assertEqual(response.status_code, 200)
        except:
            response = tester.post('/create')
            self.assertEqual(response.status_code, 200)

    def test_reset(self):
        tester = app.test_client(self)
        try:
            response = tester.get('/reset')
            self.assertEqual(response.status_code, 200)
        except:
            response = tester.post('/reset')
            self.assertEqual(response.status_code, 200)

    def test_read(self):
        tester = app.test_client(self)
        try:
            response = tester.get('/book')
            self.assertEqual(response.status_code, 200)
        except:
            response = tester.post('/book', data = {"book_id": 1})
            self.assertEqual(response.status_code, 200)

    def test_logout(self):
        tester = app.test_client(self)
        try:
            response = tester.get('/logout')
            self.assertEqual(response.status_code, 302)
        except:
            response = tester.post('/logout')
            self.assertEquals(response.status_code, 302)

    def test_close(self):
        tester = app.test_client(self)
        try:
            response = tester.get('/close')
            self.assertEqual(response.status_code, 405)
        except:
            response = tester.post('/close')
            self.assertEqual(response.status_code, 302)

    def test_myshelf(self):
        tester = app.test_client(self)
        try:
            response = tester.get('/myshelf')
            self.assertEqual(response.status_code, 302)
        except:
            response = tester.post('/myshelf')
            self.assertEqual(response.status_code, 302)

    def test_custom(self):
        tester = app.test_client(self)
        try:
            response = tester.get('/custom')
            self.assertEqual(response.status_code, 405)
        except:
            response = tester.post('/custom')
            self.assertEqual(response.status_code, 302)

    def test_add(self):
        tester = app.test_client(self)
        try:
            response = tester.get('/add')
            self.assertEqual(response.status_code, 405)
        except:
            response = tester.post('/add')
            self.assertEqual(response.status_code, 302)

    def test_remove(self):
        tester = app.test_client(self)
        try:
            response = tester.get('/remove')
            self.assertEqual(response.status_code, 405)
        except:
            response = tester.post('/remove')
            self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main()