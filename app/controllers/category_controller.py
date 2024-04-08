from flask import request, jsonify
from flask_login import current_user
from app.models import Category

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

def get_categories():
    categories = Category.find_all()
    category_list = [{'id': category.id, 'title': category.title, 'thumbnail': category.thumbnail} for category in categories]
    return jsonify(category_list), 200
