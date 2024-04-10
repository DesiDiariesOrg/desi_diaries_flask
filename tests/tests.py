import unittest
from app import app, mongo
from app.models import User, Reel, Category

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.db = mongo.db

    def tearDown(self):
        # Clean up after each test
        self.db.users.delete_many({})
        self.db.reels.delete_many({})
        self.db.categories.delete_many({})

    def test_signup(self):
        # Test user signup
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.app.post('/api/signup', json=data)
        self.assertEqual(response.status_code, 201)
        user = User.get_user_by_email('test@example.com')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')

    def test_login(self):
        # Test user login
        user = User(username='testuser', email='test@example.com', password='testpassword')
        user.save()
        data = {'email': 'test@example.com', 'password': 'testpassword'}
        response = self.app.post('/api/login', json=data)
        self.assertEqual(response.status_code, 200)

    def test_upload_reel(self):
        # Test uploading a reel
        user = User(username='testuser', email='test@example.com', password='testpassword')
        user.save()
        data = {'title': 'Test Reel', 'description': 'Test Description'}
        response = self.app.post('/api/reels/upload', data=data)
        self.assertEqual(response.status_code, 201)
        reel = Reel.find_by_title('Test Reel')
        self.assertIsNotNone(reel)

    def test_create_category(self):
        # Test creating a category
        data = {'title': 'Test Category'}
        response = self.app.post('/api/admin/categories', json=data)
        self.assertEqual(response.status_code, 201)
        category = Category.find_by_title('Test Category')
        self.assertIsNotNone(category)

    def test_delete_category(self):
        # Test deleting a category
        category = Category(title='Test Category')
        category.save()
        response = self.app.delete(f'/api/admin/categories/{category.id}')
        self.assertEqual(response.status_code, 200)
        deleted_category = Category.find_by_id(category.id)
        self.assertIsNone(deleted_category)

if __name__ == '__main__':
    unittest.main()
