import render_graph

import simulate


def main():
    while True:
        graph=render_graph.gen_graph(14,5)
        #list(simulate.depth_first(graph))
        list(simulate.breadth_first(graph))
    
        if not render_graph.single_render(graph):
            break

if __name__=="__main__":
    main()
