import unittest
from app import create_app
from app.config import TestingConfig
import psycopg2

class TaskManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.conn = psycopg2.connect(
            dbname=TestingConfig.DB_NAME,
            user=TestingConfig.DB_USER,
            password=TestingConfig.DB_PASSWORD,
            host=TestingConfig.DB_HOST,
            port=TestingConfig.DB_PORT
        )
        self.cursor = self.conn.cursor()
        self._reset_db()

        self.app = create_app(TestingConfig, test_conn=self.conn, test_cursor=self.cursor)
        self.client = self.app.test_client()

    def tearDown(self):
        self.cursor.close()
        self.conn.close()

    def _reset_db(self):
        self.cursor.execute("DROP TABLE IF EXISTS tasks, users CASCADE;")
        self.cursor.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        """)
        self.cursor.execute("""
            CREATE TABLE tasks (                
                id SERIAL PRIMARY KEY,
                description TEXT NOT NULL,
                user_id INTEGER REFERENCES users(id),
                user_task_number INTEGER NOT NULL
            );
        """)
        self.conn.commit()


    def register_user(self, username="testuser", password="password123"):
        return self.client.post('/api/auth/register', json={
            "username": username,
            "password": password
        })


    def login_user(self, username="testuser", password="password123"):
        return self.client.post('/api/auth/login', json={
            "username": username,
            "password": password
        })
    
    def auth_headers(self, username="testuser", password="password123"):
        self.register_user(username, password)
        login_res = self.login_user(username, password)
        token = login_res.get_json()["access_token"]
        return {
            "Authorization": f"Bearer {token}"
        }
    
    def auth_full(self):
        self.register_user()
        self.login_user()
        return self.auth_headers()
    
    def test_register_user(self):
        res = self.register_user()
        self.assertEqual(res.status_code, 201)

    def test_login_user(self):
        self.register_user()

        res = self.login_user()
        self.assertEqual(res.status_code, 200)
        self.assertIn("access_token", res.get_json())

    def test_add_task(self):
        headers = self.auth_full()
        
        res = self.client.post('/api/tasks', json={
            "description": "Test task"
        }, headers = headers)

        self.assertEqual(res.status_code, 201)
        self.assertIn("Test task", res.get_json()["Added task"])

    def test_list_tasks(self):
        headers=self.auth_full()

        res = self.client.post('/api/tasks', json={
            "description": "First test task"
        }, headers=headers)

        self.assertIn("First test task", res.get_json()["Added task"])

        res = self.client.post('/api/tasks', json={
            "description": "Second test task"
        }, headers=headers)

        self.assertIn("Second test task", res.get_json()["Added task"])

        res = self.client.get('/api/tasks', headers=headers)

        self.assertEqual(res.status_code, 200)

        self.assertIn("First test task", res.get_json()[0])
        self.assertIn("Second test task", res.get_json()[1])

    def test_edit_task(self):
        headers=self.auth_full()

        res = self.client.post('/api/tasks', json={
            "description": "Test task"
        }, headers=headers)

        self.assertIn("Test task", res.get_json()["Added task"])

        res = self.client.patch('/api/tasks/1', json={"description": "Updated task"}, headers=headers)

        data = res.get_json()

        self.assertIn("Task edited", data)

        self.assertEqual(data["Task edited"]["id"], 1)
        self.assertIn("Updated task", data["Task edited"]["description"])
        
    def test_delete_task(self):
        headers=self.auth_full()

        res = self.client.post('/api/tasks', json={
            "description": "Test task"
        }, headers = headers)

        self.assertIn("Test task", res.get_json()["Added task"])

        res = self.client.delete('/api/tasks/1', headers=headers)
        self.assertEqual(res.status_code, 200)
        self.assertIn("Deleted task", res.get_json())
        self.assertIn("Test task", res.get_json()["Deleted task"])

    def test_clear_list(self):
        headers=self.auth_full()

        res = self.client.post('/api/tasks', json={
            "description": "First test task"
        }, headers=headers)

        self.assertIn("First test task", res.get_json()["Added task"])

        res = self.client.post('/api/tasks', json={
            "description": "Second test task"
        }, headers=headers)

        self.assertIn("Second test task", res.get_json()["Added task"])

        res = self.client.delete('/api/tasks/clear', headers=headers)

        self.assertIn("Clear list", res.get_json())



