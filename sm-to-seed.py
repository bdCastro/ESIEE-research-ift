from dataclasses import dataclass
import numpy as np
import sys

# # Graph class
# class Graph:
#     def __init__(self, size):
#         self.size = size
#         self.weights = np.zeros(size)
#         self.edges = np.full([size, size], None)

#     def add_egde(self, orig, dest, weight=0):
#         self.edges[orig][dest] = weight

#     def set_node(self, node, weight):
#         self.weights[node] = weight

#     def show_adj(self):
#         for line in self.edges:
#             print(line)

# g = Graph(10)
# g.add_egde(2, 4)
# g.show_adj()

# reading graph file and args

file_path = f'{sys.argv[1]}'
num_regions = int(sys.argv[2])
output_path = f'{sys.argv[3]}'

with open(file_path, 'r') as f:
    # first line has the dimmentions of the image
    line = f.readline().replace('#rs ', '').replace('cs ', '').split()
    print(line)
    width, height = map(int, line)
    # second line is the number of node and edges
    node, edges = map(int, f.readline().split())

    # skiping line with 'val sommets'
    _ = f.readline()
    
    # reading nodes
    nodes, weights = [], []

    for _ in range(node):
        node, weight = map(int, f.readline().split())

        nodes.append(node)
        weights.append(weight)

    # calculating the cut value
    cut_value = max(weights) - num_regions

    # deleting node and weights that are not in the cut
    nodes = np.array(nodes)
    weights = np.array(weights)

    nodes = nodes[weights > cut_value]
    weights = weights[weights > cut_value]

    # generating marker structure

    # to generate the seeds file, we first impute the number of seeds and the dimmentions of the image
    # opening the file
    seeds_file = open(output_path, 'w')
    seeds_file.write(f'{len(nodes)} {width} {height}\n')

    # writing the seeds
    for node, weight in zip(nodes, weights):
        # converting the node to the x and y coordinates
        x = node % width
        y = node // width

        # writing the seed
        seeds_file.write(f'{x} {y} {weight-cut_value-1} {weight-cut_value-1}\n')

    # closing the file
    seeds_file.close()