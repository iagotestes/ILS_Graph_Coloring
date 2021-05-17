from collections import Counter
import secrets
import numpy as np
import math
import os
import subprocess
from matplotlib import pyplot as plt

def import_data(path_to_file):
    graph_matrix = [[]]
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
                graph_matrix = [[0 for j in range(size) ] for i in range(size)] 
        raw_numbers.close()
    return (size, graph_matrix)

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
    free_vertices = [i for i in range(size) if history[i] == 1]
    first_iteration = True
    best_cost = None
    new_history = []
    final_solution = []

    for vertex in free_vertices:
        candidate_solution = solution.copy()
        candidate_history = history.copy()
        
        for i in range(size):
            if history[i] == 1:
                aux = candidate_solution.copy()
                candidate_solution[i] = candidate_solution[vertex]
                if validate_neighbor_candidate(graph_matrix, candidate_solution, vertex, i):
                    candidate_history[i] = 0
                    continue
                else:
                    candidate_solution = aux

        current_cost = cost_function(candidate_solution)
        if first_iteration:
            first_iteration = False
            best_cost = current_cost
            final_solution = candidate_solution
            new_history = candidate_history
        elif current_cost < best_cost:
            best_cost = current_cost
            final_solution = candidate_solution
            new_history = candidate_history
    return (new_history, best_cost, final_solution)

def perturbation(size, history, solution, graph_matrix):
    free_vertices = [i for i in range(size) if history[i] == 1]
    
    iterative_free_v = free_vertices.copy()
    for i in range(len(free_vertices)):  
        vertex_of_color_to_be_changed = iterative_free_v.pop(0)
        random_iterative_free_v = iterative_free_v.copy()
        while len(random_iterative_free_v) > 0:
            rand_vertex_of_unchanged_color = secrets.choice(random_iterative_free_v)        
            random_iterative_free_v.remove(rand_vertex_of_unchanged_color)
            
            possible_perturbated_solution = solution.copy()
            possible_perturbated_solution[vertex_of_color_to_be_changed] = possible_perturbated_solution[rand_vertex_of_unchanged_color]
            if validate_neighbor_candidate(graph_matrix,possible_perturbated_solution, rand_vertex_of_unchanged_color, vertex_of_color_to_be_changed):
                return (history, cost_function(possible_perturbated_solution), possible_perturbated_solution)
    return (history, cost_function(solution), solution)        

def better(sa, sa1):
  return sa if sa[1] < sa1[1] else sa1

def rw(sa, sa1):
  return sa1

def lsmc(sa, sa1, history):
  if sa1[1] < sa[1] :
    return sa1
  else:
    T = history.count(1) if history.count(1) != 0 else 1 
    psa1 = math.exp((sa[1] - sa1[1])/T)
    pv = [1-psa1, psa1]
    return sa if np.random.choice([0,1], 1, pv)[0] == 0 else sa1

def acceptance_criterion(sa, sa1, history, flag):
  if flag == 0:
    return better(sa,sa1)
  elif flag == 1:
    return rw(sa, sa1)
  else:
    return lsmc(sa, sa1, history)  

# perturbation(size, history, solution, graph_matrix):
def ils(size, graph_matrix, criteria_flag):
  list_plot=[]
  history = [1 for i in range(size)] # history is nothing but a bit map

  s0 = [i for i in range(size)] #s identity is the general solution
  sa = local_search(size, history, s0, graph_matrix)
  #do
  s1 = perturbation(size, sa[0], sa[2], graph_matrix)
  sa1 = local_search(size, s1[0], s1[2], graph_matrix)
  sa = acceptance_criterion(sa, sa1, sa[0], criteria_flag)
  history = sa[0]
  while history.count(1) > 1 :
    s1 = perturbation(size, sa[0], sa[2], graph_matrix)
    sa1 = local_search(size, s1[0], s1[2], graph_matrix)
    sa = acceptance_criterion(sa, sa1, sa[0], criteria_flag)
    history = sa[0]
    list_plot.append(sa[1])
