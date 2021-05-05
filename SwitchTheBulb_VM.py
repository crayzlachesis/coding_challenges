import math
from timeit import default_timer as timer

### Inserting comment he

def switch_bulbs(game_map):

	def split(word):
		return [char for char in word]

	stack_coord = []
	stack_visited = []
	adj_list = []

	def unpack_input(map):  # unpack the map and generate the coord_list which contains the coordinates for each node
		coord_list = []
		words = map.split()
		x = y = 0

		for word in words[1:-1]:
			mychars = split(word[1:-1])
			y = 0
			for char in mychars:
				if char == "B":
					coord_list.append((x, y))
				y += 1
			x += 1
		return coord_list

	def build_adjacency_list(coord_list):  # generating an adjacency list for each node
		ind = 0
		for x, y in coord_list:
			index = (x, y)
			options = pre_scan(coord_list, index)
			if len(options) == 0:
				return False, adj_list
			adj_list.append(options)
		return True, adj_list

	def optimize_lists(coord_list, adj_list):  # ordering the coord list and the adjacency list based on number of guests for each node
		starter_list = []

		for i in range(len(coord_list)):  # creating list of tuples. 1st tuple: node, 2nd tuple: nr of guests
			starter_list.append((coord_list[i], len(adj_list[i])))
		
		starter_list.sort(key=lambda tup: tup[1])  # ordering above list by number of guests

		temp_list = []
		ind = 0
		starter_count = 8

		for mini_list in adj_list:
			if len(mini_list) < starter_count:
				starter_count = len(mini_list)
				starter_index = ind

			for x, y in mini_list:  # creating a list for each node, and ordering the guests for each based on their number of guests
				index_in_coords = coord_list.index((x, y))
				num_of_guests = len(adj_list[index_in_coords])
				temp_list.append(((x, y), num_of_guests))
			temp_list.sort(key=lambda tup: tup[1])
			ready_list = []

			for x, y in temp_list:
				ready_list.append(x)
			adj_list[ind] = ready_list.copy()
			ind += 1
			ready_list.clear()
			temp_list.clear()

		return starter_list, adj_list  # adj_list format: ordered together with coord_list(based on number of  guests), sub-lists ordered based on the same

	def t_seq(coord_list, index, visited, counter):  # main function to find a viable path for switching all the bulbs.
		finished = False
		final_length = len(coord_list)
		while not finished:
			counter += 1
			visited.append(index)
			if final_length == len(visited):
				return True, visited, counter
			else:
				options = new_scan_next(coord_list, index, visited)
				if len(options) == 1:
					index = options[0]
					continue
				elif len(options) == 0:
					if len(stack_coord) != 0:
						index = stack_coord.pop()
						visited = stack_visited.pop()
						continue
					else:
						return False, visited, counter
				else:
					index = options.pop(0)
					for x, y in options[::-1]:
						stack_coord.append((x, y))
						stack_visited.append(visited.copy())
					continue

	def new_scan_next(coord_list, index, visited):  # scanning the next element(s) for the current iteration of the t_seq() func
		options = []
		for x,y in adj_list[coord_list.index(index)]:
			if (x, y) not in visited:
				options.append((x, y))
		return options

	def pre_scan(coord_list, index):  # take the coord list and the current index to build the list of neighbours
		base_row, base_col = index  # unpacking the index tuple
		options_raw = []  # contains all the nodes that are intersecting with the current one
		options = []  # contains the final, ordered options list
		options_unordered = []  # same as above, but unordered
		for row, col in coord_list:  # populating the options_raw list
			x_diff = abs(row - base_row)
			y_diff = abs(col - base_col)
			if (row == base_row or col == base_col or x_diff == y_diff) and (abs(row-base_row) + abs(col-base_col) != 0):
				options_raw.append((row, col))

		options_temp = []
		while len(options_raw) != 0:  # iterating the raw list until a certain directions elements are all selected (ie: top right, bottom etc...)
			(xrow, xcol) = options_raw.pop(0)
			options_temp.clear()
			options_temp.append((xrow, xcol))
			current_element_type = check_type(base_row, base_col, xrow, xcol)
			for x, y in options_raw:
				if current_element_type == check_type(base_row, base_col, x, y):
					options_temp.append((x, y))

			for x, y in options_temp[1:]:  # removing the above selected from the raw list
				options_raw.remove((x, y))

			min_dist = 1000000
			for row, col in options_temp:  # calculating the closest element of these, that will be the direct neighbour for a given direction
				dist = math.sqrt(pow((row - base_row), 2) + pow((col - base_col), 2))
				if dist < min_dist:
					min_dist = dist
					min_tuple = (row, col)
			options.append(min_tuple)

		return options

	def check_type(base_row, base_col, row, col):  # simply checks the direction that a certain node is located
		if row == base_row:  # left or right
			if col < base_col:
				return "left"
			else:
				return "right"
		elif col == base_col:  # up or down
			if row < base_row:
				return "up"
			else:
				return "down"
		else:
			if row < base_row and col < base_col:
				return "topleft"
			if row > base_row and col < base_col:
				return "bottomleft"
			if row < base_row and col > base_col:
				return "topright"
			if row > base_row and col > base_col:
				return "bottomright"

	def main_func():  # this function is building up the context, and calling the t_seq as long as it's needed.
		visited = []

		coord_list = unpack_input(game_map)
		viable, adj_list = build_adjacency_list(coord_list)

		if not viable:
			print("found node with no connections, aborting execution.")
			return None

		starter_list, adj_list = optimize_lists(coord_list, adj_list)

		successful = False
		total_counter = counter = trial = 0
		sum_timer = 0
		z, guest_constant = starter_list[0]

		for starter_index, nr in starter_list:  # invoking bulb switching algorithm
			start = timer()
			if guest_constant < nr:
				break
			visited.clear()
			trial += 1
			successful, visited, counter = t_seq(coord_list, starter_index, visited, counter)
			total_counter += counter
			end = timer()
			sub_timer = end - start
			sum_timer += sub_timer
			print("Attempt: {}, Steps: {}, Sub-time: {}".format(trial, counter, sub_timer))
			if sum_timer > 2:
				break
			if successful:
				break

		if successful:
			print("Success! Total Steps: {}, Total Run-Time: {}".format(total_counter, sum_timer))
			return visited
		else:
			print("Failure! Total Steps: {}, Total Run-Time: {}".format(total_counter, sum_timer))
			return None

	return main_func()

