from app import mongo

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