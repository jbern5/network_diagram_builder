import pyyed
import pandas as pd

df = pd.read_csv("net_data.csv")
df = df[df['cati'] == 'ICTO-0001']
df = df.sort_values(by=['data_center'])

g = pyyed.Graph()

data = {'data_centers': [],
        'level1_objects': [],
        'level2_objects': [],
        'level3_objects': [],
        'level4_objects': []
        }

coords = {}

listOfConnections = []
level1, level2, level3, level4 = ['lb'], ['dmz'], ['app'], ['db']
level1_count, level2_count, level3_count, level4_count = 0, 0, 0, 0

MAX_WIDTH = 1000

# Gets each data center and creates a group for each unique data center
for dc in df['data_center'].unique():
    if str(dc) != 'nan':
        data['data_centers'].append(g.add_group(str(dc)))



for index, node in df.iterrows():
    if node['zone'] in level1:
        data['level1_objects'].append(node)
    elif node['zone'] in level2:
        data['level2_objects'].append(node)
    elif node['zone'] in level3:
        data['level3_objects'].append(node)
    elif node['zone'] in level4:
        data['level4_objects'].append(node)

x4, y4 = 250, 400
x3, y3 = 0, 300
x2, y2 = 0, 200
for node in data['level3_objects']:
    for dc in data['data_centers']:
        if node['data_center'] == dc.label:
            dc.add_node(node['ip'], label=str(node['ip'] + "\n" + node['version']), height="50", width="100",
                        x=str(x3), y=str(y3))
            x3 += 150
for node in data['level2_objects']:
    for dc in data['data_centers']:
        if node['data_center'] == dc.label:
            dc.add_node(node['ip'], label=str(node['ip'] + "\n" + node['version']), height="50", width="100",
                        x=str(x2), y=str(y2))
            x2 += 150

x1, y1 = (MAX_WIDTH / len((data['level3_objects']))), 100
for node in data['level1_objects']:
    for dc in data['data_centers']:
        if node['data_center'] == dc.label:
            dc.add_node(node['ip'], label=str(node['ip'] + "\n" + node['version']), height="50", width="100",
                        x=str(x1), y=str(y1))
            x1 += 150
for node in data['level4_objects']:
    for dc in data['data_centers']:
        if node['data_center'] == dc.label:
            dc.add_node(node['ip'], label=str(node['ip'] + "\n" + node['version']), height="50", width="100",
                        x=str(x4), y=str(y4))
            x4 += 150


# for dc in data['data_centers']:
#     x1 = 'x_pos1' + str(dc)
#     y1 = 'y_pos1' + str(dc)
#     coords[x1] = 0
#     coords[y1] = 0
#
#     x2 = 'x_pos2' + str(dc)
#     y2 = 'y_pos2' + str(dc)
#     coords[x2] = 0
#     coords[y2] = 150
#
#     x3 = 'x_pos3' + str(dc)
#     y3 = 'y_pos3' + str(dc)
#     coords[x3] = 0
#     coords[y3] = 300
#
#     x4 = 'x_pos4' + str(dc)
#     y4 = 'y_pos4' + str(dc)
#     coords[x4] = 0
#     coords[y4] = 450
#
# # Nodes
# for index, node in df.iterrows():
#     for dc in data['data_centers']:
#         if node['zone'] in level1:
#             if node['data_center'] == dc.label:
#                 x_key = 'x_pos1' + str(dc)
#                 y_key = 'y_pos1' + str(dc)
#                 coords[x_key] += (MAX_WIDTH / (data['level1_count'] + 1))
#                 dc.add_node(node['ip'], label=str(node['ip'] + "\n" + node['version']), height="50", width="100", x=str(coords[x_key]), y=str(coords[y_key]))
#         if node['zone'] in level2:
#             if node['data_center'] == dc.label:
#                 x_key = 'x_pos2' + str(dc)
#                 y_key = 'y_pos2' + str(dc)
#                 coords[x_key] += (MAX_WIDTH / (data['level2_count'] + 1))
#                 dc.add_node(node['ip'], label=str(node['ip'] + "\n" + node['version']), height="50", width="100", x=str(coords[x_key]), y=str(coords[y_key]))
#         if node['zone'] in level3:
#             if node['data_center'] == dc.label:
#                 x_key = 'x_pos3' + str(dc)
#                 y_key = 'y_pos3' + str(dc)
#                 coords[x_key] += (MAX_WIDTH / data['level3_count'])
#                 dc.add_node(node['ip'], label=str(node['ip'] + "\n" + node['version']), height="50", width="100", x=str(coords[x_key]), y=str(coords[y_key]))
#         if node['zone'] in level4:
#             if node['data_center'] == dc.label:
#                 x_key = 'x_pos4' + str(dc)
#                 y_key = 'y_pos4' + str(dc)
#                 coords[x_key] += (MAX_WIDTH / data['level4_count'])
#                 dc.add_node(node['ip'], label=str(node['ip'] + "\n" + node['version']), height="50", width="100", x=str(coords[x_key]), y=str(coords[y_key]))

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


# data center object that takes a list of child node objects
