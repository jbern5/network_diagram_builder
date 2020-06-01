import networkx as nx
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html

G=nx.Graph()

G.add_node(1, pos=(1, 1))

G.add_node(2, pos=(2, 2))

G.add_node(3, pos=(3, 3))

G.add_edge(1, 2, weight=0.6)
G.add_edge(2, 3, weight=0.6)








pos=nx.get_node_attributes(G,'pos')
elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.5]
esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.5]

# pos = nx.spring_layout(G)  # positions for all nodes


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