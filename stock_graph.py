import dash_core_components as dcc
import dash_html_components as html
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime, timedelta, date
from iexfinance.stocks import get_historical_intraday
import pandas as pd


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
def MarketDateAdj(DateObj, IntBusinessDays, ExchangeName):
    from datetime import datetime, time, timedelta
    import pandas_market_calendars as mcal
    from pandas.tseries.offsets import BDay

    mkt = mcal.get_calendar(ExchangeName)
    holidays = mkt.holidays()

    inDay = DateObj.date()
    outDay = inDay + BDay(IntBusinessDays)

    while outDay in holidays.holidays:
        outDay += BDay(np.sign(IntBusinessDays) * 1)

    return outDay


def generate_graph(year, month, day, symbol, height):
    #tdate = datetime(2019, 2, 6)
    tdate = datetime(year, month, day)
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
        height=380,
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
