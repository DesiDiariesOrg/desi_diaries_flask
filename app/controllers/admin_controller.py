from flask import jsonify, request
from app.models import Category
from flask_login import current_user
from app import mongo
from bson import ObjectId

def list_users():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403

    users = mongo.db.users.find()
    user_list = [{'username': user['username'], 'email': user['email']} for user in users]
    return jsonify(user_list), 200

def delete_user(user_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403

    mongo.db.users.delete_one({'_id': ObjectId(user_id)})
    return jsonify({'message': 'User deleted successfully'}), 200

def create_category():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403

    data = request.json
    title = data.get('title')
    thumbnail = data.get('thumbnail')

    new_category = Category(title, thumbnail)
    new_category.save()
    return jsonify({'message': 'Category created successfully'}), 201

def delete_category(category_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403

    Category.delete_by_id(category_id)
    return jsonify({'message': 'Category deleted successfully'}), 200