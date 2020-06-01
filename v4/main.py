import pyyed
import networkx as nx
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from data_center import DataCenter

df = pd.read_csv("net_data.csv")
df = df[df['cati'] == 'ICTO-0001']

G = nx.DiGraph()
DataCenterGraph = nx.Graph()


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

# for dc in data['data_centers']:
#     # subgraph_name = dc + "_subgraph"
#     subgraph = nx.Graph()
#     # subgraph.add_nodes_from(dc.get_network_objects())
#     dc.add_to_graph(subgraph)
#     G.add_node(subgraph)

#
# for dc in data['data_centers']:
#     graph['data_centers'].append(g.add_group(str(dc.get_name())))
#
# for dc_group in graph['data_centers']:
#     for dc in data['data_centers']:
#         if dc_group.label == dc.get_name():
#             dc.add_to_graph(dc_group)

for index, node in df.iterrows():
    if node['zone'] in level1:
        G.add_node(node['ip'], pos=(x_pos1, y_pos1))
        x_pos1 += 10
    if node['zone'] in level2:
        G.add_node(node['ip'], pos=(x_pos2, y_pos2))
        x_pos2 += 10
    if node['zone'] in level3:
        G.add_node(node['ip'], pos=(x_pos3, y_pos3))
        x_pos3 += 10

# Edges
for index, node in df.iterrows():
    if str(node['connections']) != 'nan':
        connections = node['connections'].split(',')
        for conn in connections:
            listOfConnections.append((node['ip'], str(conn)))

for conn in listOfConnections:
    G.add_edge(conn[0], conn[1], weight=0.5)


# pos=nx.get_node_attributes(G,'pos')
elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.5]
esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.5]

pos = nx.spring_layout(G)  # positions for all nodes


Xn=[pos[k][0] for k in pos]
Yn=[pos[k][1] for k in pos]
labels = [k for k in pos]

nodes=dict(type='scatter',
           x=Xn,
           y=Yn,
           mode='markers+text',
           marker=dict(size=28, color='rgb(31,120,180)'),
           textfont=dict(size=22, color='#DBD700'),
           text=labels,
           hoverinfo='text')

Xaxis=dict(showline=False, zeroline=False, showgrid=False, showticklabels=True,
          mirror='allticks', ticks='inside', ticklen=5, tickfont = dict(size=14),
          title='')

Yaxis=dict(showline=False, zeroline=False, showgrid=False, showticklabels=True,
          mirror='allticks', ticks='inside', ticklen=5, tickfont = dict(size=14),
          title='')

annotateELarge = [ dict(showarrow=True, arrowsize=0.9, arrowwidth=6, arrowhead=5, standoff=14, startstandoff=4,
                         ax=pos[arrow[0]][0], ay=pos[arrow[0]][1], axref='x', ayref='y',
                         x=pos[arrow[1]][0], y=pos[arrow[1]][1], xref='x', yref='y'
                        ) for arrow in elarge]
annotateESmall = [ dict(showarrow=True, arrowsize=1.5, arrowwidth=2, arrowhead=5, opacity=0.5, standoff=14, startstandoff=4,
                        ax=pos[arrow[0]][0], ay=pos[arrow[0]][1], axref='x', ayref='y',
                        x=pos[arrow[1]][0], y=pos[arrow[1]][1], xref='x', yref='y'
                        ) for arrow in esmall]

layout=dict(width=800, height=600,
            showlegend=False,
            xaxis=Xaxis,
            yaxis=Yaxis,
            hovermode='closest',
            plot_bgcolor='#E5ECF6',
            annotations= annotateELarge + annotateESmall, #arrows
            )

plotly_fig = dict(data=[nodes], layout=layout)


#Dash page stub
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    dcc.Graph(id='network-graph', figure=plotly_fig)
])


# nx.draw(G,pos)
# plt.show()


if __name__ == '__main__':
    app.run_server(debug=True)