#         cost  result[]  plot[]  
  return (sa[1], sa[2], list_plot)
    
def timer():
    import time
    return time.time()

# execution tests
def execute_mean_test(cicles, path, criteria_flag):
    size, graph  = import_data(path)
   
    start = timer()
    result = ils(size, graph, criteria_flag)
    end = timer()

    mean = result[2]
    best_result = result[1]
    best_cost = result[0]
    mean_cost = result[0]
    mean_time = end - start
    i=1
    print("cicle: " + str(i) +" m_size:" +  str(size) + " criteria: " + str(criteria_flag))
    while i < cicles:
            start = timer()
            result = ils(size, graph, criteria_flag)
            end = timer()

            time = end - start
            mean_time = (time + mean_time) / 2 
            if result[0] < best_cost:
                best_cost = result[0]
                best_result = result[1]
            mean = [x + y for x, y in zip(mean, result[2])]
            mean = [x / 2 for x in mean]
            mean_cost = (mean_cost + result[0]) / 2

            print("cicle: " + str(i) +" m_size:" +  str(size) + " criteria: " + str(criteria_flag))
            i += 1
    return (best_cost, best_result, mean, mean_time, mean_cost)                
 

########################################### EXECUTION ##################################################

local_path = os.getcwd()
problem_folder = "graph_coloring"
file_names = os.listdir("./"+ problem_folder)
results_dir = local_path + os.path.sep + "results_e_imgs"
result_file = results_dir + os.path.sep + "results.txt"
try: 
    os.mkdir(results_dir)
except OSError:
    print("could not create images folder, it may already exists")
else:
    for problem_file in file_names:
        path = local_path + os.path.sep + problem_folder + os.path.sep + problem_file
        a = 0
        #FOR EACH ACCEPTANCE CRITERIA 0=BETTER 1=RW 2=LSMC
        while a < 3:
            #MEAN RESULTS OF 30 TESTS
            number_of_tests = 30
            res = execute_mean_test(number_of_tests, path, a) 
           
            t_color = ('blue' if a == 0 else ('red' if a == 1 else 'green')) 

            plt.title(os.path.splitext(problem_file)[0])
            plt.plot(res[2], color=t_color)
            plt.ylabel('cost')
            plt.xlabel('iteractions')

            text =  "best cost: " + str(res[0])
            plt.text(0.02, (1+a*0.05), text, fontsize=14, transform=plt.gcf().transFigure, c=t_color )
            
            text =  "mean cost: " + str(int((res[4])))
            plt.text(0.4, (1+a*0.05), text, fontsize=14, transform=plt.gcf().transFigure, c=t_color )

            text =  "mean time: " + str('%.5f'%(res[3]))
            plt.text(0.8, (1+a*0.05), text, fontsize=14, transform=plt.gcf().transFigure, c=t_color )
        
            text =  ('better' if a ==0 else ('rw' if a == 1 else 'lsmc'))
            plt.text(1.2, (1+a*0.05), text, fontsize=14, transform=plt.gcf().transFigure, c=t_color )

            #put the results in a file
            # (best_cost, best_result, mean, mean_time, mean_cost)                
            bash_cmd = "echo \"" + problem_file +  (' better' if a ==0 else (' rw' if a == 1 else ' lsmc')) + "\" >> " + result_file
            bash_cmd += " && echo \"" + str(res[0]) + "\" >> " + result_file
            bash_cmd += " && echo \"" + str(res[1]) + "\" >> " + result_file
            bash_cmd += " && echo \"" + str('%.5f'%(res[3])) + "\" >> " + result_file
            bash_cmd += " && echo \"" + str(int(res[4])) + "\" >> " + result_file
            bash_cmd += " && echo \"\"  >> " + result_file
            
            error = subprocess.run(bash_cmd, shell=True, check=True, text=True)        
            a += 1 

        plt.savefig(results_dir + os.path.sep + "plot_" + os.path.splitext(problem_file)[0] + ".png" , bbox_inches='tight')
        plt.clf()
    print("end")
