class Vertex:
    def __init__(self):
        self.edges=[]
        self.color=-1
    def degree(self):
        return len(self.edges)
    def add_edge(self,v: 'Vertex'):
        '''Adds an edge between both this vertex and another.'''
        if v not in self.edges:
            self.edges.append(v)
        if self not in v.edges:
            v.edges.append(self)
    def transfer_data(self,v:'Vertex'):
        v.color=self.color
    def can_walk_to(self,targ:'Vertex',excluding:['Vertex']):
        if self==targ:
            return True
        if len(self.edges)==0:
            return False
        
        stack=[edge for edge in self.edges if edge not in excluding]
        visited=[]

        while len(stack)>0:
            v=stack.pop()
            if v==targ:
                return True
            visited.append(v)
            stack=[edge for edge in v.edges if (edge not in visited and edge not in excluding)]+[item for item in stack if (item not in excluding and item not in v.edges and item not in visited)]

            
        return False

class Graph:
    def __init__(self):
        self.vertices=[]
        self.colors_used=0
    def new(self):
        return Graph()
    def add_color(self):
        self.colors_used+=1
    def transfer_colors(self,graph:'Graph'):
        graph.colors_used=self.colors_used
    def transfer_vertices(self,graph:'Graph'):
        graph.vertices.clear()
        for vertex in self.vertices:
            v=Vertex()
            vertex.transfer_data(v)
            graph.vertices.append(v)
    def add_edge(self,v:Vertex,v2:Vertex):
        '''Adds an edge between two vertices'''
        v.add_edge(v2)
    def add_vertex(self,v:Vertex):
        '''Adds a vertex to the graph '''
        self.vertices.append(v)
        #We will keep vertices sorted by their degrees
        self.vertices=sorted(self.vertices, key=lambda vertex: len(vertex.edges), reverse=False)

    def largest_degree(self):
        if len(self.vertices)==0:
            raise ValueError("Graph is empty!")
        largest=-1
        for vertex in self.vertices:
            if largest==-1 or largest < vertex.degree():
                largest=vertex.degree()
        return largest
    def smallest_degree(self):
        if len(self.vertices)==0:
            raise ValueError("Graph is empty!")
        smallest=len(self.vertices)+1
        for vertex in self.vertices:
            if smallest==len(self.vertices)+1 or smallest > vertex.degree():
                smallest=vertex.degree()
        return smallest
    def vertex_count(self):
        return len(self.vertices)
    def __len__(self):
        return self.vertex_count()
    def __eq__(self,other):
        return self.vertices==other.vertices and self.colors_used==other.colors_used
    def chromatic_number(self):
        return self.colors_used
