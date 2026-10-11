from flask import request, jsonify
from auth.jwt_utils import get_current_user_id
from extentions import get_db


def register_chat_routes(app):
    @app.route('/chat/messages', methods=['GET'])
    def get_messages():
        user_id = get_current_user_id(request)
        if user_id is None:
            return jsonify({'error': 'Unauthorized'}), 401

        db = get_db()
        cur = db.cursor()

        cur.execute("""
            SELECT C.id, C.user_id, C.message, C.created_at, U.name as user_name
            FROM chats as C
            LEFT JOIN users as U ON U.id = C.user_id
            ORDER BY C.created_at DESC
            LIMIT 50
        """) # get latest 50 messages from the database 
        messages = cur.fetchall()

        return jsonify([{
            'id': str(row['id']),
            'user_id': str(row['user_id']),
            'message': row['message'],
            'created_at': row['created_at'].isoformat(),
            'user_name': row['user_name']
        } for row in messages]) , 200

