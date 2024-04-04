from app import mongo, bcrypt

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


