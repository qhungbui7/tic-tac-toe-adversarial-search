from visualization_utils import *
import numpy as np
from bot import bot_random_move 

PLAYER_NOTATION = 1
BOT_NOTATION = 2

class GameConfigure: 
    def __init__(self):
        self.map_game = np.zeros((4,4), dtype='int')
        self.is_playing = True
        self.count_moves = 0
        for i in range(1,4):
            self.map_game[0][i] = i
            self.map_game[i][0] = i
        self.check_win_range = [
            [(0,2), (0,1), (0,0)],
            [(2,0), (1,0), (0,0)],
            [(2,2), (1,1), (0,0)],
        ]
        self.moves_saving_dir = 'moves.txt'
    def reset_config(self):
        self.map_game = np.zeros((4,4), dtype='int')
        self.is_playing = True
        self.count_moves = 0
        for i in range(1,4):
            self.map_game[0][i] = i
            self.map_game[i][0] = i
    

def move_and_check_valid(x, y, game_map, notation):
    if x >= 1 and x <= 3 and y >= 1 and y <= 3 and game_map[y][x] == 0:
        game_map[y][x] = notation
        return True, game_map
    return False, game_map 


def check_win(game_map, notation, directions):
    for i in range(1, 4): # height 
        for j in range(1, 4): # width
            if game_map[i][j] == notation:
                for direction in directions:
                    check = True
                    for adds_x, adds_y in direction:
                        if i + adds_y > 3 or j + adds_x > 3 or game_map[i + adds_y][j + adds_x] != notation:
                            check = False
                            break
                    if check:
                        return True 
    return False



def play_game():
    config = GameConfigure()

    console_displaying(config.map_game)
    while config.is_playing == True: 
        config.count_moves += 1
        while True:
            print('Your\'s turn')
            x = int(input('Enter the X coordinate (1-3): '))
            y = int(input('Enter the Y coordinate (1-3): '))
            is_valid_move, temporary_map = move_and_check_valid(x, y, config.map_game, PLAYER_NOTATION)
            if is_valid_move:
                config.map_game = temporary_map
                console_displaying(config.map_game)
                break
            else: 
                print('Invalid move, please re-input the coordinate!')
                


        if check_win(config.map_game, PLAYER_NOTATION, config.check_win_range):
            print('You win!')
            config.is_playing = False
            return

        if config.count_moves == 9:
            print('Draw !')
            return

        
        config.count_moves += 1
        print('Bot\'s turn')
        config.map_game, x, y = bot_random_move(config.map_game, BOT_NOTATION)
        print ('Bot makes a move to (x, y) : ({}, {})'.format(x, y))
        console_displaying(config.map_game)


        if check_win(config.map_game, BOT_NOTATION, config.check_win_range):
            print('Bot win!')
            config.is_playing = False
            return
        
        