from flask import request, jsonify
from app import app
from app.controllers.user_controller import *
from app.controllers.reels_controller import *
from app.controllers.admin_controller import *
from app.controllers.category_controller import *
from app.controllers.auth_controller import *

# Auth routes
@app.route('/api/login', methods=['POST'])
def login_route():
    return login()

@app.route('/api/signup', methods=['POST'])
def signup_route():
    return signup()

@app.route('/api/logout')
def logout_route():
    return logout()

# User management routes
@app.route('/api/account/delete', methods=['POST'])
def delete_account_route():
    return delete_account()

@app.route('/api/profile/edit', methods=['POST'])
def edit_profile_route():
    return edit_profile()

@app.route('/api/profile/picture', methods=['POST'])
def upload_profile_picture_route():
    return upload_profile_picture()

@app.route('/api/profile/banner', methods=['POST'])
def upload_banner_picture_route():
    return upload_banner_picture()

@app.route('/api/profile/picture', methods=['DELETE'])
def delete_profile_picture_route():
    return delete_profile_picture()

@app.route('/api/profile/banner', methods=['DELETE'])
def delete_banner_picture_route():
    return delete_banner_picture()

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user_route(user_id):
    return get_user(user_id)

# Reel management routes
@app.route('/api/reels/upload', methods=['POST'])
def upload_reel_route():
    return upload_reel()

@app.route('/api/reels/<reel_id>', methods=['GET'])
def get_reel_route(reel_id):
    return get_reel(reel_id)

@app.route('/api/reels/<reel_id>/comments', methods=['POST'])
def post_comment_route(reel_id):
    return post_comment(reel_id)

@app.route('/api/reels/<reel_id>/share', methods=['POST'])
def share_reel_route(reel_id):
    return share_reel(reel_id)

@app.route('/api/reels/<reel_id>/like', methods=['POST'])
def like_reel_route(reel_id):
    return like_reel(reel_id)

@app.route('/api/comments/<comment_id>/reply', methods=['POST'])
def reply_to_comment_route(comment_id):
    return reply_to_comment(comment_id)

@app.route('/api/reels/<reel_id>/bookmark', methods=['POST'])
def bookmark_reel_route(reel_id):
    return bookmark_reel(reel_id)

@app.route('/api/reels/<reel_id>/unbookmark', methods=['POST'])
def unbookmark_reel_route(reel_id):
    return unbookmark_reel(reel_id)

# Admin management routes
@app.route('/api/admin/users', methods=['GET'])
def list_users_route():
    return list_users()

@app.route('/api/admin/users/<user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    return delete_user(user_id)

@app.route('/api/admin/categories', methods=['POST'])
def create_category_route():
    return create_category()

@app.route('/api/admin/categories/<category_id>', methods=['DELETE'])
def delete_category_route(category_id):
    return delete_category(category_id)

# Category management routes
@app.route('/api/categories', methods=['GET'])
def get_categories_route():
    return get_categories()
