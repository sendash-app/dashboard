from datetime import datetime
from time_handling import TimeConvert
import ast


def GetLastBidAsk(df, stockcode):
    """return the last dict within trading hours"""
    for i in range(len(df)):
        df[stockcode][i] = ast.literal_eval(df[stockcode][i])
        if df[stockcode][i][0][0]['quote']['latestSource'] == 'IEX real time price':
            if (len(df[stockcode][i][0][0]['bids']) > 0) or (len(df[stockcode][i][0][0]['asks']) > 0):
                df[stockcode][i] = df[stockcode][i][0][0]
            else:
                del df[stockcode][i]
        else:
            del df[stockcode][i]

    return df[stockcode][df[stockcode].tail(1).index[0]]


def PrintBidAsk(quote_dict):
    bid_dict = {}
    ask_dict = {}
    if not quote_dict['bids'] or not quote_dict['asks']:
        data = quote_dict['quote']
        for side in ['Bid', 'Ask']:
            price = data[f'iex{side}Price']
            size = data[f'iex{side}Size']

            if price == 0 or size == 0:
                price = '-'
                size = '-'
            elif(price == None or size == None):
                price = '-'
                size = '-'

            if(side == 'Bid'):
                bid_dict[size] = price
            else:
                ask_dict[size] = price

        LastTimestamp = data['iexLastUpdated']
        if(LastTimestamp == None):
            last_update = f'Updated at: -'
        else:
            LastDT = datetime.fromtimestamp(LastTimestamp / 1e3)
            LastDTstr = f'{TimeConvert(LastDT, "EST").strftime("%d %b %y %H:%M %Z")}'
            last_update = f'Updated at: {LastDTstr}'

        return bid_dict, ask_dict, last_update

    else:   # Show Live Bid Ask
        data = quote_dict['quote']
        for side in ['bids', 'asks']:
            price = quote_dict[side][0]['price']
            size = quote_dict[side][0]['size']

            if(side == 'bids'):
                bid_dict[size] = price
            else:
                ask_dict[size] = price

            #last_update = 'Updated at: Current'
            LastTimestamp = data['iexLastUpdated']
            if(LastTimestamp == None):
                last_update = f'Updated at: -'
            else:
                LastDT = datetime.fromtimestamp(LastTimestamp / 1e3)
                LastDTstr = f'{TimeConvert(LastDT, "EST").strftime("%d %b %y %H:%M %Z")}'
                last_update = f'Updated at: {LastDTstr}'

        return bid_dict, ask_dict, last_update
