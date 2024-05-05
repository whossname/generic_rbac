import unittest
import json
from app import create_app, db

from app.models import Permission


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
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
        response = self.client.post(
            '/api/v1/role/create',
            headers=self.get_api_headers(),
            data=json.dumps({"name": "test-role"})
            )

        self.assertEqual(response.status_code, 308)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)
        self.assertEqual(url, 'http://localhost/api/v1/role/create/')


    def create_role(self):
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

    def add_permission(self, write_access):
        response = self.client.post(
            '/api/v1/role/add-permission/',
            headers=self.get_api_headers(),
            data=json.dumps({"role_id": 1, "permission_id": 1, "write_access": write_access})
            )

        self.assertEqual(response.status_code, 201)

        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['permission_id'], 1)
        self.assertEqual(json_response['role_id'], 1)
        self.assertEqual(json_response['write_access'], write_access)

    def add_user(self):
        response = self.client.post(
            '/api/v1/role/add-user/',
            headers=self.get_api_headers(),
            data=json.dumps({"role_id": 1, "user_id": "test-user"})
            )

        self.assertEqual(response.status_code, 201)

        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['user_id'], 'test-user')
        self.assertEqual(json_response['role_id'], 1)

    def fetch_all(self, write_access, has_user_and_permission):
        response = self.client.get(
            '/api/v1/rbac/fetch-all/',
            headers=self.get_api_headers()
            )

        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['permissions'], [{'id': 1, 'name': 'rbac'}])
        role = json_response['roles'][0]

        user_ids = []
        role_permissions = []

        if has_user_and_permission:
            user_ids = ['test-user']
            role_permissions = [{'permission_id': 1, 'write_access': write_access}]

        expected_role = {
            'id': 1,
            'is_everyone': False,
            'is_super_admin': False,
            'name': 'test-role',
            'role_permissions': role_permissions,
            'user_ids': user_ids
            }

        self.assertEqual(role, expected_role)

    def fetch_all_no_roles(self):
        response = self.client.get(
            '/api/v1/rbac/fetch-all/',
            headers=self.get_api_headers()
            )

        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['permissions'], [{'id': 1, 'name': 'rbac'}])
        self.assertEqual(json_response['roles'], [])

    def has_permission(self, write_access):
        response = self.client.get(
            '/api/v1/user/has_permission/',
            headers=self.get_api_headers(),
            data=json.dumps(
                {"user_id": "test-user", "permission": "rbac", "require_write_access": True}
                )
            )

        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['has_permission'], write_access)

    def remove_permission(self):
        response = self.client.delete(
            '/api/v1/role/remove-permission/',
            headers=self.get_api_headers(),
            data=json.dumps({"role_id": 1, "permission_id": 1})
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), 'Success')

    def remove_user(self):
        response = self.client.delete(
            '/api/v1/role/remove-user/',
            headers=self.get_api_headers(),
            data=json.dumps({"role_id": 1, "user_id": 1})
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), 'Success')

    def delete_role(self):
        response = self.client.delete(
            '/api/v1/role/delete/',
            headers=self.get_api_headers(),
            data=json.dumps({"role_id": 1})
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), 'Success')

    def test_roles(self):
        # setup
        rbac_permission = Permission(name='rbac')
        db.session.add(rbac_permission)
        db.session.commit()

        write_access = False

        # create
        self.create_role()
        self.add_permission(write_access)
        self.add_user()

        # read
        has_user_and_permission= True
        self.fetch_all(write_access, has_user_and_permission)
        self.has_permission(write_access)

        # change permission write_access
        write_access = True
        self.add_permission(write_access)
        self.has_permission(write_access)

        # delete
        self.remove_permission()
        self.remove_user()
        has_user_and_permission = False
        self.fetch_all(write_access, has_user_and_permission)
        self.delete_role()
        self.fetch_all_no_roles()
