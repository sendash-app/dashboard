import dash_core_components as dcc
import dash_html_components as html
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime, timedelta, date
from iexfinance.stocks import get_historical_intraday
import pandas as pd
from time_handling import MarketDateAdj
import numpy as np

# def generate_graph(x, y, height, title, id_name, graph_type):
#     return dcc.Graph(
#         id=id_name,
#         figure={
#             'data': [
#                 {'x': x, 'y': y, 'type': graph_type, 'name': title},
#             ],
#             'layout': {
#                 'title': title,
#                 'height': height,
#                 'font': dict(color='#CCCCCC'),
#                 'titlefont': dict(color='#CCCCCC', size='14'),
#                 'margin': dict(l=35, r=35, b=35, t=45),
#                 'hovermode': "closest",
#                 'plot_bgcolor': "#191A1A",
#                 'paper_bgcolor': "#777777",
#                 'legend': dict(font=dict(size=10), orientation='h'),
#                 'xaxis': dict(
#                     showgrid=True,
#                     gridcolor='#777777',
#                 ),
#                 'yaxis': dict(
#                     showgrid=True,
#                     gridcolor='#777777',
#                 )
#             }
#         }
#     )


def generate_graph(input_date, symbol, height):
    #tdate = datetime(2019, 2, 6)
    #print(input_date)
    tdate = datetime(input_date.year, input_date.month, input_date.day)
    tdate_neg1 = MarketDateAdj(tdate, -1, 'NYSE')

    tdata = get_historical_intraday(symbol, tdate, output_format='pandas')
    tdata_neg1 = get_historical_intraday(symbol, tdate_neg1, output_format='pandas')

    tdata.index = pd.DatetimeIndex(tdata.index)
    tdata_neg1.index = pd.DatetimeIndex(tdata_neg1.index)

    trace1 = go.Scatter(
        x=tdata_neg1.index,
        y=tdata_neg1['close'],
        name='tdate_neg1 Close',
        textposition='bottom center'
    )
    trace2 = go.Scatter(
        x=tdata.index,
        y=tdata['close'],
        name='tdate Close',
        textposition='bottom center'
    )

    plot_dict = {
        tdate_neg1: tdata_neg1,
        tdate: tdata
    }

    date_list = []

    for i, idate in enumerate(plot_dict):
        date_list.append(idate)

    fig = tools.make_subplots(rows=1, cols=2, specs=[[{}, {}]], subplot_titles=(f'{symbol} | {date_list[0].strftime("%a, %d %b %y")}', f'{symbol} | {date_list[1].strftime("%a, %d %b %y")}'), shared_yaxes=True)

    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)

    fig['layout'].update(
        height=400,
        font=dict(color='#CCCCCC'),
        margin=dict(l=35, r=35, b=35, t=45),
        hovermode="closest",
        plot_bgcolor="#191A1A",
        paper_bgcolor="#777777",
        legend=dict(font=dict(size=10), orientation='h'),
        xaxis1=dict(
            showgrid=True,
            gridcolor='#777777',
            tickformat='%H:%M'
        ),
        yaxis1=dict(
            showgrid=True,
            gridcolor='#777777',
        ),
        xaxis2=dict(
            showgrid=True,
            gridcolor='#777777',
            tickformat='%H:%M'
        ),
        yaxis2=dict(
            showgrid=True,
            gridcolor='#777777',
        )
    )

    return html.Div([
        dcc.Graph(
            figure=fig)
    ])


