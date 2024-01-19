from graph import Vertex
from graph import Graph

import random

class SaveState:
    def __init__(self,graph:Graph,stack,visited,new_stack):
        self.graph=graph.new()

        graph.transfer_colors(self.graph)
        graph.transfer_vertices(self.graph)

        i=0
        for vertex in graph.vertices:
            v=self.graph.vertices[i]
            for edge in vertex.edges:
                v.add_edge(self.graph.vertices[graph.vertices.index(edge)])
            i+=1
        self.stack=[]
        for ver in stack:
            self.stack.append(self.graph.vertices[graph.vertices.index(ver)])
            
        self.visited=[]
        for ver in visited:
            self.visited.append(self.graph.vertices[graph.vertices.index(ver)])

        if new_stack is not None:
            self.new_stack=[]
            for ver in new_stack:
                self.new_stack.append(self.graph.vertices[graph.vertices.index(ver)])
            
    def load(self,graph:'Graph',stack,visited,new_stack):
        graph.vertices.clear()
        self.graph.shallow_transfer_colors(graph)
        self.graph.shallow_transfer_vertices(graph)
        

        stack.clear()
        for ver in self.stack:
            stack.append(ver)
            
        visited.clear()
        for ver in self.visited:
            visited.append(ver)
            
        if new_stack is not None:
            new_stack.clear()
            for ver in self.new_stack:
                new_stack.append(ver)

def depth_first(graph:Graph):
    save_states=[]
    started=False

    best_state=None


    while not started or len(save_states)>0:

        stack=[graph.vertices[0]]
        visited=[]

        if started:
            live=save_states.pop()
            stack.clear()
            visited.clear()
            live.load(graph,stack,visited,None)


            
        started=True

        while len(stack) > 0:
            if best_state is not None:
                if graph.colors_used >= best_state.graph.colors_used:
                    break
            
            v=stack.pop()
            if v in visited:
                raise Exception("Traversal Failed!")
            visited.append(v)
            stack=[edge for edge in v.edges if edge not in visited]+[item for item in stack if (item not in v.edges and item not in visited)]

            #Determine Color:

            if graph.colors_used==0:
                graph.add_color()
            taken_colors=[]
            for edge in v.edges:
                taken_colors.append(edge.color)
            options=[item for item in list(range(graph.colors_used)) if item not in taken_colors]
            if len(options)==0:
                graph.add_color()
                options.append(graph.colors_used-1)
                
            for i in range(1,len(options)):
                v.color=options[i]
                save_states.append(SaveState(graph,stack,visited,None))
                
                #Split save state here

            #This state will use the first option available:
            v.color=options[0]

            
            #
            yield

            if len(stack)==0: #Catch Isolated Segments (IE Not Connected Graph)
                for ver in graph.vertices:
                    if ver not in visited:
                        stack.append(ver)
                        break

        
        if best_state is None or graph.colors_used < best_state.graph.colors_used:
            best_state=SaveState(graph,stack,visited,None)
    best_state.load(graph,stack,visited,None)
    print("\nOptimal Coloring Discovered:\nOptimal Graph Chromatic Number Of " + str(graph.colors_used)+"\nVertex Count Of "+str(graph.vertex_count())+"\nLargest Degree Of "+str(graph.largest_degree())+"\nSmallest Degree Of "+str(graph.smallest_degree()))
        


def breadth_first(graph:Graph):
    save_states=[]
    started=False

    best_state=None


    while not started or len(save_states)>0:

        stack=[graph.vertices[0]]
        new_stack=[]
        visited=[]

        if started:
            live=save_states.pop()
            stack.clear()
            visited.clear()
            live.load(graph,stack,visited,new_stack)


            
        started=True

        while len(new_stack)>0 or len(stack)>0:
            if best_state is not None:
                if graph.colors_used >= best_state.graph.colors_used:
                    break
            while len(stack) > 0:
                if best_state is not None:
                    if graph.colors_used >= best_state.graph.colors_used:
                        break
                v=stack.pop()
                if v in visited:
                    raise Exception("Traversal Failed!")
                visited.append(v)
                new_stack=[el for el in (v.edges+[item for item in new_stack if item not in v.edges]) if el not in visited]
                
                #Determine Color:

                if graph.colors_used==0:
                    graph.add_color()
                taken_colors=[]
                for edge in v.edges:
                    taken_colors.append(edge.color)
                options=[item for item in list(range(graph.colors_used)) if item not in taken_colors]
                if len(options)==0:
                    graph.add_color()
                    options.append(graph.colors_used-1)
                    
                for i in range(1,len(options)):
                    v.color=options[i]
                    save_states.append(SaveState(graph,stack,visited,new_stack))
                    
                    #Split save state here

                #This state will use the first option available:
                v.color=options[0]

                
                #
                yield
            stack=new_stack

            if len(stack)==0: #Catch Isolated Segments (IE Not Connected Graph)
                for ver in graph.vertices:
                    if ver not in visited:
                        stack.append(ver)
                        break

        
        if best_state is None or graph.colors_used < best_state.graph.colors_used:
            best_state=SaveState(graph,stack,visited,new_stack)
    best_state.load(graph,stack,visited,new_stack)
    print("\nOptimal Coloring Discovered:\nOptimal Graph Chromatic Number Of " + str(graph.colors_used)+"\nVertex Count Of "+str(graph.vertex_count())+"\nLargest Degree Of "+str(graph.largest_degree())+"\nSmallest Degree Of "+str(graph.smallest_degree()))
        
