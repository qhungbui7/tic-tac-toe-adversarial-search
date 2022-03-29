import pygame, sys
import numpy as np

# Source code of Graphic User Interface of this application
# mainly references from this repo: https://github.com/AlejoG10/python-tictactoe-yt




# constant declaration

WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

RED = (255, 0, 0)
BG_COLOR = (100, 156, 253) # (28, 170, 156)
LINE_COLOR =  (62, 92, 220) # (100, 156, 199)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)


def console_displaying(map):
    for j in range(3):
        for i in range(3):
            print(map[j][i], end=' ')
        print('')


def visualization_gui():
    pygame.init()

    # setting config
    # source of the image: https://www.flaticon.com/free-icon/tic-tac-toe_1021366
    img = pygame.image.load('tic-tac-toe.png')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_icon(img)
    pygame.display.set_caption('Tic Tac Toe versus James - the unbeatable bot')
    screen.fill(BG_COLOR)

    board = np.zeros((BOARD_ROWS, BOARD_COLS))



    draw_lines(screen)

    player = 1 # first player - the player has notation 1
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over: # need to replace the function inside

                mouseX = event.pos[0] # x
                mouseY = event.pos[1] # y

                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_col = int(mouseX // SQUARE_SIZE)

                if available_square(board, clicked_row, clicked_col ):

                    mark_square(board, clicked_row, clicked_col, player )
                    if check_win(screen, board, player ):
                        game_over = True
                    player = player % 2 + 1 # player then bot then player again and again

                    draw_figures(screen, board)


        pygame.display.update()


def draw_lines(screen):
	pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
	pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)

	pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
	pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures(screen, board):
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == 1: # draw circle
				pygame.draw.circle( screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE//2 ), int( row * SQUARE_SIZE + SQUARE_SIZE//2)), CIRCLE_RADIUS, CIRCLE_WIDTH )
			elif board[row][col] == 2: # draw cross
				pygame.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH )	
				pygame.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH )

def mark_square(board, row, col, player): # mark the board to the notation, need to replace
	board[row][col] = player

def available_square(board, row, col): # check if the position is available, need to replace
	return board[row][col] == 0

def is_board_full(board): # need to replace, this function is not optimized yet
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == 0:
				return False

	return True

def check_win(screen, board, player): # 1 for player 2 for bot, need to replace
	# vertical win check
	for col in range(BOARD_COLS):
		if board[0][col] == player and board[1][col] == player and board[2][col] == player:
			draw_vertical_winning_line(screen, col, player)
			return True

	# horizontal win check
	for row in range(BOARD_ROWS):
		if board[row][0] == player and board[row][1] == player and board[row][2] == player:
			draw_horizontal_winning_line(screen, row, player)
			return True

	# asc diagonal win check
	if board[2][0] == player and board[1][1] == player and board[0][2] == player:
		draw_asc_diagonal(screen, player)
		return True

	# desc diagonal win chek
	if board[0][0] == player and board[1][1] == player and board[2][2] == player:
		draw_desc_diagonal(screen, player)
		return True

	return False

# draw winning line phase 

def draw_vertical_winning_line(screen, col, player):
	posX = col * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1: # player plays circle
		color = CIRCLE_COLOR
	elif player == 2: # bot plays cross
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (posX, 15), (posX, HEIGHT - 15), LINE_WIDTH )

def draw_horizontal_winning_line(screen, row, player):
	posY = row * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (15, posY), (WIDTH - 15, posY), WIN_LINE_WIDTH )

def draw_asc_diagonal(screen, player):
	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), WIN_LINE_WIDTH )

def draw_desc_diagonal(screen, player):
	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), WIN_LINE_WIDTH )

if __name__ == '__main__':
    visualization_gui()