def generate_graph_now(input_date, symbol, height):
    #tdate = datetime(2019, 2, 6)

    #print(input_date)
    tdate = datetime(input_date.year, input_date.month, input_date.day)
    tdate_neg1 = MarketDateAdj(tdate, -1, 'NYSE')

    tdata = get_historical_intraday(symbol, tdate, output_format='pandas')
    tdata_neg1 = get_historical_intraday(symbol, tdate_neg1, output_format='pandas')

    tdata.index = pd.DatetimeIndex(tdata.index)
    tdata_neg1.index = pd.DatetimeIndex(tdata_neg1.index)

    # x_data = np.array(['09:31','09:32','09:33','09:34','09:35','09:36','09:37','09:38','09:39','09:41','09:42','09:43','09:44','09:45','09:46','09:47','09:48','09:49','09:50','09:51','09:52','09:53','09:54','09:55','09:56','09:57','09:58','09:59','10:00','10:01','10:02','10:03','10:04','10:05','10:06','10:07','10:08','10:09','10:10','10:11','10:12','10:13','10:14','10:15','10:16','10:17','10:18','10:19','10:20','10:21','10:22','10:23','10:24','10:25','10:26','10:27','10:28','10:29','10:30','10:31','10:32','10:33','10:34','10:35','10:36','10:37','10:38','10:39','10:40','10:41','10:42','10:43','10:44','10:45','10:46','10:47','10:48','10:49','10:50','10:51','10:52','10:53','10:54','10:55','10:56','10:57','10:58','10:59','11:00','11:01','11:02','11:03','11:04','11:05','11:06','11:07','11:08','11:09','11:10','11:11','11:12','11:13','11:14','11:15','11:16','11:17','11:18','11:19','11:20','11:21','11:22','11:23','11:24','11:25','11:26','11:27','11:28','11:29','11:30','11:31','11:32','11:33','11:34','11:35','11:36','11:37','11:38','11:39','11:40','11:41','11:42','11:43','11:44','11:45','11:46','11:47','11:48','11:49','11:50','11:51','11:52','11:53','11:54','11:55','11:56','11:57','11:58','11:59','12:00','12:01','12:02','12:03','12:04','12:05','12:06','12:07','12:08','12:09','12:10','12:11','12:12','12:13','12:14','12:15','12:16','12:17','12:18','12:19','12:20','12:21','12:22','12:23','12:24','12:25','12:26','12:27','12:28','12:29','12:30','12:31','12:32','12:33','12:34','12:35','12:36','12:37','12:38','12:39','12:40','12:41','12:42','12:43','12:44','12:45','12:46','12:47','12:48','12:49','12:50','12:51','12:52','12:53','12:54','12:55','12:56','12:57','12:58','12:59','13:00','13:01','13:02','13:03','13:04','13:05','13:06','13:07','13:08','13:09','13:10','13:11','13:12','13:13','13:14','13:15','13:16','13:17','13:18','13:19','13:20','13:21','13:22','13:23','13:24','13:25','13:26','13:27','13:28','13:29','13:30','13:31','13:32','13:33','13:34','13:35','13:36','13:37','13:38','13:39','13:40','13:41','13:42','13:43','13:44','13:45','13:46','13:47','13:48','13:49','13:50','13:51','13:52','13:53','13:54','13:55','13:56','13:57','13:58','13:59','14:00','14:01','14:02','14:03','14:04','14:05','14:06','14:07','14:08','14:09','14:10','14:11','14:12','14:13','14:14','14:15','14:16','14:17','14:18','14:19','14:20','14:21','14:22','14:23','14:24','14:25','14:26','14:27','14:28','14:29','14:30','14:31','14:32','14:33','14:34','14:35','14:36','14:37','14:38','14:39','14:40','14:41','14:42','14:43','14:44','14:45','14:46','14:47','14:48','14:49','14:50','14:51','14:52','14:53','14:54','14:55','14:56','14:57','14:58','14:59','15:00','15:01','15:02','15:03','15:04','15:05','15:06','15:07','15:08','15:09','15:10','15:11','15:12','15:13','15:14','15:15','15:16','15:17','15:18','15:19','15:20','15:21','15:22','15:23','15:24','15:25','15:26','15:27','15:28','15:29','15:30','15:31','15:32','15:33','15:34','15:35','15:36','15:37','15:38','15:39','15:40','15:41','15:42','15:43','15:44','15:45','15:46','15:47','15:48','15:49','15:50','15:51','15:52','15:53','15:54','15:55','15:56','15:57','15:58','15:59'])

    trace1 = go.Scatter(
        x=tdata_neg1.index,
        y=tdata_neg1['close'],
        name='tdate_neg1 Close',
        textposition='bottom center'
    )
    trace2 = go.Scatter(
        x=tdata_neg1.index,
        y=np.repeat(tdata_neg1['close'][-1], 390),
        # y=np.zeros(390),

        name='tdate Close',
        textposition='bottom center',
        line=dict(color='#191A1A'),
    )

    plot_dict = {
        tdate_neg1: tdata_neg1,
        tdate: tdata_neg1
    }

    date_list = []

    for i, idate in enumerate(plot_dict):
        print(idate)
        date_list.append(idate)

    fig = tools.make_subplots(rows=1, cols=2, specs=[[{}, {}]], subplot_titles=(f'{symbol} | {date_list[0].strftime("%a, %d %b %y")}', f'{symbol} | {date_list[1].strftime("%a, %d %b %y")}'), shared_yaxes=True, )

    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)

    fig['layout'].update(
        height=400,
        font=dict(color='#CCCCCC'),
        margin=dict(l=35, r=35, b=35, t=45),
        hovermode="closest",
        plot_bgcolor="#191A1A",
        paper_bgcolor="#777777",
        legend=dict(font=dict(size=10), orientation='h'),
        xaxis1=dict(
            showgrid=True,
            gridcolor='#777777',
            tickformat='%H:%M'
        ),
        yaxis1=dict(
            showgrid=True,
            gridcolor='#777777',
        ),
        xaxis2=dict(
            showgrid=True,
            gridcolor='#777777',
            tickformat='%H:%M'
        ),
        yaxis2=dict(
            showgrid=True,
            gridcolor='#777777',
        )
    )

    return html.Div([
        dcc.Graph(
            figure=fig)
    ])


def generate_sentiment_analysis_piechart():

    fig = {
        "data": [
            {
                "values": [58, 42],
                "hoverinfo":"closest",
                "hole": .4,
                "type": "pie",
                'marker': {'colors':
                           ['#3399ff', '#a9ebff']
                           }
            },
        ],
        "layout": {
            "height": 277,
            "showlegend": False,
            "margin": go.layout.Margin(
                l=10,
                r=10,
                b=10,
                t=10,
            ),
            'plot_bgcolor': "#191A1A",
            'paper_bgcolor': "#232b2b",
            'font': dict(color='#CCCCCC'),
        }
    }

    return html.Div([
        dcc.Graph(
            figure=fig, config={'displayModeBar': False})
    ])
