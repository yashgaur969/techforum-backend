import unittest

from app import create_app, db, app


class CustomerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = app.test_client(self)

        with app.app_context():
            db.create_all()

    def test_get(self):
        response = self.client.get('/user/posts/shubham', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_get_data(self):
        response = self.client.get('/info/shubham@gmail.com', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_post(self):
        sudo_data = {'email_id': 'shubham@gmail.com', 'password': 'qwerty123'}
        res = self.client.post('/users/login', json=sudo_data, content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def tearDown(self):
        """teardown all initialized variables."""
        with app.app_context():
            db.session.remove()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
