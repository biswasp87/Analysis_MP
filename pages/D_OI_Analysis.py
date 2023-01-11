import dash
# Code from: https://github.com/plotly/dash-labs/tree/main/docs/demos/multi_page_example1
dash.register_page(__name__)

from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from screeninfo import get_monitors
import numpy as np
from nsepython import *
from dash import dash_table as dt



# Get Screen Resolution
for m in get_monitors():
    hgt = int(m.height)
    wd = int(m.width)

# Declaring Folder Paths
OI_cur_dir = os.getcwd()
OI_cur_master_dir = OI_cur_dir + r"\Master_Files"
OI_cur_support_dir = OI_cur_dir + r"\Support_Files"
OI_cur_fo_dir = OI_cur_dir + r"\dumps\bhavcopy\nse\eod_fo"
Expiry_Date_Monthly = pd.read_csv(OI_cur_support_dir + r"/Expiry_Date_Monthly.csv")

# Assessing, Sorting & Filtering the Future Master File

OI_dir_name_fo = OI_cur_master_dir + r"\master_fo.csv"
OI_fut_data = pd.read_csv(OI_dir_name_fo)
OI_fut_data['TIMESTAMP'] = pd.to_datetime(OI_fut_data['TIMESTAMP'])
OI_fut_data = OI_fut_data.sort_values(by='TIMESTAMP', ascending=True)
OI_fut_data['index'] = OI_fut_data.reset_index().index

# Assessing, Sorting & Filtering the Equity Master File

OI_dir_name_eq = OI_cur_master_dir + r"\master_eq.csv"  # Home desktop
OI_eq_data = pd.read_csv(OI_dir_name_eq)
OI_eq_data['TIMESTAMP'] = pd.to_datetime(OI_eq_data['TIMESTAMP'])
OI_eq_data = OI_eq_data.sort_values(by='TIMESTAMP', ascending=True)
OI_eq_data.drop(OI_eq_data.iloc[:, 6:9], inplace = True, axis=1) # Dropping the unnecessary Columns
OI_eq_data.drop(OI_eq_data.iloc[:, 8:11], inplace = True, axis=1) # Dropping the unnecessary Columns
OI_eq_data = OI_eq_data[['SYMBOL', 'TIMESTAMP', 'OPEN', 'HIGH', 'LOW', 'CLOSE']] # Rearranging the Columns

# Assessing, Sorting & Filtering the Index Master File

OI_dir_name_index = OI_cur_master_dir + r"\master_indices.csv"  # Home desktop
OI_index_data = pd.read_csv(OI_dir_name_index, parse_dates=['Index_Date'], dayfirst=True)
OI_index_data = OI_index_data.sort_values(by='Index_Date', ascending=True)
OI_index_data['index'] = OI_index_data.reset_index().index
OI_index_data = OI_index_data[(OI_index_data.Index_Name == 'Nifty 50')|(OI_index_data.Index_Name == 'Nifty Bank')]
OI_index_data.drop(OI_index_data.iloc[:, 6:14], inplace = True, axis=1)
OI_index_data = OI_index_data.rename(columns={'Index_Name': 'SYMBOL',
                                              'Index_Date': 'TIMESTAMP',
                                              'Open_Index_Value': 'OPEN',
                                              'High_Index_Value': 'HIGH',
                                              'Low_Index_Value': 'LOW',
                                              'Closing_Index_Value': 'CLOSE'})

# Replacing values in the Column to make it similar in both the files
OI_index_data = OI_index_data.replace(to_replace='Nifty 50', value='NIFTY')
OI_index_data = OI_index_data.replace(to_replace='Nifty Bank', value='BANKNIFTY')
OI_index_data['OPEN'] = OI_index_data['OPEN'].astype(float)
OI_index_data['CLOSE'] = OI_index_data['CLOSE'].astype(float)

# Appending(Merging EQ Data & Indices Data one below the another)

# Master_Spot_Data = OI_eq_data.append(OI_index_data, ignore_index=True)
Master_Spot_Data = pd.concat([OI_eq_data, OI_index_data], ignore_index=True)

# Filtering the Future DataFrame into separate DataFrames of Each Expiry Month

OI_fut_data_cur = OI_fut_data[OI_fut_data.EXPIRY_DT == Expiry_Date_Monthly.Monthly[0]]
OI_fut_data_near = OI_fut_data[OI_fut_data.EXPIRY_DT == Expiry_Date_Monthly.Monthly[1]]
OI_fut_data_far = OI_fut_data[OI_fut_data.EXPIRY_DT == Expiry_Date_Monthly.Monthly[2]]


# Renaming the Columns for avoiding similar names in Merged DataFrame
OI_fut_data_cur = OI_fut_data_cur.rename(columns={col: 'Cur_' + col
                        for col in OI_fut_data_cur.columns if col not in ['TIMESTAMP', 'SYMBOL']})
OI_fut_data_near = OI_fut_data_near.rename(columns={col: 'Near_' + col
                        for col in OI_fut_data_near.columns if col not in ['TIMESTAMP', 'SYMBOL']})
