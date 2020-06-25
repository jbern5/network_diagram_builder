import pyyed
from data_center import DataCenter


def make_graph(df, cati):
    df = df.sort_values(by='data_center')

    # Create the yed graph
    g = pyyed.Graph(graph_id=cati)

    # Local storage
    data = {'data_centers': []}
    graph = {'data_centers': []}

    instruction_types = df['version'].unique()
    list_of_connections = []

    MAX_WIDTH = 1500
    global_x_start = 0

    # Gets each data center and creates a group for each unique data center
    for dc in df['data_center'].unique():
        if str(dc) != 'nan':
            # data stores the DataCenter version and graph stores the graph object of the DataCenter
            data['data_centers'].append(DataCenter(str(dc), global_x_start))
            graph['data_centers'].append(g.add_group(str(DataCenter(str(dc), global_x_start).get_name()), fill='#2153c4', font_style='bold'))
            global_x_start += 500  # MAX_WIDTH / len(df['data_center'].unique())

    # grabs relevant info for graph generation
    for index, node in df.iterrows():
        # assigns nodes to their corresponding data center
        for dc in data['data_centers']:
            if node['data_center'] == dc.get_name():
                dc.add_child_object(node['ip'], node)
        # checks if there are connections to be made and if so adds the connection pair to a list
        if str(node['connections']) != 'nan':
            connections = node['connections'].split(',')
            for conn in connections:
                list_of_connections.append((node['ip'], str(conn)))

    for dc_group in graph['data_centers']:
        for dc in data['data_centers']:
            if dc_group.label == dc.get_name():
                dc.add_to_graph(g, dc_group)

    draw_connections(g, list_of_connections)

    # General Info needed on graph
    add_title(g, cati, global_x_start)
    add_instructions(g, instruction_types, global_x_start)

    z = g.get_graph()

    # if running directly with python, use 'graphs/' | if running with docker, use '/graphs/'
    with open("graphs/" + cati + '.graphml', 'w') as graph_file:
        graph_file.write(z)
        graph_file.close()


def draw_connections(g, list_of_connections):
    for conn in list_of_connections:
        g.add_edge(conn[0], conn[1])


def add_title(g, cati, global_x_start):
    g.add_node('title', label=str(cati), height="50", width="200", x=str(global_x_start / 3), y=str(0),
               shape_fill='#dadee6', font_size='20')


def add_instructions(g, instruction_types, global_x_start):
    for index, instruction in enumerate(instruction_types):
        with open('../instructions/' + instruction, 'r') as file:
            file_text = file.read()
            g.add_node(instruction, label=str(file_text), height="100", width="150", x=str((global_x_start/2) + (150 * index)), y=str(0),
                       shape_fill='#dadee6', font_size='12')
            file.close()
