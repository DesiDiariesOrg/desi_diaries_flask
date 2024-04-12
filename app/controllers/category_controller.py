from flask import jsonify
from app.models import Category

def get_categories():
    categories = Category.find_all()
    category_list = [{'id': category.id, 'title': category.title, 'thumbnail': category.thumbnail} for category in categories]
    return jsonify(category_list), 200
