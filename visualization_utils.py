def console_displaying(map):
    h, w = map.shape
    for i in range(h):
        for j in range(w):
            print(map[i][j], end=' ')
        print('')
