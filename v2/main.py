import pyyed
import pandas as pd
from data_center import DataCenter

df = pd.read_csv("net_data.csv")
df = df[df['cati'] == 'ICTO-0001']

g = pyyed.Graph()

data = {'data_centers': [],
        'level1_count': 0,
        'level2_count': 0,
        'level3_count': 0,
        }
graph = {'data_centers': []}

listOfConnections = []
level1, level2, level3 = ['lb'], ['dmz'], ['app']
level1_count, level2_count, level3_count = 0, 0, 0

MAX_WIDTH = 1000
global_x_start = 0
x_pos1 = 0
y_pos1 = 0
x_pos2 = 0
y_pos2 = 150
x_pos3 = 0
y_pos3 = 300

# for dc in df['data_center'].unique():
#     if str(dc) != 'nan':
#         data['data_centers'].append({dc: []})
# for index, node in df.iterrows():
#     for dc in data['data_centers']:
#         for k, v in dc.items():
#             if node['data_center'] == k:
#                 v.append(node['ip'])

# Gets each data center and creates a group for each unique data center
for dc in df['data_center'].unique():
    if str(dc) != 'nan':
        # data['data_centers'].append(g.add_group(str(dc)))
        data['data_centers'].append(DataCenter(str(dc), global_x_start))
        global_x_start += 500


'''
    for data center in datacenter list, call data center add to graph function and pass the main graph
'''

for index, node in df.iterrows():
    for dc in data['data_centers']:
        if node['data_center'] == dc.get_name():
            dc.add_child_object(node['ip'], node)


for dc in data['data_centers']:
    graph['data_centers'].append(g.add_group(str(dc.get_name())))

for dc_group in graph['data_centers']:
    for dc in data['data_centers']:
        if dc_group.label == dc.get_name():
            dc.add_to_graph(g, dc_group)



# for dc in data['data_centers']:
#     print(dc.get_name())

# for index, node in df.iterrows():
#     if node['zone'] in level1:
#         data['level1_count'] += 1
#     elif node['zone'] in level2:
#         data['level2_count'] += 1
#     elif node['zone'] in level3:
#         data['level3_count'] += 1
#
# # Nodes
# for index, node in df.iterrows():
#     for dc in data['data_centers']:
#         if node['zone'] in level1:
#             if node['data_center'] == dc.label:
#                 x_pos1 += (MAX_WIDTH / (data['level1_count'] + 1))
#                 dc.add_node(node['ip'], label=str(node['ip'] + "\n" + node['version']), height="50", width="100", x=str(x_pos1), y=str(y_pos1))
#             # else:
#             #     g.add_node(node['ip'], label=str(node['ip'] + "\n" + node['version']), height="50", width="100", x=str(x_pos1), y=str(y_pos1))
#         if node['zone'] in level2:
#             if node['data_center'] == dc.label:
#                 x_pos2 += (MAX_WIDTH / (data['level2_count'] + 1))
#                 dc.add_node(node['ip'], label=str(node['ip'] + "\n" + node['version']), height="50", width="100", x=str(x_pos2), y=str(y_pos2))
#         if node['zone'] in level3:
#             if node['data_center'] == dc.label:
#                 x_pos3 += (MAX_WIDTH / data['level3_count'])
#                 dc.add_node(node['ip'], label=str(node['ip'] + "\n" + node['version']), height="50", width="100", x=str(x_pos3), y=str(y_pos3))
#
# Edges
for index, node in df.iterrows():
    if str(node['connections']) != 'nan':
        connections = node['connections'].split(',')
        for conn in connections:
            listOfConnections.append((node['ip'], str(conn)))

for conn in listOfConnections:
    g.add_edge(conn[0], conn[1])

z = g.get_graph()

graph_file = open("test" + '.graphml', 'w')
graph_file.write(z)
graph_file.close()
#
#
# # data center object that takes a list of child node objects
