import os

class Config:
    SECRET_KEY = 'your_secret_key'
    MONGO_URI = 'mongodb://localhost:27017/mydatabase'
    FLASKS3_BUCKET_NAME = 'your-bucket-name'
    AWS_REGION = 'your-aws-region'
    AWS_ACCESS_KEY_ID = 'your-access-key-id'
    AWS_SECRET_ACCESS_KEY = 'your-secret-access-key'
