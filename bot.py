import random
import numpy as np
from generate_moves import generate_moves_with_labels
from utils import convert_to_singular


def initialize_strategy():
    return generate_moves_with_labels()


def bot_random_move(game_map, notation):
    x = random.randint(0, 2)
    y = random.randint(0, 2)
    while game_map[y][x] != 0:
        x = random.randint(0, 2)
        y = random.randint(0, 2)
    game_map[y][x] = notation
    return game_map, x, y


def bot_strategy(notation, config):

    temporary_history = config.history.copy()
    argminX, argminY = 0, 0
    argmin_moves = None
    minimum_loss = float('inf')

    config.count_moves += 1

    for i in range(0,3):
        for j in range(0,3):
            sing = convert_to_singular(j, i) # x is j, y is i
            if config.map_game[i][j] == 0: 
                
                temp_history = np.append(temporary_history, sing)
                temp_gen_moves = config.generated_moves[config.generated_moves[:, config.count_moves - 1] == sing]
                temp_gen_labels = config.generated_labels[config.generated_moves[:, config.count_moves - 1] == sing]
                temp_gen_lim = config.limit[config.generated_moves[:, config.count_moves - 1] == sing]
                
                
                # need to eliminate that is the same within the limit
                # exp = 5
                # print('Move ', sing)
                # print(min(temp_gen_lim[temp_gen_labels == 2] - config.count_moves + config.epsilon)**5) # error in the count_moves
                # truth = (temp_gen_lim - config.count_moves == 0) & (temp_gen_labels == 2)
                # print(temp_gen_moves[truth])
                # print(temp_gen_lim[truth])
                # print(temp_gen_labels[truth])
                # print(temp_gen_moves[((temp_gen_lim - config.count_moves == 0) & (temp_gen_labels == 2)).all()])
                print((3 * np.sum(1 / (temp_gen_lim[temp_gen_labels == 2] - config.count_moves + config.epsilon)**5)))
                print((1 * np.sum(1 / (temp_gen_lim[temp_gen_labels == 0] - config.count_moves + config.epsilon)**5)))
                print((4 * (np.sum(1 / (temp_gen_lim[temp_gen_labels == 1] - config.count_moves + config.epsilon)**5) - 1)))

                loss_function = -(3 * np.sum(1 / (temp_gen_lim[temp_gen_labels == 2] - config.count_moves + config.epsilon)**5) + \
                1 * np.sum(1 / (temp_gen_lim[temp_gen_labels == 0] - config.count_moves + config.epsilon)**5)  + \
                -4 * (np.sum(1 / (temp_gen_lim[temp_gen_labels == 1] - config.count_moves + config.epsilon)**5) - 1))

                print(loss_function)        

                temp_history = np.delete(temporary_history, len(temporary_history) - 1)

                if loss_function < minimum_loss:
                    minimum_loss = loss_function
                    argminX, argminY = j, i
    print('Best loss: ', minimum_loss)
    print(argminX, argminY)
    config.map_game[argminY][argminX] = notation

    config.history = np.append(config.history, convert_to_singular(argminX, argminY))
    config.update_generated_by_history()
    return argminX, argminY
             

                





    