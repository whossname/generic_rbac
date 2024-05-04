import unittest
import json
import re
from base64 import b64encode
from app import create_app, db

from app.scripts import seeds
from app.models import RoleUser, Role, RolePermission, Permission


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # seeds.seed()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_404(self):
        response = self.client.get('/wrong/url')
        self.assertEqual(response.status_code, 404)
        html = response.get_data(as_text=True)
        self.assertIn('<title>404 Not Found</title>', html)
        self.assertIn('<h1>Not Found</h1>', html)

    def test_redirect(self):
        # create role
        response = self.client.post(
            '/api/v1/role/create',
            headers=self.get_api_headers(),
            data=json.dumps({"name": "test-role"})
            )

        self.assertEqual(response.status_code, 308)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)
        self.assertEqual(url, 'http://localhost/api/v1/role/create/')

    def test_roles(self):
        # create role
        response = self.client.post(
            '/api/v1/role/create/',
            headers=self.get_api_headers(),
            data=json.dumps({"name": "test-role"})
            )

        self.assertEqual(response.status_code, 201)

        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['id'], 1)
        self.assertEqual(json_response['is_everyone'], False)
        self.assertEqual(json_response['is_super_admin'], False)
        self.assertEqual(json_response['name'], 'test-role')
        self.assertEqual(json_response['role_permissions'], [])
        self.assertEqual(json_response['user_ids'], [])