OI_fut_data_far = OI_fut_data_far.rename(columns={col: 'Far_' + col
                        for col in OI_fut_data_far.columns if col not in ['TIMESTAMP', 'SYMBOL']})

# Merging the Equity DataFrame with Current, Near & Far Month DataFrame
OI_fut_data_cur_near = pd.merge(OI_fut_data_cur, OI_fut_data_near, on=['TIMESTAMP', 'SYMBOL'])
OI_fut_data_cur_near_far = pd.merge(OI_fut_data_cur_near, OI_fut_data_far, on=['TIMESTAMP', 'SYMBOL'])
OI_fut_master_data = pd.merge(Master_Spot_Data, OI_fut_data_cur_near_far, on=['TIMESTAMP', 'SYMBOL'])

# -------Calculating the required filed----------

OI_fut_master_data['COI'] = OI_fut_master_data['Cur_OPEN_INT'] + OI_fut_master_data['Near_OPEN_INT'] + OI_fut_master_data['Far_OPEN_INT']
OI_fut_master_data['COI Chng'] = OI_fut_master_data['Cur_CHG_IN_OI'] + OI_fut_master_data['Near_CHG_IN_OI'] + OI_fut_master_data['Far_CHG_IN_OI']
OI_fut_master_data["Spot %"] = (OI_fut_master_data['CLOSE']-OI_fut_master_data['OPEN']) / OI_fut_master_data['OPEN']*100
OI_fut_master_data["COI %"] = OI_fut_master_data['COI Chng']/(OI_fut_master_data['COI']-OI_fut_master_data['COI Chng'])*100

OI_fut_master_data["BU"] = np.where((OI_fut_master_data['Spot %'] > 0) & (OI_fut_master_data["COI %"] > 0), 'LB',
                                    np.where((OI_fut_master_data['Spot %'] > 0) & (OI_fut_master_data["COI %"] < 0), 'SC',
                                             np.where((OI_fut_master_data['Spot %'] < 0) & (OI_fut_master_data["COI %"] > 0), 'SB',
                                                      np.where((OI_fut_master_data['Spot %'] < 0) & (OI_fut_master_data["COI %"] < 0), 'LW', ''))))

# Calculating the Current month data fields
OI_fut_master_data["Cur %"] = (OI_fut_master_data['Cur_CLOSE']-OI_fut_master_data['Cur_OPEN']) / \
                                                                        OI_fut_master_data['Cur_OPEN']*100
OI_fut_master_data["Cur OI %"] = OI_fut_master_data['Cur_CHG_IN_OI'] / (OI_fut_master_data['Cur_OPEN_INT'] -
                                                                        OI_fut_master_data['Cur_CHG_IN_OI'])*100
OI_fut_master_data["Cur BU"] = np.where((OI_fut_master_data['Cur %'] > 0) & (OI_fut_master_data["Cur OI %"] > 0), 'LB',
                                    np.where((OI_fut_master_data['Cur %'] > 0) & (OI_fut_master_data["Cur OI %"] < 0), 'SC',
                                             np.where((OI_fut_master_data['Cur %'] < 0) & (OI_fut_master_data["Cur OI %"] > 0), 'SB',
                                                      np.where((OI_fut_master_data['Cur %'] < 0) & (OI_fut_master_data["Cur OI %"] < 0), 'LW', ''))))


# Calculating the Near month data fields
OI_fut_master_data["Near %"] = (OI_fut_master_data['Near_CLOSE']-OI_fut_master_data['Near_OPEN']) / \
                                                                        OI_fut_master_data['Near_OPEN']*100
OI_fut_master_data["Near OI %"] = OI_fut_master_data['Near_CHG_IN_OI'] / (OI_fut_master_data['Near_OPEN_INT'] -
                                                                        OI_fut_master_data['Near_CHG_IN_OI'])*100
OI_fut_master_data["Near BU"] = np.where((OI_fut_master_data['Near %'] > 0) & (OI_fut_master_data["Near OI %"] > 0), 'LB',
                                    np.where((OI_fut_master_data['Near %'] > 0) & (OI_fut_master_data["Near OI %"] < 0), 'SC',
                                             np.where((OI_fut_master_data['Near %'] < 0) & (OI_fut_master_data["Near OI %"] > 0), 'SB',
                                                      np.where((OI_fut_master_data['Near %'] < 0) & (OI_fut_master_data["Near OI %"] < 0), 'LW', ''))))

# Calculating the Far month data fields
OI_fut_master_data["Far %"] = (OI_fut_master_data['Far_CLOSE']-OI_fut_master_data['Far_OPEN']) / \
                                                                        OI_fut_master_data['Far_OPEN']*100
OI_fut_master_data["Far OI %"] = OI_fut_master_data['Far_CHG_IN_OI'] / (OI_fut_master_data['Far_OPEN_INT'] -
                                                                        OI_fut_master_data['Far_CHG_IN_OI'])*100
