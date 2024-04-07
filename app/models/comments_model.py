from app import mongo

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