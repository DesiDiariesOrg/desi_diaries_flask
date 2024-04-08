from flask import request, jsonify
from flask_login import current_user
from app.models.reels_model import Reel
from app.models.comments_model import Comment
from app.models.share_model import Share
from app.models.notifications_model import Notification
from app.models.likes_model import Like
from app.models.reply_model import Reply

def upload_reel():
    # Check if the request contains the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    # Check if the file is provided
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        # Extract other reel data from the request JSON payload
        data = request.form
        title = data.get('title')
        description = data.get('description')
        
        # Create a new Reel object and save it
        new_reel = Reel(title, description, file, current_user.id)
        new_reel.save()
        
        return jsonify({'message': 'Reel uploaded successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_reel(reel_id):
    reel = Reel.find_by_id(reel_id)
    if reel:
        return jsonify({
            'title': reel['title'],
            'description': reel['description'],
            'video_url': reel['video_url'],
            'user_id': reel['user_id']
        }), 200
    else:
        return jsonify({'error': 'Reel not found'}), 404

def post_comment(reel_id):
    data = request.json
    text = data.get('text')

    if not text:
        return jsonify({'error': 'Comment text is required'}), 400

    new_comment = Comment(current_user.id, reel_id, text)
    new_comment.save()
    # Fetch the reel to get its owner ID
    reel = Reel.find_by_id(reel_id)
    if reel:
        reel_owner_id = reel.user_id
        # Trigger notification to the reel owner
        if current_user.id != reel_owner_id:
            notification = Notification(reel_owner_id, 'comment', new_comment._id)
            notification.save()
    else:
        return jsonify({'error': 'Reel not found'}), 404
    return jsonify({'message': 'Comment posted successfully'}), 201

def share_reel(reel_id):
    if Reel.find_by_id(reel_id):
        if not Share.find_by_user_and_reel(current_user.id, reel_id):
            new_share = Share(current_user.id, reel_id)
            new_share.save()
            return jsonify({'message': 'Reel shared successfully'}), 200
        else:
            return jsonify({'error': 'Reel already shared by user'}), 400
    else:
        return jsonify({'error': 'Reel not found'}), 404

def like_reel(reel_id):
    # Check if the reel exists
    reel = Reel.find_by_id(reel_id)
    if not reel:
        return jsonify({'error': 'Reel not found'}), 404

    # Check if the user has already liked the reel
    if Like.find_by_user_and_reel(current_user.id, reel_id):
        return jsonify({'error': 'You have already liked this reel'}), 400

    # Like the reel
    new_like = Like(current_user.id, reel_id)
    new_like.save()

    # Trigger notification to the reel owner if the liker is not the owner
    if current_user.id != reel.user_id:
        notification = Notification(reel.user_id, 'like', reel_id)
        notification.save()

    return jsonify({'message': 'Reel liked successfully'}), 200

def reply_to_comment(comment_id):
    data = request.json
    text = data.get('text')

    # Check if the comment exists
    comment = Comment.find_by_id(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    # Reply to the comment
    new_reply = Reply(current_user.id, comment_id, text)
    new_reply.save()

    # Trigger notification to the commented user if the replier is not the commented user
    if current_user.id != comment.user_id:
        notification = Notification(comment.user_id, 'reply', new_reply._id)
        notification.save()

    return jsonify({'message': 'Reply posted successfully'}), 201

def bookmark_reel(reel_id):
    current_user.add_bookmark(reel_id)
    return jsonify({'message': 'Reel bookmarked successfully'}), 200

def unbookmark_reel(reel_id):
    current_user.remove_bookmark(reel_id)
    return jsonify({'message': 'Reel unbookmarked successfully'}), 200
