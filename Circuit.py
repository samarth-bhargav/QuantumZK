from Node import Node
from random import randint

class Circuit:
    def __init__(self, N):
        # Generate initial nodes
        pass

    def create(self, N):
        garbled_g = [(randint(0, 1 << 32 - 1), randint(0, 1 << 32 - 1)) for i in range(N)]
        garbled_h = [(randint(0, 1 << 32 - 1), randint(0, 1 << 32 - 1)) for i in range(N)]
        data = [Node.create(garbled_g[i][0], garbled_g[i][1], garbled_h[i][0], garbled_h[i][1], "XOR") for i in range(N)]
        init_nodes = [node[0] for node in data]
        i_vals = [node[1] for node in data]

        #after running the init nodes, nee to implement rechecking functionality

        check_data = [Node.create(i_vals[i][0], i_vals[i][1], garbled_h[i][0], garbled_h[i][1]) for i in range(N)]
        check_nodes = [node[0] for node in check_data]
        check_garbled = [node[1] for node in check_data]

        
