field =    [[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                 [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                 [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 1, 1, 1, 0, 0, 0, 0, 0, 0]]

baseline_ship_list = [1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4]

global length
length = len(field)
ship_list = []


def check_interference(arr):

    for row in range(length):
        for col in range(length):
            if arr[row][col] == 1:
                if not check_corners(row, col, arr):
                    return False

    return True


def check_corners(row, col, arr):

    if row == 0 and col == 0:  # top left
        if arr[row+1][col+1] == 1:
            return False
    elif row == length-1 and col == 0:  # bottom left
        if arr[row-1][col+1] == 1:
            return False
    elif row == 0 and col == length-1:  # top right
        if arr[row+1][col-1] == 1:
            return False
    elif row == length-1 and col == length-1:  # bottom right
        if arr[row-1][col-1] == 1:
            return False
    elif row == 0:  # topmost
        if arr[row+1][col-1] == 1 or arr[row+1][col+1] == 1:
            return False
    elif row == length - 1:  # bottommost
        if arr[row-1][col-1] == 1 or arr[row-1][col+1] == 1:
            return False
    elif col == 0:  # leftmost
        if arr[row-1][col+1] == 1 or arr[row+1][col+1] == 1:
            return False
    elif col == length - 1:  # rightmost
        if arr[row-1][col-1] == 1 or arr[row+1][col-1] == 1:
            return False
    else:  # everywhere within the boarders
        if arr[row+1][col+1] == 1 or arr[row-1][col+1] == 1 or arr[row+1][col-1] == 1 or arr[row-1][col-1] == 1:
            return False

    return True


def locate_ships(arr):
    for row in range(length):
        print("ROW: ", row)
        for col in range(length):
            print(col)
            if arr[row][col] == 1:
                collect_ship(row, col, arr)


def collect_ship(row, col, arr):
    ship_size_counter = 0

    def go_right(row, col, arr, ship_size_counter):
        while arr[row][col] == 1:
            ship_size_counter += 1
            arr[row][col] = 0
            col += 1
            if col == length:
                break

        ship_list.append(ship_size_counter)

    def go_down(row, col, arr, ship_size_counter):
        while arr[row][col] == 1:
            ship_size_counter += 1
            arr[row][col] = 0
            row += 1
            if row == length:
                break

        ship_list.append(ship_size_counter)

    def single_ship(row, col, arr, ship_size_counter):
        ship_size_counter = 1
        arr[row][col] = 0
        ship_list.append(ship_size_counter)

    if row < length - 1 and col < length - 1: # neither the row nor the column is at its maximum
        if arr[row+1][col] == 0 and arr[row][col+1] == 0:
            single_ship(row, col, arr, ship_size_counter)
        elif arr[row+1][col] == 1:
            go_down(row, col, arr, ship_size_counter)
        else:
            go_right(row, col, arr, ship_size_counter)

    elif row == length - 1 and col < length - 1:  # row is maxed, can only go right
        go_right(row, col, arr, ship_size_counter)
    elif row < length - 1 and col == length - 1:  # column is maxed out, can only go down
        go_down(row, col, arr, ship_size_counter)
    else:  # bottom right corner (wut? is this really needed?)
        ship_size_counter += 1
        arr[row][col] = 0
        ship_list.append(ship_size_counter)

def main_func(ship_array):
    if check_interference(ship_array):
        locate_ships(ship_array)
        if sorted(ship_list) == baseline_ship_list:
            #print("valid")
            return True
        else:
            #print("invalid")
            return False
    else:
        # print("invalid")
        return False


print(main_func(field))
