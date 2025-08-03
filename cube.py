import copy

class RubikCube:
    """
    Represents a 3x3 Rubik's Cube.
    Faces: U (Up/W), D (Down/Y), L (Left/O), R (Right/R), F (Front/G), B (Back/B).
    """

    def __init__(self):
        # Each face is a 3x3 grid of a single color
        self.faces = {
            'U': [['W'] * 3 for _ in range(3)], # Up: White
            'D': [['Y'] * 3 for _ in range(3)], # Down: Yellow
            'L': [['O'] * 3 for _ in range(3)], # Left: Orange
            'R': [['R'] * 3 for _ in range(3)], # Right: Red
            'F': [['G'] * 3 for _ in range(3)], # Front: Green
            'B': [['B'] * 3 for _ in range(3)], # Back: Blue
        }

    def _rotate_face_clockwise(self, face):
        """Rotates a face in place clockwise (90 degrees)."""
        self.faces[face] = [list(row) for row in zip(*self.faces[face][::-1])]

    def _rotate_face_counterclockwise(self, face):
        """Rotates a face in place counterclockwise (90 degrees)."""
        self.faces[face] = [list(row) for row in zip(*self.faces[face])][::-1]

    def move(self, notation):
        """
        Apply a move to the cube by notation (e.g., 'U', "U'", 'F2').
        Supports single, prime, and double moves.
        """
        # Mapping from face to the 4 sides affected in order (U, R, D, L)
        side_map = {
            'U': [('B', 0), ('R', 0), ('F', 0), ('L', 0)],
            'D': [('F', 2), ('R', 2), ('B', 2), ('L', 2)],
            'F': [('U', 2), ('R', 'col0'), ('D', 0), ('L', 'col2')],
            'B': [('U', 0), ('L', 'col0'), ('D', 2), ('R', 'col2')],
            'L': [('U', 'col0'), ('F', 'col0'), ('D', 'col0'), ('B', 'col2')],
            'R': [('U', 'col2'), ('B', 'col0'), ('D', 'col2'), ('F', 'col2')],
        }
        face = notation[0]
        turns = 1
        if len(notation) == 2:
            if notation[1] == "'":
                turns = 3
            elif notation[1] == '2':
                turns = 2
        # Rotate face
        for _ in range(turns):
            self._rotate_face_clockwise(face)
            # Move the adjacent side stickers
            if face in 'UD':
                idx = 0 if face == 'U' else 2
                temp = [self.faces[side_map[face][i][0]][idx][:] for i in range(4)]
                for i in range(4):
                    src = temp[(i - 1) % 4]
                    self.faces[side_map[face][i][0]][idx] = src
            elif face in 'FB':
                if face == 'F':
                    rows = [
                        self.faces['U'][2][:],
                        [self.faces['R'][i][0] for i in range(3)],
                        self.faces['D'][0][:],
                        [self.faces['L'][i][2] for i in range(3)],
                    ]
                    for i in range(3):
                        self.faces['U'][2][i] = rows[3][i]
                        self.faces['R'][i][0] = rows[0][i]
                        self.faces['D'][0][i] = rows[1][i]
                        self.faces['L'][i][2] = rows[2][i]
                else: # B
                    rows = [
                        self.faces['U'][0][:],
                        [self.faces['L'][i][0] for i in range(3)],
                        self.faces['D'][2][:],
                        [self.faces['R'][i][2] for i in range(3)],
                    ]
                    for i in range(3):
                        self.faces['U'][0][i] = rows[3][2 - i]
                        self.faces['L'][i][0] = rows[0][2 - i]
                        self.faces['D'][2][i] = rows[1][2 - i]
                        self.faces['R'][i][2] = rows[2][2 - i]
            else: # L or R
                coln = 0 if face == 'L' else 2
                adj = ['U', 'F', 'D', 'B']
                cols = [
                    [self.faces[adj[0]][i][coln] for i in range(3)],
                    [self.faces[adj[1]][i][coln] for i in range(3)],
                    [self.faces[adj[2]][i][coln] for i in range(3)],
                    [self.faces[adj[3]][2-i][2-coln] for i in range(3)]
                ]
                for i in range(3):
                    self.faces[adj[0]][i][coln] = cols[3][i]
                    self.faces[adj[1]][i][coln] = cols[0][i]
                    self.faces[adj[2]][i][coln] = cols[1][i]
                    self.faces[adj[3]][2 - i][2 - coln] = cols[2][i]

    def apply_move(self, notation):
        """External interface for move."""
        if notation not in [
            'U', "U'", 'U2', 'D', "D'", 'D2',
            'L', "L'", 'L2', 'R', "R'", 'R2',
            'F', "F'", 'F2', 'B', "B'", 'B2'
        ]:
            raise ValueError(f"Invalid move: '{notation}'")
        self.move(notation)


    def __str__(self):
        # Nicely print all faces for display/debug
        out = ""
        for face in ['U', 'D', 'L', 'R', 'F', 'B']:
            out += f'{face}:\n'
            for row in self.faces[face]:
                out += ' '.join(row) + '\n'
        return out.strip()
    def apply_move(self, move: str):
        """Apply a single move to the cube."""
        self.move(move)

    def apply_moves(self, moves: list[str]):
        """Apply a sequence of moves to the cube."""
        for move in moves:
            self.apply_move(move)

