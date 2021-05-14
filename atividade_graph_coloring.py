from collections import Counter
import secrets
def import_data(path_to_file):
    graph_matrix = [[]]
    vertices_color = []
    size = 0
    with open(path_to_file) as raw_numbers:
        for line in raw_numbers: 
            line_type = list(map(str, line.split()))[0]
            if line_type == 'e':
                v1 = int(list(map(str, line.split()))[1])
                v2 = int(list(map(str, line.split()))[2])
                graph_matrix[v1-1][v2-1]=1
                graph_matrix[v2-1][v1-1]=1
            if line_type == 'p':
                size = int(list(map(str, line.split()))[2])
                vertices_color = [i for i in range(size)]
                graph_matrix = [[0 for j in range(size) ] for i in range(size)] 
        raw_numbers.close()
    return (size, graph_matrix, vertices_color)

"""###################### Iterated Local Search #######################
"""
def cost_function(vertices_color):
    return len(Counter(vertices_color).values())

def validate_neighbor_candidate(graph_matrix, neighbor_candidate, vertex_original_color, vertex_color_changed):
    color = neighbor_candidate[vertex_original_color]
    i = 0
    for vertex in graph_matrix[vertex_color_changed]:
        if vertex == 1 and color == neighbor_candidate[i]:
            return False
        i += 1
    return True

def local_search(size, history, solution, graph_matrix):
    cost_of_neighbors = []
    first = 0
    #find first, this one will be the index for mapping the neighbors
    while first < size:
        if history[first] == 0: #immutable memory value
            first += 1
            continue
        else:
            break
    #find the cost of all valid neighbors of colors
    i = first + 1
    index_min_cost = 0
    while i < size:
        if history[i] == 1:
            neighbor_candidate = solution.copy()
            neighbor_candidate[i] = neighbor_candidate[first] #trying to reduce colors
            if validate_neighbor_candidate(graph_matrix, neighbor_candidate, first, i):
                cost = cost_function(neighbor_candidate)
                cost_of_neighbors.append(cost)
                if min(cost_of_neighbors) == cost: # keep track of minimum cost
                    index_min_cost = i
        i += 1
    if len(cost_of_neighbors) > 0:
        minimum_cost = min(cost_of_neighbors)
        new_solution = solution.copy()
        new_solution[index_min_cost] = new_solution[first]
        new_history = history.copy()
        new_history[first]=0
        new_history[index_min_cost]=0
        return (new_history, minimum_cost, new_solution)
    return (history, cost_function(solution), solution)

def perturbation(size, history, solution, graph_matrix):
    #available_colors = list(set(solution))
     
size, graph, trivial_solution = import_data("./graph_coloring/teste.txt")
s0 = local_search(size, [1 for i in range(size)], trivial_solution, graph)
print(s0[1])
print(s0[2])
