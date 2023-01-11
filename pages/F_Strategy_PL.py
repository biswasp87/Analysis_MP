import dash
# Code from: https://github.com/plotly/dash-labs/tree/main/docs/demos/multi_page_example1
import pandas as pd

dash.register_page(__name__)
from dash import Dash, dcc, html, Input, Output, callback

# This page Calculates the P/L of 10MOption Strategy
# Available reports: CE Breakout (Option Buy & Sell) and CE Breakdown (Option Buy & Sell)

import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import dash_table, no_update
from dash.dependencies import Input, Output, State
from screeninfo import get_monitors
import numpy as np
from dash import dash_table as dt
from nsepython import *
from dash.dash_table import DataTable, FormatTemplate
from dash.dash_table.Format import Format, Scheme, Trim

# Declaring Format variables for Formatting the Dash Table
money = FormatTemplate.money(2)
percentage = FormatTemplate.percentage(2)

# Get Screen Resolution
for m in get_monitors():
    hgt = int(m.height)
    wd = int(m.width)

# Call the required databases
cur_dir = os.getcwd()
cur_master_dir = cur_dir + r"\Master_Files"
cur_fo_dir = cur_dir + r"\dumps\bhavcopy\nse\eod_fo"
cur_support_dir = cur_dir + r"\Support_Files"
lot_size_list = pd.read_csv(cur_support_dir + r"\Lot_Size_Filtered.csv")
#
# dir_name_opt_ce = cur_master_dir + r"\master_ce.csv"  # Home desktop
# opt_ce_data = pd.read_csv(dir_name_opt_ce)
# opt_ce_data['TIMESTAMP'] = pd.to_datetime(opt_ce_data['TIMESTAMP'])
# opt_ce_data = opt_ce_data.sort_values(by='TIMESTAMP', ascending=True)
# opt_ce_data['index'] = opt_ce_data.reset_index().index
# opt_ce_data.to_csv(cur_dir + "/opt_ce_data.csv", index=False)
#
# dir_name_opt_pe = cur_master_dir + r"\master_pe.csv"
# opt_pe_data = pd.read_csv(dir_name_opt_pe)
# opt_pe_data['TIMESTAMP'] = pd.to_datetime(opt_pe_data['TIMESTAMP'])
# opt_pe_data = opt_pe_data.sort_values(by='TIMESTAMP', ascending=True)
# opt_pe_data['index'] = opt_pe_data.reset_index().index
#
# dir_name_eq = cur_master_dir + r"\master_eq.csv"  # Home desktop
# eq_data = pd.read_csv(dir_name_eq)
# eq_data['TIMESTAMP'] = pd.to_datetime(eq_data['TIMESTAMP'])
# eq_data = eq_data.sort_values(by='TIMESTAMP', ascending=True)
#
# dir_name_index = cur_master_dir + r"\master_indices.csv"  # Home desktop
# index_data = pd.read_csv(dir_name_index, parse_dates=['Index_Date'], dayfirst=True)
# index_data = index_data.sort_values(by='Index_Date', ascending=True)
# index_data['index'] = index_data.reset_index().index
# index_data.to_csv(cur_dir + "/index_data.csv", index=False) # Write master_indices.csv in the same directory
#
# dir_name_fo = cur_master_dir + r"\master_fo.csv"
# fut_data = pd.read_csv(dir_name_fo)
# fut_data['TIMESTAMP'] = pd.to_datetime(fut_data['TIMESTAMP'])
# fut_data = fut_data.sort_values(by='TIMESTAMP', ascending=True)
# fut_data['index'] = fut_data.reset_index().index
# fut_data = fut_data[fut_data.INSTRUMENT == 'FUTSTK']
# OI_all_dates = fut_data.EXPIRY_DT.unique()
# print(OI_all_dates)
#
# wl = pd.read_csv(os.path.join(cur_support_dir, 'WL_10MVOL.csv'))
#
# # Declaring the Dataframes
# master_PL_CE_BO_B = pd.DataFrame() #CE Breakout CE Buy
# master_PL_CE_BO_S = pd.DataFrame() #CE Breakout PE Sell
# master_PL_CE_BD_B = pd.DataFrame() #CE Breakdown PE Buy
# master_PL_CE_BD_S = pd.DataFrame() #CE Breakdown CE Sell
#
# # Calculating the P/L for Each Stock from the 10MOptVol Watchlist and Merging for master Table
#
# for item in wl['Symbol']:
#     dropdown_value = item
#     print(item)
#     dropdown_exp_value = '30-Jun-2022'
#     df_eq_g3 = eq_data[eq_data.SYMBOL == dropdown_value]
#
#     lot_size_g3 = lot_size_list[lot_size_list.SYMBOL == dropdown_value]
#     lot_g3 = lot_size_g3["LOT_SIZE"].iloc[0]
#     df_opt_ce_ind_g3 = opt_ce_data[
#         (opt_ce_data.EXPIRY_DT == dropdown_exp_value) & (opt_ce_data.SYMBOL == dropdown_value)]
#     df_opt_ce_ind_g3.loc[:, 'indicator_sr_price'] = np.where(df_opt_ce_ind_g3['CONTRACTS']*int(lot_g3) > 10000000,
#                                                       df_opt_ce_ind_g3['STRIKE_PR'], '')
#
#     df_sl_timestamp_g3 = df_opt_ce_ind_g3[df_opt_ce_ind_g3.indicator_sr_price != '']
#     no_of_indicators = len(df_sl_timestamp_g3.indicator_sr_price)
#     if no_of_indicators > 0:
#
#         df_sl_timestamp_g3 = df_sl_timestamp_g3.iloc[0:1]
#         df_sl_timestamp_g3 = df_sl_timestamp_g3.reset_index()
#         df_eq_sl_g3 = eq_data[
#             (eq_data.TIMESTAMP == str(df_sl_timestamp_g3['TIMESTAMP'][0])) & (eq_data.SYMBOL == dropdown_value)]
#         df_eq_sl_g3 = df_eq_sl_g3.reset_index()
#         df_eq_g3['ENTRY'] = np.where(df_eq_g3['TIMESTAMP'] >= df_sl_timestamp_g3['TIMESTAMP'][0],
#                                      float(df_eq_sl_g3['HIGH'][0]), '')
#         df_eq_g3['SL'] = np.where(df_eq_g3['TIMESTAMP'] >= str(df_sl_timestamp_g3['TIMESTAMP'][0]),
#                                   float(df_eq_sl_g3['LOW'][0]), '')
#         df_eq_g3['EQ_CLOSE'] = df_eq_g3['CLOSE']
#         df_eq_g3 = df_eq_g3[df_eq_g3.ENTRY != '']
#         df_eq_g3 = df_eq_g3[df_eq_g3.SL != '']
#         df_eq_g3 = df_eq_g3.drop(['SYMBOL', 'SERIES', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'LAST',
#                                   'PREVCLOSE', 'TOTTRDQTY', 'TOTALTRADES', 'ISIN', 'Unnamed: 13', 'TOTTRDVAL'],
#                                  axis=1)
#
#         df_opt_ce_ini_price = df_opt_ce_ind_g3[df_opt_ce_ind_g3.indicator_sr_price != '']
#         df_opt_ce_ini_price = df_opt_ce_ini_price.reset_index()
#         df_opt_ce_ini_price['indicator_sr_price'] = df_opt_ce_ini_price.indicator_sr_price.astype(float)
#         df_opt_ce_ini_price.sort_values(["TIMESTAMP", "indicator_sr_price"], axis=0,
#                                         ascending=[True, True], inplace=True)
#         opt_ce_cur_strike = float(df_opt_ce_ini_price['STRIKE_PR'].iloc[0])
#         opt_ce_cur_date = df_opt_ce_ini_price['TIMESTAMP'].iloc[0]
#         print("opt ce cur date")
#         print(opt_ce_cur_date)
#
#         df_opt_ce_cur_price = opt_ce_data[(opt_ce_data.EXPIRY_DT == dropdown_exp_value) &
#                                           (opt_ce_data.SYMBOL == dropdown_value) &
#                                           (opt_ce_data.STRIKE_PR == opt_ce_cur_strike) &
#                                           (opt_ce_data.TIMESTAMP >= opt_ce_cur_date)]
#         df_opt_ce_cur_price = df_opt_ce_cur_price.drop(['Unnamed: 15', 'index'], axis=1)
#
#         df_eq_opt_g3 = pd.merge(df_opt_ce_cur_price, df_eq_g3, on=["TIMESTAMP"])
#
#         df_eq_opt_g3['ENTRY'] = df_eq_opt_g3.ENTRY.astype(float)
#         df_eq_opt_g3['SL'] = df_eq_opt_g3.SL.astype(float)
#         df_eq_opt_g3.to_csv(cur_dir + "/df_eq_opt_g3.csv", index=False)
#         for i in range(len(df_eq_opt_g3)):
#             if df_eq_opt_g3.loc[i, 'EQ_CLOSE'] >= df_eq_opt_g3.loc[i, 'ENTRY']:
#                 df_eq_opt_g3.loc[i, 'trd_status'] = "BUY"
#                 for j in range(i + 1, len(df_eq_opt_g3)):
#                     if df_eq_opt_g3.loc[j, 'EQ_CLOSE'] >= df_eq_opt_g3.loc[j, 'SL']:
#                         df_eq_opt_g3.loc[j, 'trd_status'] = "HOLD"
#                     elif df_eq_opt_g3.loc[j, 'EQ_CLOSE'] < df_eq_opt_g3.loc[j, 'SL']:
#                         df_eq_opt_g3.loc[j, 'trd_status'] = "SELL"
#                         for k in range(j + 1, len(df_eq_opt_g3)):
#                             df_eq_opt_g3.loc[k, 'trd_status'] = ''
#                         break
#                 break
#             else:
#                 df_eq_opt_g3.loc[i, 'trd_status'] = ''
#
#         df_eq_opt_g3 = df_eq_opt_g3[df_eq_opt_g3.trd_status != '']
#
#         no_of_signals_g3 = len(df_eq_opt_g3.trd_status)
#         print("Number of Triggred Trades: " + str(no_of_signals_g3))
#
#         if no_of_signals_g3 > 0:
#             df_pl_ce_bo_buy = df_eq_opt_g3
#             df_pl_ce_bo_buy.insert(5, column='Lot Size', value=lot_g3)
#             df_pl_ce_bo_buy['Entry(EQ)'] = df_pl_ce_bo_buy['EQ_CLOSE']
#             df_pl_ce_bo_buy['Entry(OPT)'] = df_pl_ce_bo_buy['CLOSE']
#             df_pl_ce_bo_buy['Invst(EQ)'] = df_pl_ce_bo_buy['EQ_CLOSE']
#             df_pl_ce_bo_buy['Invst(OPT)'] = df_pl_ce_bo_buy['CLOSE'] * int(lot_g3)
#             df_pl_ce_bo_buy.insert(16, column='Status', value=df_pl_ce_bo_buy['trd_status'].iloc[-1])
#             df_pl_ce_bo_buy['Cur Pr(EQ)'] = df_pl_ce_bo_buy['EQ_CLOSE'].iloc[-1]
#             df_pl_ce_bo_buy['Cur Pr(OPT)'] = df_pl_ce_bo_buy['CLOSE'].iloc[-1]
#             df_pl_ce_bo_buy['Cur Val(EQ)'] = df_pl_ce_bo_buy['EQ_CLOSE'].iloc[-1]
#             df_pl_ce_bo_buy['Cur Val(OPT)'] = df_pl_ce_bo_buy['CLOSE'].iloc[-1] * int(lot_g3)
#             df_pl_ce_bo_buy['P/L (EQ)'] = df_pl_ce_bo_buy['Cur Val(EQ)'] - df_pl_ce_bo_buy['Invst(EQ)']
#             df_pl_ce_bo_buy['P/L (OPT)'] = df_pl_ce_bo_buy['Cur Val(OPT)'] - df_pl_ce_bo_buy['Invst(OPT)']
#             df_pl_ce_bo_buy['P/L (EQ)%'] = df_pl_ce_bo_buy['P/L (EQ)'] / df_pl_ce_bo_buy['Invst(EQ)'] # Percentage to be displayed while formatting
#             df_pl_ce_bo_buy['P/L (OPT)%'] = df_pl_ce_bo_buy['P/L (OPT)'] / df_pl_ce_bo_buy['Invst(OPT)'] # Percentage to be displayed while formatting
#             df_pl_ce_bo_buy = df_pl_ce_bo_buy.drop(['INSTRUMENT','EXPIRY_DT','OPTION_TYP','OPEN', 'HIGH', 'LOW', 'CLOSE', 'SETTLE_PR', 'CONTRACTS', 'VAL_INLAKH',
#                                 'OPEN_INT', 'CHG_IN_OI', 'EQ_CLOSE', 'trd_status'], axis=1)
#             len_of_col = len(df_pl_ce_bo_buy.Status)
#             df_pl_ce_bo_buy = df_pl_ce_bo_buy.drop(df_pl_ce_bo_buy.index[range(1, len_of_col)])
#             master_PL_CE_BO_B = master_PL_CE_BO_B.append(df_pl_ce_bo_buy, ignore_index=True)
#             # master_PL_CE_BO_B.to_csv(cur_dir + "/master_PL_CE_BO_B.csv", index=False)
#
#         df_opt_pe_cur_price_g4 = opt_pe_data[(opt_pe_data.EXPIRY_DT == dropdown_exp_value) &
#                                              (opt_pe_data.SYMBOL == dropdown_value) &
#                                              (opt_pe_data.STRIKE_PR == opt_ce_cur_strike) &
#                                              (opt_pe_data.TIMESTAMP >= opt_ce_cur_date)]
#         df_opt_pe_cur_price_g4 = df_opt_pe_cur_price_g4.drop(['Unnamed: 15', 'index'], axis=1)
#
#         df_eq_opt_g4 = pd.merge(df_opt_pe_cur_price_g4, df_eq_g3, on=["TIMESTAMP"])
#
#         df_eq_opt_g4['ENTRY'] = df_eq_opt_g4.ENTRY.astype(float)
#         df_eq_opt_g4['SL'] = df_eq_opt_g4.SL.astype(float)
#
#         for i in range(len(df_eq_opt_g4)):
#             if df_eq_opt_g4.loc[i, 'EQ_CLOSE'] >= df_eq_opt_g4.loc[i, 'ENTRY']:
#                 df_eq_opt_g4.loc[i, 'trd_status'] = "SELL"
#                 for j in range(i + 1, len(df_eq_opt_g4)):
#                     if df_eq_opt_g4.loc[j, 'EQ_CLOSE'] >= df_eq_opt_g4.loc[j, 'SL']:
#                         df_eq_opt_g4.loc[j, 'trd_status'] = "HOLD"
#                     elif df_eq_opt_g4.loc[j, 'EQ_CLOSE'] < df_eq_opt_g4.loc[j, 'SL']:
#                         df_eq_opt_g4.loc[j, 'trd_status'] = "BUY"
#                         for k in range(j + 1, len(df_eq_opt_g4)):
#                             df_eq_opt_g4.loc[k, 'trd_status'] = ''
#                         break
#                 break
#             else:
#                 df_eq_opt_g4.loc[i, 'trd_status'] = ''
#
#         df_eq_opt_g4 = df_eq_opt_g4[df_eq_opt_g4.trd_status != '']
#         # df_eq_opt_g4.to_csv(cur_dir + "/df_eq_opt_g4.csv", index=False)
#
#         no_of_signals_g4 = len(df_eq_opt_g4.trd_status)
#         print("Number of Triggred Trades: " + str(no_of_signals_g3))
#
#         if no_of_signals_g4 > 0:
#             df_pl_ce_bo_sell = df_eq_opt_g4
#             df_pl_ce_bo_sell.insert(5, column='Lot Size', value=lot_g3)
#             # df_pl_ce_bo_sell['Lot_Size'] = lot_g3
#             df_pl_ce_bo_sell['Entry(EQ)'] = df_pl_ce_bo_sell['EQ_CLOSE']
#             df_pl_ce_bo_sell['Entry(OPT)'] = df_pl_ce_bo_sell['CLOSE']
#             df_pl_ce_bo_sell['Invst(EQ)'] = df_pl_ce_bo_sell['EQ_CLOSE']
#             df_pl_ce_bo_sell['Invst(OPT)'] = df_pl_ce_bo_sell['CLOSE'] * int(lot_g3)
#             df_pl_ce_bo_sell.insert(16, column='Status', value=df_pl_ce_bo_sell['trd_status'].iloc[-1])
#             df_pl_ce_bo_sell['Cur Pr(EQ)'] = df_pl_ce_bo_sell['EQ_CLOSE'].iloc[-1]
#             df_pl_ce_bo_sell['Cur Pr(OPT)'] = df_pl_ce_bo_sell['CLOSE'].iloc[-1]
#             df_pl_ce_bo_sell['Cur Val(EQ)'] = df_pl_ce_bo_sell['EQ_CLOSE'].iloc[-1]
#             df_pl_ce_bo_sell['Cur Val(OPT)'] = df_pl_ce_bo_sell['CLOSE'].iloc[-1] * int(lot_g3)
#             df_pl_ce_bo_sell['P/L (EQ)'] = df_pl_ce_bo_sell['Invst(EQ)'] - df_pl_ce_bo_sell['Cur Val(EQ)']
#             df_pl_ce_bo_sell['P/L (OPT)'] = df_pl_ce_bo_sell['Invst(OPT)'] - df_pl_ce_bo_sell['Cur Val(OPT)']
#             df_pl_ce_bo_sell['P/L (EQ)%'] = df_pl_ce_bo_sell['P/L (EQ)'] / df_pl_ce_bo_sell['Invst(EQ)'] # Percentage to be displayed while formatting
#             df_pl_ce_bo_sell['P/L (OPT)%'] = df_pl_ce_bo_sell['P/L (OPT)'] / df_pl_ce_bo_sell['Invst(OPT)'] # Percentage to be displayed while formatting
#             df_pl_ce_bo_sell = df_pl_ce_bo_sell.drop(['INSTRUMENT','EXPIRY_DT','OPTION_TYP','OPEN', 'HIGH', 'LOW', 'CLOSE', 'SETTLE_PR', 'CONTRACTS', 'VAL_INLAKH',
#                                 'OPEN_INT', 'CHG_IN_OI', 'EQ_CLOSE', 'trd_status'], axis=1)
#             len_of_col = len(df_pl_ce_bo_sell.Status)
#             df_pl_ce_bo_sell = df_pl_ce_bo_sell.drop(df_pl_ce_bo_sell.index[range(1, len_of_col)])
#             master_PL_CE_BO_S = master_PL_CE_BO_S.append(df_pl_ce_bo_sell, ignore_index=True)
#             # master_PL_CE_BO.to_csv(cur_dir + "/master_PL_CE_BO.csv", index=False)
#
#
#
#     df_eq_g6 = eq_data[eq_data.SYMBOL == dropdown_value]
#
#     lot_size_g6 = lot_size_list[lot_size_list.SYMBOL == dropdown_value]
#     lot_g6 = int(lot_size_g6["LOT_SIZE"].iloc[0])
#
#     df_opt_ce_ind_g6 = opt_ce_data[
#         (opt_ce_data.EXPIRY_DT == dropdown_exp_value) & (opt_ce_data.SYMBOL == dropdown_value)]
#     df_opt_ce_ind_g6['indicator_sr_price'] = np.where(df_opt_ce_ind_g6['CONTRACTS'] * lot_g6 > 10000000,
#                                                       df_opt_ce_ind_g6['STRIKE_PR'], '')
#
#     df_sl_timestamp_g6 = df_opt_ce_ind_g6[df_opt_ce_ind_g6.indicator_sr_price != '']
#     no_of_indicators = len(df_sl_timestamp_g6.indicator_sr_price)
#
#     if no_of_indicators > 0:
#         df_sl_timestamp_g6 = df_sl_timestamp_g6.iloc[0:1]
#         df_sl_timestamp_g6 = df_sl_timestamp_g6.reset_index()
#         df_eq_sl_g6 = eq_data[
#            (eq_data.TIMESTAMP == str(df_sl_timestamp_g6['TIMESTAMP'][0])) & (eq_data.SYMBOL == dropdown_value)]
#         df_eq_sl_g6 = df_eq_sl_g6.reset_index()
#         df_eq_g6['ENTRY'] = np.where(df_eq_g6['TIMESTAMP'] >= df_sl_timestamp_g6['TIMESTAMP'][0],
#                                          float(df_eq_sl_g6['LOW'][0]), '')
#         df_eq_g6['SL'] = np.where(df_eq_g6['TIMESTAMP'] >= str(df_sl_timestamp_g6['TIMESTAMP'][0]),
#                                       float(df_eq_sl_g6['HIGH'][0]), '')
#         df_eq_g6['EQ_CLOSE'] = df_eq_g6['CLOSE']
#         df_eq_g6 = df_eq_g6[df_eq_g6.ENTRY != '']
#         df_eq_g6 = df_eq_g6[df_eq_g6.SL != '']
#         df_eq_g6 = df_eq_g6.drop(['SYMBOL', 'SERIES', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'LAST',
#                                       'PREVCLOSE', 'TOTTRDQTY', 'TOTALTRADES', 'ISIN', 'Unnamed: 13', 'TOTTRDVAL'],
#                                      axis=1)
#
#         df_opt_ce_ini_price = df_opt_ce_ind_g6[df_opt_ce_ind_g6.indicator_sr_price != '']
#         df_opt_ce_ini_price = df_opt_ce_ini_price.reset_index()
#         df_opt_ce_ini_price['indicator_sr_price'] = df_opt_ce_ini_price.indicator_sr_price.astype(float)
#         df_opt_ce_ini_price.sort_values(["TIMESTAMP", "indicator_sr_price"], axis=0,
#                          ascending=[True,True], inplace=True)
#         opt_ce_cur_strike = float(df_opt_ce_ini_price['STRIKE_PR'].iloc[0])
#         opt_ce_cur_date = df_opt_ce_ini_price['TIMESTAMP'].iloc[0]
#
#         df_opt_ce_cur_price = opt_ce_data[(opt_ce_data.EXPIRY_DT == dropdown_exp_value) &
#                                           (opt_ce_data.SYMBOL == dropdown_value) &
#                                           (opt_ce_data.STRIKE_PR == opt_ce_cur_strike) &
#                                           (opt_ce_data.TIMESTAMP >= opt_ce_cur_date)]
#         df_opt_ce_cur_price = df_opt_ce_cur_price.drop(['Unnamed: 15', 'index'], axis=1)
#
#         df_eq_opt_g6 = pd.merge(df_opt_ce_cur_price, df_eq_g6, on=["TIMESTAMP"])
#
#         df_eq_opt_g6['ENTRY'] = df_eq_opt_g6.ENTRY.astype(float)
#         df_eq_opt_g6['SL'] = df_eq_opt_g6.SL.astype(float)
#
#         for i in range(len(df_eq_opt_g6)):
#             if df_eq_opt_g6.loc[i, 'EQ_CLOSE'] <= df_eq_opt_g6.loc[i, 'ENTRY']:
#                 df_eq_opt_g6.loc[i, 'trd_status'] = "SELL"
#                 for j in range(i + 1, len(df_eq_opt_g6)):
#                     if df_eq_opt_g6.loc[j, 'EQ_CLOSE'] <= df_eq_opt_g6.loc[j, 'SL']:
#                         df_eq_opt_g6.loc[j, 'trd_status'] = "HOLD"
#                     elif df_eq_opt_g6.loc[j, 'EQ_CLOSE'] > df_eq_opt_g6.loc[j, 'SL']:
#                         df_eq_opt_g6.loc[j, 'trd_status'] = "BUY"
#                         for k in range(j+1,len(df_eq_opt_g6)):
#                             df_eq_opt_g6.loc[k, 'trd_status'] = ''
#                         break
#                 break
#             else:
#                 df_eq_opt_g6.loc[i, 'trd_status'] = ''
#
#         df_eq_opt_g6 = df_eq_opt_g6[df_eq_opt_g6.trd_status != '']
#         # df_eq_opt_g6.to_csv(cur_dir + "/df_eq_opt_g6.csv", index=False)
#
#         no_of_signals_g6 = len(df_eq_opt_g6.trd_status)
#         print("Number of Signals")
#         print(no_of_signals_g6)
#         if no_of_signals_g6 > 0:
#             df_pl_ce_bd_sell = df_eq_opt_g6
#             df_pl_ce_bd_sell.insert(5, column='Lot Size', value=lot_g3)
#             # df_pl_ce_bd_sell['Lot_Size'] = lot_g3
#             df_pl_ce_bd_sell['Entry(EQ)'] = df_pl_ce_bd_sell['EQ_CLOSE']
#             df_pl_ce_bd_sell['Entry(OPT)'] = df_pl_ce_bd_sell['CLOSE']
#             df_pl_ce_bd_sell['Invst(EQ)'] = df_pl_ce_bd_sell['EQ_CLOSE']
#             df_pl_ce_bd_sell['Invst(OPT)'] = df_pl_ce_bd_sell['CLOSE'] * int(lot_g3)
#             df_pl_ce_bd_sell.insert(16, column='Status', value=df_pl_ce_bd_sell['trd_status'].iloc[-1])
#             df_pl_ce_bd_sell['Cur Pr(EQ)'] = df_pl_ce_bd_sell['EQ_CLOSE'].iloc[-1]
#             df_pl_ce_bd_sell['Cur Pr(OPT)'] = df_pl_ce_bd_sell['CLOSE'].iloc[-1]
#             df_pl_ce_bd_sell['Cur Val(EQ)'] = df_pl_ce_bd_sell['EQ_CLOSE'].iloc[-1]
#             df_pl_ce_bd_sell['Cur Val(OPT)'] = df_pl_ce_bd_sell['CLOSE'].iloc[-1] * int(lot_g3)
#             df_pl_ce_bd_sell['P/L (EQ)'] = df_pl_ce_bd_sell['Invst(EQ)'] - df_pl_ce_bd_sell['Cur Val(EQ)']
#             df_pl_ce_bd_sell['P/L (OPT)'] = df_pl_ce_bd_sell['Invst(OPT)'] - df_pl_ce_bd_sell['Cur Val(OPT)']
#             df_pl_ce_bd_sell['P/L (EQ)%'] = df_pl_ce_bd_sell['P/L (EQ)'] / df_pl_ce_bd_sell['Invst(EQ)'] # Percentage to be displayed while formatting
#             df_pl_ce_bd_sell['P/L (OPT)%'] = df_pl_ce_bd_sell['P/L (OPT)'] / df_pl_ce_bd_sell['Invst(OPT)'] # Percentage to be displayed while formatting
#             df_pl_ce_bd_sell = df_pl_ce_bd_sell.drop(['INSTRUMENT','EXPIRY_DT','OPTION_TYP','OPEN', 'HIGH', 'LOW', 'CLOSE', 'SETTLE_PR', 'CONTRACTS', 'VAL_INLAKH',
#                                 'OPEN_INT', 'CHG_IN_OI', 'EQ_CLOSE', 'trd_status'], axis=1)
#             len_of_col = len(df_pl_ce_bd_sell.Status)
#             df_pl_ce_bd_sell = df_pl_ce_bd_sell.drop(df_pl_ce_bd_sell.index[range(1, len_of_col)])
#             master_PL_CE_BD_S = master_PL_CE_BD_S.append(df_pl_ce_bd_sell, ignore_index=True)
#             # master_PL_CE_BD_B.to_csv(cur_dir + "/master_PL_CE_BD_B.csv", index=False)
#
#         df_opt_pe_cur_price_g7 = opt_pe_data[(opt_pe_data.EXPIRY_DT == dropdown_exp_value) &
#                                           (opt_pe_data.SYMBOL == dropdown_value) &
#                                           (opt_pe_data.STRIKE_PR == opt_ce_cur_strike) &
#                                           (opt_pe_data.TIMESTAMP >= opt_ce_cur_date)]
#         df_opt_pe_cur_price_g7 = df_opt_pe_cur_price_g7.drop(['Unnamed: 15', 'index'], axis=1)
#
#         df_eq_opt_g7 = pd.merge(df_opt_pe_cur_price_g7, df_eq_g6, on=["TIMESTAMP"])
#
#         df_eq_opt_g7['ENTRY'] = df_eq_opt_g7.ENTRY.astype(float)
#         df_eq_opt_g7['SL'] = df_eq_opt_g7.SL.astype(float)
#
#         for i in range(len(df_eq_opt_g7)):
#             if df_eq_opt_g7.loc[i, 'EQ_CLOSE'] <= df_eq_opt_g7.loc[i, 'ENTRY']:
#                 df_eq_opt_g7.loc[i, 'trd_status'] = "BUY"
#                 for j in range(i + 1, len(df_eq_opt_g7)):
#                     if df_eq_opt_g7.loc[j, 'EQ_CLOSE'] <= df_eq_opt_g7.loc[j, 'SL']:
#                         df_eq_opt_g7.loc[j, 'trd_status'] = "HOLD"
#                     elif df_eq_opt_g7.loc[j, 'EQ_CLOSE'] > df_eq_opt_g7.loc[j, 'SL']:
#                         df_eq_opt_g7.loc[j, 'trd_status'] = "SELL"
#                         for k in range(j+1,len(df_eq_opt_g7)):
#                             df_eq_opt_g7.loc[k, 'trd_status'] = ''
#                         break
#                 break
#             else:
#                 df_eq_opt_g7.loc[i, 'trd_status'] = ''
#
#         df_eq_opt_g7 = df_eq_opt_g7[df_eq_opt_g7.trd_status != '']
#
#         no_of_signals_g7 = len(df_eq_opt_g7.trd_status)
#         print("Number of Signals")
#         print(no_of_signals_g7)
#         if no_of_signals_g7 > 0:
#             df_pl_ce_bd_buy = df_eq_opt_g7
#             df_pl_ce_bd_buy.insert(5, column='Lot Size', value=lot_g3)
#             df_pl_ce_bd_buy['Entry(EQ)'] = df_pl_ce_bd_buy['EQ_CLOSE']
#             df_pl_ce_bd_buy['Entry(OPT)'] = df_pl_ce_bd_buy['CLOSE']
#             df_pl_ce_bd_buy['Invst(EQ)'] = df_pl_ce_bd_buy['EQ_CLOSE']
#             df_pl_ce_bd_buy['Invst(OPT)'] = df_pl_ce_bd_buy['CLOSE'] * int(lot_g3)
#             df_pl_ce_bd_buy.insert(16, column='Status', value=df_pl_ce_bd_buy['trd_status'].iloc[-1])
#             df_pl_ce_bd_buy['Cur Pr(EQ)'] = df_pl_ce_bd_buy['EQ_CLOSE'].iloc[-1]
#             df_pl_ce_bd_buy['Cur Pr(OPT)'] = df_pl_ce_bd_buy['CLOSE'].iloc[-1]
#             df_pl_ce_bd_buy['Cur Val(EQ)'] = df_pl_ce_bd_buy['EQ_CLOSE'].iloc[-1]
#             df_pl_ce_bd_buy['Cur Val(OPT)'] = df_pl_ce_bd_buy['CLOSE'].iloc[-1] * int(lot_g3)
#             df_pl_ce_bd_buy['P/L (EQ)'] = df_pl_ce_bd_buy['Cur Val(EQ)'] - df_pl_ce_bd_buy['Invst(EQ)']
#             df_pl_ce_bd_buy['P/L (OPT)'] = df_pl_ce_bd_buy['Cur Val(OPT)'] - df_pl_ce_bd_buy['Invst(OPT)']
#             df_pl_ce_bd_buy['P/L (EQ)%'] = df_pl_ce_bd_buy['P/L (EQ)'] / df_pl_ce_bd_buy['Invst(EQ)'] # Percentage to be displayed while formatting
#             df_pl_ce_bd_buy['P/L (OPT)%'] = df_pl_ce_bd_buy['P/L (OPT)'] / df_pl_ce_bd_buy['Invst(OPT)'] # Percentage to be displayed while formatting
#             df_pl_ce_bd_buy = df_pl_ce_bd_buy.drop(['INSTRUMENT','EXPIRY_DT','OPTION_TYP','OPEN', 'HIGH', 'LOW', 'CLOSE', 'SETTLE_PR', 'CONTRACTS', 'VAL_INLAKH',
#                                 'OPEN_INT', 'CHG_IN_OI', 'EQ_CLOSE', 'trd_status'], axis=1)
#             len_of_col = len(df_pl_ce_bd_buy.Status)
#             df_pl_ce_bd_buy = df_pl_ce_bd_buy.drop(df_pl_ce_bd_buy.index[range(1, len_of_col)])
#             master_PL_CE_BD_B = master_PL_CE_BD_B.append(df_pl_ce_bd_buy, ignore_index=True)
#             # master_PL_CE_BD_B.to_csv(cur_dir + "/master_PL_CE_BD_B.csv", index=False)
#
#
#
# Industry_List = pd.read_csv(os.path.join(cur_support_dir, 'Nifty500_Industry_List.csv'))
# Industry_List = Industry_List.drop(['Company Name','Series', 'ISIN Code'], axis=1)
# Industry_List = Industry_List.rename(columns={'Symbol': 'SYMBOL'})
#
# master_PL_CE_BO_B = pd.merge(master_PL_CE_BO_B, Industry_List, on=['SYMBOL'])
# master_PL_CE_BO_B = master_PL_CE_BO_B.sort_values(by='Industry', ascending=True)
# master_PL_CE_BO_B.at['Total', 'P/L (OPT)'] = master_PL_CE_BO_B['P/L (OPT)'].sum()
# master_PL_CE_BO_B.at['Total', 'P/L (EQ)'] = master_PL_CE_BO_B['P/L (EQ)'].sum()
# master_PL_CE_BO_B.at['Total', 'Invst(OPT)'] = master_PL_CE_BO_B['Invst(OPT)'].sum()
# master_PL_CE_BO_B.at['Total', 'Invst(EQ)'] = master_PL_CE_BO_B['Invst(EQ)'].sum()
# master_PL_CE_BO_B.to_csv(cur_support_dir + "/master_PL_CE_BO_Buy.csv", index=False)
#
# master_PL_CE_BO_S = pd.merge(master_PL_CE_BO_S, Industry_List, on=['SYMBOL'])
# master_PL_CE_BO_S = master_PL_CE_BO_S.sort_values(by='Industry', ascending=True)
# master_PL_CE_BO_S.at['Total', 'P/L (OPT)'] = master_PL_CE_BO_S['P/L (OPT)'].sum()
# master_PL_CE_BO_S.at['Total', 'P/L (EQ)'] = master_PL_CE_BO_S['P/L (EQ)'].sum()
# master_PL_CE_BO_S.at['Total', 'Invst(OPT)'] = master_PL_CE_BO_S['Invst(OPT)'].sum()
# master_PL_CE_BO_S.at['Total', 'Invst(EQ)'] = master_PL_CE_BO_S['Invst(EQ)'].sum()
# master_PL_CE_BO_S.to_csv(cur_support_dir + "/master_PL_CE_BD_Sell.csv", index=False)
#
# master_PL_CE_BD_B = pd.merge(master_PL_CE_BD_B, Industry_List, on=['SYMBOL'])
# master_PL_CE_BD_B = master_PL_CE_BD_B.sort_values(by='Industry', ascending=True)
# master_PL_CE_BD_B.at['Total', 'P/L (OPT)'] = master_PL_CE_BD_B['P/L (OPT)'].sum()
# master_PL_CE_BD_B.at['Total', 'P/L (EQ)'] = master_PL_CE_BD_B['P/L (EQ)'].sum()
# master_PL_CE_BD_B.at['Total', 'Invst(OPT)'] = master_PL_CE_BD_B['Invst(OPT)'].sum()
# master_PL_CE_BD_B.at['Total', 'Invst(EQ)'] = master_PL_CE_BD_B['Invst(EQ)'].sum()
# master_PL_CE_BD_B.to_csv(cur_support_dir + "/master_PL_CE_BD_Buy.csv", index=False)
#
# master_PL_CE_BD_S = pd.merge(master_PL_CE_BD_S, Industry_List, on=['SYMBOL'])
# master_PL_CE_BD_S = master_PL_CE_BD_S.sort_values(by='Industry', ascending=True)
# master_PL_CE_BD_S.at['Total', 'P/L (OPT)'] = master_PL_CE_BD_S['P/L (OPT)'].sum()
# master_PL_CE_BD_S.at['Total', 'P/L (EQ)'] = master_PL_CE_BD_S['P/L (EQ)'].sum()
# master_PL_CE_BD_S.at['Total', 'Invst(OPT)'] = master_PL_CE_BD_S['Invst(OPT)'].sum()
# master_PL_CE_BD_S.at['Total', 'Invst(EQ)'] = master_PL_CE_BD_S['Invst(EQ)'].sum()
# master_PL_CE_BD_S.to_csv(cur_support_dir + "/master_PL_CE_BD_Sell.csv", index=False)
#
# #Creating the Summary Table by Summation of P/L as per Industry Wise
# master_PL_CE_BO_B_Industry = master_PL_CE_BO_B.groupby(['Industry'], as_index=False, sort=True)['Invst(EQ)','P/L (EQ)','Invst(OPT)','P/L (OPT)'].sum()
# master_PL_CE_BO_B_Industry['P/L (EQ)%'] = master_PL_CE_BO_B_Industry['P/L (EQ)'] / master_PL_CE_BO_B_Industry['Invst(EQ)']  # Percentage to be displayed while formatting
# master_PL_CE_BO_B_Industry['P/L (OPT)%'] = master_PL_CE_BO_B_Industry['P/L (OPT)'] / master_PL_CE_BO_B_Industry['Invst(OPT)']  # Percentage to be displayed while formatting
# master_PL_CE_BO_B_Industry.to_csv(cur_support_dir + "/master_PL_CE_BO_B_Industry.csv", index=False)
#
# master_PL_CE_BO_S_Industry = master_PL_CE_BO_S.groupby(['Industry'], as_index=False, sort=True)['Invst(EQ)','P/L (EQ)','Invst(OPT)','P/L (OPT)'].sum()
# master_PL_CE_BO_S_Industry['P/L (EQ)%'] = master_PL_CE_BO_S_Industry['P/L (EQ)'] / master_PL_CE_BO_S_Industry['Invst(EQ)']  # Percentage to be displayed while formatting
# master_PL_CE_BO_S_Industry['P/L (OPT)%'] = master_PL_CE_BO_S_Industry['P/L (OPT)'] / master_PL_CE_BO_S_Industry['Invst(OPT)']  # Percentage to be displayed while formatting
# master_PL_CE_BO_S_Industry.to_csv(cur_support_dir + "/master_PL_CE_BO_S_Industry.csv", index=False)
#
# master_PL_CE_BD_B_Industry = master_PL_CE_BD_B.groupby(['Industry'], as_index=False, sort=True)['Invst(EQ)','P/L (EQ)','Invst(OPT)','P/L (OPT)'].sum()
# master_PL_CE_BD_B_Industry['P/L (EQ)%'] = master_PL_CE_BD_B_Industry['P/L (EQ)'] / master_PL_CE_BD_B_Industry['Invst(EQ)']  # Percentage to be displayed while formatting
# master_PL_CE_BD_B_Industry['P/L (OPT)%'] = master_PL_CE_BD_B_Industry['P/L (OPT)'] / master_PL_CE_BD_B_Industry['Invst(OPT)']  # Percentage to be displayed while formatting
# master_PL_CE_BD_B_Industry.to_csv(cur_support_dir + "/master_PL_CE_BD_B_Industry.csv", index=False)
#
# master_PL_CE_BD_S_Industry = master_PL_CE_BD_S.groupby(['Industry'], as_index=False, sort=True)['Invst(EQ)','P/L (EQ)','Invst(OPT)','P/L (OPT)'].sum()
# master_PL_CE_BD_S_Industry['P/L (EQ)%'] = master_PL_CE_BD_S_Industry['P/L (EQ)'] / master_PL_CE_BD_S_Industry['Invst(EQ)']  # Percentage to be displayed while formatting
# master_PL_CE_BD_S_Industry['P/L (OPT)%'] = master_PL_CE_BD_S_Industry['P/L (OPT)'] / master_PL_CE_BD_S_Industry['Invst(OPT)']  # Percentage to be displayed while formatting
# master_PL_CE_BD_S_Industry.to_csv(cur_support_dir + "/master_PL_CE_BD_S_Industry.csv", index=False)

