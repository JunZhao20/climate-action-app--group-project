import unittest
from flask_testing import TestCase
from models import db, Forum
from app import app, load_user
from models import User
import mock


class BaseTestCase(TestCase):
    ''' Base test'''

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(Forum(user_id=1, title='Test', body='This is a test'))
        db.session.add(User(email='Jerry@email.com',
                            password='Password',
                            pin_key='BFB5S34STBLZCOB22K6PPYDCMZMH46OJ',
                            firstname='Jerry',
                            lastname='Jones',
                            phone='0191-123-4567',
                            role='user'))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()




class TestForum(BaseTestCase):
    def test_forum(self):
        with self.client:
            self.client.post('/login', data=dict(email='Jerry@email.com', password='Password', pin='000000'))
            response = self.client.get('/forum', follow_redirects=True)
            self.assertIn(b'This is a test', response.data)

    """def test_delete_forum(self):
        with self.client:
            response = self.client.post(/)"""



class TestCreateForum(BaseTestCase):
    @mock.patch('flask_login.utils._get_user')
    def test_create_forum(self, current_user):
        user = User.query.get(1)
        current_user.return_value = user
        with self.client:
            self.client.post('/login', data=dict(email='Jerry@email.com', password='Password', pin='000000'))
            self.client.get('/forum', follow_redirects=True)
            response = self.client.post('/create', data=dict(title='Create post', body='Forum created'),
                                        follow_redirects=True)
            self.assertIn(b"Forum created", response.data)

