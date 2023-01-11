import dash
# Code from: https://github.com/plotly/dash-labs/tree/main/docs/demos/multi_page_example1
dash.register_page(__name__)

from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from screeninfo import get_monitors
import numpy as np
from nsepython import *

# Get Screen Resolution
for m in get_monitors():
    hgt = int(m.height)
    wd = int(m.width)

cur_dir = os.getcwd()
print(cur_dir)

cur_master_dir = cur_dir + r"\Master_Files"
cur_fo_dir = cur_dir + r"\dumps\bhavcopy\nse\eod_fo"
cur_support_dir = cur_dir + r"\Support_Files"

equity_folder_path = os.path.join(cur_dir, 'Script_Files_Equity')
del_folder_path = os.path.join(cur_dir, 'Script_Files_Delivery')
fut_folder_path = os.path.join(cur_dir, 'Script_Files_Future')
ce_folder_path = os.path.join(cur_dir, 'Script_Files_CE')
pe_folder_path = os.path.join(cur_dir, 'Script_Files_PE')
index_folder_path = os.path.join(cur_dir, 'Script_Files_Index')

lot_size_list = pd.read_csv(cur_support_dir + r"\Lot_Size_Filtered.csv")
watchlist = pd.read_csv(cur_support_dir + r"\WL_ALL.csv")
dropdown_opt_list = pd.read_csv(cur_support_dir + r"\Dropdown_options.csv")
Expiry_Date_Monthly = pd.read_csv(cur_support_dir + r"/Expiry_Date_Monthly.csv")



# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'height': '700px',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

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
                        id='dropdown_opt',
                        options=[{'label': x, 'value': x}
                                 for x in dropdown_opt_list.DRP_OPT],
                        value=dropdown_opt_list.DRP_OPT[0],  # default value
                        multi=False
                    ),
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id='dropdown',
                        options=[{'label': x, 'value': x}
                                 for x in watchlist.Symbol],
                        value='TATAMOTORS',  # default value
                    ),
                    dcc.Graph(id='graph_1', config={'displayModeBar': False})
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id='dropdown_exp',
                        options=[{'label': x, 'value': x}
                                 for x in Expiry_Date_Monthly.Monthly],
                        value=Expiry_Date_Monthly.Monthly[0],  # default value
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
    ]
)

content_second_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_31', config=dict({'scrollZoom': True})), md=12,
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
    Output('dropdown', 'options'),
    [Input('dropdown_opt', 'value')])
def update_dropdown_list(dropdown_item_value):
    dir_wl = cur_support_dir + '/' + dropdown_item_value + '.csv'
    wl = pd.read_csv(dir_wl)
    options = [{'label': x, 'value': x}
               for x in wl['Symbol']]
    return options

@callback(
    Output('dropdown', 'value'),
    Input('submit_button', 'n_clicks'),
    Input('submit_button_next', 'n_clicks'),
    Input('dropdown', 'value'),
    Input('dropdown_opt', 'value')
)
def update_dropdown(n_clicks, n_clicks_next, dropdown_value, dropdown_opt_val):

    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == 'submit_button':
        dropdown_opt_val = dropdown_opt_val+str('.csv')
        wl = pd.read_csv(os.path.join(cur_support_dir, dropdown_opt_val) )
        cur_position = wl[wl['Symbol'] == dropdown_value].index[0]
        cur_position = int(cur_position)
        print(cur_position)
        value_analysis = wl['Symbol'].iloc[cur_position - 1]

    elif trigger_id == 'submit_button_next':
        dropdown_opt_val = dropdown_opt_val + str('.csv')
        wl = pd.read_csv(os.path.join(cur_support_dir, dropdown_opt_val) )
        cur_position = wl[wl['Symbol'] == dropdown_value].index[0]
        cur_position = int(cur_position)
        print(cur_position)
        value_analysis = wl['Symbol'].iloc[cur_position + 1]
    else:
        value_analysis = dropdown_value
    return value_analysis



@callback(
    Output('graph_1', 'figure'),
    [Input('dropdown_exp', 'value'),
     Input('dropdown', 'value')])
