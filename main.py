import json
import random
import numpy as np
import osmnx as ox
import networkx as nx
from aco_tso import *
import matplotlib.pyplot as plt

distance = []

with open('graph_dist.json') as file:
    data = json.load(file)
    distance = data['graph_dist']


to_add_stations = 5
to_add_scooters = 10

distance = np.asarray(distance)

def add_scooters_and_stations(num_scooters, num_stations):
    res = distance

    res = np.delete(res, [el for el in range(10 + num_stations, 20)], axis=1)
    res = np.delete(res, [el for el in range(10 + num_stations, 20)], axis=0)

    res = np.delete(res, [el for el in range(170 + num_scooters - (20 - (10 + num_stations)), 190 - (20 - (10 + num_stations)))], axis=1)
    res = np.delete(res, [el for el in range(170 + num_scooters - (20 - (10 + num_stations)), 190 - (20 - (10 + num_stations)))], axis=0)

    return res


cur = add_scooters_and_stations(to_add_scooters, to_add_stations)

cur[np.isinf(cur)] = 0

graph = Graph(160 + to_add_scooters + to_add_stations, cur)

solution, prev_area_power, cur_area_power = ant_colony_optimization(graph, iterations=200, scooters_cnt=150+ to_add_scooters, stations_cnt=10+to_add_stations)

solution += [11]

G = ox.load_graphml('central_moscow.graphml')

stations_nodes = np.loadtxt('station_nodes.txt').astype(np.int64)
scooters_nodes = np.loadtxt('scooter_nodes.txt').astype(np.int64)

stations_nodes = stations_nodes[:10 + to_add_stations]
scooters_nodes = scooters_nodes[:150 + to_add_scooters]

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

plt.scatter(
    [positions[nodes_to_calculate[11]][0]],
    [positions[nodes_to_calculate[11]][1]],
    c='yellow', s=50, label='Точка старта'
)

for i in range(len(solution) - 1):
    plt.plot(
        [G.nodes[nodes_to_calculate[solution[i]]]['x'], G.nodes[nodes_to_calculate[solution[i + 1]]]['x']],
        [G.nodes[nodes_to_calculate[solution[i]]]['y'], G.nodes[nodes_to_calculate[solution[i + 1]]]['y']],
        c='red', alpha=0.6
    )

    plt.text((G.nodes[nodes_to_calculate[solution[i]]]['x'] + G.nodes[nodes_to_calculate[solution[i + 1]]]['x']) /2, (G.nodes[nodes_to_calculate[solution[i]]]['y'] + G.nodes[nodes_to_calculate[solution[i + 1]]]['y']) / 2, str(i + 1), fontsize=7, ha='center', va='center')

with open('result.txt', 'w') as file_out:
    file_out.write('Before area_power:\n')
    file_out.write(f'{prev_area_power}%\n')
    file_out.write('After area_power:\n')
    file_out.write(f'{cur_area_power}%\n')
    file_out.write('Best cycle:\n')
    file_out.write(f"[{','.join(map(str, solution))}]\n")
    file_out.write('Length:\n')
    file_out.write(str(cycle_length(graph, solution[:-1])))


plt.legend()
plt.title("Граф района с объектами")
plt.show()