GAME_MAPS = [
		"+--------+\n" +
		"|........|\n" +
		"|...B....|\n" +
		"|........|\n" +
		"|........|\n" +
		"|........|\n" +
		"|...B....|\n" +
		"|........|\n" +
		"|........|\n" +
		"+--------+",

		"+--------+\n" +
		"|........|\n" +
		"|...B....|\n" +
		"|........|\n" +
		"|.....B..|\n" +
		"|........|\n" +
		"|...B....|\n" +
		"|........|\n" +
		"|........|\n" +
		"+--------+",

		"+--------+\n" +
		"|........|\n" +
		"|...B....|\n" +
		"|........|\n" +
		"|........|\n" +
		"|........|\n" +
		"|...B....|\n" +
		"|........|\n" +
		"|.....B..|\n" +
		"+--------+",

		"+--------+\n" +
		"|........|\n" +
		"|...B....|\n" +
		"|.B......|\n" +
		"|........|\n" +
		"|........|\n" +
		"|...B....|\n" +
		"|........|\n" +
		"|.B...B..|\n" +
		"+--------+",

		"+--------+\n" +
		"|........|\n" +
		"|...B....|\n" +
		"|.B......|\n" +
		"|........|\n" +
		"|........|\n" +
		"|...BB...|\n" +
		"|........|\n" +
		"|.B...B..|\n" +
		"+--------+",

		"+--------+\n" +
		"|........|\n" +
		"|.B......|\n" +
		"|.B..B...|\n" +
		"|........|\n" +
		"|........|\n" +
		"|.B..B...|\n" +
		"|.B......|\n" +
		"|........|\n" +
		"+--------+",

		"+--------+\n" +
		"|...B....|\n" +
		"|........|\n" +
		"|.B......|\n" +
		"|......B.|\n" +
		"|......B.|\n" +
		"|.B......|\n" +
		"|......BB|\n" +
		"|BB......|\n" +
		"+--------+",

		"+--------+\n" +
		"|...BB...|\n" +
		"|........|\n" +
		"|..B..B..|\n" +
		"|....B...|\n" +
		"|....B...|\n" +
		"|..B.....|\n" +
		"|.B....B.|\n" +
		"|........|\n" +
		"+--------+",

		"+--------+\n" +
		"|........|\n" +
		"|.B.B..B.|\n" +
		"|........|\n" +
		"|.B..B.B.|\n" +
		"|........|\n" +
		"|.B.B..B.|\n" +
		"|........|\n" +
		"+--------+",

		"+----------+\n" +
		"|..........|\n" +
		"|..........|\n" +
		"|..........|\n" +
		"|..B.B....B|\n" +
		"|.B...B...B|\n" +
		"|.....B....|\n" +
		"|..........|\n" +
		"|.B......B.|\n" +
		"|....B.....|\n" +
		"|.B..BB..B.|\n" +
		"+----------+",

		"+--------+\n" +
		"|........|\n" +
		"|.BBBBBB.|\n" +
		"|.BBBBBB.|\n" +
		"|.BBBBBB.|\n" +
		"|.BBBBBB.|\n" +
		"|.BBBBBB.|\n" +
		"|.BBBBBB.|\n" +
		"|........|\n" +
		"+--------+",

		"+---------+\n" +
		"|.........|\n" +
		"|.B.B.B.B.|\n" +
		"|..B.B.B..|\n" +
		"|.B.B.B.B.|\n" +
		"|..B.B.B..|\n" +
		"|.B.B.B.B.|\n" +
		"|..B.B.B..|\n" +
		"|.B.B.B.B.|\n" +
		"|.........|\n" +
		"+---------+",

		"+---------+\n" +
		"|.B......B|\n" +
		"|.B.......|\n" +
		"|......B..|\n" +
		"|.........|\n" +
		"|....B....|\n" +
		"|.....B...|\n" +
		"|.........|\n" +
		"|.......B.|\n" +
		"|.........|\n" +
		"+---------+",

		"+---------+\n" +
		"|.........|\n" +
		"|...BBB...|\n" +
		"|..B...B..|\n" +
		"|......B..|\n" +
		"|.....B...|\n" +
		"|....B....|\n" +
		"|....B....|\n" +
		"|.........|\n" +
		"|....B....|\n" +
		"|.........|\n" +
		"+---------+",

		"+----------------+\n" +
		"|B.............B.|\n" +
		"|.B..........B...|\n" +
		"|................|\n" +
		"|..B........B....|\n" +
		"|....B.....B.....|\n" +
		"|.....B..B.......|\n" +
		"|.......B........|\n" +
		"|......B.........|\n" +
		"|......B.B.......|\n" +
		"|.....B....B.....|\n" +
		"|................|\n" +
		"|....B......B....|\n" +
		"|..B.........B...|\n" +
		"|.B............B.|\n" +
		"|................|\n" +
		"|B..............B|\n" +
		"+----------------+",

		"+--------+\n" +
		"|........|\n" +
		"|...B....|\n" +
		"|........|\n" +
		"|..B.....|\n" +
		"|........|\n" +
		"|...B....|\n" +
		"|........|\n" +
		"|........|\n" +
		"+--------+",  # no solution

		"+------------------+\n" +
		"|.B...B...B........|\n" +
		"|B.................|\n" +
		"|.....B.B.....B....|\n" +
		"|..............B...|\n" +
		"|..................|\n" +
		"|..............B...|\n" +
		"|.B.......B........|\n" +
		"|..................|\n" +
		"|..................|\n" +
		"|..................|\n" +
		"|.......B.B........|\n" +
		"|..................|\n" +
		"|..................|\n" +
		"|..................|\n" +
		"|..................|\n" +
		"|..B........B......|\n" +
		"|...............B..|\n" +
		"|..................|\n" +
		"|..................|\n" +
		"|..............B...|\n" +
		"|..................|\n" +
		"|..........B.......|\n" +
		"+------------------+",

		"+------------------------+\n" +
		"|.....................B..|\n" +
		"|........................|\n" +
		"|............B...........|\n" +
		"|........................|\n" +
		"|........................|\n" +
		"|......B....B.........B..|\n" +
		"|........................|\n" +
		"|...................B....|\n" +
		"|........................|\n" +
		"|........................|\n" +
		"|........B..B............|\n" +
		"|........................|\n" +
		"|........................|\n" +
		"|........B...............|\n" +
		"|B.......................|\n" +
		"|.B......................|\n" +
		"|.............BB....B....|\n" +
		"|............B.....B.....|\n" +
		"|.................B......|\n" +
		"|........................|\n" +
		"|........................|\n" +
		"|........................|\n" +
		"|........................|\n" +
		"|............B...........|\n" +
		"|........................|\n" +
		"|........................|\n" +
		"|........................|\n" +
		"|........................|\n" +
		"+------------------------+",

		"+--------------------+\n" +
		"|....B.....B.BBB..B..|\n" +
		"|.....B.B...BB.B.....|\n" +
		"|........B...B..B....|\n" +
		"|.......B.B.B..B.....|\n" +
		"|.............B......|\n" +
		"|.B.......B..........|\n" +
		"|..B.................|\n" +
		"|....................|\n" +
		"|....................|\n" +
		"|....................|\n" +
		"|...................B|\n" +
		"+--------------------+\n"

]

"""
def doit():
	for board in GAME_MAPS:
		start = timer()
		print(switch_bulbs(board))
		end = timer()
		print(end - start)
		print("---------------------")

doit()
"""
sample_maps = "+--------------------+\n" +  "|....B.....B.BBB..B..|\n" + "|.....B.B...BB.B.....|\n" + "|........B...B..B....|\n" + "|.......B.B.B..B.....|\n" + "|.............B......|\n" + "|.B.......B..........|\n" + "|..B.................|\n" + "|....................|\n" + "|....................|\n" + "|....................|\n" + "|...................B|\n" + "+--------------------+\n"

print(switch_bulbs(sample_maps))
