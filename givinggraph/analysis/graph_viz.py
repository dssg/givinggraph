import networkx as nx
import csv
import matplotlib.pyplot as plt
import forceatlas as fa2
import community

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

reader = csv.reader(open('friends.csv', 'rb'), delimiter=';')

for edge in reader:
    my_list = [edge[0], edge[1]]
    my_list2 = [unicode(s, errors='ignore') for s in my_list]
    G.add_edge(my_list2[0], my_list2[1])

partition = community.best_partition(G)
pos = fa2.forceatlas2_layout(G, iterations=500, nohubs=True)
colors = [community_colors.get(partition[node], '#000000') for node in G.nodes()]
nx.draw(G, pos, node_color=colors)

fig = plt.gcf()
fig.set_size_inches(80, 60)
plt.savefig('graph.png', dpi=100)

plt.show()
