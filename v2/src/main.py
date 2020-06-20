import pyyed
import pandas as pd
import sys
from data_center import DataCenter

# cati = sys.argv[1]
cati = 'ICTO-0001'
# Data wrangling
df = pd.read_csv("net_data.csv")

df = df[df['cati'] == cati]
df = df.sort_values(by='data_center')

# Create the yed graph
g = pyyed.Graph(graph_id=cati)

# Local storage
data = {'data_centers': [],
        'level1_count': 0,
        'level2_count': 0,
        'level3_count': 0,
        }
graph = {'data_centers': []}

listOfConnections = []
level1, level2, level3 = ['lb'], ['dmz'], ['app']
level1_count, level2_count, level3_count = 0, 0, 0

MAX_WIDTH = 1500
global_x_start = 0


# Gets each data center and creates a group for each unique data center
for dc in df['data_center'].unique():
    if str(dc) != 'nan':
        # data['data_centers'].append(g.add_group(str(dc)))
        data['data_centers'].append(DataCenter(str(dc), global_x_start))
        global_x_start += 500 # MAX_WIDTH / len(df['data_center'].unique())

g.add_node('title', label=str(cati), height="50", width="200", x=str(global_x_start / 3), y=str(0), shape_fill='#dadee6', font_size='20')


'''
    for data center in datacenter list, call data center add to graph function and pass the main graph
'''

for index, node in df.iterrows():
    for dc in data['data_centers']:
        if node['data_center'] == dc.get_name():
            dc.add_child_object(node['ip'], node)


for dc in data['data_centers']:
    graph['data_centers'].append(g.add_group(str(dc.get_name()), fill='#2153c4', font_style='bold'))

for dc_group in graph['data_centers']:
    for dc in data['data_centers']:
        if dc_group.label == dc.get_name():
            dc.add_to_graph(g, dc_group)

# Edges
for index, node in df.iterrows():
    if str(node['connections']) != 'nan':
        connections = node['connections'].split(',')
        for conn in connections:
            listOfConnections.append((node['ip'], str(conn)))

for conn in listOfConnections:
    g.add_edge(conn[0], conn[1])

z = g.get_graph()
print(g.nodes)
# TEMP
# cati = 'ICTO-0001'

with open("graphs/" + cati + '.graphml', 'w') as graph_file:
    graph_file.write(z)
    graph_file.close()
