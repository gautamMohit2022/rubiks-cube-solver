import random
import time

MOVES = [
    "U", "U'", "U2", "D", "D'", "D2", "F", "F'", "F2", 
    "B", "B'", "B2", "L", "L'", "L2", "R", "R'", "R2"
]

def generate_scramble(length=20):
    scramble = []
    prev_face = ''
    for _ in range(length):
        move = random.choice(MOVES)
        while move[0] == prev_face and len(MOVES) > 1:
            move = random.choice(MOVES)
        scramble.append(move)
        prev_face = move[0]
    return scramble

def apply_scramble(cube, scramble_moves):
    for move in scramble_moves:
        if hasattr(cube, 'apply_move'):
            cube.apply_move(move)
        else:
            cube.move(move)
    return cube

def is_solved(cube):
    for face in cube.faces:
        stickers = cube.faces[face]
        first = stickers[0][0]
        for row in stickers:
            if any(cell != first for cell in row):
                return False
    return True

def print_cube_state(cube, label=None):
    if label:
        print(f"\n📦 {label}")
    print(cube)

def timer_start():
    return time.time()

def timer_end(start_time):
    return round(time.time() - start_time, 4)












