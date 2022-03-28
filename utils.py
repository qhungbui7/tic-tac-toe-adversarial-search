def convert_to_singular(x, y):
    return y * 3 + x
def concatenate_nparr_string(arr):
    result = ''
    for element in arr:
        result += str(element)
    return result     