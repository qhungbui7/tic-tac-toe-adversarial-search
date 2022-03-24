from gameplay import GameConfigure
import numpy as np
from tqdm import tqdm
from joblib import Parallel, delayed

class MovesConfigure:
    def __init__(self):
        self.ordinal_limit = 8
        self.generated_moves = []

def add_moves(history, storage):
    storage.append(history.copy())
    return storage
    
def brute_force(num, history, is_visisted, move_config, storage):
    for i in range(0, 9):
        x = i % 3
        y = i // 3
        if not is_visisted[y,x]:
            is_visisted[y,x] = True
            history.append(i)
            if num == move_config.ordinal_limit:
                add_moves(history, storage) 
            else:
                brute_force(num + 1, history, is_visisted, move_config, storage)
            history.pop(len(history) - 1)
            is_visisted[y][x] = False

if __name__ == '__main__':
    storage = []
    move_config = MovesConfigure()
    is_visisted = np.full((3,3), False)
    history = []
    brute_force(0, history, is_visisted, move_config, storage)
    print(storage[len(storage)-1])