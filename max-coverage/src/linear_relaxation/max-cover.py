import numpy as np
from utlis.data import get_mask
from utlis.data import convert_numpy
from gurobipy import *

# https://www.gurobi.com/documentation/9.0/refman/py_model_addvars.html
def linear_guboric_vars(nums, input_data):
    data = convert_numpy(input_data)  # n*size_sub
    universe = np.unique(data)  # A 1D numpy array m*1
    mask = get_mask(data, universe) # n*m with true or false
    import time
    start = time.time()
    mask = mask.astype(int).T
    n = data.shape[0] # the size of subsets
    m = universe.shape[0] # the size of ground elements

    # Build model
    linear_model = Model()

    # add Variables
    z = linear_model.addVars(m, vtype=GRB.BINARY, name="z")
    x = linear_model.addVars(n, vtype=GRB.BINARY, name="x")

    # Lazy evaluation, need call this func to update value to variables
    linear_model.update()

    # add constraits
    linear_model.addConstr(quicksum(x[j] for j in range(n)) == nums)

    # x: A fractional x in [0,1]^n, where n is len(data)
    def function():
        total = 0
        for i in range(0, m):
            mul = 1
            for j in range(0, n):
                if mask[i,j]:
                    mul = mul * (1 - x[j])
            total += (1 - mul)
        return total

    for i in range(m):
        linear_model.addConstr(quicksum(x[j] for j in np.where(mask[i] == 1)[0]) >= z[i])

    linear_model.setObjective(quicksum(z[i] for i in range(m)), GRB.MAXIMIZE)

    linear_model.setParam('OutputFlag', 0)
    linear_model.optimize()
    end = time.time()

    print('----- Output -----')
    print('  Running time : %s seconds' % float(end - start))
    print('  Optimal coverage points: %g' % linear_model.objVal)

    covered = set()
    cover = []
    for i in range(len(x)):
        if int(x[i].X) == 1:
            cover.append(input_data[i])
            covered |= input_data[i]

    return cover, covered



def linear_guboric(nums, input_data):
    data = convert_numpy(input_data)  # n*size_sub
    universe = np.unique(data)  # A 1D numpy array m*1
    mask = get_mask(data, universe) # n*m with true or false
    import time
    start = time.time()
    mask = mask.astype(int).T
    n = data.shape[0] # the size of subsets
    m = universe.shape[0] # the size of ground elements

    # Build model
    linear_model = Model()

    # add Variables
    z = {}
    x = {}
    for i in range(m):
        z[i] = linear_model.addVar(vtype=GRB.BINARY, name="z%d " % i)
    for j in range(n):
        x[j] = linear_model.addVar(vtype=GRB.BINARY, name="x%d " % j)

    linear_model.update()

    # add constraits
    # linear_model.addConstr(quicksum(x[j] for j in range(n)) == nums)
    linear_model.addConstr(quicksum(x[j] for j in range(n)) == nums)

    for i in range(m):
        linear_model.addConstr(quicksum(x[j] for j in np.where(mask[i] == 1)[0]) >= z[i])

    linear_model.setObjective(quicksum(z[i] for i in range(m)), GRB.MAXIMIZE)

    linear_model.setParam('OutputFlag', 0)
    linear_model.optimize()
    end = time.time()

    print('----- Output -----')
    print('  Running time : %s seconds' % float(end - start))
    print('  Optimal coverage points: %g' % linear_model.objVal)

    covered = set()
    cover = []
    for i in range(len(x)):
        if int(x[i].X) == 1:
            cover.append(input_data[i])
            covered |= input_data[i]

    return cover, covered


if __name__ == "__main__":
    print("Hello World")

    print("*************************pipage_rounding******************************")
    input_data = [{14, 278}, {65, 109, 187, 158, 63}, {3, 228, 201, 170, 240, 158, 220, 286, 95}, {232, 236, 286},
                  {101, 169, 141, 110, 81, 91, 156, 126}, {280, 242, 56, 114}, {296, 281, 89, 263},
                  {67, 69, 27, 150, 88, 56, 187, 31}, {195, 13, 157, 158, 31}, {100, 198, 91, 84, 246, 58, 59},
                  {164, 41, 237, 206, 18, 147, 281, 189}, {160, 97, 223, 300, 236, 148, 188, 189, 63}, {212, 277},
                  {64, 215, 200}, {5, 135, 10, 204, 238, 213, 248, 189}, {49, 146}, {291}, {1, 218, 237, 247},
                  {42, 164, 239}, {99, 106, 43, 44, 243, 254, 158}]
    cover, covered = linear_guboric_fx(10, input_data)

    print("The max covered nums: " + str(len(covered)))
    for sub_set in cover:
        print(sub_set)