def update_graph_1(dropdown_exp_value, dropdown_value):
    print(dropdown_value)
    print(dropdown_exp_value)

    df_eq_g1 = pd.read_csv(os.path.join(equity_folder_path, (dropdown_value + ".csv")))  # Fetch Equity master Data and filter by Stock Name
    spot_price = df_eq_g1['CLOSE'].iloc[-1]  # Find the Spot price as per last Closing
    prev_price = df_eq_g1['CLOSE'].iloc[-2]  # Find the Previous Day price as per Closing

    fig_g1 = go.Figure()
    fig_g1.add_trace(go.Indicator(
        mode="number+delta",
        value=spot_price,
        delta={'reference': prev_price, 'relative': True},
    ))
    fig_g1.update_traces(delta_font={'size': 15})
    fig_g1.update_traces(number_font_size=15, selector=dict(type='indicator'))
    fig_g1.update_traces(delta_position='left', selector=dict(type='indicator'))
    fig_g1.update_traces(number_prefix='Close ', selector=dict(type='indicator'))
    fig_g1.update_traces(align='left', selector=dict(type='indicator'))
    fig_g1.update_layout(height=20, width=150)
    fig_g1.update_layout(margin_l=0)
    return fig_g1


@callback(
    Output('graph_31', 'figure'),
    [Input('dropdown_exp', 'value'),
     Input('dropdown', 'value'),
     Input('dropdown_opt', 'value')])
