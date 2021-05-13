from collections import Counter



def import_data(path_to_file):
    graph_matrix = [[]]
    vertice_color = []
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
                vertice_color = [i for i in range(size)]
                graph_matrix = [[0 for j in range(size) ] for i in range(size)] 
        raw_numbers.close()
    return (graph_matrix, vertice_color)


def cost_function(vertice_color):
    return len(Counter(vertice_color).values())


#print(import_data("./graph_coloring/dsjc250.5.col")[0])
print(cost_function(import_data("./graph_coloring/teste.txt")[1]))
#import_data("./graph_coloring/dsjc250.5.col")
