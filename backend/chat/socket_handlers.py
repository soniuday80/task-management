from flask_socketio import SocketIO, emit
from chat.socket_io_setup import socketio
from auth.jwt_utils import jwt_Decode
from backend.extentions import get_db, close_db
from flask import request

connected_users = {} # Dictionary to keep track of connected users and their user_ids

def socket_handlers():
    @socketio.on('connect')
    def handle_connect(auth):
        token = auth.get('token') if auth else None
        user_id = jwt_Decode(token) if token else None
        if user_id is None:
            emit('unauthorized', {'message': 'Invalid or missing token'})
            return False

        connected_users['request.sid'] = user_id
        

    @socketio.on('message')
    def handle_message(data):
        user_id = connected_users.get(request.sid)

        if user_id is None:
            return 


        message = data.get('text' or '').strip()
        if not message:
            return None

        db = get_db()
        cur = db.cursor()

        row = cur.execute("INSERT INTO chat(user_id, message , created_at) VALUES (%s , %s , NOW()) RETURNING id , message , created_at", (user_id , message))
        db.commit()

        emit(
            'message',
            {
                'id': str(row['id']),
                'user_id': str(row['user_id']),
                'message': row['message'],
                'created_at': row['created_at'].isoformat()
            },
            broadcast=True
        )
        



    @socketio.on('disconnect')
    def handle_disconnect(reason):
        connected_users.pop(request.sid, None)

        list_users = list(connected_users.values())

        emit('presence', {'user_id': list_users}, broadcast=True)




    @socketio.on('typing')
    def handle_typing(data):
       emit('typing', {'user_id': connected_users.get(request.sid)}, broadcast=True, include_self=False)