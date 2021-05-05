from timeit import default_timer as timer

def find_missing_number(numbers, method):

	def sum_input_rek(numbers, index_low, index_hi):
		if index_low < index_hi:
			return numbers[index_low] + numbers[index_hi] + sum_input_rek(numbers, index_low+1, index_hi-1)
		elif index_low == index_hi:
			return numbers[index_low]
		else:
			return 0

	def sum_baseline_rek(value_low, value_hi):
		if value_low < value_hi:
			return value_low + value_hi + sum_baseline_rek(value_low + 1, value_hi - 1)
		elif value_low == value_hi:
			return value_low
		else:
			return 0

	def sum_input_seq(numbers, ceiling):
		sum_input = low = 0
		high = ceiling
		while low <= high:
			if low < high:
				sum_input += numbers[low] + numbers[high]
			else:
				sum_input += numbers[low]
			low += 1
			high -= 1
		return sum_input

	def sum_baseline_seq(ceiling):
		low = 1
		sum_base = 0
		high = ceiling
		while low < high:
			if low < high:
				sum_base += low + high
			else:
				sum_base += low
			low += 1
			high -= 1
		return sum_base

	def sum_mixed(numbers, ceiling):
		x = 0
		low = 1
		y = ceiling - 1
		high = ceiling+1
		real_sum = 0
		while low <= high:
			if x < y:
				real_sum -= numbers[x]+numbers[y]
			elif x == y:
				real_sum -= numbers[x]

			if low < high:
				real_sum += low + high
			else:
				real_sum += low
			x += 1
			low += 1
			high -= 1
			y -= 1
		return real_sum

	def max_select(numbers):
		maxmax = len(numbers)+1
		if min(numbers) != 1:
			return 1
		else:
			while maxmax >= 2:

				if max(numbers) == maxmax:
					numbers[maxmax-2] = 0
					maxmax -= 1
				else:
					return maxmax

	def max_multiply(numbers):
		length = len(numbers) + 1
		half = int(length / 2)
		if length % 2 == 0:
			return ((length + 1) * half) - sum(numbers)
		else:
			return (((length + 1) * half) + half + 1) - sum(numbers)


	if method == "rek":
		return sum_baseline_rek(1, len(numbers)+1) - sum_input_rek(numbers, 0, len(numbers)-1)
	elif method == "seq":
		return (sum_baseline_seq(len(numbers)+1)) - sum_input_seq(numbers, len(numbers)-1)
	elif method == "combined":
		return sum_mixed(numbers, len(numbers))
	elif method == "max":
		return max_select(numbers)
	elif method == "multiply":
		return max_multiply(numbers)

numbers = [2,3,4,5,6,7,8,9,10]


print(find_missing_number(numbers, "rek"))
print(find_missing_number(numbers, "seq"))
print(find_missing_number(numbers, "combined"))
print(find_missing_number(numbers, "max"))
print(find_missing_number(numbers, "multiply"))
