import json

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import osmnx as ox
import random
from tqdm import tqdm
from aco_moscow_graph import *

G = ox.load_graphml('central_moscow.graphml')

nodes = G.nodes

SCOOTERS_CNT = 150
STATIONS_CNT = 10

scooter_nodes = np.random.choice(G.nodes, SCOOTERS_CNT, replace=False)
station_nodes = np.random.choice(np.setdiff1d(G.nodes, scooter_nodes), STATIONS_CNT, replace=False)

np.savetxt('scooter_nodes.txt', scooter_nodes)
np.savetxt('station_nodes.txt', station_nodes)


all_nodes = list(station_nodes) + list(scooter_nodes)

graph_dist = [[float('inf') for i in range(len(all_nodes))] for j in range(len(all_nodes))]

for i in tqdm(range(len(all_nodes))):
    for j in range(i + 1, len(all_nodes)):
        dist = nx.shortest_path_length(G, source=all_nodes[i], target=all_nodes[j], weight='length')
        graph_dist[i][j] = dist
        graph_dist[j][i] = dist

with open('graph_dist.json', 'w') as file:
    data = dict()

    data['graph_dist'] = graph_dist

    json.dump(data, file)


