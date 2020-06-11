import unittest
import json
from flask import render_template

from ..index import app


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.app = app.test_client()
        app.app_context().push()
        app.config['DEBUG'] = False
        app.config['TESTING'] = True

        # # Template testing
        # @app.route('/')
        # @app.route('/home')
        # @app.route('/index')
        # def home():
        #     return render_template('index.html')

    def tearDown(self) -> None:
        pass

    def test_index_page(self):
        with app.test_client() as c:
            rx = c.get('/')
            rc = c.get('/home')
            rv = c.get('/index')

        assert rx.status_code == 200
        assert rc.status_code == 200
        assert rv.status_code == 200
        assert 'HNGi7 Team Granite' in rx.get_data(as_text=True)
        assert 'HNGi7 Team Granite' in rc.get_data(as_text=True)
        assert 'HNGi7 Team Granite' in rv.get_data(as_text=True)

    def test_index_with_url_request_strings(self):
        with app.test_client() as c:
            rx = c.get('/?json')

        assert rx.status_code == 200
        assert rx.content_type == 'application/json'

    def test_404_error(self):
        with app.test_client() as c:
            rx = c.get('/ginger', follow_redirects=True)

        assert rx.status_code == 404
        assert '404 Page' in rx.get_data(as_text=True)

    def test_405_error(self):
        with app.test_client() as c:
            rx = c.post('/', data={'name': 'george'}, follow_redirects=True,
                        headers={"Content-Type": "application/x-www-form-urlencoded"})
        assert rx.status_code == 405
        assert '405 Page' in rx.get_data(as_text=True)


if __name__ == '__main__':
    unittest.main()
