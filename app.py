import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas_datareader.data as web
import datetime
import plotly.graph_objs as go
from headlines import generate_headline_bar, generate_link_table
from quotes import generate_top_bar_logo, generate_pick_stock
from stock_graph import generate_graph, MarketDateAdj, generate_sentiment_analysis_piechart
from iexfinance.stocks import Stock
from IPython.display import Image

from PIL import Image
import urllib.request

from datetime import datetime, time
import pandas_market_calendars as mcal
import pytz
import pandas as pd

import plotly.plotly as py

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

        # stock indicator
        html.Div(
            [
                html.Div(id='output-symbol'),
                #dcc.Input(id='output-ticker', type='hidden'),
                dcc.Interval(id='input-symbol', interval=6 * 10000, n_intervals=0),

            ], className="col s2 top-bar-col borders"
        ),

        # QQQ indicator
        html.Div(
            [
                html.Div(id="output-QQQ"),
                dcc.Interval(id='input-QQQ', interval=6 * 10000, n_intervals=0),
            ], className="col s2 top-bar-col borders"
        ),

        # SPY indicator
        html.Div(
            [
                html.Div(id="output-SPY"),
                dcc.Interval(id='input-SPY', interval=6 * 10000, n_intervals=0),

            ], className="col s2 top-bar-col borders"
        ),

        # Market Clock
        html.Div(
            [
                html.Div(id='output-time-clock'),
                dcc.Interval(id='input-time-clock', interval=2 * 1000, n_intervals=0),
            ], className="col s3 top-bar-col borders"
        ),
    ], className="row row-margin-reduce"),


    # 2nd Row Div
    html.Div([
        # Left Panel
        html.Div(
            [
                generate_headline_bar("Headlines"),
                generate_link_table(),
                # generate_headline_bar("Tweets"),
                # generate_link_table(),
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
                    ], className="col s2 borders", style={'max-height': '120px', 'padding-top':'5px'}),

                    html.Div([
                        html.Div(id="output-key-stats"),
                    ], className="col s10 borders", style={'min-height': '120px', 'padding':'0px'})
                ], className="row borders row-margin-reduce"),

                html.Div([
                    html.Div(id='output-get-company')
                ], className="row borders row-margin-reduce"),

            ], className="col s6 borders"  # 230px
        ),


        html.Div(
            [
                #html.P('5'), html.P('5'), html.P('5'), html.P('5'), html.P('5'),
                html.Div([
                    html.Strong("Sentiment Analysis Score", className="section-title"),
                ], className="row row-margin-reduce left-div-header-div borders"),
                html.Div([
                    #html.P('5'), html.P('5'), html.P('5'), html.P('5'), html.P('5'),html.P('5'), html.P('5'), html.P('5'), html.P('5'),
                    generate_sentiment_analysis_piechart()

                ], className="row row-margin-reduce")
            ], className="col s2 borders"  # 230px
        ),
        html.Div(
            [
                #html.P('5'), html.P('5'), html.P('5'), html.P('5'), html.P('5'),
                html.Div([
                    html.Strong("Probability Score", className="section-title"),
                ], className="row row-margin-reduce left-div-header-div borders"),
                html.Div([
                    generate_sentiment_analysis_piechart()
                    #html.P('5'), html.P('5'), html.P('5'), html.P('5'), html.P('5'),html.P('5'), html.P('5'), html.P('5'), html.P('5'),
                ], className="row row-margin-reduce")
            ], className="col s2 borders"  # 230px
        ),
        html.Div(
            [
                #html.P('5'), html.P('5'), html.P('5'), html.P('5'), html.P('5'),
                html.Div([
                    html.Div([
                        html.Strong("Bid", className="section-title"),
                    ], className="col s6"),
                    html.Div([
                        html.Strong("Ask", className="section-title"),
                    ], className="col s6")
                ], className="row row-margin-reduce left-div-header-div borders"),
                html.Div([
                    html.Div([
                        html.P('5'), html.P('5'), html.P('5'), html.P('5'), html.P('5'),html.P('5'), html.P('5'), html.P('5'), html.P('5'),
                    ], className="col s6 borders"),
                    html.Div([
                        html.P('5'), html.P('5'), html.P('5'), html.P('5'), html.P('5'),html.P('5'), html.P('5'), html.P('5'), html.P('5'),
                    ], className="col s6 borders")
                ], className="row row-margin-reduce")
            ], className="col s2 borders"  # 230px
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
        html.Div([
            html.Strong("--- Company Description ---", className="section-title"),
        ], className="left-div-header-div"),
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
        'Beta': ('beta', '{:.2f}'),
        'Dividend Rate': ('dividendRate', '{:.2f}'),
        'Shares Outstanding': ('sharesOutstanding', '{:,.0f}'),
        'Ex-Dividend Date': ('exDividendDate', '{}'),
        'Price to Book': ('priceToBook', '{:.2f}'),
        'Week 52 High': ('week52high', '{:.2f}'),
        'Price to Sales': ('priceToSales', '{:.2f}'),
        'Week 52 Low': ('week52low', '{:.2f}')
    }

    key_list = []
    value_list = []

    for key in DisplayDict:
        key_list.append(f'{DisplayDict[key][0]}:')
        value_list.append(DisplayDict[key][1].format(stats[DisplayDict[key][0]]))

    return [
        html.Div([
            html.Strong("--- Key Stats ---", className="section-title"),
        ], className="left-div-header-div"),
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
    Output(component_id='output-symbol', component_property='children'),
    [Input('input-symbol', 'n_intervals'),
        Input('input-stock-label', 'value')]
)
def update_symbol(intervals, input_data):

    batch = Stock(input_data)
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

    tstamp = quotes['latestUpdate']
    dt = TimeConvert(datetime.fromtimestamp(tstamp/1e3),'EST')
    text = f'Updated at: {dt.strftime("%d %b %y %H:%M %Z")}'

    return [
        html.Div([
            html.Div([
                html.Strong(input_data, className="market-indicator-title"),
            ], className="col s3"),
            html.Div([
                html.Strong(text, style={'font-size':'9px', 'color':'white', 'float':'right', 'padding-top':'5px'})
            ], className="col s9")
        ], className="row borders row-margin-reduce"),

        html.Div([
            # html.Div(id="output-QQQ"),
            html.Strong(quotes['latestPrice'], style={'color': 'white', 'padding-left': '10px', 'padding-right': '5px', 'font-size': '18px'}),
            html.Img(
                src=source, style={'max-height': '18px', 'padding-left': '15px', 'padding-right': '5px'}
            ),
            html.Strong('{0:.2f}%'.format(quotes['changePercent'] * 100), style={'color': cols, 'font-size': '18px', 'letter-spacing': '0px'}),
            #dcc.Interval(id='input-QQQ', interval=6 * 10000, n_intervals=0),
        ], className="row borders row-margin-reduce"),

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

    tstamp = quotes['latestUpdate']
    dt = TimeConvert(datetime.fromtimestamp(tstamp/1e3),'EST')
    text = f'Updated at: {dt.strftime("%d %b %y %H:%M %Z")}'

    return [
        html.Div([
            html.Div([
                html.Strong("QQQ", className="market-indicator-title"),
            ], className="col s3"),
            html.Div([
                html.Strong(text, style={'font-size':'9px', 'color':'white', 'float':'right', 'padding-top':'5px'})
            ], className="col s9")
        ], className="row borders row-margin-reduce"),

        html.Div([
            # html.Div(id="output-QQQ"),
            html.Strong(quotes['latestPrice'], style={'color': 'white', 'padding-left': '10px', 'padding-right': '5px', 'font-size': '18px'}),
            html.Img(
                src=source, style={'max-height': '18px', 'padding-left': '15px', 'padding-right': '5px'}
            ),
            html.Strong('{0:.2f}%'.format(quotes['changePercent'] * 100), style={'color': cols, 'font-size': '18px', 'letter-spacing': '0px'}),
            #dcc.Interval(id='input-QQQ', interval=6 * 10000, n_intervals=0),
        ], className="row borders row-margin-reduce"),
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

    tstamp = quotes['latestUpdate']
    dt = TimeConvert(datetime.fromtimestamp(tstamp/1e3),'EST')
    text = f'Updated at: {dt.strftime("%d %b %y %H:%M %Z")}'

    return [
        html.Div([
            html.Div([
                html.Strong("SPY", className="market-indicator-title"),
            ], className="col s3"),
            html.Div([
                html.Strong(text, style={'font-size':'9px', 'color':'white', 'float':'right', 'padding-top':'5px'})
            ], className="col s9")
        ], className="row borders row-margin-reduce"),

        html.Div([
            # html.Div(id="output-QQQ"),
            html.Strong(quotes['latestPrice'], style={'color': 'white', 'padding-left': '10px', 'padding-right': '5px', 'font-size': '18px'}),
            html.Img(
                src=source, style={'max-height': '18px', 'padding-left': '15px', 'padding-right': '5px'}
            ),
            html.Strong('{0:.2f}%'.format(quotes['changePercent'] * 100), style={'color': cols, 'font-size': '18px', 'letter-spacing': '0px'}),
            #dcc.Interval(id='input-QQQ', interval=6 * 10000, n_intervals=0),
        ], className="row borders row-margin-reduce"),
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
    #new_image.save(path, format="PNG")
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
    return html.Img(src=path, style={'height': 'auto', 'width': 'auto', 'max-height': '100px', 'max-width': '100px'}, className="responsive-img")

@app.callback(
    Output(component_id='output-time-clock', component_property='children'),
    [Input(component_id='input-time-clock', component_property='n_intervals')]
)
def update_time_clock(input_data):
    exchange = 'NYSE'
    MktTimeDict = GetTimeToMktOpen( datetime.now(pytz.utc), exchange)
    d,h,m,s = MktTimeDict['d-h-m-s']

    if MktTimeDict['status'] == 'open':
        nextAction = f'until {exchange} close'
        cols = '#45df7e'
    else:
        nextAction = f'until {exchange} open'
        cols = '#da5657'

    msg = f'{h}:{"{:02d}".format(m)}:{"{:02d}".format(s)}'
    if d > 0:
        msg = f'{d} days {msg}'

    #print(f'{msg} {nextAction}')
    return [
        html.Div([
            html.Div([
                html.Strong('Status: ', style={'color':'white', 'font-size':'18px'})
            ], className="col s3"),
            html.Div([
                html.Strong(MktTimeDict["status"], style={'color':cols, 'font-size':'18px'})
            ], className="col s9"),
        ], className="row borders row-margin-reduce"),
        html.Div([
            html.Strong(f'{msg} {nextAction}', style={'color':'white', 'font-size':'18px', 'padding-left':'10px'})
        ], className="row borders row-margin-reduce")
    ]


def make_square(im, min_size=115, fill_color=(35, 43, 43, 1)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, ((size - x) // 2, (size - y) // 2))
    return new_im


def TimeConvert( inDateTime, OutZone):
    from datetime import datetime
    import pytz

    #from_zone = pytz.utc
    to_zone = pytz.timezone(OutZone)

    return inDateTime.astimezone(to_zone)


def IsMarketOpen(DateTimeObj, ExchangeName):
    import pandas_market_calendars as mcal
    from pandas.tseries.offsets import BDay

    mkt = mcal.get_calendar(ExchangeName)
    tDate = DateTimeObj.date()
    dateRange = pd.bdate_range( start = tDate - BDay(1), end = tDate + BDay(1))
    mkt_hours = mkt.schedule( start_date = dateRange[0], end_date = dateRange[-1])

    return mkt.open_at_time( schedule = mkt_hours, timestamp = DateTimeObj, include_close = True)


def days_hours_mins_secs( TimeDeltaObj):
    '''
    Note that in Python 3 // is for integer division
    '''
    td = TimeDeltaObj
    hours, remainder = divmod( td.seconds, 3600)
    minutes, seconds = divmod( remainder, 60)

    return td.days, hours, minutes, seconds


def GetTimeToMktOpen( DateTimeObj, ExchangeName, debugmode = False):
    import pandas_market_calendars as mcal
    from datetime import timedelta

    # let's standardize time to UTC
    dt_now = TimeConvert(DateTimeObj, 'UTC')
    mkt = mcal.get_calendar(ExchangeName)
    sch = mkt.schedule( start_date = dt_now.date(),
                           end_date = MarketDateAdj(dt_now, 1, ExchangeName))

    close_time = sch['market_close'][0]

    # determine today's open or next day's open
    l_which_open = [h > dt_now for h in sch['market_open']]
    if l_which_open[0]:
        open_time = sch['market_open'][0]
    else:
        open_time = sch['market_open'][1]

    if IsMarketOpen(DateTimeObj, ExchangeName):
        # Show Time to Market Close
        tdelta = close_time.to_pydatetime() - dt_now

        if debugmode :
            print( f'--- Market is Open ---\nClose Time is {close_time}, Time Now is {dt_now}')

        return { 'status': 'open', 'd-h-m-s': days_hours_mins_secs(tdelta)}
    else:
        # Show Time to Next Market Open
        tdelta = open_time.to_pydatetime() - dt_now
        if debugmode :
            print( f'--- Market is Closed ---\nNext Open Time is {open_time}, Time Now is {dt_now}')
            print( f'\n--- Market Open Time ---\n{sch["market_open"]}')

        return { 'status': 'closed', 'd-h-m-s': days_hours_mins_secs(tdelta)}


@app.server.route('/assets/<path:path>')
def assets_file(path):
    assets_folder = os.path.join(os.getcwd(), 'assets')
    return send_from_directory(assets_folder, path)

if __name__ == '__main__':
    app.run_server(debug=True)
