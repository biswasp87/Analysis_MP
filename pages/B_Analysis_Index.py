import dash
# Code from: https://github.com/plotly/dash-labs/tree/main/docs/demos/multi_page_example1
dash.register_page(__name__)

from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from datetime import date
from screeninfo import get_monitors
import os
import numpy as np
from nsepython import *



# Get Screen Resolution
for m in get_monitors():
    hgt = int(m.height)
    wd = int(m.width)

cur_dir = os.getcwd()
cur_master_dir = cur_dir + r"\Master_Files"
cur_support_dir = cur_dir + r"\Support_Files"
cur_fo_dir = cur_dir + r"\dumps\bhavcopy\nse\eod_fo"
lot_size_list = pd.read_csv(cur_support_dir + r"\Lot_Size_Filtered.csv")
Index_Watchlist = pd.read_csv(cur_support_dir + r"\Index_Watchlist.csv")
Expiry_Date_All = pd.read_csv(cur_support_dir + r"/Expiry_Date_All.csv")

# for n in range(15):
#     start_date = date.today() - timedelta(days=n)
#     start_year = start_date.year
#     start_month = start_date.month
#     start_date = start_date.day
#     print(start_year, start_month, start_date)
#
#     if start_month == 1:
#         month_str = 'JAN'
#     elif start_month == 2:
#         month_str = 'FEB'
#     elif start_month == 3:
#         month_str = 'MAR'
#     elif start_month == 4:
#         month_str = 'APR'
#     elif start_month == 5:
#         month_str = 'MAY'
#     elif start_month == 6:
#         month_str = 'JUN'
#     elif start_month == 7:
#         month_str = 'JUL'
#     elif start_month == 8:
#         month_str = 'AUG'
#     elif start_month == 9:
#         month_str = 'SEP'
#     elif start_month == 10:
#         month_str = 'OCT'
#     elif start_month == 11:
#         month_str = 'NOV'
#     elif start_month == 12:
#         month_str = 'DEC'
#     else:
#         print('Invalid number')
#
#     if start_date < 10:
#         start_file_name = 'fo' + '0' + str(start_date) + str(month_str) + str(start_year) + 'bhav' + '.csv' + '.zip'
#     else:
#         start_file_name = 'fo' + str(start_date) + str(month_str) + str(start_year) + 'bhav' + '.csv' + '.zip'
#
#     if os.path.exists(cur_fo_dir + '/' + start_file_name) == True:
#         exp_data = pd.read_csv(cur_fo_dir + '/' + start_file_name)
#         exp_data = exp_data[exp_data.INSTRUMENT == 'FUTSTK']
#         print(exp_data)
#         break
#     elif os.path.exists(cur_fo_dir + '/' + start_file_name) == False:
#         print('File not Available')
#
# expiry_dates = exp_data.EXPIRY_DT.unique()
# print(expiry_dates)

dir_name_fo = cur_master_dir + r"\master_fo.csv"
fut_data = pd.read_csv(dir_name_fo)
fut_data['TIMESTAMP'] = pd.to_datetime(fut_data['TIMESTAMP'])
fut_data = fut_data.sort_values(by='TIMESTAMP', ascending=True)
fut_data['index'] = fut_data.reset_index().index


dir_name_opt_ce = cur_master_dir + r"\master_ce.csv"  # Home desktop
opt_ce_data = pd.read_csv(dir_name_opt_ce)
opt_ce_data['TIMESTAMP'] = pd.to_datetime(opt_ce_data['TIMESTAMP'])
opt_ce_data = opt_ce_data.sort_values(by='TIMESTAMP', ascending=True)
opt_ce_data['index'] = opt_ce_data.reset_index().index

dir_name_opt_pe = cur_master_dir + r"\master_pe.csv"  # Home desktop
opt_pe_data = pd.read_csv(dir_name_opt_pe)
opt_pe_data['TIMESTAMP'] = pd.to_datetime(opt_pe_data['TIMESTAMP'])
opt_pe_data = opt_pe_data.sort_values(by='TIMESTAMP', ascending=True)
opt_pe_data['index'] = opt_pe_data.reset_index().index


dir_name_eq = cur_master_dir + r"\master_eq.csv"  # Home desktop
eq_data = pd.read_csv(dir_name_eq)
eq_data['TIMESTAMP'] = pd.to_datetime(eq_data['TIMESTAMP'])
eq_data = eq_data.sort_values(by='TIMESTAMP', ascending=True)

