from cube import RubikCube as Cube
from utils import generate_scramble, is_solved, print_cube_state, timer_start, timer_end

class RubiksCubeSolver:
    def __init__(self, cube=None, scramble=None):
        self.cube = cube if cube else Cube()
        self.scramble = scramble if scramble else generate_scramble()
        self.solution_moves = []
        self.side_colors = ['R', 'G', 'O', 'B']

        self.left_of = {'F': 'L', 'R': 'F', 'B': 'R', 'L': 'B'}
        self.right_of = {'F': 'R', 'R': 'B', 'B': 'L', 'L': 'F'}

    def apply_moves(self, moves):
        # Supports both 'F2' and ['F','F'] style notations.
        for move in moves:
            self.solution_moves.append(move)
            self.cube.apply_move(move)

    def solve_white_cross(self):
        print("\nℹ️ Solving bulletproof white cross")
        target_edges = [
            # face, center color, D-layer position (goal), D-layer position (actual)
            ('F', 'F', (0, 1), (0, 1)),
            ('R', 'R', (1, 2), (1, 2)),
            ('B', 'B', (2, 1), (2, 1)),
            ('L', 'L', (1, 0), (1, 0)),
        ]
        for face, color_face, dpos, dside in target_edges:
            for _ in range(12):  # Prevents infinite loops
                # 1. Already solved for this edge
                if (self.cube.faces['D'][dside[0]][dside[1]] == 'W' and
                    self.cube.faces[face][2][1] == self.cube.faces[face][1][1]):
                    break
                placed = False
                # (a) U-layer, aligned to center
                for _ in range(4):
                    if (self.cube.faces['U'][2][1] == 'W' and
                        self.cube.faces[face][0][1] == self.cube.faces[face][1][1]):
                        self.apply_moves([face, face])
                        placed = True
                        break
                    self.apply_moves(['U'])
                if placed:
                    break
                # (b) D-layer but wrong orientation/slot
                if self.cube.faces['D'][dside[0]][dside[1]] == 'W':
                    self.apply_moves([face, face])
                    continue
                # (c) Middle layer extraction – left/right edges
                middle_found = False
                if self.cube.faces[face][1][0] == 'W':
                    opp = {'F':'L', 'R':'F', 'B':'R', 'L':'B'}
                    self.apply_moves([opp[face]+"'", 'U', face, "U'"])
                    middle_found = True
                elif self.cube.faces[face][1][2] == 'W':
                    opp = {'F':'R', 'R':'B', 'B':'L', 'L':'F'}
                    self.apply_moves([opp[face], "U'", face+"'", 'U'])
                    middle_found = True
                if middle_found:
                    continue
                # (d) Bottom layer, misaligned (other D positions)
                for f in ['F', 'R', 'B', 'L']:
                    for pos in [(0, 1), (1, 0), (1, 2), (2, 1)]:
                        if self.cube.faces['D'][pos[0]][pos[1]] == 'W':
                            for _ in range(4):
                                if (f == face) and (pos == dside):
                                    break
                                self.apply_moves(['D'])
                            self.apply_moves([face, face])
                            break
        # Final alignment to centers (rarely needed)
        for _ in range(4):
            for face, _, _, dside in target_edges:
                if self.cube.faces['D'][dside[0]][dside[1]] == 'W':
                    while self.cube.faces[face][2][1] != self.cube.faces[face][1][1]:
                        self.apply_moves(['D'])
                    break
        print('✅ White cross complete')

    def solve_white_corners(self):
        print("ℹ️ Solving bulletproof white corners")
        corner_targets = [
            (('F', 'R'), (0, 2), ["R'", "D'", "R"]),
            (('R', 'B'), (2, 2), ["B'", "D'", "B"]),
            (('B', 'L'), (2, 0), ["L'", "D'", "L"]),
            (('L', 'F'), (0, 0), ["F'", "D'", "F"]),
        ]
        for (f1, f2), (dr, dc), algo in corner_targets:
            for tries in range(18):
                colors = [
                    self.cube.faces['D'][dr][dc],
                    self.cube.faces[f1][2][0],
                    self.cube.faces[f2][2][2],
                ]
                centers = [self.cube.faces[f1][1][1], self.cube.faces[f2][1][1]]
                dest = ['W', centers[0], centers[1]]
                if sorted(colors) == sorted(dest) and self.cube.faces['D'][dr][dc] == 'W':
                    break
                if self.cube.faces['D'][dr][dc] == 'W':
                    self.apply_moves(algo)
                    continue
                found = False
                for _ in range(4):
                    corner = [self.cube.faces['U'][2][2], 
                              self.cube.faces[f1][0][2], 
                              self.cube.faces[f2][0][0]]
                    if 'W' in corner:
                        maxu = 0
                        while not (self.cube.faces[f1][1][1] == centers[0] and 
                                   self.cube.faces[f2][1][1] == centers[1]) and maxu < 4:
                            self.apply_moves(['U'])
                            maxu += 1
                        for _ in range(3):
                            if self.cube.faces['D'][dr][dc] != 'W':
                                self.apply_moves(algo)
                            else:
                                break
                        found = True
                        break
                    self.apply_moves(['U'])
                if found:
                    break
        print("✅ White corners complete")

    def solve_middle_layer(self):
        print("ℹ️ Solving middle layer")

        def is_middle_layer_solved():
            # Check if middle layer edges are aligned properly
            left = self.cube.faces['L'][1][2]
            front = self.cube.faces['F'][1][0]
            right = self.cube.faces['R'][1][0]
            back = self.cube.faces['B'][1][2]
            return left != 'Y' and front != 'Y' and right != 'Y' and back != 'Y'

        attempts = 0
        while attempts < 4:
            for _ in range(4):
                edge = self.cube.faces['U'][1][2]  # top-front edge
                color1 = self.cube.faces['U'][1][1]
                color2 = self.cube.faces['F'][0][1]

                # Insert right
                if color1 in self.side_colors and color2 in self.side_colors:
                    self.apply_moves(["U", "R", "U'", "R'", "U'", "F'", "U", "F"])
                # Insert left
                elif color1 in self.side_colors and color2 in self.side_colors:
                    self.apply_moves(["U'", "L'", "U", "L", "U", "F", "U'", "F'"])
                else:
                    self.apply_moves(["U"])

            if is_middle_layer_solved():
                print("✅ Middle layer complete")
                return
            attempts += 1

        print("⚠️ Middle layer — still incomplete after fix")










    def align_u_edge(self, color1, color2):
        # Rotate U until the front center matches either of the colors
        for _ in range(4):
            front_center = self.cube.faces['F'][1][1]
            top_edge = self.cube.faces['U'][2][1]
            if top_edge == color1 or top_edge == color2:
                if front_center == color1 or front_center == color2:
                    return
            self.cube.move("U")




    def solve_yellow_cross(self):
        print("ℹ️ Advanced yellow cross phase")

        def get_yellow_edges():
            u = self.cube.faces['U']
            return [
                u[0][1] == 'Y',  # Top
                u[1][0] == 'Y',  # Left
                u[1][2] == 'Y',  # Right
                u[2][1] == 'Y'   # Bottom
            ]

        for _ in range(4):  # Max 4 attempts
            edges = get_yellow_edges()
            count = sum(edges)
            if count == 4:
                break  # Yellow cross complete
            elif edges[1] and edges[2]:  # L-shape
                self.apply_moves(["F", "U", "R", "U'", "R'", "F'"])
            elif edges[0] and edges[2]:  # Line
                self.apply_moves(["F", "R", "U", "R'", "U'", "F'"])
            else:  # Dot case
                self.apply_moves(["F", "R", "U", "R'", "U'", "F'"])

        print("✅ Yellow cross complete")

          


    def position_yellow_corners(self):
        print("ℹ️ Yellow corner positioning")
        self.apply_moves(["U", "R", "U'", "L'", "U", "R'", "U'", "L"])
        print("✅ Yellow corners positioned")

    def orient_yellow_corners(self):
        print("ℹ️ Orienting yellow corners")
        attempts = 0

        def all_oriented():
            up_face = self.cube.faces['U']
            corners = [up_face[0][0], up_face[0][2], up_face[2][0], up_face[2][2]]
            return all(color == 'Y' for color in corners)

        while not all_oriented() and attempts < 6:
            for _ in range(4):
                corner = self.cube.faces['U'][2][2]  # UFR corner
                if corner != 'Y':
                    self.apply_moves(["R'", "D'", "R", "D"])
                    self.apply_moves(["R'", "D'", "R", "D"])
                    self.apply_moves(["R'", "D'", "R", "D"])
                self.apply_moves(["U"])
            attempts += 1

        if all_oriented():
            print("✅ Yellow corner orientation complete")
        else:
            print("⚠️ Yellow corner orientation — failed")








    def final_edge_permutation(self):
        print("ℹ️ Final edge positioning")
        for _ in range(4):
            front = self.cube.faces['F'][1][1]
            right = self.cube.faces['R'][1][1]
            if (self.cube.faces['F'][0][1] == front and
                self.cube.faces['R'][0][1] == right):
                break
            self.apply_moves(["U"])
        # U-Perm (clockwise 3-edge cycle)
        self.apply_moves(["R", "U", "R'", "U", "R", "U2", "R'", "U"])
        self.apply_moves(["R'", "F", "R'", "B2", "R", "F'", "R'", "B2", "R2"])

        print("✅ Final edge positioning complete")


    def solve(self):
        print(f"ℹ️ Scramble — {' '.join(self.scramble)}")
        self.apply_moves(self.scramble)
        self.solve_white_cross()
        self.solve_white_corners()
        self.solve_middle_layer()
        self.solve_yellow_cross()
        self.position_yellow_corners()
        self.orient_yellow_corners()
        self.final_edge_permutation()
        

        print("\n🧩 Final Solution Moves:")
        print(" ".join(self.solution_moves))
        print("\n📦 Final Cube State:")
        print_cube_state(self.cube)
        if is_solved(self.cube):
            print("\n✅ Cube Solved")
        else:
            print("\n❌ Cube Not Solved")
if __name__ == '__main__':
    start = timer_start()
    solver = RubiksCubeSolver()  # Still works — no cube passed
    solver.solve()

    
    