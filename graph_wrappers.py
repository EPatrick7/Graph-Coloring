import pygame
from pygame.math import Vector2
from pygame import Color
import random

import graph as base_graph


class PyVertex(base_graph.Vertex):
    def __init__(self):
        base_graph.Vertex.__init__(self)
        self.pos=Vector2()
    
    def transfer_data(self,v:'Vertex'):
        super().transfer_data(v)
        v.pos=Vector2(self.pos.x,self.pos.y)

        
class PyGraph(base_graph.Graph):
    def __init__(self):
        base_graph.Graph.__init__(self)
        self.center=Vector2()
        self.colors=[]
    def get_color(self,vertex):
        if vertex.color==-1:
            return Color(255,255,255)
        else:
            return self.colors[vertex.color]
    def new(self):
        return PyGraph()
    
    def shallow_transfer_colors(self,graph:'PyGraph'):
        super().transfer_colors(graph)
        graph.colors.clear()
        for col in self.colors:
            graph.colors.append(Color(col.r,col.g,col.b))
    def get_at(self,pos):
        for vertex in self.vertices:
            if vertex.pos==pos:
                return vertex
        raise ValueError("Nothing found at position "+str(pos))
    def shallow_transfer_vertices(self,graph:'PyGraph'):
        graph.vertices.clear()
        for vertex in self.vertices:
            graph.vertices.append(vertex)
    def transfer_colors(self,graph:'PyGraph'):
        super().transfer_colors(graph)
        graph.colors.clear()
        for col in self.colors:
            graph.colors.append(col)
    def transfer_vertices(self,graph:'PyGraph'):
        graph.vertices.clear()
        for vertex in self.vertices:
            v=PyVertex()
            vertex.transfer_data(v)
            graph.vertices.append(v)
    def add_color(self):
        super().add_color()
        if len(self.colors)==0:
            self.colors.append(Color(255,0,0))
        elif len(self.colors)==1:
            self.colors.append(Color(0,255,0))
        elif len(self.colors)==2:
            self.colors.append(Color(0,0,255))
        elif len(self.colors)==3:
            self.colors.append(Color(0,255,255))
        elif len(self.colors)==4:
            self.colors.append(Color(255,0,255))
        elif len(self.colors)==5:
            self.colors.append(Color(255,255,0))
        elif len(self.colors)==6:
            self.colors.append(Color(162,0,255))
        elif len(self.colors)==7:
            self.colors.append(Color(255,0,162))
        else:
            self.colors.append(Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

