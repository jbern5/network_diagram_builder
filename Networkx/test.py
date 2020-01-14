import pyyed

g = pyyed.Graph()
# g.add_node('foo', font_family="Zapfino")
#
# gg = g.add_group("MY_Group", shape="diamond")
# gg.add_node('foo2', shape="roundrectangle", font_style="bolditalic",
#             underlined_text="true")
# gg.add_node('abc', font_size="72", height="100")
#
# g.add_edge('foo2', 'abc')
# g.add_edge('foo', 'MY_Group')

group_list = []
data_centers = ['pri', 'cdc']
for dc in data_centers:
    group_list.append(g.add_group(str(dc)))
print(group_list)

print(g.get_graph())
z = g.get_graph()
new_config_file = open("test2" +'.graphml','w')
new_config_file.write(z)
new_config_file.close()