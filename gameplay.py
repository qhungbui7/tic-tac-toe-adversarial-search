from visualization_utils import *
import numpy as np
from bot import bot_random_move , initialize_strategy, bot_strategy
from utils import convert_to_singular



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
    config.generated_moves = np.loadtxt('moves.txt').astype('int')
    config.generated_labels = np.loadtxt('labels.txt').astype('int')
    config.limit = np.loadtxt('limit.txt').astype('int') 
    

    img = pygame.image.load('tic-tac-toe.png')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.Font('freesansbold.ttf', 50)
    pygame.display.set_icon(img)
    pygame.display.set_caption('Tic Tac Toe versus James - the unbeatable bot')

    text_1 = font.render('Tic Tac Toe', True, CIRCLE_COLOR, BR_TEXT_COLOR)
    text_2 = font.render('F: play first', True, CIRCLE_COLOR, BR_TEXT_COLOR)
    text_3 = font.render('S: play second', True, CIRCLE_COLOR, BR_TEXT_COLOR)

    textRect_1 = text_1.get_rect()
    textRect_1.center = (300, 100)

    textRect_2 = text_2.get_rect()
    textRect_2.center = (300, 300)

    textRect_3 = text_3.get_rect()
    textRect_3.center = (300, 400)

    
    text_win = font.render('You win !', True, CIRCLE_COLOR, BR_TEXT_COLOR)
    text_lose = font.render('You lose !', True, CROSS_COLOR, BR_TEXT_COLOR)
    text_draw = font.render('Draw !', True, TEXT_COLOR, BR_TEXT_COLOR)
    
    textRect_win = text_win.get_rect()
    textRect_win.center = (300, 300)

    textRect_lose = text_lose.get_rect()
    textRect_lose.center = (300, 290)

    textRect_draw = text_draw.get_rect()
    textRect_draw.center = (300, 300)


    screen.fill(BG_COLOR)   
    screen.blit(text_1, textRect_1)
    screen.blit(text_2, textRect_2)
    screen.blit(text_3, textRect_3)
 
    pygame.display.update()

    print('Initialization done !')

    true_menu = True 
    first = True
    while true_menu: 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                sys.exit()  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    true_menu = False
                    break 
                if event.key == pygame.K_s:
                    true_menu = False
                    first = False
                    break 
                    

    
    screen.fill(BG_COLOR)
    draw_lines(screen)
    
    
    draw_figures(screen, config.map_game) # initially display
    pygame.display.update()

    if first == True:
        PLAYER_NOTATION = 1
        BOT_NOTATION = 2
        while True: 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    sys.exit()    
                if event.type == pygame.MOUSEBUTTONDOWN and config.is_playing: 
                    print('Your\'s turn')
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
                    else: 
                        print('Invalid move, please re-input the coordinate!')
                        continue
                            

                    if check_win(config.map_game, PLAYER_NOTATION, config.check_win_range):
                        print('You win!')
                        config.is_playing = False
                        screen.blit(text_win, textRect_win)
                        pygame.display.update()
                        break
                    if config.count_moves == 9:
                        print('Draw !')
                        config.is_playing = False
                        screen.blit(text_draw, textRect_draw)
                        pygame.display.update()
                        break
                    
                    print('Bot\'s turn')

                    x, y = bot_strategy(BOT_NOTATION, config)
                    print ('Bot makes a move to (x, y) : ({}, {})'.format(x, y))
                    draw_figures(screen, config.map_game)
                    pygame.display.update()
                    if check_win(config.map_game, BOT_NOTATION, config.check_win_range):
                        print('Bot win!')
                        config.is_playing = False
                        screen.blit(text_lose, textRect_lose)
                        pygame.display.update()
                        break
                    
    if first == False: # player plays secondly
        PLAYER_NOTATION = 2
        BOT_NOTATION = 1

        x, y = bot_strategy(BOT_NOTATION, config, bot_first=True)
        print ('Bot makes a move to (x, y) : ({}, {})'.format(x, y))
        draw_figures(screen, config.map_game)
        pygame.display.update()

        while True: 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    sys.exit()    
                if event.type == pygame.MOUSEBUTTONDOWN and config.is_playing: 
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
                        draw_figures(screen, config.map_game)
                        pygame.display.update()
                    else: 
                        print('Invalid move, please re-input the coordinate!')
                        continue
                            

                    if check_win(config.map_game, PLAYER_NOTATION, config.check_win_range):
                        print('You win!')
                        config.is_playing = False
                        screen.blit(text_win, textRect_win)
                        pygame.display.update()
                        break
                    if config.count_moves == 9:
                        print('Draw !')
                        config.is_playing = False
                        screen.blit(text_draw, textRect_draw)
                        pygame.display.update()
                        break

                    print('Bot\'s turn')


                    x, y = bot_strategy(BOT_NOTATION, config, bot_first=True)
                    print ('Bot makes a move to (x, y) : ({}, {})'.format(x, y))
                    draw_figures(screen, config.map_game)
                    pygame.display.update()
                    if check_win(config.map_game, BOT_NOTATION, config.check_win_range):
                        print('Bot win!')
                        config.is_playing = False
                        screen.blit(text_lose, textRect_lose)
                        pygame.display.update()
                        break
                    if config.count_moves == 9:
                        print('Draw !')
                        config.is_playing = False
                        screen.blit(text_draw, textRect_draw)
                        pygame.display.update()
                        break