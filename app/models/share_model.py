from app import mongo

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