import dash_html_components as html
import dash_core_components as dcc


def generate_top_bar_logo():
    html_script = html.Div(
        [
            html.Img(
                src='/assets/sendash_logo_v2.png', style={'max-height': '54px'}, className="responsive-img"
            )
        ], className="col s1 top-bar-col borders", style={'padding': '0px'}
    )
    return html_script


def generate_pick_stock():
    html_script = html.Div(
        [
            html.Div([
                dcc.Dropdown(
                    id='input-stock-label',
                    options=[
                        {'label': 'GOOGL | Alphabet Inc.', 'value': 'GOOGL'},
                        {'label': 'FB | Facebook, Inc.', 'value': 'FB'},
                        {'label': 'AMZN Amazon.com, Inc.', 'value': 'AMZN'},
                        {'label': 'NFLX | Netflix, Inc.', 'value': 'NFLX'},
                    ],
                    value='GOOGL'
                )
            ], style={'margin-top': '10px', 'margin-bottom': '10px'})
        ], className="col s2 top-bar-col borders"
    )
    return html_script

# TO-DO
# generate get quote, get close function

    # # 3rd Div
    # html.Div(
    #     [
    #         html.P('1'),
    #     ], className="col s2 top-bar-col bg-color borders"
    # ),
    # # 4th Div
    # html.Div(
    #     [
    #         html.P('1'),
    #     ], className="col s2 top-bar-col bg-color borders"
    # ),
    # # 5th Div
    # html.Div(
    #     [
    #         html.P('1'),
    #     ], className="col s1 top-bar-col bg-color borders"
    # ),
    # # 6th Div
    # html.Div(
    #     [
    #         html.P('1'),
    #     ], className="col s5 top-bar-col bg-color borders"
    # ),