master_PL_CE_BO_B = pd.read_csv(cur_support_dir + "/master_PL_CE_BO_B.csv")
master_PL_CE_BO_S = pd.read_csv(cur_support_dir + "/master_PL_CE_BO_S.csv")
master_PL_CE_BD_B = pd.read_csv(cur_support_dir + "/master_PL_CE_BD_B.csv")
master_PL_CE_BD_S = pd.read_csv(cur_support_dir + "/master_PL_CE_BD_S.csv")

master_PL_CE_BO_B_Industry = pd.read_csv(cur_support_dir + "/master_PL_CE_BO_B_Industry.csv")
master_PL_CE_BO_S_Industry = pd.read_csv(cur_support_dir + "/master_PL_CE_BO_S_Industry.csv")
master_PL_CE_BD_B_Industry = pd.read_csv(cur_support_dir + "/master_PL_CE_BD_B_Industry.csv")
master_PL_CE_BD_S_Industry = pd.read_csv(cur_support_dir + "/master_PL_CE_BD_S_Industry.csv")


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
                        id='PL_Buy_Sell_Option',
                        options=[{'label': 'Option Buy', 'value': 'Option Buy'},
                                 {'label': 'Option Sell', 'value': 'Option Sell'}
                                 ],
                        value='Option Buy',  # default value
                        multi=False
                    ),
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id='PL_Strategy_Option',
                        options=[{'label': 'CE Breakout', 'value': 'CE Breakout'},
                                 {'label': 'CE Breakdown', 'value': 'CE Breakdown'},
                                 {'label': 'PE Breakout', 'value': 'PE Breakout'},
                                 {'label': 'PE Breakdown', 'value': 'PE Breakdown'}
                                 ],
                        value='CE Breakout',  # default value
                        multi=False
                    ),
                ]
            )
        ),
        # dbc.Card(
        #     dbc.CardBody(
        #         [
        #             dcc.Dropdown(
        #                 id='PL_Expiry_Dates',
        #                 options=[{'label': x, 'value': x}
        #                          for x in fut_data.EXPIRY_DT.unique()],
        #                 value=fut_data.EXPIRY_DT.unique()[0],  # default value
        #                 multi=False
        #             ),
        #         ]
        #     )
        # ),
    ]
)

