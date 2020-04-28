import pyyed
import pandas as pd

df = pd.read_csv("net_data.csv")
df = df[df['cati'] == 'ICTO-0001']

g = pyyed.Graph()

data = {'data_centers': [],
        'level1_count': 0,
        'level2_count': 0,
        'level3_count': 0,
        'level4_count': 0
        }

coords = {}

listOfConnections = []
level1, level2, level3, level4 = ['lb'], ['dmz'], ['app'], ['db']
level1_count, level2_count, level3_count = 0, 0, 0

MAX_WIDTH = 1000
# x_pos1 = 0
# y_pos1 = 0
# x_pos2 = 0
# y_pos2 = 150
# x_pos3 = 0
# y_pos3 = 300
# x_pos4 = 0
# y_pos4 = 400

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
        data['data_centers'].append(g.add_group(str(dc)))


for index, node in df.iterrows():
    if node['zone'] in level1:
        data['level1_count'] += 1
    elif node['zone'] in level2:
        data['level2_count'] += 1
    elif node['zone'] in level3:
        data['level3_count'] += 1
    elif node['zone'] in level4:
        data['level4_count'] += 1

data_center_offset_x = 0
for dc in data['data_centers']:
    x1 = 'x_pos1' + str(dc)
    y1 = 'y_pos1' + str(dc)
    coords[x1] = data_center_offset_x
    coords[y1] = 0

    x2 = 'x_pos2' + str(dc)
    y2 = 'y_pos2' + str(dc)
    coords[x2] = data_center_offset_x
    coords[y2] = 150

    x3 = 'x_pos3' + str(dc)
    y3 = 'y_pos3' + str(dc)
    coords[x3] = data_center_offset_x
    coords[y3] = 300

    x4 = 'x_pos4' + str(dc)
    y4 = 'y_pos4' + str(dc)
    coords[x4] = data_center_offset_x
    coords[y4] = 450

    data_center_offset_x += 500

# Nodes
for index, node in df.iterrows():
    for dc in data['data_centers']:
        if node['zone'] in level1:
            if node['data_center'] == dc.label:
                x_key = 'x_pos1' + str(dc)
                y_key = 'y_pos1' + str(dc)
                coords[x_key] += (MAX_WIDTH / (data['level1_count'] + 1))
                dc.add_node(node['ip'], label=str(node['ip'] + "\n" + node['version']), height="50", width="100", x=str(coords[x_key]), y=str(coords[y_key]))
        if node['zone'] in level2:
            if node['data_center'] == dc.label:
                x_key = 'x_pos2' + str(dc)
                y_key = 'y_pos2' + str(dc)
                coords[x_key] += (MAX_WIDTH / (data['level2_count'] + 1))
                dc.add_node(node['ip'], label=str(node['ip'] + "\n" + node['version']), height="50", width="100", x=str(coords[x_key]), y=str(coords[y_key]))
        if node['zone'] in level3:
            if node['data_center'] == dc.label:
                x_key = 'x_pos3' + str(dc)
                y_key = 'y_pos3' + str(dc)
                coords[x_key] += (MAX_WIDTH / data['level3_count'])
                dc.add_node(node['ip'], label=str(node['ip'] + "\n" + node['version']), height="50", width="100", x=str(coords[x_key]), y=str(coords[y_key]))
        if node['zone'] in level4:
            if node['data_center'] == dc.label:
                x_key = 'x_pos4' + str(dc)
                y_key = 'y_pos4' + str(dc)
                coords[x_key] += (MAX_WIDTH / data['level3_count'])
                dc.add_node(node['ip'], label=str(node['ip'] + "\n" + node['version']), height="50", width="100", x=str(coords[x_key]), y=str(coords[y_key]))

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
