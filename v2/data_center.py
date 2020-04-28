import pyyed

class DataCenter:
    def __init__(self, name, global_x_axis):
        self.child_objects = {}
        self.global_x_axis = global_x_axis
        self.name = name
        self.dc_max_width = 250
        self.level1, self.level2, self.level3 = ['lb'], ['dmz'], ['app']

    def get_network_objects(self):
        return self.child_objects

    def get_name(self):
        return self.name

    def add_child_object(self, child_ip, child_data):
        self.child_objects[child_ip] = child_data

    def add_to_graph(self, graph, group):
        x_pos1, y_pos1 = 0, 0
        x_pos2, y_pos2 = 0, 100
        x_pos3, y_pos3 = 0, 200
        for child_ip, child_data in self.child_objects.items():
            if child_data['zone'] in self.level1:
                group.add_node(child_ip, label=str(child_ip + "\n" + child_data['version']), height="50", width="100",
                               x=str(x_pos1 + self.global_x_axis), y=str(y_pos1))
                x_pos1 += 150
            if child_data['zone'] in self.level2:
                group.add_node(child_ip, label=str(child_ip + "\n" + child_data['version']), height="50", width="100",
                               x=str(x_pos2 + self.global_x_axis), y=str(y_pos2))
                x_pos2 += 150
            if child_data['zone'] in self.level3:
                group.add_node(child_ip, label=str(child_ip + "\n" + child_data['version']), height="50", width="100",
                               x=str(x_pos3 + self.global_x_axis), y=str(y_pos3))
                x_pos3 += 150