content_second_row = dbc.Row(
    [
        dbc.Col(
                html.Br()
        )
    ]
)

content_third_row = dt.DataTable(id="PL_Industry_table",
                                    columns=[
                                         dict(id='Industry', name='Industry'),
                                         dict(id='Invst(EQ)', name='Invst(EQ)', type='numeric', format=Format(precision=2, scheme=Scheme.fixed)),
                                         dict(id='P/L (EQ)', name='P/L (EQ)', type='numeric', format=Format(precision=2, scheme=Scheme.fixed)),
                                         dict(id='P/L (EQ)%', name='P/L (EQ)%', type='numeric', format=percentage),
                                         dict(id='Invst(OPT)', name='Invst(OPT)', type='numeric', format=Format(precision=2, scheme=Scheme.fixed)),
                                         dict(id='P/L (OPT)', name='P/L (OPT)', type='numeric', format=Format(precision=2, scheme=Scheme.fixed)),
                                         dict(id='P/L (OPT)%', name='P/L (OPT)%', type='numeric', format=percentage)
                                      ],
                                    style_header={
                                         'backgroundColor': 'grey',
                                         'fontWeight': 'bold'
                                    },
                                    style_cell_conditional=[
                                            {
                                                'if': {'column_id': i},
                                                'textAlign': 'left'
                                            } for i in ['SYMBOL', 'Industry']
                                        ],
                                    style_as_list_view=True,
                                    style_data_conditional=[
                                        {
                                            'if': {
                                                'filter_query': '{P/L (EQ)} >0',
                                                'column_id': ['P/L (EQ)'],
                                            },
                                            'backgroundColor': '#318500',
                                            'color': 'white'

                                        },
                                        {
                                            'if': {
                                                'filter_query': '{P/L (OPT)} >0',
                                            },
                                            'backgroundColor': '#318500',
                                            'color': 'white'

                                        },
                                        ]
                                 )
