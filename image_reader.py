import render_graph
import simulate
from graph_wrappers import PyVertex as Vertex
from graph_wrappers import PyGraph as Graph
import pygame
from pygame import Vector2

class Continent:
    def __init__(self):
        self.pixels=dict()
        self.avg_pos=(0,0)
        self.real_value=None
        self.neighbors=set()
        self.color=None
    def real(self):
        if self.real_value is self:
            raise ValueError("Real Value Cannot Be Self!")
        if self.real_value is None:
            return self
        else:
            return self.real_value.real()
    def pos(self):
        return Vector2(self.avg_pos[0]*4,self.avg_pos[1]*4)
    def add_pixel(self,pos:tuple):
        self.pixels[(pos[0],pos[1])]=True
        if len(pos) > 2:
            self.color=pos[2]
        if len(self.pixels)==0:
            self.avg_pos=pos
        else:
            x=self.avg_pos[0]
            y=self.avg_pos[1]

            x*=len(self.pixels)/(len(self.pixels)+1)
            x+=pos[0]/(len(self.pixels)+1)
            
            y*=len(self.pixels)/(len(self.pixels)+1)
            y+=pos[1]/(len(self.pixels)+1)

            self.avg_pos=(x,y)
    def merge_continent(self,continent:'Continent'):
        if self == continent:
            return
        #print("Merge")
        for pos in continent.pixels.keys():
            self.add_pixel(pos)
        continent.pixels=dict()
        continent.avg_pos=(0,0)
        continent.real_value=self.real()
        self.neighbors|=continent.neighbors
    def has_pixel(self,pos:tuple):
        if len(pos)>2:
            return (pos[0],pos[1]) in self.pixels and pos[2] ==self.color
            
        return (pos[0],pos[1]) in self.pixels
