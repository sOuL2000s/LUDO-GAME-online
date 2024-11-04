from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ludo_secret_key'
socketio = SocketIO(app)

# Game rooms
games = {}

# Player joins game room
@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    games.setdefault(room, {"players": [], "state": {}})
    games[room]["players"].append(data['username'])
    emit('player_joined', {"players": games[room]["players"]}, room=room)

# Player rolls dice
@socketio.on('roll_dice')
def roll_dice(data):
    dice_roll = random.randint(1, 6)
    room = data['room']
    emit('dice_rolled', {"roll": dice_roll, "player": data['player']}, room=room)

# Handle player movement and update game state
@socketio.on('move_piece')
def move_piece(data):
    room = data['room']
    player = data['player']
    position = data['position']
    games[room]["state"][player] = position  # Update player position
    emit('update_position', games[room]["state"], room=room)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