content_fourth_row = dbc.Row(
    [
        dbc.Col(
                html.Br()
        )
    ]
)

content_fifth_row = dt.DataTable(id="PL_table",
                                  columns=[
                                     dict(id='SYMBOL', name='SYMBOL'),
                                     dict(id='Industry', name='Industry'),
                                     dict(id='STRIKE_PR', name='STRIKE_PR'),
                                     dict(id='Lot Size', name='Lot Size'),
                                     dict(id='TIMESTAMP', name='TIMESTAMP',type='date'),
                                     dict(id='Status', name='Status'),
                                     dict(id='ENTRY', name='ENTRY', type='numeric', format=Format(precision=2, scheme=Scheme.fixed)),
                                     dict(id='SL', name='SL', type='numeric', format=Format(precision=2, scheme=Scheme.fixed)),
                                     dict(id='Entry(EQ)', name='Entry(EQ)', type='numeric', format=Format(precision=2, scheme=Scheme.fixed)),
                                     dict(id='Invst(EQ)', name='Invst(EQ)', type='numeric', format=Format(precision=2, scheme=Scheme.fixed)),
                                     dict(id='Cur Pr(EQ)', name='Cur Pr(EQ)', type='numeric', format=Format(precision=2, scheme=Scheme.fixed)),
                                     dict(id='Cur Val(EQ)', name='Cur Val(EQ)', type='numeric', format=Format(precision=2, scheme=Scheme.fixed)),
                                     dict(id='P/L (EQ)', name='P/L (EQ)', type='numeric', format=Format(precision=2, scheme=Scheme.fixed)),
                                     dict(id='P/L (EQ)%', name='P/L (EQ)%', type='numeric', format=percentage),
                                     dict(id='Entry(OPT)', name='Entry(OPT)', type='numeric', format=Format(precision=2, scheme=Scheme.fixed)),
                                     dict(id='Invst(OPT)', name='Invst(OPT)', type='numeric', format=Format(precision=2, scheme=Scheme.fixed)),
                                     dict(id='Cur Pr(OPT)', name='Cur Pr(OPT)', type='numeric', format=Format(precision=2, scheme=Scheme.fixed)),
                                     dict(id='Cur Val(OPT)', name='Cur Val(OPT)', type='numeric', format=Format(precision=2, scheme=Scheme.fixed)),
                                     dict(id='P/L (OPT)', name='P/L (OPT)', type='numeric', format=Format(precision=2, scheme=Scheme.fixed)),
                                     dict(id='P/L (OPT)%', name='P/L (OPT)%', type='numeric', format=percentage)
                                      ],
                                    style_header={
                                     'backgroundColor': 'grey',
                                     'fontWeight': 'bold'
                                    },
                                    style_cell_conditional=[
                                            {
                                                'if': {'column_id': i},
                                                'textAlign': 'left'
                                            } for i in ['SYMBOL', 'TIMESTAMP','Industry','STRIKE_PR','Lot Size']
                                        ],
                                    style_as_list_view=True,
                                 )
