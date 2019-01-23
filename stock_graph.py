import dash_core_components as dcc


def generate_graph(x, y, height, title, id_name, graph_type):
    return dcc.Graph(
        id=id_name,
        figure={
            'data': [
                {'x': x, 'y': y, 'type': graph_type, 'name': title},
            ],
            'layout': {
                'title': title,
                'height': height,
                'font': dict(color='#CCCCCC'),
                'titlefont': dict(color='#CCCCCC', size='14'),
                'margin': dict(l=35, r=35, b=35, t=45),
                'hovermode': "closest",
                'plot_bgcolor': "#191A1A",
                'paper_bgcolor': "#777777",
                'legend': dict(font=dict(size=10), orientation='h'),
                'xaxis': dict(
                    showgrid=True,
                    gridcolor='#777777',
                ),
                'yaxis': dict(
                    showgrid=True,
                    gridcolor='#777777',
                )
            }
        }
    )
