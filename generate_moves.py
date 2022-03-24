from gameplay import GameConfigure
import numpy as np
from tqdm import tqdm
from joblib import Parallel, delayed

class MovesConfigure:
    def __init__(self):
        self.ordinal_limit = 8
        self.generated_moves = []
        self.generated_labels = []
        self.directions = [
            [(0,2), (0,1), (0,0)],
            [(2,0), (1,0), (0,0)],
            [(2,2), (1,1), (0,0)],
        ]
def add_moves(history, config):
    config.generated_moves.append(history.copy())
    game_map = np.zeros((3,3))
    for i in range(0, 9):
        x = history[i] % 3
        y = history[i] // 3
        game_map[y][x] = i % 2 + 1
        # print(game_map)
        if i >= 4:
            check = check_win_both(game_map, config.directions)  
            if check != 0: 
                config.generated_labels.append(check)
                return 
    config.generated_labels.append(0)
        

    
def check_win_both(game_map, directions):
    for notation in range(1, 3):
        for i in range(0, 3): # height 
            for j in range(0, 3): # width
                if game_map[i][j] == notation:
                    for direction in directions:
                        check = True
                        for adds_x, adds_y in direction:
                            if i + adds_y > 2 or j + adds_x > 2 or game_map[i + adds_y][j + adds_x] != notation:
                                check = False
                                break
                        if check:
                            return notation
    return 0 # draw

def brute_force(num, history, is_visisted, move_config):
    for i in range(0, 9):
        x = i % 3
        y = i // 3
        if not is_visisted[y,x]:
            is_visisted[y,x] = True
            history.append(i)
            if num == move_config.ordinal_limit:
                add_moves(history, move_config) 
            else:
                brute_force(num + 1, history, is_visisted, move_config)
            history.pop(len(history) - 1)
            is_visisted[y][x] = False

if __name__ == '__main__':
    move_config = MovesConfigure()
    is_visisted = np.full((3,3), False)
    history = []
    brute_force(0, history, is_visisted, move_config)
    print(move_config.generated_moves[len(move_config.generated_moves) - 1])
    print(move_config.generated_labels[len(move_config.generated_labels) - 1])


    # history = move_config.generated_moves[999]
    # print(move_config.generated_labels[999])

    # game_map = np.zeros((3,3))
    # for i in range(0, 9):
    #     x = history[i] % 3
    #     y = history[i] // 3
    #     game_map[y][x] = i % 2 + 1
    #     print(game_map)
    #     if i >= 4:
    #         check = check_win_both(game_map, move_config.directions)  
    #         if check != 0:
    #             print(check) 
    #             break
                
    
    