class World:
    def __init__(self):
        self.continents=[]
        self.bridges=[]
    
    def add_pixel(self,pos:tuple,bridge:bool):
        if not bridge:
            if len(self.continents)==0:
                self.continents.append(Continent())
                self.continents[0].add_pixel(pos)

                for c in self.bridges:
                    if c.has_pixel((pos[0],pos[1]+1)):
                        c.neighbors|={self.continents[0]}
                    elif c.has_pixel((pos[0]-1,pos[1])):
                        c.neighbors|={self.continents[0]}
                    elif c.has_pixel((pos[0]+1,pos[1])):
                        c.neighbors|={self.continents[0]}
                    elif c.has_pixel((pos[0],pos[1]-1)):
                        c.neighbors|={self.continents[0]}                
            else:
                added=None
                i=0
                for c in self.continents:
                    if added is None:
                        if c.has_pixel((pos[0],pos[1]+1,pos[2])):
                            c.add_pixel(pos)
                            added=c
                        elif c.has_pixel((pos[0]-1,pos[1],pos[2])):
                            c.add_pixel(pos)
                            added=c
                        elif c.has_pixel((pos[0]+1,pos[1],pos[2])):
                            c.add_pixel(pos)
                            added=c
                        elif c.has_pixel((pos[0],pos[1]-1,pos[2])):
                            c.add_pixel(pos)
                            added=c
                    else:
                        if c.has_pixel((pos[0],pos[1]+1,pos[2])):
                            added.merge_continent(self.continents.pop(i))
                            i-=1
                        elif c.has_pixel((pos[0]-1,pos[1],pos[2])):
                            added.merge_continent(self.continents.pop(i))
                            i-=1
                        elif c.has_pixel((pos[0]+1,pos[1],pos[2])):
                            added.merge_continent(self.continents.pop(i))
                            i-=1
                        elif c.has_pixel((pos[0],pos[1]-1,pos[2])):
                            added.merge_continent(self.continents.pop(i))
                            i-=1
                        
                    i+=1
                if added is None:
                    cn=Continent()
                    cn.add_pixel(pos)
                    self.continents.append(cn)
                    
                    for c in self.bridges:
                        if c.has_pixel((pos[0],pos[1]+1)):
                            c.neighbors|={cn}
                        elif c.has_pixel((pos[0]-1,pos[1])):
                            c.neighbors|={cn}
                        elif c.has_pixel((pos[0]+1,pos[1])):
                            c.neighbors|={cn}
                        elif c.has_pixel((pos[0],pos[1]-1)):
                            c.neighbors|={cn}
                    i=0
                    for c in self.continents:
                        if c !=cn:
                            if c.has_pixel((pos[0],pos[1]+1,pos[2])):
                                cn.merge_continent(self.continents.pop(i))
                                i-=1
                            elif c.has_pixel((pos[0]-1,pos[1],pos[2])):
                                cn.merge_continent(self.continents.pop(i))
                                i-=1
                            elif c.has_pixel((pos[0]+1,pos[1],pos[2])):
                                cn.merge_continent(self.continents.pop(i))
                                i-=1
                            elif c.has_pixel((pos[0],pos[1]-1,pos[2])):
                                cn.merge_continent(self.continents.pop(i))
                                i-=1
                        i+=1
                else:
                    for c in self.bridges:
                        if c.has_pixel((pos[0]+0,pos[1]+1)):
                            c.neighbors|={added}
                        elif c.has_pixel((pos[0]-1,pos[1])):
                            c.neighbors|={added}
                        elif c.has_pixel((pos[0]+1,pos[1])):
                            c.neighbors|={added}
                        elif c.has_pixel((pos[0],pos[1]-1)):
                            c.neighbors|={added}
        else:
            if len(self.bridges)==0:
                self.bridges.append(Continent())
                self.bridges[0].add_pixel(pos)
                for c in self.continents:
                    if c.has_pixel((pos[0],pos[1]+1)):
                        self.bridges[0].neighbors|={c}
                    elif c.has_pixel((pos[0]-1,pos[1])):
                        self.bridges[0].neighbors|={c}
                    elif c.has_pixel((pos[0]+1,pos[1])):
                        self.bridges[0].neighbors|={c}
                    elif c.has_pixel((pos[0],pos[1]-1)):
                        self.bridges[0].neighbors|={c}
            else:
                added=None
                i=0
                for c in self.bridges:
                    if added is None:
                        if c.has_pixel((pos[0],pos[1]+1,pos[2])):
                            c.add_pixel(pos)
                            added=c
                        elif c.has_pixel((pos[0]-1,pos[1],pos[2])):
                            c.add_pixel(pos)
                            added=c
                        elif c.has_pixel((pos[0]+1,pos[1],pos[2])):
                            c.add_pixel(pos)
                            added=c
                        elif c.has_pixel((pos[0],pos[1]-1,pos[2])):
                            c.add_pixel(pos)
                            added=c
                        elif c.has_pixel((pos[0]-1,pos[1]-1,pos[2])):
                            c.add_pixel(pos)
                            added=c
                        elif c.has_pixel((pos[0]+1,pos[1]-1,pos[2])):
                            c.add_pixel(pos)
                            added=c
                        elif c.has_pixel((pos[0]-1,pos[1]+1,pos[2])):
                            c.add_pixel(pos)
                            added=c
                        elif c.has_pixel((pos[0]+1,pos[1]+1,pos[2])):
                            c.add_pixel(pos)
                            added=c
                    else:
                        if c.has_pixel((pos[0],pos[1]+1,pos[2])):
                            added.merge_continent(self.bridges.pop(i))
                            i-=1
                        elif c.has_pixel((pos[0]-1,pos[1],pos[2])):
                            added.merge_continent(self.bridges.pop(i))
                            i-=1
                        elif c.has_pixel((pos[0]+1,pos[1],pos[2])):
                            added.merge_continent(self.bridges.pop(i))
                            i-=1
                        elif c.has_pixel((pos[0],pos[1]-1,pos[2])):
                            added.merge_continent(self.bridges.pop(i))
                            i-=1
                        elif c.has_pixel((pos[0]-1,pos[1]-1,pos[2])):
                            added.merge_continent(self.bridges.pop(i))
                            i-=1
                        elif c.has_pixel((pos[0]+1,pos[1]-1,pos[2])):
                            added.merge_continent(self.bridges.pop(i))
                            i-=1
                        elif c.has_pixel((pos[0]-1,pos[1]+1,pos[2])):
                            added.merge_continent(self.bridges.pop(i))
                            i-=1
                        elif c.has_pixel((pos[0]+1,pos[1]+1,pos[2])):
                            added.merge_continent(self.bridges.pop(i))
                            i-=1
                        
                    i+=1
                if added is None:
                    cn=Continent()
                    cn.add_pixel(pos)
                    self.bridges.append(cn)
                    
                    for c in self.continents:
                        if c.has_pixel((pos[0],pos[1]+1)):
                            cn.neighbors|={c}
                        elif c.has_pixel((pos[0]-1,pos[1])):
                            cn.neighbors|={c}
                        elif c.has_pixel((pos[0]+1,pos[1])):
                            cn.neighbors|={c}
                        elif c.has_pixel((pos[0],pos[1]-1)):
                            cn.neighbors|={c}
                    i=0
                    for c in self.bridges:
                        if c !=cn:
                            if c.has_pixel((pos[0],pos[1]+1,pos[2])):
                                cn.merge_continent(self.bridges.pop(i))
                                i-=1
                            elif c.has_pixel((pos[0]-1,pos[1],pos[2])):
                                cn.merge_continent(self.bridges.pop(i))
                                i-=1
                            elif c.has_pixel((pos[0]+1,pos[1],pos[2])):
                                cn.merge_continent(self.bridges.pop(i))
                                i-=1
                            elif c.has_pixel((pos[0],pos[1]-1,pos[2])):
                                cn.merge_continent(self.bridges.pop(i))
                                i-=1
                            elif c.has_pixel((pos[0]-1,pos[1]-1,pos[2])):
                                cn.merge_continent(self.bridges.pop(i))
                                i-=1
                            elif c.has_pixel((pos[0]+1,pos[1]-1,pos[2])):
                                cn.merge_continent(self.bridges.pop(i))
                                i-=1
                            elif c.has_pixel((pos[0]-1,pos[1]+1,pos[2])):
                                cn.merge_continent(self.bridges.pop(i))
                                i-=1
                            elif c.has_pixel((pos[0]+1,pos[1]+1,pos[2])):
                                cn.merge_continent(self.bridges.pop(i))
                                i-=1
                        i+=1
                else:
                    for c in self.continents:
                        if c.has_pixel((pos[0],pos[1]+1)):
                            added.neighbors|={c}
                        elif c.has_pixel((pos[0]-1,pos[1])):
                            added.neighbors|={c}
                        elif c.has_pixel((pos[0]+1,pos[1])):
                            added.neighbors|={c}
                        elif c.has_pixel((pos[0],pos[1]-1)):
                            added.neighbors|={c}
                            
                
        
