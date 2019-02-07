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
from krakenio import Client

from PIL import Image
import urllib.request


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

        # QQQ indicator
        html.Div(
            [
                html.Div([
                    html.Strong("QQQ", className="market-indicator-title"),
                ], className="row borders row-margin-reduce"),

                html.Div([
                    html.Div(id="output-QQQ"),
                    dcc.Interval(id='input-QQQ', interval=6 * 10000, n_intervals=0),
                ], className="row borders row-margin-reduce"),

            ], className="col s2 top-bar-col borders"
        ),

        # SPY indicator
        html.Div(
            [
                html.Div([
                    html.Strong("SPY", className="market-indicator-title"),
                ], className="row borders row-margin-reduce"),

                html.Div([
                    html.Div(id="output-SPY"),
                    dcc.Interval(id='input-SPY', interval=6 * 10000, n_intervals=0),
                ], className="row borders row-margin-reduce"),

            ], className="col s2 top-bar-col borders"
        ),

        # Market Clock
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
            ], className="col s9 row-margin-reduce borders"

        )
        #], className="row row-margin-reduce", style={'height': '406px'}),
    ], className="row row-margin-reduce"),


    # 3rd Row Div
    html.Div([
        html.Div(
            [
                html.Div([
                    html.Div([
                        html.Div(id="output-stock-logo"),
                    ], className="col s2 borders", style={'max-height': '120px'}),

                    html.Div([
                        html.Div(id="output-key-stats"),
                    ], className="col s10 borders", style={'min-height': '120px'})
                ], className="row borders row-margin-reduce"),

                html.Div([
                    html.Div(id='output-get-company')
                ], className="row borders row-margin-reduce"),

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
    return generate_graph(2019, 2, 6, input_data, 380)


@app.callback(
    Output(component_id='output-get-company', component_property='children'),
    [Input(component_id='input-stock-label', component_property='value')]
)
def update_companyName(input_data):
    myStock = Stock(input_data)
    info = myStock.get_company()
    DisplayDict = {
        'Company Name': 'companyName',
        'Description': 'description',
        'Exchange': 'exchange'
    }

    key_list = []
    value_list = []

    for key in DisplayDict:
        key_list.append(f'{key}:')
        value_list.append(info[DisplayDict[key]])

    return [
        html.Strong("--- Company Description ---", className="section-title"),
        html.Table([
            html.Tr([
                html.Td([
                    key_list[0]
                ], className="table-title"),
                html.Td([
                    value_list[0]
                ], className="table-text"),
            ]),
            html.Tr([
                html.Td([
                    key_list[1]
                ], className="table-title"),
                html.Td([
                    value_list[1]
                ], className="table-text"),
            ]),
            html.Tr([
                html.Td([
                    key_list[2]
                ], className="table-title"),
                html.Td([
                    value_list[2]
                ], className="table-text"),
            ]),
        ])
    ]


@app.callback(
    Output(component_id='output-key-stats', component_property='children'),
    [Input(component_id='input-stock-label', component_property='value')]
)
def update_key_stats(input_data):
    myStock = Stock(input_data)
    stats = myStock.get_key_stats()
    DisplayDict = {
        'Beta': 'beta',
        'Dividend Rate': 'dividendRate',
        'Shares Outstanding': 'sharesOutstanding',
        'Ex-Dividend Date': 'exDividendDate',
        'Price to Book': 'priceToBook',
        'Week 52 High': 'week52high',
        'Price to Sales': 'priceToSales',
        'Week 52 Low': 'week52low'
    }

    key_list = []
    value_list = []

    for key in DisplayDict:
        key_list.append(f'{key}:')
        value_list.append(stats[DisplayDict[key]])

    return [
        html.Strong("--- Key Stats ---", className="section-title"),
        html.Table([
            html.Tr([
                html.Td([
                    key_list[0]
                ], className="table-title"),
                html.Td([
                    value_list[0]
                ], className="table-text"),
                html.Td([
                    key_list[1]
                ], className="table-title"),
                html.Td([
                    value_list[1]
                ], className="table-text"),
            ]),
            html.Tr([
                html.Td([
                    key_list[2]
                ], className="table-title"),
                html.Td([
                    value_list[2]
                ], className="table-text"),
                html.Td([
                    key_list[3]
                ], className="table-title"),
                html.Td([
                    value_list[3]
                ], className="table-text"),
            ]),
            html.Tr([
                html.Td([
                    key_list[4]
                ], className="table-title"),
                html.Td([
                    value_list[4]
                ], className="table-text"),
                html.Td([
                    key_list[5]
                ], className="table-title"),
                html.Td([
                    value_list[5]
                ], className="table-text"),
            ]),
            html.Tr([
                html.Td([
                    key_list[6]
                ], className="table-title"),
                html.Td([
                    value_list[6]
                ], className="table-text"),
                html.Td([
                    key_list[7]
                ], className="table-title"),
                html.Td([
                    value_list[7]
                ], className="table-text"),
            ]),
        ])
    ]


@app.callback(
    Output(component_id='output-QQQ', component_property='children'),
    [Input(component_id='input-QQQ', component_property='n_intervals')]
)
def update_QQQ(input_data):

    batch = Stock('QQQ')
    quotes = batch.get_quote()

    if(quotes['changePercent'] > 0):
        source = '/assets/arrow-up.png'
        cols = '#45df7e'
    elif(quotes['changePercent'] == 0):
        source = '/assets/substract.png'
        cols = 'white'
    else:
        source = '/assets/arrow-down.png'
        cols = '#da5657'

    return [
        html.Strong(quotes['latestPrice'], style={'color': 'white', 'padding-left': '10px', 'padding-right': '5px', 'font-size': '18px'}),
        html.Img(
            src=source, style={'max-height': '18px', 'padding-left': '15px', 'padding-right': '5px'}
        ),
        html.Strong('{0:.2f}%'.format(quotes['changePercent'] * 100), style={'color': cols, 'font-size': '18px', 'letter-spacing': '0px'}),
    ]


@app.callback(
    Output(component_id='output-SPY', component_property='children'),
    [Input(component_id='input-SPY', component_property='n_intervals')]
)
def update_SPY(input_data):

    batch = Stock('SPY')
    quotes = batch.get_quote()

    if(quotes['changePercent'] > 0):
        source = '/assets/arrow-up.png'
        cols = '#45df7e'
    elif(quotes['changePercent'] == 0):
        source = '/assets/substract.png'
        cols = 'white'
    else:
        source = '/assets/arrow-down.png'
        cols = '#da5657'

    return [
        html.Strong(quotes['latestPrice'], style={'color': 'white', 'padding-left': '10px', 'padding-right': '5px', 'font-size': '18px'}),
        html.Img(
            src=source, style={'max-height': '18px', 'padding-left': '15px', 'padding-right': '5px'}
        ),
        html.Strong('{0:.2f}%'.format(quotes['changePercent'] * 100), style={'color': cols, 'font-size': '18px', 'letter-spacing': '0px'}),
    ]


@app.callback(
    Output(component_id='output-stock-logo', component_property='children'),
    [Input(component_id='input-stock-label', component_property='value')]
)
def update_stock_logo(input_data):
    myStock = Stock(input_data)
    logo = myStock.get_logo()

    image = Image.open(urllib.request.urlopen(logo['url']))
    new_image = make_square(image)
    print(new_image)
    path = f'./assets/{input_data}.png'
    new_image.save(path, format="PNG")
    #api = Client('2f8f8da3544e9d704d0081a6ea2aa5fb', '55c4f243a2d9925204714ff7202c404c2653d779')

    # data = {
    #     'wait': True,
    #     "resize": {
    #         "width": 115,
    #         "height": 115,
    #         "strategy": "fill",
    #         "background": "rgba(35, 43, 43, 1)"
    #     }
    # }

    # result = api.url(logo['url'], data)

    # if result.get('success'):
    #     print(result.get('kraked_url'))
    # else:
    #     print(result.get('message'))

    # return html.Img(src=result.get('kraked_url'), style={'height': 'auto', 'width': 'auto', 'max-height': '115px', 'max-width': '115px'}, className="responsive-img")
    return html.Img(src=path, style={'height': 'auto', 'width': 'auto', 'max-height': '115px', 'max-width': '115px'}, className="responsive-img")


def make_square(im, min_size=115, fill_color=(35, 43, 43, 1)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, ((size - x) // 2, (size - y) // 2))
    return new_im


@app.server.route('/assets/<path:path>')
def assets_file(path):
    assets_folder = os.path.join(os.getcwd(), 'assets')
    return send_from_directory(assets_folder, path)


if __name__ == '__main__':
    app.run_server(debug=True)
