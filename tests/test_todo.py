import tempfile
import unittest
from pathlib import Path
from application import create_app
from application.extensions import db
from application.models import Todo


class TodoTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.app = create_app('production', {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + str(Path(self.tmp.name) / 'test.sqlite'),
        })
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()
        self.tmp.cleanup()

    def test_task_lifecycle(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TODO Lists', response.data)
        response = self.client.post('/', data={'title': 'CI test task'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'CI test task', response.data)
        task = Todo.query.one()
        task_id = task.id
        self.client.get(f'/{task_id}/done')
        db.session.expire_all()
        self.assertTrue(db.session.get(Todo, task_id).status)
        self.client.get(f'/{task_id}/redo')
        db.session.expire_all()
        self.assertFalse(db.session.get(Todo, task_id).status)
        self.client.post(f'/{task_id}/edit', data={'title': 'Updated task'})
        db.session.expire_all()
        self.assertEqual(db.session.get(Todo, task_id).title, 'Updated task')
        self.client.get(f'/{task_id}/del')
        self.assertEqual(Todo.query.count(), 0)


if __name__ == '__main__':
    unittest.main()
