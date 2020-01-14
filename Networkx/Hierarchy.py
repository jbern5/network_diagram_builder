class Hierarchy:
    def __init__(self):
        self.level1 = ['lb']
        self.level2 = ['dmz']
        self.level3 = ['app']
        self.level1_count = 0
        self.level2_count = 0
        self.level3_count = 0

    def find_hierarchy(self, df):
        for index, node in df.iterrows():
            if node['zone'] in self.level1:
                self.level1_count += 1
            elif node['zone'] in self.level2:
                self.level2_count += 1
            elif node['zone'] in self.level3:
                self.level3_count += 1
            return self.level1_count, self.level2_count, self.level3_count
