import math

from AntColonyOptimization import AntColonyOptimization, Graph
from plot import plot


def distance(landmark1: dict, landmark2: dict):
    return math.sqrt((landmark1['x'] - landmark2['x']) ** 2 + (landmark1['y'] - landmark2['y']) ** 2)


def main():
    landmarks = []
    points = []
    with open('./data/chn31.txt') as f:
        for line in f.readlines():
            landmark = line.split(' ')
            landmarks.append(dict(index=int(landmark[0]), x=int(landmark[1]), y=int(landmark[2])))
            points.append((int(landmark[1]), int(landmark[2])))
    cost_matrix = []
    rank = len(landmarks)
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(distance(landmarks[i], landmarks[j]))
        cost_matrix.append(row)
    AntColonyOptimization = AntColonyOptimization(10, 100, 1.0, 10.0, 0.5, 10, 2)
    graph = Graph(cost_matrix, rank)
    path, cost = AntColonyOptimization.solve(graph)
    print('cost: {}, path: {}'.format(cost, path))
    plot(points, path)

if __name__ == '__main__':
    main()
