import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas_datareader.data as web
import datetime
import plotly.graph_objs as go

from headlines import generate_headline_bar, generate_link_table
from quotes import generate_top_bar_logo, generate_pick_stock
from stock_graph import generate_graph
from iexfinance.stocks import Stock
from IPython.display import Image

app = dash.Dash('SENDASH')

# a config setting for run css and js in locally
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True


# Container Div
app.layout = html.Div([

    # import local stylesheet
    html.Link(
        rel='stylesheet',
        href='/assets/materialize.min.css'
    ),

    html.Link(
        rel='stylesheet',
        href='/assets/sendash.css'
    ),

    # import local javascript
    html.Link(
        rel='javascript',
        href='/assets/materialize.min.js'
    ),


    # Top Bar Div
    html.Div([
        generate_top_bar_logo(),
        generate_pick_stock(),

        # 3rd Div
        html.Div(
            [
                # html.P('1'),
                html.Div([

                    html.Strong("QQQ", style={'color': 'white', 'padding-left': '10px'}),

                ], className="row borders row-margin-reduce"),

                html.Div([

                    html.Strong("5.41", style={'color': 'white', 'padding-left': '10px', 'padding-right': '5px'}),

                    html.Img(
                        src='/assets/arrow-up.png', style={'max-height': '18px', 'padding-left': '5px', 'padding-right': '5px'}
                    ),

                    html.Strong("0.09%", style={'color': '#45df7e', 'font-size': '18px', 'letter-spacing': '0px'}),
                ], className="row borders row-margin-reduce"),

            ], className="col s2 top-bar-col borders"
        ),

        html.Div(
            [
                # html.P('1'),
                html.Div([

                    html.Strong("SPY", style={'color': 'white', 'padding-left': '10px'}),

                ], className="row borders row-margin-reduce"),

                html.Div([

                    html.Strong("5.41", style={'color': 'white', 'padding-left': '10px', 'padding-right': '5px'}),

                    html.Img(
                        src='/assets/arrow-down.png', style={'max-height': '18px', 'padding-left': '5px', 'padding-right': '5px'}
                    ),

                    html.Strong("0.09%", style={'color': '#da5657', 'font-size': '18px', 'letter-spacing': '0px'}),
                ], className="row borders row-margin-reduce"),

            ], className="col s2 top-bar-col borders"
        ),

        # 4th Div
        html.Div(
            [
                html.P('1'),
            ], className="col s5 top-bar-col borders"
        ),
    ], className="row row-margin-reduce"),


    # 2nd Row Div
    html.Div([
        # Left Panel
        html.Div(
            [
                generate_headline_bar("Headlines"),
                generate_link_table(),
                generate_headline_bar("Tweets"),
                generate_link_table(),
                #], className="col s3 row-margin-reduce borders", style={'height': '406px'}
            ], className="col s3 row-margin-reduce borders"
        ),

        # Right Panel
        html.Div(
            [
                html.Div(children=[
                    html.Div(id='output-stock-price-graph')
                ]),

                # html.Div(children=[
                #     html.Div(id='output-graph2')
                # ])
                #], className="col s9 row-margin-reduce borders", style={'height': '406px'}
            ], className="col s9 row-margin-reduce borders"

        )
        #], className="row row-margin-reduce", style={'height': '406px'}),
    ], className="row row-margin-reduce"),


    # 3rd Row Div
    html.Div([
        html.Div(
            [
                # html.P('4'), html.P('4'), html.P('4'), html.P('4'), html.P('4'),
                html.Div([
                    html.Div(children=[
                        html.Div(id="output-stock-logo"),
                    ]),
                ], className="col s2 borders"),
                html.Div([
                    html.Strong("--- Company Description ---", style={'color': 'white'}),
                    html.Div(children=[
                        html.Div(id='output-companyName', style={'color': 'white'})
                    ]),
                    html.Div(children=[
                        html.Div(id='output-description', style={'color': 'white'})
                    ]),
                    html.Div(children=[
                        html.Div(id='output-exchange', style={'color': 'white'})
                    ]),
                ], className="col s10 borders")

            ], className="col s8 borders"  # 230px
        ),

        html.Div(
            [
                html.P('5'), html.P('5'), html.P('5'), html.P('5'), html.P('5'),
            ], className="col s4 borders"  # 230px
        ),
    ], className="row row-margin-reduce"),

], className="container bg-color", style={'width': '100%', 'max-width': 50000})


# Generate stock price closing graph
@app.callback(
    Output(component_id='output-stock-price-graph', component_property='children'),
    [Input(component_id='input-stock-label', component_property='value')]
)
def update_graph(input_data):
    start = datetime.datetime(2019, 1, 31)
    end = datetime.datetime.now()
    df = web.DataReader(input_data, 'yahoo', start, end)

    return generate_graph(df.index, df.Close, 380, input_data, 'stock-price-graph', 'line')


@app.callback(
    Output(component_id='output-companyName', component_property='children'),
    [Input(component_id='input-stock-label', component_property='value')]
)
def update_companyName(input_data):
    myStock = Stock(input_data)
    info = myStock.get_company()
    lKeyInfo = 'companyName'
    text = f'{lKeyInfo}: {info[lKeyInfo]}'

    return text


@app.callback(
    Output(component_id='output-description', component_property='children'),
    [Input(component_id='input-stock-label', component_property='value')]
)
def update_description(input_data):
    myStock = Stock(input_data)
    info = myStock.get_company()
    lKeyInfo = 'description'
    text = f'{lKeyInfo}: {info[lKeyInfo]}'

    return text


@app.callback(
    Output(component_id='output-exchange', component_property='children'),
    [Input(component_id='input-stock-label', component_property='value')]
)
def update_description(input_data):
    myStock = Stock(input_data)
    info = myStock.get_company()
    lKeyInfo = 'exchange'
    text = f'{lKeyInfo}: {info[lKeyInfo]}'

    return text


@app.callback(
    Output(component_id='output-stock-logo', component_property='children'),
    [Input(component_id='input-stock-label', component_property='value')]
)
def update_stock_logo(input_data):
    myStock = Stock(input_data)
    logo = myStock.get_logo()
    return html.Img(src=logo['url'], style={'min-width': '100%', 'min-height': '100%', 'height': 'auto', 'width': 'auto'})


# Generate stock volume graph
# @app.callback(
#     Output(component_id='output-graph2', component_property='children'),
#     [Input(component_id='input-stock-label', component_property='value')]
# )
# def update_graph(input_data):
#     start = datetime.datetime(2015, 1, 1)
#     end = datetime.datetime.now()
#     df = web.DataReader(input_data, 'yahoo', start, end)

#     return generate_graph(df.index, df.Volume, 136, 'Volume', 'volume-graph', 'bar')


@app.server.route('/assets/<path:path>')
def assets_file(path):
    assets_folder = os.path.join(os.getcwd(), 'assets')
    return send_from_directory(assets_folder, path)


if __name__ == '__main__':
    app.run_server(debug=True)