dir_name_del = cur_master_dir + r"\master_del.csv"  # Home desktop
del_data = pd.read_csv(dir_name_del)
del_data['TIMESTAMP'] = pd.to_datetime(del_data['TIMESTAMP'])
del_data = del_data.sort_values(by='TIMESTAMP', ascending=True)
del_data['index'] = del_data.reset_index().index

dir_name_index = cur_master_dir + r"\master_indices.csv"  # Home desktop
index_data = pd.read_csv(dir_name_index, parse_dates=['Index_Date'], dayfirst=True)
index_data = index_data.sort_values(by='Index_Date', ascending=True)
index_data['index'] = index_data.reset_index().index


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
                        id='dropdown_opt_index',
                        options=[{'label': 'ALL', 'value': 'ALL'},
                                 {'label': 'FNO', 'value': 'FNO'}],
                        value='ALL',  # default value
                        multi=False
                    ),
                    dcc.Graph(id='graph_1_index', config={'displayModeBar': False})
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id='dropdown_index',
                        options=[{'label': x, 'value': x}
                                 for x in Index_Watchlist.ALL],
                        value='Nifty 50',  # default value
                    ),
                    # dcc.Graph(id='graph_1', config={'displayModeBar': False})
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id='dropdown_exp_index',
                        options=[{'label': x, 'value': x}
                                 for x in Expiry_Date_All.All],
                        value=Expiry_Date_All.All[0],  # default value
                        multi=False
                    ),
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                id='submit_button',
                                n_clicks=0,
                                children='Prev',
                                color='primary',
                                className="ml-0",
                                size='sm',
                            ),
                        ]),
                        dbc.Col([
                            dbc.Button(
                                id='submit_button_next',
                                n_clicks=0,
                                children='Next',
                                color='primary',
                                className="ml-0",
                                size='sm'
                            ),
                        ])
                            ])
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [

                ]
            )
        ),
    ]
)

content_second_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_31_index', config=dict({'scrollZoom': True})), md=12,
        )
    ]
)

content = html.Div(
    [
        content_first_row,
        content_second_row,
    ],
    style=CONTENT_STYLE
)


layout = html.Div([content])


@callback(
    Output('dropdown_index', 'value'),
    Input('submit_button', 'n_clicks'),
    Input('submit_button_next', 'n_clicks'),
    Input('dropdown_index', 'value'),
    Input('dropdown_opt_index', 'value')
)
def update_dropdown(n_clicks, n_clicks_next, dropdown_value, dropdown_opt_val):
    print(n_clicks)
    print(n_clicks_next)
    print(dropdown_value)
    print(dropdown_opt_val)
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    print(ctx)
    print(trigger_id)
    if trigger_id == 'submit_button':
        cur_position = Index_Watchlist[Index_Watchlist[dropdown_opt_val] == dropdown_value].index[0]
        cur_position = int(cur_position)
        print(cur_position)
        value = Index_Watchlist[dropdown_opt_val].iloc[cur_position - 1]

    elif trigger_id == 'submit_button_next':
        cur_position = Index_Watchlist[Index_Watchlist[dropdown_opt_val] == dropdown_value].index[0]
        cur_position = int(cur_position)
        print(cur_position)
        value = Index_Watchlist[dropdown_opt_val].iloc[cur_position + 1]
    else:
        value = dropdown_value

    return value


@callback(
    Output('dropdown_index', 'options'),
    [Input('dropdown_opt_index', 'value')])
def update_dropdown_list(dropdown_item_value):
    print(dropdown_item_value)
    options = [{'label': x, 'value': x}
               for x in Index_Watchlist[dropdown_item_value]]
    return options


@callback(
    Output('graph_1_index', 'figure'),
    [Input('dropdown_exp_index', 'value'),
     Input('dropdown_index', 'value')])
