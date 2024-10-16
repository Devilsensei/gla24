from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# MongoDB Setup (replace with your connection string)
client = MongoClient('mongodb://localhost:27017/')
db = client['notification_system']
users_collection = db['users']
notifications_collection = db['notifications']

# User preferences structure
def get_default_preferences():
    return {
        "likes": True,
        "comments": True,
        "follows": True,
        "recommendations": True
    }

# Alert settings structure
def get_default_alert_settings():
    return {
        "email": True,
        "pushNotifications": False
    }

# Endpoint to update notification preferences
@app.route('/update_preferences/<user_id>', methods=['POST'])
def update_preferences(user_id):
    preferences = request.json.get('preferences')
    users_collection.update_one({'_id': user_id}, {'$set': {'notificationPreferences': preferences}})
    return jsonify({"message": "Preferences updated successfully"}), 200

# Endpoint to update alert settings
@app.route('/update_alert_settings/<user_id>', methods=['POST'])
def update_alert_settings(user_id):
    alert_settings = request.json.get('alertSettings')
    users_collection.update_one({'_id': user_id}, {'$set': {'alertSettings': alert_settings}})
    return jsonify({"message": "Alert settings updated successfully"}), 200

# Notification Creation
def create_notification(notification_type, from_user_id, to_user_id, post_id=None):
    notification = {
        'type': notification_type,
        'fromUserId': from_user_id,
        'toUserId': to_user_id,
        'postId': post_id,
        'isRead': False,
        'createdAt': datetime.utcnow()
    }
    notifications_collection.insert_one(notification)
    return notification

# Function to send email notifications (if enabled)
def send_email_notification(user_email, notification_message):
    # Simulate email sending (you can integrate with an SMTP server or email provider)
    print(f"Sending email to {user_email}: {notification_message}")

# Socket.IO Events
@socketio.on('join')
def on_join(data):
    user_id = data['userId']
    join_room(user_id)
    print(f'User {user_id} joined their notification room')

# Handle like event
@socketio.on('like_post')
def handle_like_post(data):
    from_user_id = data['fromUserId']
    to_user_id = data['toUserId']
    post_id = data['postId']

    # Check if the user has enabled notifications for likes
    user = users_collection.find_one({'_id': to_user_id})
    if user and user['notificationPreferences'].get('likes', True):
        notification = create_notification('like', from_user_id, to_user_id, post_id)
        emit('newNotification', {'message': 'Someone liked your post!', 'postId': post_id}, room=to_user_id)
        
        # Send email notification if enabled
        if user['alertSettings'].get('email', True):
            send_email_notification(user['email'], 'Someone liked your post!')

# Handle follow event
@socketio.on('follow_user')
def handle_follow_user(data):
    from_user_id = data['fromUserId']
    to_user_id = data['toUserId']

    # Check if the user has enabled notifications for follows
    user = users_collection.find_one({'_id': to_user_id})
    if user and user['notificationPreferences'].get('follows', True):
        notification = create_notification('follow', from_user_id, to_user_id)
        emit('newNotification', {'message': 'Someone started following you!'}, room=to_user_id)

        # Send email notification if enabled
        if user['alertSettings'].get('email', True):
            send_email_notification(user['email'], 'Someone started following you!')

# Handle recommendation system integration (Student 8)
@socketio.on('recommendation')
def handle_recommendation(data):
    to_user_id = data['toUserId']
    recommendation_message = data['message']

    # Check if the user has enabled notifications for recommendations
    user = users_collection.find_one({'_id': to_user_id})
    if user and user['notificationPreferences'].get('recommendations', True):
        notification = create_notification('recommendation', 'system', to_user_id)
        emit('newNotification', {'message': recommendation_message}, room=to_user_id)

        # Send email notification if enabled
        if user['alertSettings'].get('email', True):
            send_email_notification(user['email'], recommendation_message)

# Fetch user notifications (with pagination)
@app.route('/notifications/<user_id>', methods=['GET'])
def get_notifications(user_id):
    notifications = list(notifications_collection.find({'toUserId': user_id}).sort('createdAt', -1))
    return jsonify(notifications)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
