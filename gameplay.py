from visualization_utils import *
import numpy as np
from bot import bot_random_move , initialize_strategy, bot_strategy
from utils import convert_to_singular

PLAYER_NOTATION = 1
BOT_NOTATION = 2

class GameConfigure: 
    def __init__(self):
        self.map_game = np.zeros((3,3), dtype='int')
        self.is_playing = True
        self.count_moves = 0
        self.history = np.array([])

        # constants 
        self.epsilon = 0.0001

        self.check_win_range = [
            [(0,2), (0,1), (0,0)],
            [(2,0), (1,0), (0,0)],
            [(2,2), (1,1), (0,0)],
            [(-2,2), (-1,1), (0,0)],
        ]
        self.moves_saving_dir = 'moves.txt'
        self.generated_moves = None
        self.generated_labels = None
        self.limit = None

    def update_generated_by_history(self):
        sing = self.history[len(self.history) - 1]
        self.limit = self.limit[self.generated_moves[:, self.count_moves - 1] == sing].copy()
        self.generated_labels = self.generated_labels[self.generated_moves[:, self.count_moves - 1] == sing].copy()
        self.generated_moves = self.generated_moves[self.generated_moves[:, self.count_moves - 1] == sing].copy()

    

def move_and_check_valid(x, y, game_map, notation):
    if x >= 0 and x <= 2 and y >= 0 and y <= 2 and game_map[y][x] == 0:
        game_map[y][x] = notation
        return True, game_map
    return False, game_map 


def check_win(game_map, notation, directions):
    for i in range(0, 3): # height 
        for j in range(0, 3): # width
            if game_map[i][j] == notation:
                for direction in directions:
                    check = True
                    for adds_x, adds_y in direction:
                        if i + adds_y < 0 or j + adds_x < 0 or i + adds_y > 2 or j + adds_x > 2 or game_map[i + adds_y][j + adds_x] != notation:
                            check = False
                            break
                    if check:
                        return True 
    return False






def play_game():
    pygame.init()
    print('Initializing the game...')
    config = GameConfigure()
    # config.generated_moves, config.generated_labels, config.limit = initialize_strategy()
    config.generated_moves = np.loadtxt('moves.txt').astype('int')
    config.generated_labels = np.loadtxt('labels.txt').astype('int')
    config.limit = np.loadtxt('limit.txt').astype('int') 
    

    img = pygame.image.load('tic-tac-toe.png')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_icon(img)
    pygame.display.set_caption('Tic Tac Toe versus James - the unbeatable bot')
    screen.fill(BG_COLOR)

    board = np.zeros((BOARD_ROWS, BOARD_COLS)) # config
    draw_lines(screen)

    print('Initialization done !')
    # console_displaying(config.map_game)
    draw_figures(screen, config.map_game) # initially display
    pygame.display.update()
    while True: 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                sys.exit()    
            if event.type == pygame.MOUSEBUTTONDOWN and config.is_playing: 
                print('Your\'s turn')
                # while True:
                mouseX = event.pos[0] # x
                mouseY = event.pos[1] # y

                x = int(mouseX // SQUARE_SIZE)
                y = int(mouseY // SQUARE_SIZE)

                
                is_valid_move, temporary_map = move_and_check_valid(x, y, config.map_game, PLAYER_NOTATION)
                if is_valid_move:
                    config.count_moves += 1
                    config.history = np.append(config.history, convert_to_singular(x, y))
                    config.update_generated_by_history()
                    config.map_game = temporary_map
                    # console_displaying(config.map_game)
                    draw_figures(screen, config.map_game)
                    pygame.display.update()
                    # break
                else: 
                    print('Invalid move, please re-input the coordinate!')
                    continue
                        

                if check_win(config.map_game, PLAYER_NOTATION, config.check_win_range):
                    print('You win!')
                    config.is_playing = False
                    break
                if config.count_moves == 9:
                    print('Draw !')
                    config.is_playing = False
                    break

                
                
                print('Bot\'s turn')

                

                # config.map_game, x, y = bot_random_move(config.map_game, BOT_NOTATION)
                x, y = bot_strategy(BOT_NOTATION, config)
                print ('Bot makes a move to (x, y) : ({}, {})'.format(x, y))
                draw_figures(screen, config.map_game)
                pygame.display.update()
                if check_win(config.map_game, BOT_NOTATION, config.check_win_range):
                    print('Bot win!')
                    config.is_playing = False
                    break
                    
    
                
        