def update_graph_1(dropdown_exp_value, dropdown_value):
    print(dropdown_value)
    print(dropdown_exp_value)

    if dropdown_value == 'NIFTY' or dropdown_value == 'BANKNIFTY' or dropdown_value == 'FINNIFTY':
        df_fut_g1_index = fut_data[(fut_data.EXPIRY_DT == dropdown_exp_value) & (
                    fut_data.SYMBOL == dropdown_value)]  # Fetch Equity master Data and filter by Stock Name
        spot_price = df_fut_g1_index['CLOSE'].iloc[-1]  # Find the Spot price as per last Closing
        prev_price = df_fut_g1_index['CLOSE'].iloc[-2]  # Find the Previous Day price as per Closing
    else:
        df_eq_g1_index = eq_data[eq_data.SYMBOL == dropdown_value]  # Fetch Equity master Data and filter by Stock Name
        spot_price = 2 #df_eq_g1_index['CLOSE'].iloc[-1]  # Find the Spot price as per last Closing
        prev_price = 1 #df_eq_g1_index['CLOSE'].iloc[-2]  # Find the Previous Day price as per Closing

    fig_g1_index = go.Figure()
    fig_g1_index.add_trace(go.Indicator(
        mode="number+delta",
        value=spot_price,
        delta={'reference': prev_price, 'relative': True},
    ))
    fig_g1_index.update_traces(delta_font={'size': 15})
    fig_g1_index.update_traces(number_font_size=15, selector=dict(type='indicator'))
    fig_g1_index.update_traces(delta_position='left', selector=dict(type='indicator'))
    fig_g1_index.update_traces(number_prefix='Close ', selector=dict(type='indicator'))
    fig_g1_index.update_traces(align='left', selector=dict(type='indicator'))
    fig_g1_index.update_layout(height=20, width=150)
    fig_g1_index.update_layout(margin_l=0)
    return fig_g1_index

@callback(
    Output('graph_31_index', 'figure'),
    [Input('dropdown_exp_index', 'value'),
     Input('dropdown_index', 'value'),
     Input('dropdown_opt_index', 'value')])
