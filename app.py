import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas_datareader.data as web
import datetime as dateT
import plotly.graph_objs as go
from headlines import generate_headline_bar, generate_link_table
from quotes import generate_top_bar_logo, generate_pick_stock
from stock_graph import generate_graph, generate_sentiment_analysis_piechart, generate_graph_now, generate_sentiment_analysis_heatmap
from iexfinance.stocks import Stock
#from IPython.display import Image
from time_handling import TimeConvert, IsMarketOpen, days_hours_mins_secs, MarketDateAdj, GetTimeToMktOpen, IsMarketOpen_pd
from convert_image_to_square import make_square
from bid_ask import PrintBidAsk

from PIL import Image
import urllib.request

from datetime import datetime#, time
# import pandas_market_calendars as mcal
import pytz
# import pandas as pd

import plotly.plotly as py
import pandas as pd

#import sqlite3


app = dash.Dash('SENDASH')

# a config setting for run css and js in locally
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

#conn = sqlite3.connect('stocks.db')
#c = conn.cursor()


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
                html.Div(id='output-headline')

                #generate_link_table(),
                # generate_headline_bar("Tweets"),
                # generate_link_table(),
                #], className="col s3 row-margin-reduce borders", style={'height': '406px'}
            ], className="col s3 row-margin-reduce borders"
        ),

        # Right Panel
        html.Div(
            [
                #dcc.Input(id='input-date', value=dateT.datetime.today(), type='datetime-local', max=dateT.datetime.today(), style={'color':'white'}),
                dcc.Input(id='input-date', value=dateT.datetime.today().date(), type='date', max=dateT.date.today(), style={'color':'white'}),

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
                    #generate_sentiment_analysis_piechart()
                    html.Div(id='output-sentiment-score')
                    #generate_sentiment_analysis_heatmap(a)

                ], className="row row-margin-reduce")
            ], className="col s2 borders"  # 230px
        ),
        html.Div(
            [
                html.Div([
                    html.Div([
                        html.Div([
                            html.Strong("Bid", className="section-title"),
                        ], className="col s6 borders"),
                        html.Div([
                            html.Strong("Ask", className="section-title"),
                        ], className="col s6 borders")
                    ], className="row row-margin-reduce left-div-header-div borders", style={'margin-left':'0px', 'margin-right': '0px'}),
                    html.Div([
                        html.Div(id='output-bid-ask'),
                        dcc.Interval(id='input-bid-ask', interval=10 * 1000, n_intervals=0),
                    ], className="row row-margin-reduce"),
                ], className="row borders row-margin-reduce"),
                html.Div([
                    html.Div([
                        html.Strong("Opening Range Prediction", className="section-title"),
                    ], className="row row-margin-reduce left-div-header-div borders", style={'margin-left':'0px', 'margin-right': '0px'}),
                    html.Div([
                        #generate_sentiment_analysis_piechart()
                        #html.P('5'), html.P('5'), html.P('5'), html.P('5'), html.P('5'),html.P('5'), html.P('5'), html.P('5'), html.P('5'),
                    ], className="row row-margin-reduce")
                ], className="row borders row-margin-reduce")

            ], className="col s4 borders"  # 230px
        ),
        # html.Div(
        #     [
        #         #html.P('5'), html.P('5'), html.P('5'), html.P('5'), html.P('5'),
        #         html.Div([
        #             html.Div([
        #                 html.Strong("Bid", className="section-title"),
        #             ], className="col s6"),
        #             html.Div([
        #                 html.Strong("Ask", className="section-title"),
        #             ], className="col s6")
        #         ], className="row row-margin-reduce left-div-header-div borders"),
        #         html.Div([
        #             html.Div([
        #                 # html.P('5'), html.P('5'), html.P('5'), html.P('5'), html.P('5'),html.P('5'), html.P('5'), html.P('5'), html.P('5'),
        #                 html.Div(id='output-bid-ask'),
        #                 dcc.Interval(id='input-bid-ask', interval=30 * 1000, n_intervals=0),
        #             ], className="col s6 borders"),
        #             html.Div([
        #                 html.P('5'), html.P('5'), html.P('5'), html.P('5'), html.P('5'),html.P('5'), html.P('5'), html.P('5'), html.P('5'),
        #             ], className="col s6 borders")
        #         ], className="row row-margin-reduce")
        #     ], className="col s2 borders"  # 230px
        # ),
    ], className="row row-margin-reduce"),

], className="container bg-color", style={'width': '100%', 'max-width': 50000})


