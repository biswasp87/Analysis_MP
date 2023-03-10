import dash
# Code from: https://github.com/plotly/dash-labs/tree/main/docs/demos/multi_page_example1
dash.register_page(__name__)

from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dash import html
from screeninfo import get_monitors
from nsepython import *
from dash import dash_table as dt



# Get Screen Resolution
for m in get_monitors():
    hgt = int(m.height)
    wd = int(m.width)

# Declaring Folder Paths
FPI_cur_dir = os.getcwd()
FPI_cur_master_dir = FPI_cur_dir + r"\Master_Files"


# Declaring DataFrames
OI_exp_data = pd.DataFrame()
Master_Spot_Data = pd.DataFrame()


# Assessing, Sorting & Filtering the Future Master File
Full_File_Path = str(FPI_cur_master_dir +r'\FPI_Data.xlsx')

FPI_Data = pd.read_excel(Full_File_Path, sheet_name='MasterSheet-Equity')
FPI_Data.columns.astype(str)
#print(FPI_Data)



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
                        id='FPI_Dropdown',
                        options=[{'label': 'Equity', 'value': 'Equity'},
                                 {'label': 'Debt', 'value': 'Debt'}],
                        value='Equity',  # default value
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

content_third_row = dt.DataTable(id="FPI_table",
                                    columns=[{'name': i, 'id': i} for i in FPI_Data.columns],
                                    style_header={
                                     'backgroundColor': 'grey',
                                     'fontWeight': 'bold'
                                    },
                                    style_cell_conditional=[
                                            {
                                                'if': {'column_id': i},
                                                'textAlign': 'left'
                                            } for i in ['Sector']
                                        ],
                                    style_as_list_view=True,
                                    style_data_conditional=
                                     # Colour red when values are negative
                                    [
                                         {
                                             'if': {'column_id': field_name,
                                                    'filter_query': '{' + field_name + '}' + ' < 0'},
                                             'backgroundColor': '#FF4136',
                                             'color': 'white'
                                         } for field_name in FPI_Data.columns
                                    ]
                                    +
                                    [
                                         # Colour green when values are positive
                                         {
                                             'if': {'column_id': field_name,
                                                    'filter_query': '{' + field_name + '}' + ' > 0'},
                                             'backgroundColor': '#318500',
                                             'color': 'white'
                                         } for field_name in FPI_Data.columns
                                    ],
                                )
content = html.Div(
    [
        content_first_row,
        content_second_row,
        content_third_row,
    ],
    style=CONTENT_STYLE
)

#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
layout = html.Div([content])

@callback(
    Output('FPI_table','data'),
    Input('FPI_Dropdown','value')
)

def update_table(tableoption):
    print(tableoption)
    if tableoption == 'Debt':
        FPI_Data = pd.read_excel(Full_File_Path, sheet_name='MasterSheet-Debt')
        FPI_Data.columns.astype(str)
    else:
        FPI_Data = pd.read_excel(Full_File_Path, sheet_name='MasterSheet-Equity')
        FPI_Data.columns.astype(str)
    return FPI_Data.to_dict('records')