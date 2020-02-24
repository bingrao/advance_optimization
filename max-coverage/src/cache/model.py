import numpy as np
import gurobipy as gp
from gurobipy import GRB


def build_model():
    # data attributes
    # {
    #    genOp: op_idx
    #    size: int
    # }

    attr_data  = [{"genop": 0, "size": 256},
                  {"genop": 1, "size": 512},
                  {"genop": 2, "size": 128}]  # a row is a kind of an data attriubte  |D|*

    # operation attriubtes
    # {
    #    input: [1, 2, 3]
    #    output: 4
    #    time:10
    # }

    attr_op = [
        {
            "input": {},
            "out": 0,
            "time":  25,
            "pred":[],
            "succ":[1]
        },
        {
            "in": {0},
            "out": 1,
            "time": 27,
            "pred": [0],
            "succ": [2]
        },
        {
            "in": {1},
            "out": 2,
            "time": 37,
            "pred": [1],
            "succ": []
        }
    ]  # a row is a set of an operation attribute  |P|*

    capacity = 512
    import time
    start = time.time()

    model = gp.Model()

    nums_data = len(attr_data)
    nums_op = len(attr_op)

    cache_map = model.addVars(nums_op, nums_data, vtype=GRB.BINARY, name="cache_map")
    model.update()

    # [sum(cache_map[i,j]) for j in range(nums_data) for i in range(j)]

    # model.addConstr(gp.quicksum(
    #     cache_map[i, j] for i in range(nums_op)
    #     for j in range(nums_data) if i < j
    # ) == 0)

    model.addConstrs(
        (cache_map[i, j] == 0 for i in range(nums_op) for j in range(nums_data) if i < j)
    )

    for j in range(nums_data):
        model.addConstrs(
            (cache_map[j, j] == 1 for i in range(nums_op))
        )

    for i in range(nums_op):
        model.addConstr(gp.quicksum(cache_map[i, j]*attr_data[j]["size"] for j in range(nums_data)) <= capacity)

    # def getOpIdx(data_idx):
    #
    # def getDataIdx(op_Idx):
    #

    def lamda_func(op_idex):
        op = attr_op[op_idex]
        a = sum(attr_data[attr_op[i]["out"]]["size"] * cache_map[i, attr_op[i]["out"]] for i in op["pred"])
        b = sum(attr_data[attr_op[i]["out"]]["size"] for i in op["pred"])
        return a*1.0/(b+1)

    model.setObjective(sum(lamda_func(i)*attr_op[i]["time"] for i in range(nums_op)), GRB.MAXIMIZE)

    model.setParam('OutputFlag', 0)
    model.optimize()
    end = time.time()

    print('----- Output -----')
    print('  Running time : %s seconds' % float(end - start))
    print('  Optimal coverage points: %g' % model.objVal)
    # print(cache_map)
    for i in range(nums_op):
        for j in range(nums_data):
            print(int(cache_map[i,j].X)),
        print()


if __name__ == "__main__":
    build_model()