@app.callback(
    Output(component_id='output-headline', component_property='children'),
    [Input('input-stock-label', 'value'),
    Input('input-date', 'value')]
)
def update_headline(input_data, input_date):
    #raw = pd.read_csv('./assets/dataset/raw.csv', encoding='utf-8')
    raw = pd.read_csv('https://raw.githubusercontent.com/sendash-app/study_stocks_sentiments/master/dataset/nasdaq/overnight_sentiments.csv', encoding='utf-8')

    inputDate = datetime.strptime(input_date, '%Y-%m-%d')

    raw = raw.drop(labels='Unnamed: 0', axis=1)
    raw['date'] = raw['dt'].apply(lambda x: datetime.strptime(x[:-6], '%Y-%m-%d %H:%M:%S').date())
    raw = raw.dropna(subset=['_sentiment'])
    filter_by_date = raw[raw['date'] == inputDate.date()]
    filter_by_stock = filter_by_date[filter_by_date['stockcode'] == input_data]
    headline = filter_by_stock[['date', '_relevance', '_sentiment', 'urls', 'headline']].copy()
    headline['_sentiment'] = headline['_sentiment'].apply(lambda x: '{0:.2f}'.format(x))
    headline = headline.reset_index()
    headline = headline.drop(labels='index', axis=1)

    # print(headline['_sentiment'].head())
    # print(headline['_relevance'].head())
    # raw['datetime'] = raw['datetime'].str.replace('EDT', '')
    # raw['datetime'] = raw['datetime'].apply(get_est_dt_object)
    # raw['datetime'].dropna(inplace=True)

    # inputDate = datetime.strptime(input_date, '%Y-%m-%d')

    # raw['date'] = raw['datetime'].apply(lambda x: x.date())

    # filter_by_date = raw[raw['date'] == inputDate.date()]

    # filter_by_stock = filter_by_date[filter_by_date['stockcode'] == input_data]

    # headline = filter_by_stock[['headline', 'urls']].copy()
    # headline = headline.reset_index()
    # headline = headline.drop(labels='index', axis=1)

    #print(len(headline))

    return generate_link_table(headline)

@app.callback(
    Output(component_id='output-sentiment-score', component_property='children'),
    [Input('input-stock-label', 'value'),
    Input('input-date', 'value')]
)
def update_sentiment_score(input_data, input_date):

    inputDate = datetime.strptime(input_date, '%Y-%m-%d')

    raw = pd.read_csv('https://raw.githubusercontent.com/sendash-app/study_stocks_sentiments/master/dataset/nasdaq/daily_sentiment.csv', header=None,encoding='utf-8')

    raw = raw.rename(columns={0: "stockcode", 1: "date", 2: "_sentiment"})
    raw['_sentiment'] = raw['_sentiment'].apply(lambda x: '{0:.3f}'.format(x))
    raw['date'] = raw['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').date())
    filter_by_date = raw[raw['date'] == inputDate.date()]
    filter_by_stock = filter_by_date[filter_by_date['stockcode'] == input_data]
    filter_by_stock = filter_by_stock.reset_index()
    filter_by_stock = filter_by_stock.drop(labels='index', axis=1)

    print(filter_by_stock['_sentiment'])


    if(len(filter_by_stock) == 0):
        #print("is empty")
        sentiment_val = 0.0
    else:
        sentiment_val = float(filter_by_stock['_sentiment'][0])

    # raw = pd.read_csv('./assets/dataset/raw.csv', encoding='utf-8')
    # raw['datetime'] = raw['datetime'].str.replace('EDT','')
    # raw['datetime'] = raw['datetime'].apply(get_est_dt_object)
    # raw['datetime'].dropna(inplace=True)

    # inputDate = datetime.strptime(input_date, '%Y-%m-%d')

    # raw['date'] = raw['datetime'].apply(lambda x: x.date())

    # filter_by_date = raw[raw['date'] == inputDate.date()]

    # filter_by_stock = filter_by_date[filter_by_date['stockcode'] == input_data]

    # headline_list = filter_by_stock['headline'].tolist()
    # url_list = filter_by_stock['urls'].tolist()

    # print(headline_list)
    # print(url_list)

    #print(a['datetime'].head())
    #print(input_data)
    #print(datetime.input_date)



    return generate_sentiment_analysis_heatmap(sentiment_val)

def get_est_dt_object(x):
    try:
        ts = pytz.timezone('EST')
        x = ts.localize(datetime.strptime(str(x), '%B %d, %Y, %I:%M:%S %p '))
    except:
        x = None
    return x

# Generate stock price closing graph


