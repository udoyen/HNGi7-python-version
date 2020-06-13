import unittest
import re
import json
from flask import render_template

from ..index import app, process_users
data = process_users()
files = data[2]


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

        assert rx.status_code == 200
        assert 'HNGi7 Team Granite' in rx.get_data(as_text=True)

    def test_check_error_files_count(self):
        global data
        data = data[1]
        with app.test_client() as c:
            rc = c.get('/')
        txt = rc.get_data(as_text=True)
        assert rc.status_code == 200
        print('Txt: {}'.format(txt))
        print('Glo_fail_count: {}'.format(data))
        self.assertTrue(re.search(r'Error.*Files.*{}'.format(data), txt, re.MULTILINE))

    def test_check_files_count(self):
        # files = data[2]
        with app.test_client() as c:
            rc = c.get('/')
        txt = rc.get_data(as_text=True)
        assert rc.status_code == 200
        self.assertTrue(re.search(fr"Total.*Files.*{len(files)}", txt, re.MULTILINE))

    def test_index_page_url_index(self):
        with app.test_client() as c:
            rv = c.get('/index')

        assert rv.status_code == 200
        assert 'HNGi7 Team Granite' in rv.get_data(as_text=True)

    def test_index_page_url_home(self):
        with app.test_client() as c:
            rc = c.get('/home')

        assert rc.status_code == 200
        assert 'HNGi7 Team Granite' in rc.get_data(as_text=True)

    def test_index_with_url_request_strings(self):
        with app.test_client() as c:
            rx = c.get('/?json')

        assert rx.status_code == 200
        assert 'file' in rx.get_data(as_text=True)
        assert 'output' in rx.get_data(as_text=True)
        assert 'email' in rx.get_data(as_text=True)
        assert 'HNGId' in rx.get_data(as_text=True)
        assert 'language' in rx.get_data(as_text=True)
        assert 'status' in rx.get_data(as_text=True)
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