def update_graph_31(dropdown_exp_value, dropdown_value, dropdown_opt_value):
    print("Hi")
    print(dropdown_value)
    print(dropdown_exp_value)
    print(dropdown_opt_value)

    if dropdown_opt_value == "FNO":
        if dropdown_value == 'Nifty 50':
            Index_Value="NIFTY"
        elif dropdown_value == 'Nifty Bank':
            Index_Value='BANKNIFTY'
        else:
            Index_Value='FINNIFTY'

        df_index = index_data[(index_data.Index_Name == dropdown_value)]
        df_index['Volume'] = df_index.Volume.astype(float)
        df_index['Points_Change'] = df_index.Points_Change.astype(float)
        df_index['color'] = np.where(df_index["Points_Change"] <= 0, 'red', 'green')

        df_index['Points_Change'] = df_index.Points_Change.astype(float)
        df_fut_all = fut_data[(fut_data.SYMBOL == Index_Value)]
        # df_fut_all.to_csv(cur_dir + "/df_fut_all.csv", index=False)
        df_fut_coi = df_fut_all.groupby('TIMESTAMP').agg('sum')
        df_fut_coi['OPEN_INT']=df_fut_coi.OPEN_INT.astype(float)
        # df_fut_coi['color'] = np.where(df_fut_coi["CHG_IN_OI"] < 0, 'red', 'green')
        df_fut_coi.reset_index(inplace=True)
        # df_fut_coi.to_csv(cur_dir + "/df_fut_coi.csv", index=False)

        df_opt_ce = opt_ce_data[
            (opt_ce_data.EXPIRY_DT == dropdown_exp_value) & (opt_ce_data.SYMBOL == Index_Value)]
        df_opt_maxce = df_opt_ce.loc[df_opt_ce.groupby('TIMESTAMP')['OPEN_INT'].agg(pd.Series.idxmax)]
        df_opt_pe = opt_pe_data[
            (opt_pe_data.EXPIRY_DT == dropdown_exp_value) & (opt_pe_data.SYMBOL == Index_Value)]
        df_opt_maxpe = df_opt_pe.loc[df_opt_pe.groupby('TIMESTAMP')['OPEN_INT'].agg(pd.Series.idxmax)]

        lot_size = lot_size_list[lot_size_list.SYMBOL == Index_Value]
        lot = int(lot_size["LOT_SIZE"].iloc[0])

        df_opt_ce_ind = opt_ce_data[
            (opt_ce_data.EXPIRY_DT == dropdown_exp_value) & (opt_ce_data.SYMBOL == Index_Value)]
        df_opt_ce_ind['indicator_sr_price'] = np.where(df_opt_ce_ind['CONTRACTS'] * lot > 50000000,
                                                        df_opt_ce_ind['STRIKE_PR'], '')

        df_opt_pe_ind = opt_pe_data[
            (opt_pe_data.EXPIRY_DT == dropdown_exp_value) & (opt_pe_data.SYMBOL == Index_Value)]
        df_opt_pe_ind['indicator_sr_price'] = np.where(df_opt_pe_ind['CONTRACTS'] * lot > 50000000,
                                                        df_opt_pe_ind['STRIKE_PR'], '')

        # Draw FNO Plot for INDEXES
        # ____________________________________________________________

        fig_index = make_subplots(
                rows=4, cols=1,
                row_heights=[0.3, 0.3, 0.2, 0.2],
                specs=[[{"rowspan": 2, "colspan": 1}],
                       [None],
                       [{}],
                       [{}]],
                print_grid=True, shared_xaxes=True, horizontal_spacing=0.05, vertical_spacing=0)

        config = dict({'scrollZoom': True})
        fig_index.update_layout(height=hgt * .75, width=wd)  # title_text="Equity Data")
        fig_index.update_layout(paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
        fig_index.update_layout(margin=dict(r=2, t=2, b=2, l=2))
        fig_index.update_xaxes(rangeslider_visible=False)
        fig_index.update_xaxes(showline=True, linewidth=2, linecolor='black')
        # fig_index.update_yaxes(range=[0, 100], row=4, col=1)
        fig_index.update_yaxes(mirror=True, row=1, col=1)
        # fig_index.update_layout(xaxis6_rangeslider_visible=True, xaxis6_rangeslider_thickness=0.05)
        fig_index.update_yaxes(mirror="ticks", side='right')
        fig_index.update_layout(
                dragmode='drawline',
                newshape_line_color='cyan'
            )
        fig_index.update_layout(showlegend=False)
        fig_index.update_layout(
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

        # include Equity candlestick without rangeselector
        fig_index.add_trace(go.Candlestick(x=df_index['Index_Date'],
                                         open=df_index['Open_Index_Value'], high=df_index['High_Index_Value'],
                                         low=df_index['Low_Index_Value'], close=df_index['Closing_Index_Value'], name='Price'),
                          row=1, col=1)
        fig_index.add_trace(
                go.Scatter(x=df_opt_maxce['TIMESTAMP'], y=df_opt_maxce['STRIKE_PR'], mode='lines+markers',
                           name='Resistance'),
                row=1, col=1)
        fig_index.add_trace(
                go.Scatter(x=df_opt_maxpe['TIMESTAMP'], y=df_opt_maxpe['STRIKE_PR'], mode='lines+markers',
                           name='Support'),
                row=1, col=1)
        fig_index.add_trace(
                go.Scatter(x=df_opt_ce_ind['TIMESTAMP'], y=df_opt_ce_ind['indicator_sr_price'], mode='markers',
                           marker=dict(size=10, symbol=5, color='green'), name='CE Buildup'),
                row=1, col=1)
        fig_index.add_trace(
                go.Scatter(x=df_opt_pe_ind['TIMESTAMP'], y=df_opt_pe_ind['indicator_sr_price'], mode='markers',
                           marker=dict(size=10, symbol=6, color='red'), name='PE Buildup'),
                row=1, col=1)
        # Add 5 SMA to Closing Price in OHCL Plot
        fig_index.add_trace(go.Scatter(x=df_index['Index_Date'], y=df_index.Closing_Index_Value.rolling(5).mean(), name='5SMA Close'),
                          row=1, col=1)
        # Add 20 SMA to Closing Price in OHCL Plot
        fig_index.add_trace(go.Scatter(x=df_index['Index_Date'], y=df_index.Closing_Index_Value.rolling(20).mean(), name='20SMA Close'),
                          row=1, col=1)
        # Add Volume as Subplot
        fig_index.add_trace(
                go.Bar(x=df_index['Index_Date'], y=df_index['Volume'], name='Volume', marker_color=df_index['color']),
                row=3, col=1)
        # Add 20 SMA to Volume Subplot
        fig_index.add_trace(
                go.Scatter(x=df_index['Index_Date'], y=df_index.Volume.rolling(20).mean(), name='20SMA Vol'),
                row=3, col=1)
        # Add COI to Subplot
        fig_index.add_trace(
                go.Scatter(x=df_fut_coi['TIMESTAMP'], y=df_fut_coi['OPEN_INT'], name='COI'),
                row=4, col=1)
        # edit axis labels
        fig_index['layout']['yaxis']['title'] = 'Equity OHCL'
        fig_index['layout']['yaxis2']['title'] = 'Volume'
        fig_index['layout']['yaxis3']['title'] = 'COI'

    else:
        df_index = index_data[(index_data.Index_Name == dropdown_value)]
        df_index['Volume'] = df_index.Volume.astype(float)
        df_index['Points_Change'] = df_index.Points_Change.astype(float)
        df_index['color'] = np.where(df_index["Points_Change"] <= 0, 'red', 'green')
        df_index['Turnover']=df_index['Turnover_(Rs._Cr.)']
        df_index['Turnover'] = df_index.Turnover.astype(float)
        df_index['PE']=df_index['P/E']
        df_index['PE'] = df_index.PE.astype(float)
        df_index['PB']=df_index['P/B']
        df_index['PB'] = df_index.PB.astype(float)

        # Draw FNO Plot
        # ____________________________________________________________

        fig_index = make_subplots(
            rows=6, cols=1,
            row_heights=[0.2, 0.2, 0.15, 0.15, 0.15, 0.15],
            specs=[[{"rowspan": 2, "colspan": 1}],
                   [None],
                   [{}],
                   [{}],
                   [{}],
                   [{}]],
            print_grid=True, shared_xaxes=True, horizontal_spacing=0.05, vertical_spacing=0)

        fig_index.update_layout(height=hgt * .75, width=wd)  # title_text="Equity Data")
        fig_index.update_layout(paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
        fig_index.update_layout(margin=dict(r=2, t=2, b=2, l=2))
        fig_index.update_xaxes(rangeslider_visible=False)
        fig_index.update_xaxes(showline=True, linewidth=2, linecolor='black')
        #fig_index.update_yaxes(range=[0, 100], row=5, col=1)
        #fig_index.update_yaxes(range=[0, 10], row=6, col=1)
        fig_index.update_yaxes(mirror="ticks", side='right')
        # fig_index.update_layout(xaxis4_rangeslider_visible=True, xaxis4_rangeslider_thickness=0.05)
        fig_index.update_layout(
            dragmode='drawline',
            newshape_line_color='cyan'
        )
        fig_index.update_layout(showlegend=False)
        fig_index.update_layout(
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

        # include Equity candlestick without rangeselector
        fig_index.add_trace(go.Candlestick(x=df_index['Index_Date'],
                                     open=df_index['Open_Index_Value'], high=df_index['High_Index_Value'],
                                     low=df_index['Low_Index_Value'], close=df_index['Closing_Index_Value'], name='Price'),
                      row=1, col=1)
        # Add 5 SMA to Closing Price in OHCL Plot
        fig_index.add_trace(go.Scatter(x=df_index['Index_Date'], y=df_index.Closing_Index_Value.rolling(5).mean(), name='5SMA Close'),
                      row=1, col=1)
        # Add 20 SMA to Closing Price in OHCL Plot
        fig_index.add_trace(go.Scatter(x=df_index['Index_Date'], y=df_index.Closing_Index_Value.rolling(20).mean(), name='20SMA Close'),
                      row=1, col=1)
        # Add Volume as Subplot
        fig_index.add_trace(
            go.Bar(x=df_index['Index_Date'], y=df_index['Volume'], name='Volume', marker_color=df_index['color']),
            row=3, col=1)
        # Add 20 SMA to Volume Subplot
        fig_index.add_trace(go.Scatter(x=df_index['Index_Date'], y=df_index.Volume.rolling(20).mean(), name='20SMA Vol'),
                      row=3, col=1)
        fig_index.add_trace(
            go.Bar(x=df_index['Index_Date'], y=df_index['Turnover'], name='Turnover'),
            row=4, col=1)
        # Add QT as Subplot
        fig_index.add_trace(
            go.Scatter(x=df_index['Index_Date'], y=df_index['PE'], name='P/E'),
                      row=5, col=1)
        fig_index.add_trace(
            go.Scatter(x=df_index['Index_Date'], y=df_index['PB'], name='P/B'),
            row=6, col=1)

        # edit axis labels
        fig_index['layout']['yaxis']['title'] = 'Equity OHCL'
        fig_index['layout']['yaxis2']['title'] = 'Volume'
        fig_index['layout']['yaxis3']['title'] = 'Turnover'
        fig_index['layout']['yaxis4']['title'] = 'P/E'
        fig_index['layout']['yaxis5']['title'] = 'P/B'

    return fig_index


