from visualization_utils import *
import numpy as np


class GameConfigure: 
    def __init__(self):
        self.map_game = np.zeros((4,4), dtype='int')
        self.is_playing = True
        self.count_moves = 0
        for i in range(1,4):
            self.map_game[0][i] = i
            self.map_game[i][0] = i
    

def check_valid_move(x, y, game_map, notation):
    print(notation)
    if x >= 1 and x <= 3 and y >= 1 and y <= 3 and game_map[y][x] == 0:
        game_map[y][x] = notation
        return True, game_map
    return False, game_map 
    

def play_game():
    config = GameConfigure()

    while config.is_playing == True: 
        config.count_moves += 1
        console_displaying(config.map_game)
        x = int(input('Enter the X coordinate (1-3): '))
        y = int(input('Enter the Y coordinate (1-3): '))
        is_valid_move, temporary_map = check_valid_move(x, y, config.map_game, config.count_moves % 2 + 1)
        if is_valid_move:
            config.map_game = temporary_map
        else: 
            print('Invalid move, please re-input the coordinate!')
            continue
        

        # bot go here
        
        