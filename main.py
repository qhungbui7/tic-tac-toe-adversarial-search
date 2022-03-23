from visualization_utils import *
from gameplay import play_game
import numpy as np




if __name__ == '__main__':
    print('You go first, X for you, O for the bot')
    exit_game = False
    while not exit_game: 
        play_game()
        cmd = input('Wanna play again ? Y/N\n>>')
        if cmd == 'N':
            exit_game = True

