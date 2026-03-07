# Transport Network Map

import networkx as nx
import matplotlib.pyplot as plt

# Create a graph object
MyGraph = nx.Graph()

# Add nodes
# Green Line
MyGraph.add_node('A', npos=(10, 10), ccn='#00FF00')
MyGraph.add_node('B', npos=(50, 50), ccn='#E0E0E0')
MyGraph.add_node('C', npos=(50, 90), ccn='#00FF00')
MyGraph.add_node('D', npos=(75, 90), ccn='#00FF00')
# Orange Line
MyGraph.add_node('E', npos=(90, 90), ccn='#FF4500')
MyGraph.add_node('F', npos=(175, 90), ccn='#FF4500')
MyGraph.add_node('G', npos=(175, 70), ccn='#FF4500')
# Blue Line
MyGraph.add_node('H', npos=(100, 65), ccn='#0000FF')
MyGraph.add_node('I', npos=(130, 55), ccn='#0000FF')
MyGraph.add_node('J', npos=(150, 25), ccn='#0000FF')

# Connect nodes
# Green Line
MyGraph.add_edge('A', 'B', cce='#00FF00')
MyGraph.add_edge('B', 'C', cce='#00FF00')
MyGraph.add_edge('C', 'D', cce='#00FF00')
# Orange Line
MyGraph.add_edge('B', 'E', cce='#FF4500')
MyGraph.add_edge('E', 'F', cce='#FF4500')
MyGraph.add_edge('F', 'G', cce='#FF4500')
# Blue Line
MyGraph.add_edge('B', 'H', cce='#0000FF')
MyGraph.add_edge('H', 'I', cce='#0000FF')
MyGraph.add_edge('I', 'J', cce='#0000FF')

# Extract attributes from the graph to dictionaries
pos = nx.get_node_attributes(MyGraph, 'npos')
nodecolour = nx.get_node_attributes(MyGraph, 'ccn')
edgecolour = nx.get_edge_attributes(MyGraph, 'cce')

# Place the dictionary values in lists
NodeList = list(nodecolour.values())
EdgeList = list(edgecolour.values())

# Set the size of the figure
plt.figure(figsize=(10, 7))

# Setup the plotting area
plt.axis([0, 200, 0, 100])
plt.xticks([])
plt.yticks([])

# Display the names of the stations
plt.text(18, 10, s='Green Station 1')
plt.text(8, 50, s='Interchange Station')
plt.text(16, 90, s='Green Station 2')
plt.text(54, 80, s='Green Station 3', rotation=15)

plt.text(85, 77, s='Orange Station 1', rotation=15)
plt.text(143, 80, s='Orange Station 2', rotation=15)
plt.text(140, 62, s='Orange Station 3', rotation=15)

plt.text(104, 68, s='Blue Station 1')
plt.text(100, 48, s='Blue Station 2', rotation=15)
plt.text(120, 24, s='Blue Station 3')

# Draw the nodes and the edges
nx.draw_networkx(MyGraph, pos, node_color=NodeList)
nx.draw_networkx_edges(MyGraph, pos, edge_color=EdgeList)

# Visualise the graph
plt.show()