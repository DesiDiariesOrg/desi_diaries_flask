from app import mongo
import boto3
from bson import ObjectId
from config import Config

class Reel:
    def __init__(self, title, description, video_url, user_id, category_id):
        self.title = title
        self.description = description
        self.video_url = video_url
        self.user_id = user_id
        self.category_id = category_id

    def save(self):
        # Upload video to S3
        s3 = boto3.client('s3',
                        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
                        region_name=Config.AWS_REGION)
        s3.upload_file(self.video_url, Config.S3_BUCKET_NAME, self.video_url)

        # Save reel information to MongoDB
        mongo.db.reels.insert_one({
            'title': self.title,
            'description': self.description,
            'video_url': f"https://{Config.S3_BUCKET_NAME}.s3.amazonaws.com/{self.video_url}",
            'user_id': self.user_id,
            'category_id': self.category_id
        })

    @staticmethod
    def find_by_id(reel_id):
        return mongo.db.reels.find_one({'_id': ObjectId(reel_id)})

    @staticmethod
    def find_by_user_id(user_id):
        return mongo.db.reels.find({'user_id': user_id})

    @staticmethod
    def find_by_category_id(category_id):
        return mongo.db.reels.find({'category_id': category_id})

