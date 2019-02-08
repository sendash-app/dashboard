import dash_html_components as html


def generate_headline_bar(bar_name):
    html_script = html.Div(
        [
            html.P(bar_name, className="left-div-header-element"),
        ], className="row left-div-header-div"
    )
    return html_script


def generate_table_row():
    tr_script = html.Tr(
        [
            html.Td(
                html.A(
                    "IMF flags trade war threat and warns of global economic slowdown",
                    href="https://www.ft.com/content/8753e45c-1c91-11e9-b126-46fc3ad87c65",
                    target="_blank",
                ), style={'padding': '0px'})
        ]
    )
    return tr_script


def generate_link_table():
    html_script = html.Div(
        [
            html.Table(
                [
                    generate_table_row(),
                    generate_table_row(),
                    generate_table_row(),
                    generate_table_row(),
                    generate_table_row(),
                    generate_table_row(),
                    generate_table_row(),
                    generate_table_row(),
                    generate_table_row(),
                    generate_table_row(),
                    # for i in range(min(len(dataframe), 10))
                ]
            ),
        ], className="row borders left-div-link-table-element", style={'overflowY': 'scroll'}
    )
    return html_script
