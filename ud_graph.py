# Course: CS 261
# Author: Jeremy Vernon
# Assignment: 6
# Description: Undirected Graphs

import heapq
from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Adds new vertex to the graph
        """
        if v not in self.adj_list:
            self.adj_list[v] = []


    def add_edge(self, u: str, v: str) -> None:
        """
        Adds edge to the graph
        """
        # adds vertices if not already in graph
        if u is not v:
            self.add_vertex(u)
            self.add_vertex(v)

            # adds edge
            if v not in self.adj_list[u]:
                self.adj_list[u].append(v)
            if u not in self.adj_list[v]:
                self.adj_list[v].append(u)


    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        # checks if u and v are in the graph
        if u in self.adj_list and v in self.adj_list:

            # removes reference to the other vertex
            if v in self.adj_list[u]:
                self.adj_list[u].remove(v)
            if u in self.adj_list[v]:
                self.adj_list[v].remove(u)


    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        # removes key if it exists
        if v in self.adj_list:
            del self.adj_list[v]

        # adjusts remaining edges
        for key in self.adj_list:
            if v in self.adj_list[key]:
                self.adj_list[key].remove(v)


    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        # builds a list of all vertices
        get_vertices_results = []
        for vertex in self.adj_list:
            get_vertices_results.append(vertex)
        return get_vertices_results


    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        # builds a list of edges
        get_edges_results = []
        get_edges_seen = []
        for key in self.adj_list:
            get_edges_seen.append(key)
            for value in self.adj_list[key]:
                if value not in get_edges_seen:
                    # append edges that are not already visited
                    get_edges_results.append((key, value))
        return get_edges_results


    def is_valid_path(self, path: []) -> bool:
        """
        Returns true if provided path is valid, False otherwise
        """
        length = len(path)
        if length > 0:
            # checks first element
            if path[0] not in self.adj_list:
                return False
            # if more than one element in the given path
            for index in range(length):
                # checks if the next key contains a value for the current key
                if ((index + 1) < length) and (path[index] not in self.adj_list[path[index+1]]):
                    return False
        return True


    def dfs(self, v_start, v_end=None) -> []:
        """
        Returns list of vertices visited during DFS search
        Vertices are picked in ascending order
        """
        # initializes
        dfs_reachable_vertices = []
        dfs_stack = [v_start]
        dfs_visited = {}

        # checks if v_start is in the graph:
        dfs_vertices = self.get_vertices()
        if v_start not in dfs_vertices:
            dfs_stack.pop()

        # loops to add the current node and search for the next edge
        while dfs_stack:
            # adds node to the path
            node_curr = dfs_stack.pop()
            # if node is not already visited, adds to list of visited and to path
            if node_curr not in dfs_visited:
                dfs_visited[node_curr] = node_curr
                dfs_reachable_vertices.append(node_curr)
                # checks for end node
                if node_curr == v_end:
                    return dfs_reachable_vertices

                # Finds smallest value edge, and continues to traverse
                # creates list of current node's edges
                dfs_edges = []
                for value in self.adj_list[node_curr]:
                    if value not in dfs_visited:
                        dfs_edges.append(value)
                # sorts list of edges, then adds to stack in reverse order
                dfs_edges.sort()
                while dfs_edges:
                    edge_curr = dfs_edges.pop()
                    dfs_stack.append(edge_curr)

        # when stack is empty, return path
        return dfs_reachable_vertices


    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        # initializes
        bfs_reachable_vertices = []
        bfs_queue = deque([v_start])
        bfs_visited = {}

        # checks if v_start is in the graph:
        dfs_vertices = self.get_vertices()
        if v_start not in dfs_vertices:
            bfs_queue.pop()

        # loops to add the current edges and then to find the next level
        while bfs_queue:
            bfs_curr = bfs_queue.popleft()

            # checks if vertex has been visited. If not adds to path and to visited
            if bfs_curr not in bfs_visited:
                bfs_reachable_vertices.append(bfs_curr)
                bfs_visited[bfs_curr] = bfs_curr
                # checks if reached end node
                if bfs_curr == v_end:
                    return bfs_reachable_vertices

                # finds the vertices in the next level
                bfs_edges = []
                for value in self.adj_list[bfs_curr]:
                    if value not in bfs_visited:
                        bfs_edges.append(value)
                # sorts list of edges, then adds to queue by smallest
                heapq.heapify(bfs_edges)
                while bfs_edges:
                    lowest_edge = heapq.heappop(bfs_edges)
                    bfs_queue.append(lowest_edge)

        return bfs_reachable_vertices

    def count_connected_components(self):
        """
        Return number of connected componets in the graph
        """
        # initializes
        count = 0
        count_vertices = self.get_vertices()

        # loops to find groups of connected vertices, increment count, and remove the grouped vertices from the list
        while count_vertices:
            count_path = self.dfs(count_vertices[0])
            count += 1
            for vertex in count_path:
                count_vertices.remove(vertex)

        return count

    def has_cycle(self):
        """
        Returns True if graph contains a cycle, False otherwise
        """
        # initializes
        vertices = self.get_vertices()
        dfs_reachable_vertices = []
        dfs_stack = [vertices[0]]
        dfs_visited = {}
        node_curr = dfs_stack[-1]

        # loops to add the current node and search for the next edge
        while dfs_stack:
            # adds node to the path
            parent_node = node_curr
            node_curr = dfs_stack.pop()
            # if node is not already visited, adds to list of visited and to path
            if node_curr not in dfs_visited:
                dfs_visited[node_curr] = node_curr
                dfs_reachable_vertices.append(node_curr)

                # Finds smallest value edge, and continues to traverse
                # creates list of current node's edges
                dfs_edges = []
                for value in self.adj_list[node_curr]:
                    # checks for cycle
                    if value != parent_node and\
                        value != node_curr and\
                        value in dfs_visited:
                        return True
                    if value not in dfs_visited:
                        dfs_edges.append(value)
                # sorts list of edges, then adds to stack in reverse order
                dfs_edges.sort()
                while dfs_edges:
                    edge_curr = dfs_edges.pop()
                    dfs_stack.append(edge_curr)

        # returns false if cycle not found
        return False

   


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)

    g = UndirectedGraph()
    g.add_edge('C', 'C')
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')

    print("\nPDF - method dfs() and bfs() example 2")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'J'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')

    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
