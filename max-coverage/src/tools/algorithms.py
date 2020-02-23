import random
import numpy as np

from utlis.data import get_mask
from utlis.data import get_binary_array_with_sum
from utlis.data import convert_numpy


# nums: the numbers of sub-set selected
# data: the input data
def random_coverage(nums, data):
    cover = []
    covered = set()
    for i in range(nums):
        # Get a sub-set from input data randomly
        r = data.pop(random.randint(0, len(data)-1))

        # Append selected sub-set elements into the cover
        # array, the repeat element will be removed.
        cover.append(r)

        # |= is to | as += is to +, i.e. a combination of
        # operation and asignment.
        covered |= r
    return cover, covered


# nums: the numbers of sub-set selected
# data: the input data
def greedy_max_coverage(nums, data):
    covered = set()
    cover = []
    for i in range(nums):
        max_subset = max(data, key=lambda x: len(x - covered))
        cover.append(max_subset)
        covered |= max_subset
    return cover, covered


# nums: the numbers of sub-set selected
# data: the input data, should be a list, rather a set
def pipage_rounding(nums, data):
    data = convert_numpy(data)
    universe = np.unique(data)  # A 1D numpy array k*1
    mask = get_mask(data,universe)

    # m: the total number of unique elements in [[data]]
    m = universe.shape[0]
    # n: the total number of elements in data
    n = data.shape[0]
    # x_vector = np.random.randint(2, size=n)

    # x: A fractional x in [0,1]^n, where n is len(data)
    def function(x):
        total = 0
        for i in range(0, m):
            mul = 1
            for j in range(0, n):
                if mask[j, i]:
                    mul = mul * (1 - x[j])
            total += (1 - mul)
        return total

    # x: A fractional x in [0,1]^n, where n is len(data)
    # p: A polytope, that is P = {x in [0,1]^n, 1 =< j <= n: sum x_j = k} where n is len(data)
    # f: A object function F(x) to evaluate F(x), F(x+ad), F(x-bd).
    def run(f):
        possible_solution = np.array(get_binary_array_with_sum(n,nums))
        nums_solutions = possible_solution.shape[0] % n

        x = possible_solution[np.random.randint(0, nums_solutions)]
        p = np.random.randint(0, nums_solutions)
        e_p = possible_solution[p]
        q = np.random.randint(0, nums_solutions)
        e_q = possible_solution[q]

        # x = np.pad(np.ones(nums, dtype=int), (0, n - nums), 'constant', constant_values=0)
        # np.random.shuffle(x)
        for i in range(0, n):
            # e_p = np.pad(np.ones(nums, dtype=int), (0, n - nums), 'constant', constant_values=0)
            # e_q = np.pad(np.ones(nums, dtype=int), (0, n - nums), 'constant', constant_values=0)
            # np.random.shuffle(e_p)
            # np.random.shuffle(e_q)
            d_x = e_p - e_q
            alpha_x = min(1 - x[p], x[q])
            beta_x = min(1 - x[q], x[p])
            x1 = x + alpha_x * d_x
            x2 = x - beta_x * d_x
            if f(x1) >= f(x):
                x = x1
            else:
                x = x2
        return x
    return run(function)

# # nums: the numbers of sub-set selected
# # # data: the input data, should be a list, rather a set
# # def pipage_rounding(nums, data):
# #     # x: A fractional x in [0,1]^n, where n is len(data)
# #     # p: A polytope, that is P = {x in [0,1]^n, 1 =< j <= n: sum x_j = k} where n is len(data)
# #     # f: A object function F(x) to evaluate F(x), F(x+ad), F(x-bd).
# #     def run(x, f):
# #         b = np.random.randint(2, size=(n, 2*n))
# #         matriod = Matroid(Matrix(GF(2), b))
# #         bases = matriod.bases()
# #         length = len(bases)
# #         a, b = np.random.randint(0, length, 2)
# #         if a == b:
# #             b = (a + b) % length
# #         p = np.array(Matrix(bases[a]) % 2)
# #         q = np.array(Matrix(bases[b]) % 2)
# #         d_x = p - q
# #         alpha_x = min(1-x[a], x[b])
# #         beta_x = min(1-x[b], x[a])
# #         for i in range(0, n):
# #             x1 = x + alpha_x * d_x
# #             x2 = x - beta_x * d_x
# #             if f(x1) >= f(x):
# #                 x = x1
# #             else:
# #                 x = x2
# #
# #         return x
# #
# #     # x: A fractional x in [0,1]^n, where n is len(data)
# #     def function(x):
# #         total = 0
# #         for i in range(0, m):
# #             ele = universe[i]
# #             mul = 1
# #             for j in range(0,n):
# #                 ele_set = data[j]
# #                 if ele in ele_set:
# #                    mul **= (1 - x[j])
# #             total += (1 - mul)
# #         return total
# #
# #     universe = list(set(itertools.chain(*data)))
# #     # m: the total number of unique elements in [[data]]
# #     m = len(universe)
# #     # n: the total number of elements in data
# #     n = len(data)
# #     x_vector = np.random.randint(2, size=n)
# #     return run(x_vector, function)

