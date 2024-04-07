from app import mongo
from bson import ObjectId

class Reply:
    def __init__(self, user_id, comment_id, text):
        self.user_id = user_id
        self.comment_id = comment_id
        self.text = text

    def save(self):
        mongo.db.replies.insert_one({
            'user_id': self.user_id,
            'comment_id': self.comment_id,
            'text': self.text
        })

    @staticmethod
    def find_by_id(reply_id):
        return mongo.db.replies.find_one({'_id': ObjectId(reply_id)})