content = html.Div(
    [
        content_first_row,
        content_second_row,
        content_third_row,
        content_fourth_row,
        content_fifth_row
    ],
    style=CONTENT_STYLE
)

# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# app.layout = html.Div([content])
layout = html.Div([content])


@callback(Output('PL_Industry_table', 'data'),
              Input('PL_Buy_Sell_Option', 'value'),
              Input('PL_Strategy_Option', 'value'))
def update_industry_summary_data(Strategy_Stance, Strategy_option):
    print(Strategy_Stance)
    print(Strategy_option)

    if Strategy_Stance == 'Option Buy' and Strategy_option == 'CE Breakout':
        data = master_PL_CE_BO_B_Industry
    elif Strategy_Stance == 'Option Sell' and Strategy_option == 'CE Breakout':
        data = master_PL_CE_BO_S_Industry
    elif Strategy_Stance == 'Option Buy' and Strategy_option == 'CE Breakdown':
        data = master_PL_CE_BD_B_Industry
    else:
        data = master_PL_CE_BD_S_Industry

    return data.to_dict('records')

@callback(Output('PL_table', 'data'),
              Output('PL_table', 'style_data_conditional'),
              Input('PL_Buy_Sell_Option', 'value'),
              Input('PL_Strategy_Option', 'value'))
