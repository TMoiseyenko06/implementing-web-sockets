from web_socket_server import WebSocketServer, socketio, app
from flask import render_template, request, session, redirect

app = WebSocketServer().create_app(True)

users = {}
message_storage = {}

@socketio.on('connect')
def handle_connect():
    pass

@socketio.on('disconnect')
def handle_disconnect():
    users.pop(request.sid, None)

@socketio.on('message')
def handle_message(message):
    message_storage[users[request.sid]].append(message)
    socketio.emit('message',f'{users[request.sid]}: {message}')

@app.route('/')
def chat():
    return render_template('chat.html')

@socketio.on('set_username')
def set_username(username):
    users[request.sid] = username
    message_storage[username] = []

@socketio.on('getMessages')
def get_messages(name):
    socketio.emit("messages",message_storage[name])


socketio.run(app)