import boto3
from config import Config
from botocore.exceptions import NoCredentialsError
from flask_mail import Message
from flask import render_template
from app import mongo, bcrypt, mail
from datetime import datetime, timedelta
import secrets
from bson import ObjectId

class User:
    def __init__(self, username, email, password, profile_pic=None, banner_pic=None, role='user', bookmarks=None):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.profile_pic = profile_pic
        self.banner_pic = banner_pic
        self.role = role
        self.bookmarks = bookmarks if bookmarks else []
        self.verification_token = None
        self.email_verified = False
        self.reset_password_token = None
        self.reset_password_expires = None

    def save(self):
        user_data = {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'profile_pic': self.profile_pic,
            'banner_pic': self.banner_pic,
            'role': self.role,
            'bookmarks': self.bookmarks,
            'verification_token': self.verification_token,
            'email_verified': self.email_verified,
            'reset_password_token': self.reset_password_token,
            'reset_password_expires': self.reset_password_expires
        }
        result = mongo.db.users.insert_one(user_data)
        self._id = result.inserted_id

    @staticmethod
    def get_user_by_id(user_id):
        return mongo.db.users.find_one({'_id': ObjectId(user_id)})

    @staticmethod
    def get_user_by_email(email):
        return mongo.db.users.find_one({'email': email})

    def generate_verification_token(self):
        self.verification_token = secrets.token_urlsafe()
        return self.verification_token

    def send_verification_email(self):
        token = self.verification_token
        if token:
            subject = "Verify Your Email"
            recipient = self.email
            verification_link = f"https://example.com/verify-email/{token}"  # Update with your actual verification link
            message_body = render_template('verification_email.html', verification_link=verification_link)
            msg = Message(subject=subject, recipients=[recipient], html=message_body)
            mail.send(msg)

    def send_password_reset_email(self):
        self.reset_password_token = secrets.token_urlsafe()
        token = self.reset_password_token
        if token:
            subject = "Reset Your Password"
            recipient = self.email
            reset_link = f"https://example.com/reset-password/{token}"  # Update with your actual reset link
            message_body = render_template('password_reset_email.html', reset_link=reset_link)
            msg = Message(subject=subject, recipients=[recipient], html=message_body)
            mail.send(msg)

    def verify_email(self, token):
        if token == self.verification_token:
            self.email_verified = True
            self.verification_token = None
            mongo.db.users.update_one({'_id': self._id}, {'$set': {'email_verified': True, 'verification_token': None}})
            return True
        else:
            return False

    def request_password_reset(self):
        self.send_password_reset_email()
        self.reset_password_expires = datetime.utcnow() + timedelta(hours=1)
        mongo.db.users.update_one({'_id': self._id}, {'$set': {'reset_password_expires': self.reset_password_expires}})

    def reset_password(self, token, new_password):
        if token == self.reset_password_token and datetime.utcnow() < self.reset_password_expires:
            self.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            self.reset_password_token = None
            self.reset_password_expires = None
            mongo.db.users.update_one({'_id': self._id}, {'$set': {'password': self.password, 'reset_password_token': None, 'reset_password_expires': None}})
            return True
        else:
            return False

    def update_profile(self, username=None, email=None):
        if username:
            self.username = username
        if email:
            self.email = email
        self.save()

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