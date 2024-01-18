import render_graph
import simulate
from graph import Vertex
from graph import Graph

import image_reader
#graph.vertices = [Vertex]
#You must add_color() before you can read colors (Default # of colors =0)


def allowed_colors(vertex:Vertex,graph:Graph):
    if graph.colors_used==0:
        return []
    taken_colors=[]
    for edge in vertex.edges:
        taken_colors.append(edge.color)
    return [color for color in list(range(graph.colors_used)) if color not in taken_colors]
def set_new_color(vertex:Vertex,graph:Graph):
    graph.add_color()
    vertex.color=graph.colors_used-1

def algorithm(graph:Graph):

    #Run the greedy algorithm once.
    for vertex in graph.vertices:
        options=allowed_colors(vertex,graph)
        if len(options)==0:
            set_new_color(vertex,graph)
        else:
            vertex.color=options[0]
        yield

    for vertex in graph.vertices:
        if vertex.color==graph.colors_used-1:
            vertex.color=-1
            for edge1 in vertex.edges:
                for edge2 in vertex.edges:
                    if edge1!=edge2 and edge1.color==edge2.color and edge1.can_walk_to(edge2,[vertex]):
                        print("Loop")
        yield
    print("\nColoring Completed:\nGraph Chromatic Number Of " + str(graph.colors_used)+"\nVertex Count Of "+str(graph.vertex_count())+"\nLargest Degree Of "+str(graph.largest_degree())+"\nSmallest Degree Of "+str(graph.smallest_degree()))






    
def confirm_algorithm(graph,baseline,func):
    print("\nConfirming Algorithmic Correctness...")
    def reset_graph():
        temp_graph=graph.new()

        graph.transfer_colors(temp_graph)
        graph.transfer_vertices(temp_graph)
        i=0
        for vertex in graph.vertices:
            v=temp_graph.vertices[i]
            for edge in vertex.edges:
                v.add_edge(temp_graph.vertices[graph.vertices.index(edge)])
            i+=1
        return temp_graph
    baseline_grid=reset_graph()
    list(baseline(baseline_grid))

    algorithm_grid=reset_graph()
    list(algorithm(algorithm_grid))

    if baseline_grid.colors_used == algorithm_grid.colors_used:
        print("PASS! The algorithm has determined the Chromatic Number of " +str(algorithm_grid.colors_used))
    else:
        print("FAIL! The algorithm determined a Chromatic Number of " +str(algorithm_grid.colors_used)+ ",\nBut the reliable baseline said it was " +str(baseline_grid.colors_used)+"!")
    return baseline_grid.colors_used == algorithm_grid.colors_used

def run_checks():
    correct=True
    check_num=25
    
    for i in range(check_num):
        if not confirm_algorithm(render_graph.gen_graph(15,6),simulate.depth_first,algorithm):
            correct=False
            break
    if correct:
        print("The algorithm has passed a total of "+str(check_num)+"checks")
    else:
        print("The algorithm has failed...")

    
    
    
def main():
    #render_graph.run(render_graph.gen_graph(15,3),algorithm)
    #render_graph.gen_run(15,6,algorithm)
    render_graph.run(image_reader.img_to_graph("simple_map.png"),algorithm)
    #confirm_algorithm(image_reader.img_to_graph("simple_map.png"),simulate.depth_first,algorithm)
    run_checks()
if __name__=="__main__":
    main()