def update_graph_31(dropdown_exp_value, dropdown_value, dropdown_opt_value):
    print("Hi")
    print(dropdown_value)
    print(dropdown_exp_value)
    print(dropdown_opt_value)

    if dropdown_opt_value == "WL_FNO" or dropdown_opt_value == "WL_10MVOL" or dropdown_opt_value == "WL_10MVOL_LTD":
        eq_data = pd.read_csv(os.path.join(equity_folder_path, (dropdown_value + ".csv")))
        del_data = pd.read_csv(os.path.join(del_folder_path, (dropdown_value + ".csv")))
        fut_data = pd.read_csv(os.path.join(fut_folder_path, (dropdown_value + ".csv")))
        opt_ce_data=pd.read_csv(os.path.join(ce_folder_path, (dropdown_value + ".csv")))
        opt_pe_data=pd.read_csv(os.path.join(pe_folder_path, (dropdown_value + ".csv")))

        df_eq = eq_data[eq_data.SYMBOL == dropdown_value]
        df_eq['color'] = np.where(df_eq["CLOSE"] <= df_eq["PREVCLOSE"], 'red', 'green')
        df_del = del_data[del_data.SYMBOL == dropdown_value]

        df_fut = fut_data[(fut_data.EXPIRY_DT == dropdown_exp_value) & (fut_data.SYMBOL == dropdown_value)]
        df_fut['color'] = np.where(df_fut["CLOSE"] <= df_fut["CLOSE"].shift(1), 'red', 'green')

        df_fut_all = fut_data[(fut_data.SYMBOL == dropdown_value)]
        df_fut_coi = df_fut_all.groupby('TIMESTAMP').agg('sum')
        df_fut_coi['color'] = np.where(df_fut_coi["CHG_IN_OI"] < 0, 'red', 'green')
        df_fut_coi.reset_index(inplace=True)

        df_eq['qt'] = df_eq.TOTTRDQTY / df_eq.TOTALTRADES
        df_eq['qtco0321'] = np.where(df_eq['qt'].rolling(5).mean() > df_eq['qt'].rolling(20).mean(),
                                     df_eq['qt'], '')
        df_eq['qtco0321col'] = np.where(df_eq['qt'].rolling(5).mean() > df_eq['qt'].rolling(20).mean(),
                                        'green', 'red')

        df_opt_ce = opt_ce_data[(opt_ce_data.EXPIRY_DT == dropdown_exp_value)]
        df_opt_maxce = df_opt_ce.loc[df_opt_ce.groupby('TIMESTAMP')['OPEN_INT'].agg(pd.Series.idxmax)]
        df_opt_pe = opt_pe_data[(opt_pe_data.EXPIRY_DT == dropdown_exp_value)]
        df_opt_maxpe = df_opt_pe.loc[df_opt_pe.groupby('TIMESTAMP')['OPEN_INT'].agg(pd.Series.idxmax)]

        lot_size = lot_size_list[lot_size_list.SYMBOL == dropdown_value]
        lot = int(lot_size["LOT_SIZE"].iloc[0])

        df_opt_ce_ind = opt_ce_data[(opt_ce_data.EXPIRY_DT == dropdown_exp_value)]
        df_opt_ce_ind['indicator_sr_price'] = np.where(df_opt_ce_ind['CONTRACTS'] * lot > 10000000,
                                                       df_opt_ce_ind['STRIKE_PR'], '')
        # df_opt_ce_ind.to_csv(cur_dir + "/df_opt_ce_ind.csv", index=False)
        df_opt_ce_ind['indicator_col'] = np.where((df_opt_ce_ind['CONTRACTS'] * lot > 10000000) &
                                                  (df_opt_ce_ind['CHG_IN_OI'] < 0), 'green', 'red')
        df_opt_pe_ind = opt_pe_data[(opt_pe_data.EXPIRY_DT == dropdown_exp_value)]
        df_opt_pe_ind['indicator_sr_price'] = np.where(df_opt_pe_ind['CONTRACTS'] * lot > 10000000,
                                                       df_opt_pe_ind['STRIKE_PR'], '')
        df_opt_pe_ind['indicator_col'] = np.where((df_opt_pe_ind['CONTRACTS'] * lot > 10000000) &
                                                  (df_opt_pe_ind['CHG_IN_OI'] < 0), 'green', 'red')

        try:
            df_sl_timestamp = df_opt_ce_ind[df_opt_ce_ind.indicator_sr_price != '']
            df_sl_timestamp = df_sl_timestamp.iloc[0:1]
            df_sl_timestamp = df_sl_timestamp.reset_index()
            df_eq_sl = eq_data[
                (eq_data.TIMESTAMP == str(df_sl_timestamp['TIMESTAMP'][0])) & (eq_data.SYMBOL == dropdown_value)]
            df_eq_sl = df_eq_sl.reset_index()
            df_eq['ENTRY'] = np.where(df_eq['TIMESTAMP'] >= str(df_sl_timestamp['TIMESTAMP'][0]),
                                      float(df_eq_sl['HIGH'][0]), '')
            df_eq['SL'] = np.where(df_eq['TIMESTAMP'] >= str(df_sl_timestamp['TIMESTAMP'][0]),
                                      float(df_eq_sl['LOW'][0]), '')
        except:
            df_eq['ENTRY'] = np.where(df_eq['TIMESTAMP'] >= str(df_eq['TIMESTAMP'].iloc[-1]),
                                      float(df_eq['HIGH'].iloc[-1]), '')
            df_eq['SL'] = np.where(df_eq['TIMESTAMP'] >= str(df_eq['TIMESTAMP'].iloc[-1]),
                                      float(df_eq['LOW'].iloc[-1]), '')

            # Draw FNO Plot for STOCKS
            # ____________________________________________________________

        fig = make_subplots(
            rows=7, cols=1,
            row_heights=[0.25, 0.25, 0.1, 0.1, 0.1, 0.1, 0.1],
            specs=[[{"rowspan": 2, "colspan": 1}],
                   [None],
                   [{}],
                   [{}],
                   [{}],
                   [{}],
                   [{}]],
            print_grid=True, shared_xaxes=True, horizontal_spacing=0.05, vertical_spacing=0)

        config = dict({'scrollZoom': True})
        fig.update_layout(height=hgt * .75, width=wd)  # title_text="Equity Data")
        fig.update_layout(paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
        fig.update_layout(margin=dict(r=2, t=2, b=2, l=2))
        #fig.update_xaxes(rangeslider_visible=False)
        fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(range=[0, 100], row=4, col=1)
        fig.update_yaxes(mirror=True, row=1, col=1)
        # fig.update_layout(xaxis6_rangeslider_visible=True, xaxis6_rangeslider_thickness=0.05)
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

        # include Equity candlestick without rangeselector
        fig.add_trace(go.Candlestick(x=df_eq['TIMESTAMP'],
                                     open=df_eq['OPEN'], high=df_eq['HIGH'],
                                     low=df_eq['LOW'], close=df_eq['CLOSE'], name='Price'),
                      row=1, col=1)
        fig.add_trace(
            go.Scatter(x=df_opt_maxce['TIMESTAMP'], y=df_opt_maxce['STRIKE_PR'], mode='lines+markers',
                       name='Resistance'),
            row=1, col=1)
        fig.add_trace(
            go.Scatter(x=df_opt_maxpe['TIMESTAMP'], y=df_opt_maxpe['STRIKE_PR'], mode='lines+markers',
                       name='Support'),
            row=1, col=1)
        fig.add_trace(
            go.Scatter(x=df_opt_ce_ind['TIMESTAMP'], y=df_opt_ce_ind['indicator_sr_price'], mode='markers',
                       marker=dict(size=10, symbol=5, color=df_opt_ce_ind['indicator_col']), name='CE Buildup'),
            row=1, col=1)
        fig.add_trace(
            go.Scatter(x=df_opt_pe_ind['TIMESTAMP'], y=df_opt_pe_ind['indicator_sr_price'], mode='markers',
                       marker=dict(size=10, symbol=6, color=df_opt_pe_ind['indicator_col']), name='PE Buildup'),
            row=1, col=1)
        # Add 5 SMA to Closing Price in OHCL Plot
        fig.add_trace(go.Scatter(x=df_eq['TIMESTAMP'], y=df_eq.CLOSE.rolling(5).mean(), name='5SMA Close'),
                      row=1, col=1)
        # Add 20 SMA to Closing Price in OHCL Plot
        fig.add_trace(go.Scatter(x=df_eq['TIMESTAMP'], y=df_eq.CLOSE.rolling(20).mean(), name='20SMA Close'),
                      row=1, col=1)
        # Add ENTRY Lines
        fig.add_trace(
            go.Scatter(x=df_eq['TIMESTAMP'], y=df_eq['ENTRY'], mode='lines', name='Entry', marker_color='black'),
            row=1, col=1)
        # Add SL Lines
        fig.add_trace(
            go.Scatter(x=df_eq['TIMESTAMP'], y=df_eq['SL'], mode='lines', name='SL', marker_color='black'),
            row=1, col=1)
        # Add Volume as Subplot
        fig.add_trace(
            go.Bar(x=df_eq['TIMESTAMP'], y=df_eq['TOTTRDQTY'], name='Volume', marker_color=df_eq['color']),
            row=3, col=1)
        # Add 20 SMA to Volume Subplot
        fig.add_trace(go.Scatter(x=df_eq['TIMESTAMP'], y=df_eq.TOTTRDQTY.rolling(20).mean(), name='20SMA Vol'),
                      row=3, col=1)
        # Add Delivery Quantity to Volume Subplot
        fig.add_trace(
            go.Scatter(x=df_del['TIMESTAMP'], y=df_del['del_qty'], mode='lines+markers', name='Delivery Q'),
            row=3, col=1)
        # Add Delivery% as Subplot
        fig.add_trace(
            go.Scatter(x=df_del['TIMESTAMP'], y=df_del['del_percent'],
                       line=dict(color='firebrick', width=2, dash='dot'),
                       name='Del%'),
            row=4, col=1)
        # Add QT as Subplot
        fig.add_trace(go.Scatter(x=df_eq['TIMESTAMP'], y=df_eq['qt'], name='Q/T'),
                      row=5, col=1)
        # Add 1SD Mark to Qt Subplot
        fig.add_trace(
            go.Scatter(x=df_eq['TIMESTAMP'], y=(df_eq.qt.rolling(20).mean() + df_eq.qt.rolling(20).std()),
                       name='1SD Q/T'),
            row=5, col=1)
        # QT 3-21 Crossover Indicator
        fig.add_trace(
            go.Scatter(x=df_eq['TIMESTAMP'], y=df_eq['qtco0321'], mode='markers',
                       marker=dict(size=10, symbol=5, color=df_eq['qtco0321col']), name='QT Ind'),
            row=5, col=1)
        # Add COI to Subplot
        fig.add_trace(
            go.Scatter(x=df_fut_coi['TIMESTAMP'], y=df_fut_coi['OPEN_INT'], name='COI'),
            row=6, col=1)
        # Add Delivery Quantity Change Subplot
        fig.add_trace(
            go.Bar(x=df_del['TIMESTAMP'], y=df_del['del_qty'], name='Del Qty', marker_color='green'),
            row=7, col=1)

        # edit axis labels
        fig['layout']['yaxis']['title'] = 'Equity OHCL'
        fig['layout']['yaxis2']['title'] = 'Volume'
        fig['layout']['yaxis3']['title'] = 'Del%'
        fig['layout']['yaxis4']['title'] = 'Q/T'
        fig['layout']['yaxis5']['title'] = 'COI'
        fig['layout']['yaxis6']['title'] = 'Del Q'
    else:
        eq_data = pd.read_csv(os.path.join(equity_folder_path, (dropdown_value + ".csv")))
        df_eq = eq_data
        #df_eq['color'] = np.where(df_eq["CLOSE"] <= df_eq["PREVCLOSE"], 'red', 'green')
        df_eq.loc[:,('color')] = np.where(df_eq.loc[:,('CLOSE')] <= df_eq.loc[:,('PREVCLOSE')], 'red', 'green')
        del_data = pd.read_csv(os.path.join(del_folder_path, (dropdown_value + ".csv")))
        df_del = del_data
        df_eq['qt'] = df_eq.TOTTRDQTY / df_eq.TOTALTRADES
        df_eq['qtco0321'] = np.where(df_eq['qt'].rolling(5).mean() > df_eq['qt'].rolling(20).mean(),
                                     df_eq['qt'], '')
        df_eq['qtco0321col'] = np.where(df_eq['qt'].rolling(5).mean() > df_eq['qt'].rolling(20).mean(),
                                        'green', 'red')
        df_eq['MA_diff']=df_eq['CLOSE'].rolling(5).mean()-df_eq['CLOSE'].rolling(20).mean()
        # Draw FNO Plot
        # ____________________________________________________________

        fig = make_subplots(
            rows=6, cols=1,
            row_heights=[0.2, 0.2, 0.15, 0.15, 0.15, 0.15],
            specs=[[{"rowspan": 2, "colspan": 1}],
                   [None],
                   [{}],
                   [{}],
                   [{}],
                   [{}]],
            print_grid=True, shared_xaxes=True, horizontal_spacing=0.05, vertical_spacing=0)

        fig.update_layout(height=hgt * .75, width=wd)  # title_text="Equity Data")
        fig.update_layout(paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
        fig.update_layout(margin=dict(r=2, t=2, b=2, l=2))
        fig.update_xaxes(rangeslider_visible=False)
        fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(range=[0, 100], row=4, col=1)
        fig.update_yaxes(mirror="ticks", side='right')
        # fig.update_layout(xaxis4_rangeslider_visible=True, xaxis4_rangeslider_thickness=0.05)
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

        # include Equity candlestick without rangeselector
        fig.add_trace(go.Candlestick(x=df_eq['TIMESTAMP'],
                                     open=df_eq['OPEN'], high=df_eq['HIGH'],
                                     low=df_eq['LOW'], close=df_eq['CLOSE'], name='Price'),
                      row=1, col=1)
        # Add 5 SMA to Closing Price in OHCL Plot
        fig.add_trace(go.Scatter(x=df_eq['TIMESTAMP'], y=df_eq.CLOSE.rolling(5).mean(), name='5SMA Close'),
                      row=1, col=1)
        # Add 20 SMA to Closing Price in OHCL Plot
        fig.add_trace(go.Scatter(x=df_eq['TIMESTAMP'], y=df_eq.CLOSE.rolling(20).mean(), name='20SMA Close'),
                      row=1, col=1)
        # Add Volume as Subplot
        fig.add_trace(
            go.Bar(x=df_eq['TIMESTAMP'], y=df_eq['TOTTRDQTY'], name='Volume', marker_color=df_eq['color']),
            row=3, col=1)
        # Add 20 SMA to Volume Subplot
        fig.add_trace(go.Scatter(x=df_eq['TIMESTAMP'], y=df_eq.TOTTRDQTY.rolling(20).mean(), name='20SMA Vol'),
                      row=3, col=1)
        # Add Delivery Quantity to Volume Subplot
        fig.add_trace(
            go.Scatter(x=df_del['TIMESTAMP'], y=df_del['del_qty'], mode='lines+markers', name='Delivery Q'),
            row=3, col=1)
        # Add Delivery% as Subplot
        fig.add_trace(
            go.Scatter(x=df_del['TIMESTAMP'], y=df_del['del_percent'],
                       line=dict(color='firebrick', width=2, dash='dot'),
                       name='Del%'),
            row=4, col=1)
        # Add QT as Subplot
        fig.add_trace(go.Scatter(x=df_eq['TIMESTAMP'], y=df_eq['qt'], name='Q/T'),
                      row=5, col=1)
        # Add 1SD Mark to Qt Subplot
        fig.add_trace(
            go.Scatter(x=df_eq['TIMESTAMP'], y=(df_eq.qt.rolling(20).mean() + df_eq.qt.rolling(20).std()),
                       name='1SD Q/T'),
            row=5, col=1)
        # QT 3-21 Crossover Indicator
        fig.add_trace(
            go.Scatter(x=df_eq['TIMESTAMP'], y=df_eq['qtco0321'], mode='markers',
                       marker=dict(size=10, symbol=5, color=df_eq['qtco0321col']), name='QT Ind'),
            row=5, col=1)
        # Add Delivery Quantity Change Subplot
        fig.add_trace(
            go.Bar(x=df_del['TIMESTAMP'], y=df_del['del_qty'], name='Del Qty', marker_color='green'),
            row=6, col=1)
        # Voltility Graph
        #fig.add_trace(
        #    go.Bar(x=df_eq['TIMESTAMP'], y=df_eq['MA_diff'], name='Volatility', marker_color=df_eq['qtco0321col']),
        #    row=6, col=1)

        # edit axis labels
        fig['layout']['yaxis']['title'] = 'Equity OHCL'
        fig['layout']['yaxis2']['title'] = 'Volume'
        fig['layout']['yaxis3']['title'] = 'Del%'
        fig['layout']['yaxis4']['title'] = 'Q/T'
        fig['layout']['yaxis5']['title'] = 'Del Q'

    return fig
