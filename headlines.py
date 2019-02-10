import dash_html_components as html


def generate_headline_bar(bar_name):
    html_script = html.Div(
        [
            html.P(bar_name, className="left-div-header-element"),
        ], className="row left-div-header-div"
    )
    return html_script


def generate_table_row(df_headline, df_urls, df_s_score, df_r_score):
    print(type(df_s_score))

    if(float(df_s_score) > 0):
        cols = '#45df7e'
    elif(float(df_s_score) == 0):
        cols = 'white'
    else:
        cols = '#da5657'

    tr_script = html.Tr(
        [
            html.Td(
                html.A(
                    df_headline,
                    # "IMF flags trade war threat and warns of global economic slowdown",
                    href=df_urls,
                    # href="https://www.ft.com/content/8753e45c-1c91-11e9-b126-46fc3ad87c65",
                    target="_blank",
                ), style={'padding': '0px', 'border-bottom': '1px solid #777777'}
            ),
            html.Td(
                html.Strong(df_r_score, style={'padding': '0px', 'color': 'white'}), style={'min-width': '50px', 'padding': '0px', 'text-align': 'center'}),
            html.Td(
                html.Strong(df_s_score, style={'padding': '0px', 'color': cols, 'min-width': '15px'}), style={'min-width': '15px', 'padding': '0px', 'text-align': 'center'})
        ]
    )
    return tr_script


def generate_table_row_no_news():
    tr_script = html.Tr(
        [
            html.Td(
                html.P("No Over Night News Exist!"), style={'color': 'white', 'border-bottom': '1px solid #777777'}
            )
        ]
    )
    return tr_script


def generate_link_table(df):
    print(len(df))
    if(len(df) == 0):
        html_script = html.Div(
            [
                html.Table(
                    [
                        generate_table_row_no_news()

                    ]
                ),
            ], className="row borders left-div-link-table-element", style={'overflowY': 'scroll'}
        )
    else:
        html_script = html.Div(
            [
                html.Table(
                    [
                        generate_table_row(df['headline'][i], df['urls'][i], df['_sentiment'][i], df['_relevance'][i])
                        for i in range(len(df))

                    ]
                ),
            ], className="row borders left-div-link-table-element", style={'overflowY': 'scroll'}
        )
    return html_script
