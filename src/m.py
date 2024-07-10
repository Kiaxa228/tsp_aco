import json
import matplotlib.pyplot as plt
import numpy as np
from aco_moscow_graph import *
import osmnx as ox

distance = []

with open('graph_dist.json') as file:
    data = json.load(file)
    distance = data['graph_dist']

distance = np.asarray(distance)

distance[np.isinf(distance)] = 0

graph = Graph(160, distance)

solution = ant_colony_optimization(graph, iterations=50)

solution += [11]

G = ox.load_graphml('central_moscow.graphml')

stations_nodes = np.loadtxt('station_nodes.txt').astype(np.int64)
scooters_nodes = np.loadtxt('scooter_nodes.txt').astype(np.int64)

nodes_to_calculate = list(stations_nodes) + list(scooters_nodes)

positions = {node: (G.nodes[node]['x'], G.nodes[node]['y']) for node in nodes_to_calculate}

plt.figure(figsize=(12, 10))

ox.plot_graph(G, node_size=30, edge_linewidth=1, show=False, close=False)

plt.scatter(
    [positions[node][0] for node in scooters_nodes],
    [positions[node][1] for node in scooters_nodes],
    c='blue', s=50, label='Самокаты'
)
plt.scatter(
    [positions[node][0] for node in stations_nodes],
    [positions[node][1] for node in stations_nodes],
    c='green', s=50, label='Зарядные станции'
)

for i in range(len(solution) - 1):
    plt.plot(
        [G.nodes[nodes_to_calculate[solution[i]]]['x'], G.nodes[nodes_to_calculate[solution[i + 1]]]['x']],
        [G.nodes[nodes_to_calculate[solution[i]]]['y'], G.nodes[nodes_to_calculate[solution[i + 1]]]['y']],
        c='red', alpha=0.6
    )


plt.legend()
plt.title("Граф района с объектами")
plt.show()