@app.callback(
    Output(component_id='output-stock-price-graph', component_property='children'),
    [Input('input-stock-label', 'value'),
    Input('input-date', 'value')]
)
def update_graph(input_data, input_date):
    #print(input_date)
    DateTimeObj = datetime.strptime(input_date, "%Y-%m-%d") + dateT.timedelta(hours=9, minutes=30)
    #print(type(input_date))
    ExchangeName = 'NYSE'
    #DateTimeObj = datetime.strptime(input_date, '%d/%m/%YT%H:%M %S')
    #print(DateTimeObj.date())
    #print(dateT.date.today())
    marketOpenStatus = IsMarketOpen_pd(DateTimeObj, ExchangeName)
    print("market open status")
    print(marketOpenStatus)

    previous_date = DateTimeObj - dateT.timedelta(days=1)

    previous_date_Open_status = IsMarketOpen_pd(previous_date, ExchangeName)
    print("previsous date open status")
    print(previous_date_Open_status)

    if(marketOpenStatus == False and DateTimeObj.date() == dateT.date.today()):
        getNextDate = MarketDateAdj(DateTimeObj, 1, ExchangeName)
        result = getNextDate
        return generate_graph_now(result, input_data, 380)
    elif(marketOpenStatus == False and DateTimeObj.date() != dateT.date.today() and previous_date_Open_status == False):
        getNextDate = MarketDateAdj(DateTimeObj, 1, ExchangeName)
        result = getNextDate
        return generate_graph(result, input_data, 380)
    elif(marketOpenStatus == False and DateTimeObj.date() != dateT.date.today() and previous_date_Open_status == True):
        getNextDate = MarketDateAdj(DateTimeObj, 1, ExchangeName)
        result = getNextDate
        if(getNextDate.date() > dateT.date.today()):
            return generate_graph_now(result, input_data, 380)
        else:
            return generate_graph(result, input_data, 380)
    else:
        result = DateTimeObj
        return generate_graph(result, input_data, 380)


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
        ], style={'height':'150px'})
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


@app.callback(
    Output(component_id='output-bid-ask', component_property='children'),
    [Input('input-bid-ask', 'n_intervals'),
        Input('input-stock-label', 'value')]
)
def update_bid_ask(interval, input_data):
    myStock = Stock(input_data)
    book = myStock.get_book()

    bid, ask, lastUpdate = PrintBidAsk(book)
    # print("bid key")
    # print(list(bid.keys())[0])
    # print("bid value")
    # print(list(bid.values())[0])
    # print("ask key")
    # print(list(bid.keys())[0])
    # print("ask value")
    # print(list(bid.values())[0])
    #print(ask)
    return [
        html.Div([
            html.Div([
                html.Div([
                    html.Strong(list(bid.keys())[0], style={'color':'white'}),
                    #html.Strong("-", style={'color':'white'}),
                ], className="col s5", style={'text-align':'center', 'padding':'8px 0px'}),
                html.Div([
                    html.Strong("x", style={'color':'white'}),
                ], className="col s2", style={'text-align':'center', 'padding':'8px 0px'}),
                html.Div([
                    html.Strong(list(bid.values())[0], style={'color':'white', 'font-size':'25px'}),
                    #html.Strong("-", style={'color':'white', 'font-size':'25px'}),

                ], className="col s5", style={'text-align':'center', 'padding':'0px'}),

            ], className="col s6 borders", style={'float':'center', 'padding':'10px 0px'}),
            html.Div([
                html.Div([
                    html.Strong(list(ask.values())[0], style={'color':'white', 'font-size':'25px'}),
                    #html.Strong("-", style={'color':'white', 'font-size':'25px'}),
                ], className="col s5", style={'text-align':'center', 'padding':'0px'}),
                html.Div([
                    html.Strong("x", style={'color':'white'}),
                ], className="col s2", style={'text-align':'center', 'padding':'8px 0px'}),
                html.Div([
                    html.Strong(list(ask.keys())[0], style={'color':'white'}),
                    #html.Strong("-", style={'color':'white'}),

                ], className="col s5", style={'text-align':'center', 'padding':'8px 0px'}),

            ], className="col s6 borders", style={'float':'center', 'padding':'10px 0px'}),
        ], className="row row-margin-reduce borders", style={'margin':'0px'}),
        html.Div([
            html.P(lastUpdate, style={'color':'white', 'padding-left':'15px'})

        ], className="row row-margin-reduce borders", style={'margin':'0px'}),
    ]


@app.server.route('/assets/<path:path>')
def assets_file(path):
    assets_folder = os.path.join(os.getcwd(), 'assets')
    return send_from_directory(assets_folder, path)

if __name__ == '__main__':
    app.run_server(debug=True, processes=4)