def update_data(Strategy_Stance, Strategy_option):
    print(Strategy_Stance)
    print(Strategy_option)

    if Strategy_Stance == 'Option Buy' and Strategy_option == 'CE Breakout':
        data = master_PL_CE_BO_B
        style_data_conditional = [
            {
                'if': {
                    'column_id': 'Status',
                },
                'textAlign': 'center'
            },
            {
                'if': {
                    'filter_query': '{Status} = SELL',
                    'column_id': ['Status'],
                },
                'backgroundColor': '#FF4136',
                'color': 'white'

            },
            {
                'if': {
                    'filter_query': '{P/L (EQ)} >0',
                    'column_id': ['P/L (EQ)'],
                },
                'backgroundColor': '#318500',
                'color': 'white'

            },
            {
                'if': {
                    'filter_query': '{P/L (OPT)} >0',
                },
                'backgroundColor': '#318500',
                'color': 'white'

            },
        ]
    elif Strategy_Stance == 'Option Sell' and Strategy_option == 'CE Breakout':
        data = master_PL_CE_BO_S
        style_data_conditional = [
            {
                'if': {
                    'column_id': 'Status',
                },
                'textAlign': 'center'
            },
            {
                'if': {
                    'filter_query': '{Status} = BUY',
                    'column_id': ['Status'],
                },
                'backgroundColor': '#FF4136',
                'color': 'white'

            },
            {
                'if': {
                    'filter_query': '{P/L (EQ)} >0',
                    'column_id': ['P/L (EQ)'],
                },
                'backgroundColor': '#318500',
                'color': 'white'

            },
            {
                'if': {
                    'filter_query': '{P/L (OPT)} >0',
                },
                'backgroundColor': '#318500',
                'color': 'white'

            },
        ]
    elif Strategy_Stance == 'Option Buy' and Strategy_option == 'CE Breakdown':
        data = master_PL_CE_BD_B
        style_data_conditional = [
            {
                'if': {
                    'column_id': 'Status',
                },
                'textAlign': 'center'
            },
            {
                'if': {
                    'filter_query': '{Status} = SELL',
                    'column_id': ['Status'],
                },
                'backgroundColor': '#FF4136',
                'color': 'white'

            },
            {
                'if': {
                    'filter_query': '{P/L (EQ)} >0',
                    'column_id': ['P/L (EQ)'],
                },
                'backgroundColor': '#318500',
                'color': 'white'

            },
            {
                'if': {
                    'filter_query': '{P/L (OPT)} >0',
                },
                'backgroundColor': '#318500',
                'color': 'white'

            },
        ]
    else:
        data = master_PL_CE_BD_S
        style_data_conditional = [
            {
                'if': {
                    'column_id': 'Status',
                },
                'textAlign': 'center'
            },
            {
                'if': {
                    'filter_query': '{Status} = BUY',
                    'column_id': ['Status'],
                },
                'backgroundColor': '#FF4136',
                'color': 'white'

            },
            {
                'if': {
                    'filter_query': '{P/L (EQ)} >0',
                    'column_id': ['P/L (EQ)'],
                },
                'backgroundColor': '#318500',
                'color': 'white'

            },
            {
                'if': {
                    'filter_query': '{P/L (OPT)} >0',
                },
                'backgroundColor': '#318500',
                'color': 'white'

            },
        ]

    return data.to_dict('records'), style_data_conditional


# if __name__ == '__main__':
#     app.run_server(port=8085)