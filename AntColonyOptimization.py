import random


class Graph(object):
    def __init__(self,rank: int,cost_matrix: list):
        """
        :param cost_matrix:
        :param rank: rank of the cost matrix
        """
        self.rank = rank
        self.matrix = cost_matrix
        # noinspection PyUnusedLocal
        self.pheromone_level= [[1 / (rank * rank) for j in range(rank)] for i in range(rank)]


class AntColony(object):
    def __init__(self, count_of_ants: int, generations: int, alpha: float, beta: float, rho: float, q: int,
                 strategy: int):
        """
        :param count_of_ants:
        :param generations:
        :param alpha: relative importance of pheromone_level
        :param beta: relative importance of heuristic information
        :param rho: pheromone_level residual coefficient
        :param q: pheromone_level intensity
        :param strategy: pheromone_level update strategy. 0 - ant-cycle, 1 - ant-quality, 2 - ant-density
        """
        self.Q = q
        self.rho = rho
        self.beta = beta
        self.alpha = alpha
        self.count_of_ants = count_of_ants
        self.generations = generations
        self.update_strategy = strategy

    def _update_pheromone_level(self, graph: Graph, ants: list):
        for i, row in enumerate(graph.pheromone_level):
            for j, col in enumerate(row):
                graph.pheromone_level[i][j] *= self.rho
                for ant in ants:
                    graph.pheromone_level[i][j] = graph.pheromone_level[i][j] +ant.pheromone_level_delta[i][j]

    # noinspection PyProtectedMember
    def determine(self, graph: Graph):
        """
        :param graph:
        """
        best_cost = float('inf')
        best_solution = []
        for gen in range(self.generations):
            # noinspection PyUnusedLocal
            ants = [_Ant(self, graph) for i in range(self.count_of_ants)]
            for ant in ants:
                for i in range(graph.rank - 1):
                    ant._select_next()
                ant.total_cost =ant.total_cost+ graph.matrix[ant.tabu[-1]][ant.tabu[0]]
                if ant.total_cost < best_cost:
                    best_cost = ant.total_cost
                    best_solution = [] + ant.tabu
                # update pheromone_level
                ant._update_pheromone_level_delta()
            self._update_pheromone_level(graph, ants)
            # print('generation #{}, best cost: {}, path: {}'.format(gen, best_cost, best_solution))
        return best_solution, best_cost


class _Ant(object):
    def __init__(self, AntColony: AntColony, graph: Graph):
        self.colony = AntColony
        self.graph = graph
        self.total_cost = 0.0
        self.tabu = []  # tabu list
        self.pheromone_level_delta = []  # the local increase of pheromone_level
        self.allow = [i for i in range(graph.rank)]  # nodes which are allow for the next selection
        self.eta = [[0 if i == j else 1 / graph.matrix[i][j] for j in range(graph.rank)] for i in
                    range(graph.rank)]  # heuristic information
        start = random.randint(0, graph.rank - 1)  # start from any node
        self.tabu.append(start)
        self.current = start
        self.allow.remove(start)

    def _select_next(self):
        denominator = 0
        for i in self.allow:
            denominator =denominator+ self.graph.pheromone_level[self.current][i] ** self.colony.alpha * self.eta[self.current][
                                                                                            i] ** self.colony.beta
        # noinspection PyUnusedLocal
        probabilities = [0 for i in range(self.graph.rank)]  # probabilities for moving to a node in the next step
        for i in range(self.graph.rank):
            try:
                self.allow.index(i)  # test if allow list contains i
                probabilities[i] = self.graph.pheromone_level[self.current][i] ** self.colony.alpha * \
                    self.eta[self.current][i] ** self.colony.beta / denominator
            except ValueError:
                pass  # do nothing
        # select next node by probability roulette
        selected = 0
        rand = random.random()
        for i, probability in enumerate(probabilities):
            rand -= probability
            if rand <= 0:
                selected = i
                break
        self.allow.remove(selected)
        self.tabu.append(selected)
        self.total_cost =self.total_cost+ self.graph.matrix[self.current][selected]
        self.current = selected

    # noinspection PyUnusedLocal
    def _update_pheromone_level_delta(self):
        self.pheromone_level_delta = [[0 for j in range(self.graph.rank)] for i in range(self.graph.rank)]
        for _ in range(1, len(self.tabu)):
            i = self.tabu[_ - 1]
            j = self.tabu[_]
            if self.colony.update_strategy == 1:  # ant-quality system
                self.pheromone_level_delta[i][j] = self.colony.Q
            elif self.colony.update_strategy == 2:  # ant-density system
                # noinspection PyTypeChecker
                self.pheromone_level_delta[i][j] = self.colony.Q / self.graph.matrix[i][j]
            else:  # ant-cycle system
                self.pheromone_level_delta[i][j] = self.colony.Q / self.total_cost
