from flask import request, jsonify
from flask_login import current_user
from app.models.user_model import User
from flask_login import logout_user, login_user
from app import bcrypt


def edit_profile():
    data = request.json
    username = data.get('username')
    email = data.get('email')

    current_user.update_profile(username, email)
    return jsonify({'message': 'Profile updated successfully'}), 200

def upload_profile_picture():
    file = request.files['file']
    if current_user.upload_profile_picture(file):
        return jsonify({'message': 'Profile picture uploaded successfully'}), 200
    else:
        return jsonify({'error': 'Failed to upload profile picture. Check AWS credentials.'}), 500

def upload_banner_picture():
    file = request.files['file']
    if current_user.upload_banner_picture(file):
        return jsonify({'message': 'Banner picture uploaded successfully'}), 200
    else:
        return jsonify({'error': 'Failed to upload banner picture. Check AWS credentials.'}), 500

def delete_profile_picture():
    if current_user.delete_profile_picture():
        return jsonify({'message': 'Profile picture deleted successfully'}), 200
    else:
        return jsonify({'error': 'Failed to delete profile picture. Check AWS credentials.'}), 500

def delete_banner_picture():
    if current_user.delete_banner_picture():
        return jsonify({'message': 'Banner picture deleted successfully'}), 200
    else:
        return jsonify({'error': 'Failed to delete banner picture. Check AWS credentials.'}), 500

def get_user(user_id):
    user = User.get_user_by_id(user_id)
    if user:
        return jsonify(user.to_json()), 200
    else:
        return jsonify({'error': 'User not found'}), 404