def img_to_graph(path):
    '''Reads in a png picture and converts it to a graph'''
    pygame.init()
    img = pygame.image.load(path)
    pygame.quit()
    width, height = img.get_size()
    world=World()
    #print(width,height,sep="x")
    for col in range(width):
        for row in range(height):
            pixel_color = img.get_at((col, row))


            if pixel_color.a >= 100:
                if pixel_color.r>=100 and pixel_color.g<=100 and pixel_color.b<=100:
                    world.add_pixel((col,row,(pixel_color.r,pixel_color.g,pixel_color.b,pixel_color.a)),True)
                else:
                    world.add_pixel((col,row,(pixel_color.r,pixel_color.g,pixel_color.b,pixel_color.a)),False)
                  
    graph=Graph()
    for c in world.continents:
        v =Vertex()
        v.pos=c.pos()
        #print(v.pos)
        graph.add_vertex(v)
    
    for b in world.bridges:
        
        neighbors=[]
        for el in b.real().neighbors:
            #print(el.real().pos())
            if el.real() in world.continents and el.real() not in neighbors:
                neighbors.append(el.real())
            
        if len(neighbors)>=2:
            c=neighbors[0]
            c2=neighbors[1]
            graph.get_at(c.pos()).add_edge(graph.get_at(c2.pos()))
       # else:
            #BROKEN LINKS
        #    v =Vertex()
         #   v.pos=b.real().pos()
            #print(v.pos)
          #  graph.add_vertex(v)

    graph.vertices=sorted(graph.vertices, key=lambda vertex: len(vertex.edges), reverse=False)
    for vertex in graph.vertices:
        scale_factor=3
        vertex.pos=Vector2(vertex.pos.x/scale_factor,vertex.pos.y/scale_factor)
    return graph
def printcsv(graph):
    mapping=dict()
    numVertex=1
    visited=[]
    for vertex in graph.vertices:
        if not vertex in mapping:
            mapping[vertex]=numVertex
            numVertex+=1
        curVert=mapping[vertex]
        if len(vertex.edges)==0:
            print(curVert)
        for edge in vertex.edges:
            if not edge in mapping:
                mapping[edge]=numVertex
                numVertex+=1
            curEdge=mapping[edge]
            if not {curVert,curEdge} in visited:
                print(curVert,curEdge,sep=",")
                visited.append({curVert,curEdge})
def main():
    graph=img_to_graph("toxive.png")
    printcsv(graph)
    
    render_graph.run(graph,simulate.depth_first)
    #render_graph.run(graph,simulate.breadth_first)
    
    #list(simulate.breadth_first(graph))
    #render_graph.single_render(graph)

if __name__=="__main__":
    main()
