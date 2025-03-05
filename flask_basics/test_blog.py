import unittest
from app import app

class TestBlogBlueprint(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        response = self.app.get('/blog')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Blog', response.data)

    def test_about(self):
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'XXXXXX', response.data)

if __name__ == '__main__':
    unittest.main()
