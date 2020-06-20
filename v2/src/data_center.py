class DataCenter:
    def __init__(self, name, global_x_axis):
        self.child_objects = {}
        self.global_x_axis = global_x_axis
        self.name = name
        self.dc_max_width = 500
        self.level1, self.level2, self.level3 = ['lb'], ['dmz'], ['app']
        self.level1_count, self.level2_count, self.level3_count = 0, 0, 0 

    def get_network_objects(self):
        return self.child_objects

    def add_child_object(self, child_ip, child_data):
            self.child_objects[child_ip] = child_data

    def get_name(self):
        return self.name

    def get_type_counts(self):
        for value in self.get_network_objects().values():
            if value['zone'] in self.level1:
                self.level1_count += 1
            elif value['zone'] in self.level2:
                self.level2_count += 1
            elif value['zone'] in self.level3:
                self.level3_count += 1

    def add_node(self, group, x_pos, y_pos, child_data):
        group.add_node(child_data['ip'], label=str(child_data['ip'] + "\n" + child_data['version']), height="50", width="100",
                               x=str(x_pos + self.global_x_axis), y=str(y_pos), shape_fill='#dadee6')

    def add_to_graph(self, graph, group):
        x_pos1, y_pos1 = 0, 100
        x_pos2, y_pos2 = 0, 200
        x_pos3, y_pos3 = 0, 300
        
        self.get_type_counts()
        # x1_incrementor = self.dc_max_width / ( self.level1_count + 1 )
        # x2_incrementor = self.dc_max_width / ( self.level2_count + 1 )
        # x3_incrementor = self.dc_max_width / ( self.level3_count + 1 )

        # print("{} {} {}".format(x1_incrementor, x2_incrementor, x3_incrementor))

        for child_data in self.child_objects.values():
            if child_data['zone'] in self.level1:
                if self.level1_count == 1:
                        max_nodes = max(self.level2_count, self.level3_count)
                        x_pos1 = ((max_nodes - 1) / 2) * 150
                self.add_node(group, x_pos1, y_pos1, child_data)
                x_pos1 += 150
            if child_data['zone'] in self.level2:
                self.add_node(group, x_pos2, y_pos2, child_data)
                x_pos2 += 150
            if child_data['zone'] in self.level3:
                self.add_node(group, x_pos3, y_pos3, child_data)
                x_pos3 += 150

'''
    color options: 
        #dadee6
        #858fa6
'''