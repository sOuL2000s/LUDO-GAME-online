import pygame
import socketio

# Initialize SocketIO client
sio = socketio.Client()

# Connect to the server
sio.connect('http://localhost:5000')

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Ludo Multiplayer")

# Game variables
player_name = "Player1"
room = "LudoRoom"
current_turn = False

# Event Handlers
@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.event
def player_joined(data):
    print("Players in room:", data['players'])

@sio.event
def dice_rolled(data):
    print(f"{data['player']} rolled a {data['roll']}")
    global current_turn
    current_turn = data['player'] == player_name

@sio.event
def update_position(data):
    print("Updated positions:", data)

# Join room
sio.emit('join', {'room': room, 'username': player_name})

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and current_turn:
                sio.emit('roll_dice', {"room": room, "player": player_name})

    # Game board rendering logic goes here
    screen.fill((255, 255, 255))
    pygame.display.flip()

pygame.quit()
sio.disconnect()
