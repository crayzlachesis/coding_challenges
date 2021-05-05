grid_base = [" +-+   ",
" | |   ",
" ++++  ",
" ++++  ",
"X+++   ",
"  +---X"]


def split(word):
	return [char for char in word]

# describing constants

symbols = ("X", "+", "-", "|")
valid_horizontal = ('+', '-', 'X')
valid_vertical = ('+', '|', 'X')
valid_corner_left_right = ('X', '-', '+')
valid_corner_up_down = ('|', 'X', '+')
valid_endpoint_left_right = ('+', '-', 'X')
valid_endpoint_up_down = ('+', '|', 'X')

h = lengthX = len(grid_base)
w = lengthY = len(split(grid_base[0]))
visited = {}
start_end = []
list_multipoints = []


# Generating 2D array from string grid


grid = [["0" for x in range(w)] for y in range(h)]

for x in range(len(grid_base)):
	chars = split(grid_base[x])
	for y in range(len(chars)):
		grid[x][y] = chars[y]


def walk_the_line(grid):
	s_row, s_col = create_visited_dict(grid)

	print('Initial visited list:')
	for x, y in visited.items():
		print(x, y)

	if len(start_end) != 2:
		return False
	#print("starting point: "+s_row, s_col)
	direction = "zero"

	go_go(grid, s_row, s_col, direction)
	print("final visited list")
	for x, y in visited.items():
		print(x, y)

	if validate_visited(visited):
		return True
	else:
		return False

def validate_visited(visited):
	has_unvisited = False
	for x in visited.values():
		if x == "unvisited":
			has_unvisited = True

	if has_unvisited:
		return False
	else:
		return True

def create_visited_dict(grid):
	check_x = 0
	for row in range(h):
		for col in range(w):
			current = grid[row][col]
			if current in symbols:
				current_tostring = str(row) + ":" + str(col)
				if current == 'X':
					if check_x == 0:
						check_x = 1
						s_row = row
						s_col = col
					start_end.append(current_tostring)

				visited[current_tostring] = "unvisited"



	return s_row, s_col


def go_go(grid, row, col, direction):
	current_value = grid[row][col]
	current_tostring = str(row) + ":" + str(col)
	#print("current_element" + current_tostring)
	#print(current_value)
	if current_tostring == start_end[1]:
		#print("found end-point, exiting recursion")
		visited[current_tostring] = "visited"
		return True
	else:
		visited[current_tostring] = "visited"
		next_moves = scan_moves(grid, row, col, direction)

		if len(next_moves) == 0:
			return False
		else:
			if len(next_moves) == 2:

				if next_moves[0] == "right":
					move_a = check_path(grid, row, col + 1, next_moves[0])
				if next_moves[0] == "left":
					move_a = check_path(grid, row, col - 1, next_moves[0])
				if next_moves[0] == "up":
					move_a = check_path(grid, row - 1, col, next_moves[0])
				if next_moves[0] == "down":
					move_a = check_path(grid, row + 1, col, next_moves[0])
				if next_moves[1] == "right":
					move_b = check_path(grid, row, col + 1, next_moves[1])
				if next_moves[1] == "left":
					move_b = check_path(grid, row, col - 1, next_moves[1])
				if next_moves[1] == "up":
					move_b = check_path(grid, row - 1, col, next_moves[1])
				if next_moves[1] == "down":
					move_b = check_path(grid, row + 1, col, next_moves[1])

				if move_a == False and move_b == True:
					next_moves[0] = next_moves[1]
				elif move_b == "Ambi" and move_a == False:
					next_moves[0] = next_moves[1]
				elif move_a == "Ambi" and move_b == True:
					next_moves[0] = next_moves[1]


			move = next_moves[0]
			if move == "right":
				return go_go(grid, row, col+1, move)
			if move == "left":
				return go_go(grid, row, col - 1, move)
			if move == "up":
				return go_go(grid, row - 1, col, move)
			if move == "down":
				return go_go(grid, row + 1, col, move)


def check_path(grid, row, col, direction):
	current_value = grid[row][col]
	current_tostring = str(row) + ":" + str(col)
	if current_tostring == start_end[1]:
		return True
	else:
		next_moves = scan_moves(grid, row, col, direction)
		if len(next_moves) == 0:
			return False
		else:
			if len(next_moves) == 2:
				return "Ambi"
			move = next_moves[0]
			if move == "right":
				return check_path(grid, row, col + 1, move)
			if move == "left":
				return check_path(grid, row, col - 1, move)
			if move == "up":
				return check_path(grid, row - 1, col, move)
			if move == "down":
				return check_path(grid, row + 1, col, move)


def scan_moves(grid, row, col, prevMove):

	current_symbol = grid[row][col]
	current_tostring = str(row) + ":" + str(col)
	left = right = up = down = None
	possible_directions = []
	l_r = ("left", "right")
	u_d = ("up", "down")
	if col > 0:
		left = grid[row][col-1]
		left_dict = str(row) + ":" + str(col-1)
	if col < lengthY -1:
		right = grid[row][col+1]
		right_dict = str(row) + ":" + str(col+1)
	if row > 0:
		up = grid[row-1][col]
		up_dict = str(row-1) + ":" + str(col)
	if row < lengthX-1:
		down = grid[row+1][col]
		down_dict = str(row+1) + ":" + str(col)

	if current_symbol == "-":
		if left is not None and left in valid_horizontal and visited[left_dict] == "unvisited" and prevMove != "right":
			possible_directions.append("left")
		if right is not None and right in valid_horizontal and visited[right_dict] == "unvisited" and prevMove != "left":
			possible_directions.append("right")

	if current_symbol == "|":
		if up is not None and up in valid_vertical and visited[up_dict] == "unvisited" and prevMove != "down":
			possible_directions.append("up")
		if down is not None and down in valid_vertical and visited[down_dict] == "unvisited" and prevMove != "up":
			possible_directions.append("down")

	if current_symbol == "X":
		if left is not None and left in valid_endpoint_left_right and visited[left_dict] == "unvisited":
			possible_directions.append("left")
		if right is not None and right in valid_endpoint_left_right and visited[right_dict] == "unvisited":
			possible_directions.append("right")
		if up is not None and up in valid_endpoint_up_down and visited[up_dict] == "unvisited":
			possible_directions.append("up")
		if down is not None and down in valid_endpoint_up_down and visited[down_dict] == "unvisited":
			possible_directions.append("down")

	if current_symbol == "+":

		if left is not None and left in valid_corner_left_right and visited[left_dict] == "unvisited" and prevMove not in l_r:
			possible_directions.append("left")
		if right is not None and right in valid_corner_left_right and visited[right_dict] == "unvisited" and prevMove not in l_r:
			possible_directions.append("right")
		if up is not None and up in valid_corner_up_down and visited[up_dict] == "unvisited" and prevMove not in u_d:
			possible_directions.append("up")
		if down is not None and down in valid_corner_up_down and visited[down_dict] == "unvisited" and prevMove not in u_d:
			possible_directions.append("down")

	return possible_directions

print(walk_the_line(grid))