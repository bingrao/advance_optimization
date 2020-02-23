import random
import numpy as np
import itertools


# Gen a set of sub-sets data.
# nums:  the number of sub-sets in this set
# Output example with nums = 5
# [{191}, {169, 58}, {26, 11, 21, 174}, {176, 42}, {249, 122, 155, 124}]
def data_gen(nums):
	sets = []
	for i in range(nums):
		rand_sub_set = set()  # A sub set
		random_size_subset = random.randint(1, 9)
		for j in range(random_size_subset):
			# Generate an random number between 0 and 300
			# as an element in this sub-set
			rand_sub_set.add(random.randint(1, 300))
		# Add sub set to sets
		sets.append(rand_sub_set)
	return sets


def convert_numpy(data):
	print(len(data))
	a = list(map(list, data))
	b = np.zeros([len(a), len(max(a, key=lambda x: len(x)))], dtype=int)
	for i, j in enumerate(a):
		b[i][0:len(j)] = j
	return b


# nums: The number of total sub sets
def data_gen_numpy(nums):
	return convert_numpy(data_gen(nums))



# data: A 2D numpy array (m*n)
def get_mask(data):
	universe = np.unique(data)  # A 1D numpy array k*1
	mask = (universe == data[..., None]).any(axis=1)  # A 2D numpy m*k
	return mask


def get_mask(data, universe):
	mask = (universe == data[..., None]).any(axis=1)  # A 2D numpy m*k
	return mask


def get_binary_array(nums):
	return list(map(list, itertools.product([0,1],repeat=nums)))


def get_binary_array_with_sum(nums, sums):
	lst = get_binary_array(nums)
	reg = list(map(list, filter(lambda x: sum(x) == sums, lst)))
	return reg