import random
def bot_random_move(game_map, notation):
    x = random.randint(1, 3)
    y = random.randint(1, 3)
    while game_map[y][x] != 0:
        x = random.randint(1, 3)
        y = random.randint(1, 3)
    game_map[y][x] = notation
    return game_map, x, y


def bot_strategy():
    pass


    