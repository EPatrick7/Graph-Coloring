import pygame
from pygame.math import Vector2
from pygame import Color
from graph_wrappers import PyVertex as Vertex
from graph_wrappers import PyGraph as Graph
import random


import simulate

def init():
    global _surface
    global _overlay
    global _clock
    global _pyrunning
    global _world_center
    
    _surface= pygame.display.set_mode((1000, 700))
    _overlay=pygame.Surface((1000,700),pygame.SRCALPHA)
    _clock = pygame.time.Clock()
    _pyrunning=True
    _world_center=Vector2(_surface.get_width()/2,_surface.get_height()/2)
    
    
    _surface.blit(_overlay,(0,0))
    pygame.display.flip()
    _overlay=pygame.Surface((1000,700),pygame.SRCALPHA)
    
def render_vertex(v:Vertex,color:Color):
    pygame.draw.circle(_surface,color,v.pos+_world_center,4)
def render_edges(v:Vertex,color:Color):
    for edge in v.edges:
        halfway_point = ((v.pos[0] + edge.pos[0]) // 2, (v.pos[1] + edge.pos[1]) // 2)
        pygame.draw.line(_surface, color, v.pos+_world_center, halfway_point+_world_center, 2)

def graph_to_positions(graph: Graph):
    '''Gives a graph vertex positions based on its edge connections'''
    # This function was generated with AI assistance
    # Fruchterman-Reingold force-directed graph drawing algorithm

    # Constants
    k = 0.1  # Optimal distance between nodes
    max_iterations = 100

    # Initialize positions randomly
    for vertex in graph.vertices:
        vertex.pos = Vector2(random.uniform(0, 900), random.uniform(0, 600))

    for iteration in range(max_iterations):
        # Calculate repulsive forces
        for vertex in graph.vertices:
            vertex.disp = Vector2(0, 0)
            for other_vertex in graph.vertices:
                if vertex != other_vertex:
                    delta = vertex.pos - other_vertex.pos
                    distance_squared = max(1, delta.length_squared())
                    repulsion_force = k**2 / distance_squared
                    vertex.disp += delta.normalize() * repulsion_force

        # Calculate attractive forces
        for vertex in graph.vertices:
            for edge in vertex.edges:
                delta = vertex.pos - edge.pos
                distance = max(0.1, delta.length())
                attraction_force = distance**2 / k
                vertex.disp -= delta.normalize() * attraction_force

        # Update positions
        for vertex in graph.vertices:
            vertex.pos += vertex.disp.normalize() * min(vertex.disp.length(), 0.1)

    # Normalize positions to fit within the window
    min_x = min(vertex.pos.x for vertex in graph.vertices)
    min_y = min(vertex.pos.y for vertex in graph.vertices)
    max_x = max(vertex.pos.x for vertex in graph.vertices)
    max_y = max(vertex.pos.y for vertex in graph.vertices)
    scale_factor = min(600 / (max_x - min_x), 500 / (max_y - min_y))

    for vertex in graph.vertices:
        vertex.pos.x = (vertex.pos.x - min_x) * scale_factor
        vertex.pos.y = (vertex.pos.y - min_y) * scale_factor



def render_graph(graph: Graph):
    if type(graph)!=type(Graph()):
        raise TypeError("Cannot render a non-pygraph graph, it has no vertex positions, just edges!")
    global _surface
    global _overlay
    global _world_center
    _surface.fill(pygame.Color(0,0,0))
    for vertex in graph.vertices:
        render_vertex(vertex,graph.get_color(vertex))
    
    for vertex in graph.vertices:
        render_edges(vertex,graph.get_color(vertex))
    
    _surface.blit(_overlay,(0,0))
    pygame.display.flip()
    _overlay=pygame.Surface((700,600),pygame.SRCALPHA)

def run(graph,generator):
    pygame.init()
    init()
    
    global _surface
    global _overlay
    global _clock
    global _pyrunning
    global _world_center
    
    _world_center=Vector2(250,175)

    speed_up_system=1
    try:

        simulation=generator(graph)
        while _pyrunning:

            _clock.tick(60*speed_up_system)
            try:
                next(simulation)
                speed_up_system+=0.1
            except StopIteration:
                speed_up_system=1
            render_graph(graph)
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    _pyrunning = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
    finally:
        pygame.quit()


    
def gen_run(vertex_count:int,max_edges:int,generator):
    graph=gen_graph(vertex_count,max_edges)
    pygame.init()
    init()
    
    global _surface
    global _overlay
    global _clock
    global _pyrunning
    global _world_center
    
    _world_center=Vector2(250,175)

    speed_up_system=1
    try:

        simulation=generator(graph)
        while _pyrunning:

            _clock.tick(60*speed_up_system)
            try:
                next(simulation)
                speed_up_system+=0.1
            except StopIteration:
                speed_up_system=1
            render_graph(graph)
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    _pyrunning = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        gen_run(vertex_count,max_edges,generator)
    finally:
        pygame.quit()
def single_render(graph:Graph):
    pygame.init()
    init()
    global _surface
    global _overlay
    global _clock
    global _pyrunning
    global _world_center

    _world_center=Vector2(250,175)
    try:
        while _pyrunning:

            _clock.tick(60)
            render_graph(graph)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    _pyrunning = False
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        _pyrunning = False
                        #single_render(graph)
    finally:
        pygame.quit()
    return True
    
def gen_graph(vertex_count:int,max_edges:int):

    if '_world_center' not in globals():
        global _world_center
        _world_center=Vector2(500,350)
        
    def distance_squared(v1: Vector2, v2: Vector2) -> float:
        return (v1.x - v2.x)**2 + (v1.y - v2.y)**2
    def is_connected(vertices:[Vertex])->bool:
        if len(vertices)==0:
            return False
        
        stack=[vertices[0]]
        visited=[]
        while len(stack)>0:
            v=stack.pop()
            if v in visited:
                print("An Error Occured")
            visited.append(v)
            stack=[edge for edge in v.edges if edge not in visited]+[item for item in stack if (item not in v.edges and item not in visited)]
        return len(visited)==len(vertices)
    graph=Graph()
    for i in range(vertex_count):
        graph.add_vertex(Vertex())
    graph_to_positions(graph)
    #Generated With AI Assistance
    for vertex in graph.vertices:
        vertex._targ_amount =random.randint(1,max_edges)
        vertex.edges = []
    for vertex in graph.vertices:
        targ_amount = vertex._targ_amount

        #Calculate distances to other vertices and sort them
        distances = [(v, distance_squared(vertex.pos, v.pos)) for v in graph.vertices if v != vertex]
        distances.sort(key=lambda x: x[1])

        # Add edges to closest vertices
        for i in range(min(targ_amount, len(distances))):
            vertex.add_edge(distances[i][0])
    if not is_connected(graph.vertices):
        return gen_graph(vertex_count,max_edges)
    else:
        avpos=(0,0)
        for vertex in graph.vertices:
            avpos=(avpos[0]+vertex.pos.x,avpos[1]+vertex.pos.y)
        avpos=(avpos[0]/len(graph.vertices),avpos[1]/len(graph.vertices))
        
        _world_center= Vector2(_world_center.x-avpos[0],_world_center.y-avpos[1])


        return graph
if __name__=="__main__":
    gen_run(20,4,simulate.breadth_first)
    #run(gen_graph(15,2),simulate.breadth_first)
    
    #single_render(gen_graph(10,3))
