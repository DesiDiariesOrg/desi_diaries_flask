from app import mongo, bcrypt
import boto3
from bson import ObjectId
from config import Config
from botocore.exceptions import NoCredentialsError

class User:
    def __init__(self, username, email, password, profile_pic=None, banner_pic=None, role='user', bookmarks=None):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.profile_pic = profile_pic
        self.banner_pic = banner_pic
        self.role = role
        self.bookmarks = bookmarks if bookmarks else []

    def save(self):
        mongo.db.users.insert_one({
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'profile_pic': self.profile_pic,
            'banner_pic': self.banner_pic,
            'role': self.role,
            'bookmarks': self.bookmarks
        })

    def update_profile(self, username=None, email=None):
        if username:
            self.username = username
        if email:
            self.email = email
        self.save()

    def delete_account(self):
        mongo.db.users.delete_one({'_id': self._id})

    @staticmethod
    def get_user_by_id(user_id):
        return mongo.db.users.find_one({'_id': user_id})

    @staticmethod
    def get_all_users():
        return mongo.db.users.find()

    def to_json(self):
        return {
            'username': self.username,
            'email': self.email,
            'profile_pic': self.profile_pic,
            'banner_pic': self.banner_pic
        }


class Comment:
    def __init__(self, user_id, reel_id, text):
        self.user_id = user_id
        self.reel_id = reel_id
        self.text = text

    def save(self):
        mongo.db.comments.insert_one({
            'user_id': self.user_id,
            'reel_id': self.reel_id,
            'text': self.text
        })

    @staticmethod
    def find_by_reel_id(reel_id):
        return mongo.db.comments.find({'reel_id': reel_id})


class Share:
    def __init__(self, user_id, reel_id):
        self.user_id = user_id
        self.reel_id = reel_id

    def save(self):
        mongo.db.shares.insert_one({
            'user_id': self.user_id,
            'reel_id': self.reel_id
        })

    @staticmethod
    def find_by_user_and_reel(user_id, reel_id):
        return mongo.db.shares.find_one({'user_id': user_id, 'reel_id': reel_id})

class Notification:
    def __init__(self, user_id, type, action_id):
        self.user_id = user_id
        self.type = type  # Type of notification (e.g., 'comment', 'like', 'reply')
        self.action_id = action_id  # ID of the action triggering the notification

    def save(self):
        mongo.db.notifications.insert_one({
            'user_id': self.user_id,
            'type': self.type,
            'action_id': self.action_id,
            'read': False  # Flag to mark whether the notification has been read
        })

    @staticmethod
    def find_by_user_id(user_id):
        return mongo.db.notifications.find({'user_id': user_id})


class Like:
    def __init__(self, user_id, reel_id):
        self.user_id = user_id
        self.reel_id = reel_id

    def save(self):
        mongo.db.likes.insert_one({
            'user_id': self.user_id,
            'reel_id': self.reel_id
        })

    @staticmethod
    def find_by_user_and_reel(user_id, reel_id):
        return mongo.db.likes.find_one({'user_id': user_id, 'reel_id': reel_id})
