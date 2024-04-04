from flask import request, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from app import app, mongo, bcrypt
from bson import ObjectId
from app.models import User

# User management routes
@app.route('/api/account/delete', methods=['POST'])
@login_required
def delete_account():
    current_user.delete_account()
    return jsonify({'message': 'Account deleted successfully'}), 200

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.get_user_by_email(email)

    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    existing_user = User.get_user_by_email(email)
    if existing_user:
        return jsonify({'error': 'User with this email already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(username=username, email=email, password=hashed_password)
    new_user.save()

    return jsonify({'message': 'Signup successful'}), 201

@app.route('/api/logout')
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200


@app.route('/api/profile/edit', methods=['POST'])
@login_required
def edit_profile():
    data = request.json
    username = data.get('username')
    email = data.get('email')

    current_user.update_profile(username, email)
    return jsonify({'message': 'Profile updated successfully'}), 200

@app.route('/api/admin/users', methods=['GET'])
@login_required
def list_users():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403

    users = mongo.db.users.find()
    user_list = [{'username': user['username'], 'email': user['email']} for user in users]
    return jsonify(user_list), 200

@app.route('/api/admin/users/<user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403

    mongo.db.users.delete_one({'_id': ObjectId(user_id)})
    return jsonify({'message': 'User deleted successfully'}), 200

