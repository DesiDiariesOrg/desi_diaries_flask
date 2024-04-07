from app import mongo, bcrypt
import boto3
from bson import ObjectId
from botocore.exceptions import NoCredentialsError

class Category:
    def __init__(self, title, thumbnail, id=None):
        self.id = id
        self.title = title
        self.thumbnail = thumbnail

    def save(self):
        # Initialize S3 client
        s3 = boto3.client('s3')

        if self.id is None:
            result = mongo.db.categories.insert_one({
                'title': self.title,
                'thumbnail': self.thumbnail  # Store thumbnail URL in MongoDB
            })
            self.id = result.inserted_id
        else:
            mongo.db.categories.update_one(
                {'_id': self.id},
                {'$set': {'title': self.title, 'thumbnail': self.thumbnail}}
            )

        try:
            # Upload thumbnail image to S3 bucket
            s3.upload_file(self.thumbnail, 'your-bucket-name', f'category_thumbnails/{self.id}')
        except FileNotFoundError:
            print("The file was not found")
        except NoCredentialsError:
            print("Credentials not available")

    @staticmethod
    def find_all():
        categories = mongo.db.categories.find()
        return [Category(category['title'], category['thumbnail'], category['_id']) for category in categories]

    @staticmethod
    def find_by_id(category_id):
        category_data = mongo.db.categories.find_one({'_id': ObjectId(category_id)})
        if category_data:
            return Category(category_data['title'], category_data['thumbnail'], category_data['_id'])
        else:
            return None

    @staticmethod
    def delete_by_id(category_id):
        mongo.db.categories.delete_one({'_id': ObjectId(category_id)})
