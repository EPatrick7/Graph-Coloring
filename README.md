# Graph Coloring P Vs NP Visualizer
This python project is a PyGame undirected graph visualizer for testing out algorithms for minimal graph coloring.
There are two sets of Graph/Vertex classes, one that is a wrapper class adding PyGame visualizing functionality, and one that contains just edge relations for algorithms.

The main feature of the project is the live PyGame visualization of graph coloring. By default, a depth-first and breadth-first greedy algorithm has been provided, but this algorithm can take years with high amounts of vertices.
By replacing the code in the algorithm function of solution.py, the pygame visualizer will compare the outcomes of the new algorithm with the slow baseline, and determine if it is a correct algorithm.

In addition to randomly generated undirected graphs, this project also includes a png-to-graph interpreter. The drawings must be in white, red, transparent. White represents vertices, and red the edges between them. Provided are a map of the United States, and one simple graph doodle.


**Optimized coloring of a randomly generated undirected graph.**
![Optimized Colored Undirected Graph](https://drive.google.com/uc?id=1piYnMlpdtzZu-OlpvukzZvmWNOBhrmls)

**In-progress coloring of the US map.**
![Visualized Map Of The US (In Progress)](https://drive.google.com/uc?id=1MEbJ18bSoYqIrbN2iH4gFSn6yUXfOmnu)
