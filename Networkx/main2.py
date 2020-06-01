import pandas as pd
from v4 import network_test as nx
import matplotlib.pyplot as plt
import random
# G.add_edges_from([(1,2), (1,3), (1,4), (2,5), (2,6), (2,7), (3,8), (3,9), (4,10),
#                   (5,11), (5,12), (6,13)])
# G = nx.Graph()
# nodes = [{'data': 'one', 'type': 'dmz', 'connections': ['two', 'three', 'four']},
#          {'data': 'two', 'type': 'dmz', 'connections': ['five', 'six', 'seven']},
#          {'data': 'three', 'type': 'dmz', 'connections': ['eight', 'nine']},
#          {'data': 'four', 'type': 'dmz', 'connections': ['ten']},
#          {'data': 'five', 'type': 'dmz', 'connections': ['eleven', 'twelve']},
#          {'data': 'six', 'type': 'dmz', 'connections': ['thirteen']},
#          {'data': 'seven', 'type': 'dmz', 'connections': []},
#          {'data': 'eight', 'type': 'dmz', 'connections': []},
#          {'data': 'nine', 'type': 'dmz', 'connections': []},
#          {'data': 'ten', 'type': 'dmz', 'connections': []},
#          {'data': 'eleven', 'type': 'dmz', 'connections': []},
#          {'data': 'twelve', 'type': 'dmz', 'connections': []},
#          {'data': 'thirteen', 'type': 'dmz', 'connections': []}]

# nodes2 = {'ip': ['1.1.1.1', '2.2.2.2', '3.3.3.3'], 'connections': [['2.2.2.2', '3.3.3.3'], [], []]}
# nodes_df = pd.DataFrame(data=nodes2)
# export_csv = nodes_df.to_csv (r'/Users/justinbernstein/Desktop/Internship/Networkx/net_data.csv', index = None, header=True)


# for node in nodes:
#     for edge in node['connections']:
#         G.add_edge(node['data'], edge)


def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):

    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.
    Licensed under Creative Commons Attribution-Share Alike

    If the graph is a tree this will return the positions to plot this in a
    hierarchical layout.

    G: the graph (must be a tree)

    root: the root node of current branch
    - if the tree is directed and this is not given,
      the root will be found and used
    - if the tree is directed and this is given, then
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given,
      then a random choice will be used.

    width: horizontal space allocated for this branch - avoids overlap with other branches

    vert_gap: gap between levels of hierarchy

    vert_loc: vertical location of root

    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''

        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children)!=0:
            dx = width/len(children)
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap,
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos


    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

G=nx.Graph()
# G.add_edges_from([('1.1.1.1', '2.2.2.2'), ('1.1.1.1', '3.3.3.3'), ('1.1.1.1', '4.4.4.4'), ('2.2.2.2', '5.5.5.5'), ('2.2.2.2','6.6.6.6'), ('2.2.2.2','7.7.7.7'),
#                   ('3.3.3.3','8.8.8.8'), ('3.3.3.3','9.9.9.9'), ('4.4.4.4','10.10.10.10')])

df = pd.read_csv("net_data.csv")
listOfConnections = []

# for node in df['ip']:
#     G.add_nodes_

for index, node in df.iterrows():
    if str(node['connections']) != 'nan':
        connections = node['connections'].split(',')
        for conn in connections:
            listOfConnections.append((node['ip'], str(conn)))
print(listOfConnections)
G.add_edges_from(listOfConnections)
pos = hierarchy_pos(G, '1.1.1.1')

nx.draw_networkx_labels(G, pos)
nx.draw_networkx_nodes(G, pos, node_shape="s", node_size=[1000, 500])
nx.draw_networkx_edges(G, pos)
# nx.draw(G, pos=pos, with_labels=True)
plt.draw()
plt.show()
