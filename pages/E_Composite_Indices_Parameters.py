# This page depicts the trends of various indicators in a Sectoral manner
# The PART 1 isolates the script file from Master to Individual and save in folder 'Equity_Script_Files'
# The PART 2 fetch the Individual Files in a loop as per the Sectotal watchlist selected from dropdown and depicts in Graphical manner

import dash

# Code from: https://github.com/plotly/dash-labs/tree/main/docs/demos/multi_page_example1
dash.register_page(__name__)

from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from screeninfo import get_monitors
from nsepython import *
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Get Screen Resolution
for m in get_monitors():
    hgt = int(m.height)
    wd = int(m.width)

# Define the Paths to the required folders
Ind_cur_dir = os.getcwd()
Ind_cur_master_dir = Ind_cur_dir + r"\Master_Files"
Ind_cur_fo_dir = Ind_cur_dir + r"\dumps\bhavcopy\nse\eod_fo"
Ind_cur_support_dir = Ind_cur_dir + r"\Support_Files"
Ind_Script_Dir_Eq = Ind_cur_dir + r"\Script_Files_Equity"
Ind_Script_Dir_Del = Ind_cur_dir + r"\Script_Files_Delivery"
Ind_lot_size_list = pd.read_csv(Ind_cur_support_dir + r"\Lot_Size_Filtered.csv")
Ind_dropdown_opt_list = pd.read_csv(Ind_cur_support_dir + r"\Dropdown_options.csv")
Ind_dropdown_Industry_list = pd.read_csv(Ind_cur_support_dir + r"\WL_NIFTY_500.csv")

# PART 2
# _________________________________________________________________________________________________________
# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '2%',
    'margin-right': '5%',
    'padding': '20px 10p'
}

content_first_row = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id='Ind_dropdown_opt',
                        options=[{'label': x, 'value': x}
                                 for x in Ind_dropdown_opt_list.DRP_OPT],
                        value=Ind_dropdown_opt_list.DRP_OPT[2],  # default value
                        multi=False
                    ),
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id='Ind_dropdown_industry',
                        options=[{'label': x, 'value': x}
                                 for x in Ind_dropdown_Industry_list.Industry.unique()],
                        value='',  # default value
                        multi=False
                    ),
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id='Indicator',
                        options=[{'label': 'Volume', 'value': 'Volume'},
                                 {'label': 'Del_Qty', 'value': 'Del_Qty'},
                                 {'label': 'Del%', 'value': 'Del%'},
                                 {'label': 'Q/T', 'value': 'Q/T'},
                                 {'label': 'Trade Value', 'value': 'Trade Value'},
                                 ],
                        value='Q/T',  # default value
                        multi=False
                    ),
                ]
            )
        ),
    ]
)

content_second_row = dbc.Row(
    [
        dbc.Col(
            html.Br()
        )
    ]
)

content_third_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='indicator_graph', config=dict({'scrollZoom': True})), md=12,
        )
    ]
)

content = html.Div(
    [
        content_first_row,
        content_second_row,
        content_third_row
    ],
    style=CONTENT_STYLE
)

# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
layout = html.Div([content])


@callback(Output('indicator_graph', 'figure'),
          Input('Ind_dropdown_opt', 'value'),
          Input('Indicator', 'value'),
          Input('Ind_dropdown_industry', 'value'))
def indicator_chart(watchlist, indicator, industry):
    print(watchlist)
    print(indicator)
    print(industry)


    Ind_Script = pd.read_csv(os.path.join(Ind_cur_support_dir, (watchlist + '.csv')))
    if industry != "":
        Ind_Script = Ind_Script[Ind_Script['Industry'] == industry]
    no_of_script = len(Ind_Script)
    print(len(Ind_Script))

    fig = make_subplots(
        rows=no_of_script, cols=1,
        print_grid=True, shared_xaxes=True, horizontal_spacing=0.05, vertical_spacing=0)

    config = dict({'scrollZoom': True})
    fig.update_layout(height=(hgt / 6 * no_of_script), width=wd)  # title_text="Equity Data")
    fig.update_layout(paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
    fig.update_layout(margin=dict(r=2, t=2, b=2, l=2))
    fig.update_xaxes(rangeslider_visible=False)
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(mirror=True, row=1, col=1)
    fig.update_yaxes(mirror="ticks", side='right')
    fig.update_layout(
        dragmode='drawline',
        newshape_line_color='cyan'
    )
    fig.update_layout(showlegend=False)
    fig.update_layout(
        xaxis1=dict(
            rangeslider_visible=False,
            rangeselector=dict(
                buttons=list([
                    dict(count=5, label="5m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
    )

    # Add Volume as Subplot
    k = 1
    for item in Ind_Script['Symbol']:
        Ind_sub_plot_file_Eq = os.path.join(Ind_Script_Dir_Eq, (item + '.csv'))
        Ind_sub_plot_df_Eq = pd.read_csv(Ind_sub_plot_file_Eq)
        Ind_sub_plot_df_Eq['qt'] = Ind_sub_plot_df_Eq.TOTTRDQTY / Ind_sub_plot_df_Eq.TOTALTRADES
        Ind_sub_plot_df_Eq = Ind_sub_plot_df_Eq.rename(columns={'TOTTRDQTY': 'Volume',
                                              'TOTTRDVAL': 'Trade Value',
                                              'qt': 'Q/T'})
        # Ind_sub_plot_df_Eq['color'] = np.where(Ind_sub_plot_df_Eq["CLOSE"] <= Ind_sub_plot_df_Eq["PREVCLOSE"], 'red', 'green')
        Ind_sub_plot_file_Del = os.path.join(Ind_Script_Dir_Del, (item + '.csv'))
        Ind_sub_plot_df_Del = pd.read_csv(Ind_sub_plot_file_Del)
        Ind_sub_plot_df_Del = Ind_sub_plot_df_Del.rename(columns={
                                              'del_qty': 'Del_Qty',
                                              'del_percent': 'Del%'})

        if indicator == "Del_Qty" or indicator == "Del%":
            fig.add_trace(
                go.Bar(x=Ind_sub_plot_df_Del['TIMESTAMP'], y=Ind_sub_plot_df_Del[indicator], name=item),
                row=k, col=1)
        else:
            fig.add_trace(
                go.Bar(x=Ind_sub_plot_df_Eq['TIMESTAMP'], y=Ind_sub_plot_df_Eq[indicator], name=item),
                row=k, col=1)

        # print the script name on Yaxis
        if k == 1:
            yaxisvalue = 'yaxis'
        else:
            yaxisvalue = 'yaxis' + str(k)

        fig['layout'][str(yaxisvalue)]['title'] = item

        k = k + 1
    return fig
