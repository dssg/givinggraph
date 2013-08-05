import networkx as nx
import csv
import matplotlib.pyplot as plt
import forceatlas as fa2
import community
import math

OUT_WIDTH = 8000
OUT_HEIGHT = 6000
dpi = 100

ITERATIONS = 500
nohubs = True

EDGE_WIDTH = 0.5
EDGE_ALPHA = 0.2

NODE_SIZE = 200
NODE_ALPHA = 0.5
NODE_LABEL_FONT_SIZE = 8

community_colors = {
    0: '#9e41d0',
    1: '#79e97d',
    2: '#0699f8',
    3: '#f66baf',
    4: '#49c69c',
    5: '#f0681a',
    6: '#614dc8',
    7: '#acaf92',
    8: '#bb559e',
    9: '#f7be87',
    10: '#215193',
        11: '#ded19d',
        12: '#608615',
        13: '#6d629c',
        14: '#fbd705',
        15: '#904413',
        16: '#06be68',
        17: '#ce575b',
        18: '#efe689',
        19: '#6da673',
        20: '#dc1783',
        21: '#f9b64e',
        22: '#4a3e88',
        23: '#e2d0b8',
}

G = nx.Graph()

reader = csv.reader(open('similarity2.csv', 'rb'), delimiter=',')
next(reader)

for edge in reader:
    my_list = [edge[0], edge[1], float(edge[2])]
    G.add_edge(my_list[0], my_list[1], weight=my_list[2])

k = math.sqrt(1.0/len(G.nodes()))

partition = community.best_partition(G)
#pos = fa2.forceatlas2_layout(G, iterations=ITERATIONS, nohubs=nohubs, linlog=True)
pos=nx.spring_layout(G, iterations=ITERATIONS)
colors = [community_colors.get(partition[node], '#000000') for node in G.nodes()]

nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=NODE_SIZE)
nx.draw_networkx_edges(G, pos, width=EDGE_WIDTH, alpha=EDGE_ALPHA)
nx.draw_networkx_labels(G,pos,font_size=NODE_LABEL_FONT_SIZE, alpha=NODE_ALPHA)

#nx.draw_networkx(G,pos=pos, node_color=colors)

nx.write_gml(G,'graph.gml')

fig = plt.gcf()
fig.set_size_inches(OUT_WIDTH/dpi, OUT_HEIGHT/dpi)
plt.savefig('fa2.png', dpi=dpi)

#plt.show()
