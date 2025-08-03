from solver import RubiksCubeSolver
from utils import timer_start, timer_end

if __name__ == '__main__':
    start = timer_start()
    
    solver = RubiksCubeSolver()
    solver.solve()
    
    print(f"\n⏱️ Total Time: {timer_end(start)}s")
