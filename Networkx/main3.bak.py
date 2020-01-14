import pyyed
import pandas as pd

df = pd.read_csv("net_data.csv")
df = df[df['cati'] == 'ICTO-0001']

g = pyyed.Graph()

data = {'data_centers': [],
        'level1_count': 0,
        'level2_count': 0,
        'level3_count': 0,
        }
listOfConnections = []
level1, level2, level3 = ['lb'], ['dmz'], ['app']
MAX_WIDTH = 1000
x_pos1 = 0
y_pos1 = 0
x_pos2 = 0
y_pos2 = 150
x_pos3 = 0
y_pos3 = 300

for dc in df['data_center'].unique():
    if str(dc) == 'nan':
        data['data_centers'].append({'lb': []})
    else:
        data['data_centers'].append({dc: []})
for index, node in df.iterrows():
    for dc in data['data_centers']:
        for k, v in dc.items():
            if k == 'lb' and str(node['data_center']) == 'nan':
                v.append(pyyed.Node(node['ip'], label=str(node['ip'] + "\n" + node['version']), height="50", width="100", x=str(x_pos1), y=str(y_pos1)))
            if node['data_center'] == k:
                v.append(node['ip'])
    if node['zone'] in level1:
        data['level1_count'] += 1
    elif node['zone'] in level2:
        data['level2_count'] += 1
    elif node['zone'] in level3:
        data['level3_count'] += 1

print(data)

# Nodes
for dc in data['data_centers']:
    for index, node in df.iterrows():
        if node['zone'] in level1:
            x_pos1 += (MAX_WIDTH / (data['level1_count'] + 1))
            #g.add_node(node['ip'], label=str(node['ip'] + "\n" + node['version']), height="50", width="100", x=str(x_pos1), y=str(y_pos1))
            # if str(node['data_center']) != 'nan' and node['data_center'] == dc:
            #     dc.add_node(node['ip'])
        if node['zone'] in level2:
            x_pos2 += (MAX_WIDTH / (data['level2_count'] + 1))
            #g.add_node(node['ip'], label=str(node['ip'] + "\n" + node['version']), height="50", width="100", x=str(x_pos2), y=str(y_pos2))
            # if str(node['data_center']) != 'nan' and node['data_center'] == dc:
            #     dc.add_node(node['ip'])
        if node['zone'] in level3:
            x_pos3 += (MAX_WIDTH / data['level3_count'])
            #g.add_node(node['ip'], label=str(node['ip'] + "\n" + node['version']), height="50", width="100", x=str(x_pos3), y=str(y_pos3))
            # if str(node['data_center']) != 'nan' and node['data_center'] == dc:
            #     dc.add_node(node['ip'])


# Edges
for index, node in df.iterrows():
    if str(node['connections']) != 'nan':
        connections = node['connections'].split(',')
        for conn in connections:
            listOfConnections.append((node['ip'], str(conn)))

for conn in listOfConnections:
    g.add_edge(conn[0], conn[1])



z = g.get_graph()

# print(z)


new_config_file = open("test1" +'.graphml','w')
new_config_file.write(z)
new_config_file.close()