OI_fut_master_data["Far BU"] = np.where((OI_fut_master_data['Far %'] > 0) & (OI_fut_master_data["Far OI %"] > 0), 'LB',
                                    np.where((OI_fut_master_data['Far %'] > 0) & (OI_fut_master_data["Far OI %"] < 0), 'SC',
                                             np.where((OI_fut_master_data['Far %'] < 0) & (OI_fut_master_data["Far OI %"] > 0), 'SB',
                                                      np.where((OI_fut_master_data['Far %'] < 0) & (OI_fut_master_data["Far OI %"] < 0), 'LW', ''))))

# Reducing the dataframe vales to 02 Decimal point
OI_fut_master_data = np.round(OI_fut_master_data, decimals=2)

# Dropping all the columns except the calculated columns that are to be displayed
OI_fut_master_data.drop(OI_fut_master_data.iloc[:, 2:10], inplace=True, axis=1)
OI_fut_master_data.drop(OI_fut_master_data.iloc[:, 2:43], inplace=True, axis=1)

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
                        id='OI_dropdown_option',
                        options=[{'label': 'DAY WISE', 'value': 'DAY WISE'},
                                 {'label': 'SCRIPT WISE', 'value': 'SCRIPT WISE'}],
                        value='SCRIPT WISE',  # default value
                        multi=False
                    ),
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id='OI_dropdown_list',
                        options=[{'label': x, 'value': x}
                                 for x in sorted(OI_fut_master_data.SYMBOL.unique())],
                        value='TATASTEEL',  # default value
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
                                id='OI_submit_button_prev',
                                n_clicks=0,
                                children='Prev',
                                color='primary',
                                className="ml-0",
                                size='sm',
                            ),
                        ]),
                        dbc.Col([
                            dbc.Button(
                                id='OI_submit_button_next',
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
                html.Br()
        )
    ]
)

content_third_row = dt.DataTable(id="OI_table",
                                    columns=[{'name': i, 'id': i} for i in OI_fut_master_data.columns],
                                    style_header={
                                     'backgroundColor': 'grey',
                                     'fontWeight': 'bold'
                                    },
                                    style_cell_conditional=[
                                            {
                                                'if': {'column_id': i},
                                                'textAlign': 'left'
                                            } for i in ['SYMBOL', 'TIMESTAMP']
                                        ],
                                    style_as_list_view=True,
                                    style_data_conditional= [
                                        {
                                            'if': {
                                                'column_id': 'BU',
                                            },
                                            'textAlign': 'center'
                                        },
                                        {
                                            'if': {
                                                'filter_query': '{BU} = SB',  # matching rows of a hidden column with the id, `id`
                                                'column_id': ['SYMBOL', 'BU'],
                                                },
                                            'backgroundColor': '#FF4136',
                                            'color': 'white'

                                        },
                                        {
                                            'if': {
                                                'filter_query': '{BU} = LB',
                                                # matching rows of a hidden column with the id, `id`
                                                'column_id': ['SYMBOL', 'BU'],
                                            },
                                            'backgroundColor': '#318500',
                                            'color': 'white'

                                        },
                                        {
                                            'if': {
                                                'filter_query': '{BU} = LW',
                                                # matching rows of a hidden column with the id, `id`
                                                'column_id': ['SYMBOL', 'BU'],
                                            },
                                            'backgroundColor': '#FF9595',
                                            'color': 'white'

                                        },
                                        {
                                            'if': {
                                                'filter_query': '{BU} = SC',
                                                # matching rows of a hidden column with the id, `id`
                                                'column_id': ['SYMBOL', 'BU'],
                                            },
                                            'backgroundColor': '#9ED10F',
                                            'color': 'white'

                                        },
                                        {

                                        },
                                    ]
                                 )
content = html.Div(
    [
        content_first_row,
        content_second_row,
        content_third_row,
    ],
    style=CONTENT_STYLE
)
layout = html.Div([content])

# Dependent dropdown Function to push list of Dates OR Script as pe choice of First Dropdown

@callback(Output('OI_dropdown_list', 'options'), Input('OI_dropdown_option', 'value'))
def update_dropdown_list(dropdown_option):
    print(dropdown_option)
    if dropdown_option == 'SCRIPT WISE':
        options = [{'label': x, 'value': x}
                   for x in sorted(OI_fut_master_data.SYMBOL.unique())]
    else:
        options = [{'label': x, 'value': x}
                   for x in sorted(OI_fut_master_data.TIMESTAMP.dt.strftime('%m-%d-%y').unique())]
    return options


# Filtering and Sorting the Table values and push the Data as Output to Table

@callback(Output('OI_table', 'data'), Input('OI_dropdown_option', 'value'), Input('OI_dropdown_list', 'value'))
def update_data(dropdown_option, dropdown_list):
    print(dropdown_option)
    print(dropdown_list)
    if dropdown_option == 'SCRIPT WISE':
        data = OI_fut_master_data[OI_fut_master_data.SYMBOL == dropdown_list]
    else:
        data = OI_fut_master_data[OI_fut_master_data.TIMESTAMP == dropdown_list]
        data = data.sort_values(by=['BU', 'COI %'], ascending=False)
        print(data)
    return data.to_dict('records')


