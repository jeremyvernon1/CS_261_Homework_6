# Course: CS261 - Data Structures
# Author: Jeremy Vernon
# Assignment: 6
# Description: Directed Graphs

import heapq
from collections import deque


class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Adds a vertex to the matrix
        """
        #initializes
        length = self.v_count

        # increments size
        self.v_count += 1

        # adds 0s to the new row
        self.adj_matrix.append([0] * self.v_count)
        # adds 0s to the previous rows
        for index in range(length):
            self.adj_matrix[(length - 1)].append(0 * (self.v_count - length))
            length -= 1

        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Adds a weighted edge to the matrix
        """
        # checks for validity
        if 0 <= src < self.v_count and \
                0 <= dst < self.v_count and \
                weight > 0 and \
                src is not dst:
            # add weight to create edge
            self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Removes and edge from the graph
        """
        # checks for validity
        if 0 <= src <= self.v_count and \
                0 <= dst <= self.v_count and \
                self.adj_matrix[src][dst] > 0:
            # sets edge weight equal to 0
            self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        Returns a list of all vertices
        """
        # initializes
        get_vertices_results = []
        get_vert_length = len(self.adj_matrix)

        # searches each cell in the matrix for values greater than 0
        for row_index in range(get_vert_length):
            for edge_index in range(get_vert_length):
                # checks that weight is greater than 0 and vertex not already recorded
                if self.adj_matrix[row_index][edge_index] > 0 and \
                        row_index not in get_vertices_results:
                    # adds vertex to result list
                    get_vertices_results.append(row_index)

        return get_vertices_results

    def get_edges(self) -> []:
        """
        Returns a list of tuple edges
        """
        # initializes
        get_edges_results = []
        get_vert_length = len(self.adj_matrix)

        # checks each cell in the matrix for a weight greater than 0
        for row_index in range(get_vert_length):
            for edge_index in range(get_vert_length):
                weight = self.adj_matrix[row_index][edge_index]
                if weight > 0:
                    # adds index positions and weight to result list
                    get_edges_results.append((row_index, edge_index, weight))

        return get_edges_results

    def is_valid_path(self, path: []) -> bool:
        """
        Returns true if provided path is valid, False otherwise
        """
        # initializes
        length = len(path)

        # checks if given path is empty
        if length > 0:

            # checks if first element is a vertex
            if path[0] < 0 or path[0] > self.v_count:
                return False

            # if more than one element in the given path
            if length > 1:
                for index in range(length - 1):
                    # checks if there is no weight for the next value in the given path
                    if self.adj_matrix[path[index]][path[index + 1]] < 1:
                        return False

        # otherwise returns true
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        TODO: Write this implementation
        """
        pass

    def bfs(self, v_start, v_end=None) -> []:
        """
        TODO: Write this implementation
        """
        pass

    def has_cycle(self):
        """
        TODO: Write this implementation
        """
        pass

    def dijkstra(self, src: int) -> []:
        """
        TODO: Write this implementation
        """
        pass


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)

    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)

    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
