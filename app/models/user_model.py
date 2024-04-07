from app import mongo, bcrypt
import boto3
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

    def upload_profile_picture(self, file):
        s3 = boto3.client('s3', aws_access_key_id=Config['AWS_ACCESS_KEY_ID'],
                          aws_secret_access_key=Config['AWS_SECRET_ACCESS_KEY'])
        try:
            # Generate a unique file name or use existing user ID for the profile picture
            file_name = f"profile_{self.id}.jpg"
            s3.upload_fileobj(file, Config['FLASKS3_BUCKET_NAME'], file_name)
            self.profile_pic = f"https://{Config['FLASKS3_BUCKET_NAME']}.s3.{Config['AWS_REGION']}.amazonaws.com/{file_name}"
            self.save()
            return True
        except NoCredentialsError:
            return False

    def upload_banner_picture(self, file):
        s3 = boto3.client('s3', aws_access_key_id=Config['AWS_ACCESS_KEY_ID'],
                          aws_secret_access_key=Config['AWS_SECRET_ACCESS_KEY'])
        try:
            # Generate a unique file name or use existing user ID for the banner picture
            file_name = f"banner_{self.id}.jpg"
            s3.upload_fileobj(file, Config['FLASKS3_BUCKET_NAME'], file_name)
            self.banner_pic = f"https://{Config['FLASKS3_BUCKET_NAME']}.s3.{Config['AWS_REGION']}.amazonaws.com/{file_name}"
            self.save()
            return True
        except NoCredentialsError:
            return False

    def delete_profile_picture(self):
        if self.profile_pic:
            # Extract the file name from the URL
            file_name = self.profile_pic.split('/')[-1]
            s3 = boto3.client('s3', aws_access_key_id=Config['AWS_ACCESS_KEY_ID'],
                              aws_secret_access_key=Config['AWS_SECRET_ACCESS_KEY'])
            try:
                s3.delete_object(Bucket=Config['FLASKS3_BUCKET_NAME'], Key=file_name)
                self.profile_pic = None
                self.save()
                return True
            except NoCredentialsError:
                return False

    def delete_banner_picture(self):
        if self.banner_pic:
            # Extract the file name from the URL
            file_name = self.banner_pic.split('/')[-1]
            s3 = boto3.client('s3', aws_access_key_id=Config['AWS_ACCESS_KEY_ID'],
                              aws_secret_access_key=Config['AWS_SECRET_ACCESS_KEY'])
            try:
                s3.delete_object(Bucket=Config['FLASKS3_BUCKET_NAME'], Key=file_name)
                self.banner_pic = None
                self.save()
                return True
            except NoCredentialsError:
                return False

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

    def add_bookmark(self, reel_id):
        if reel_id not in self.bookmarks:
            self.bookmarks.append(reel_id)
            self.save()

    def remove_bookmark(self, reel_id):
        if reel_id in self.bookmarks:
            self.bookmarks.remove(reel_id)
            self.save()

    def delete_account(self):
        mongo.db.users.delete_one({'_id': self._id})