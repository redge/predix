import pandas as pd
import numpy as np
from scipy import stats
from sklearn import datasets, linear_model
from r import RedisManager
from datetime import datetime

    
def change_time(x):
    """ Change 1st value to epoch """
    try:
        x[0] = int((datetime.strptime(str(x[0]).split('.')[0], '%Y-%m-%d %H:%M:%S')).strftime('%s') + '000')
    except:
        pass
    return x


def get_data():

    df1 = pd.read_excel(open('E&T 5 min interval data_updated.xls','rb'), sheetname=0)

    temp = pd.DatetimeIndex(df1['Time'])
    temp = temp - pd.DateOffset(hours=7)
    df1['Date_Time'] = temp

    #The day of the week with Monday=0, Sunday=6
    #object 'Time' -> DatetimeIndex 'Date_Time'
    df1['Date_Time'] = temp
    df1['Day_Of_Week'] = temp.weekday
    df1['Hours'] = temp.hour
    df1['Date'] = temp.date
    #df1['Total_Cost'] = np.nan

    #combine 1.E & 2.E
    df1['kW'] = df1['Total kW 1.E & T (kW)'] + df1['Total kW 2.E & T (kW)']

    df1 = df1.drop(['Total kW 1.E & T (kW)', 'Total kW 2.E & T (kW)', 'Time'], 1)

    #df1.info()
    df20160316 = pd.read_excel(open('Hourly Interval Costs - 3.16-4.6.xlsx','rb'), sheetname=1)
    df20160316 = df20160316.drop(24)

    temp = df20160316['Time stamp'].astype(str)
    temp = temp.set_value(23, '00:00:00')

    temp = '3/16/16 ' + temp
    temp = pd.DatetimeIndex(temp)
    df20160316 = df20160316.drop(['Time stamp', 'RTP cost', 'Demand cost'], axis=1)

    df20160316['Date_Time'] = temp
    df20160316['Day_Of_Week'] = temp.weekday
    df20160316['Hours'] = temp.hour
    df20160316['Date'] = temp.date

    cols = ['Date_Time', 'Day_Of_Week', 'Hours', 'Date', 'Energy + other cost', 'Total Cost']
    df20160316 = df20160316[cols]

    #df20160316.head(60)

    df20160323 = pd.read_excel(open('Hourly Interval Costs - 3.16-4.6.xlsx','rb'), sheetname=2)
    df20160323 = df20160323.drop(24)

    temp = df20160323['Time stamp'].astype(str)
    temp = temp.set_value(23, '00:00:00')

    temp = '3/23/16 ' + temp
    temp = pd.DatetimeIndex(temp)

    df20160323 = df20160323.drop(['Time stamp', 'RTP cost', 'Demand cost'], axis=1)

    df20160323['Date_Time'] = temp
    df20160323['Day_Of_Week'] = temp.weekday
    df20160323['Hours'] = temp.hour
    df20160323['Date'] = temp.date

    cols = ['Date_Time', 'Day_Of_Week', 'Hours', 'Date', 'Energy + other cost','Total Cost']
    df20160323 = df20160323[cols]

    #df20160323.head(24)

    df20160330 = pd.read_excel(open('Hourly Interval Costs - 3.16-4.6.xlsx','rb'), sheetname=3)
    df20160330 = df20160330.drop(24)

    temp = df20160330['Time stamp'].astype(str)
    temp = temp.set_value(23, '00:00:00')

    temp = '3/30/16 ' + temp
    temp = pd.DatetimeIndex(temp)

    df20160330 = df20160330.drop(['Time stamp', 'RTP cost', 'Demand cost'], axis=1)

    df20160330['Date_Time'] = temp
    df20160330['Day_Of_Week'] = temp.weekday
    df20160330['Hours'] = temp.hour
    df20160330['Date'] = temp.date

    df20160330 = df20160330[cols]

    #df20160330.head(24)

    df20160406 = pd.read_excel(open('Hourly Interval Costs - 3.16-4.6.xlsx','rb'), sheetname=4)
    df20160406 = df20160406.drop(24)


    temp = df20160406['Time stamp'].astype(str)
    temp = temp.set_value(23, '00:00:00')

    temp = '4/06/16 ' + temp
    temp = pd.DatetimeIndex(temp)

    df20160406 = df20160406.drop(['Time stamp', 'RTP cost', 'Demand cost'], axis=1)

    df20160406['Date_Time'] = temp
    df20160406['Day_Of_Week'] = temp.weekday
    df20160406['Hours'] = temp.hour
    df20160406['Date'] = temp.date

    df20160406 = df20160406[cols]

    #df20160406.head(24)

    df2 = pd.concat([df20160316, df20160323, df20160330, df20160406], axis=0)

    df2['Total_Cost'] = df2['Total Cost']
    #df2['kW'] = np.nan
    df2 = df2.drop('Total Cost', axis = 1)
    #df2.head(2)
    result = df1.merge(df2, on=['Date_Time','Day_Of_Week','Hours','Date'], how='left')

    dff =result.groupby(pd.TimeGrouper(key='Date_Time', freq='H')).apply(lambda x: x[['kW']].sum())

    df3 = dff.to_frame()
    #df3.info()

    df3.index = df3.index.droplevel(1)
    df3=df3.reset_index()

    df3.columns = ['Date_Time', 'kW']
    df3.head(2)

    df3['Avg_Combined_kW_Hour'] = df3['kW'] / 12

    result = df2.merge(df3, how='left')

    result = result.drop(['kW', 'Date'], axis = 1)

    for i in range(24):
        temp = result.loc[(result['Hours'] == i), 'Avg_Combined_kW_Hour'].median()
        result.loc[result['Avg_Combined_kW_Hour'].isnull() & (result['Hours'] == i), 'Avg_Combined_kW_Hour'] = temp

    df1 = df1.drop(['Date', 'Day_Of_Week'], axis = 1)
    temp = pd.DatetimeIndex(df1['Date_Time'])
    df1['Hour'] = temp.hour

    cols = ['Date_Time','Hour','kW']
    df1 = df1[cols]

    #result.Date_Time.to_pydatetime()
    temp = pd.DatetimeIndex(result['Date_Time'])

    #result(result['Date_Time'].hours)
    #result['Date'] = temp.date.values
    #result.info()
    result['Hour'] = temp.hour

    result = result.drop(['Day_Of_Week'], axis = 1)

    cols1 = ['Date_Time','Hour','Avg_Combined_kW_Hour', 'Total_Cost']
    result1 = result[cols1]

    m1_values = result1.values
    #df2_values.shape

    X1_Fit = m1_values[:,1:3]
    #X_Fit.shape

    Y1_Fit = m1_values[:,3:]
    #Y_Fit.shape

    # prepare model and set parameters
    regr1 = linear_model.LinearRegression()

    # Train the model using the training sets
    regr1.fit(X1_Fit, Y1_Fit)

    cols2 = ['Date_Time','Hour','Avg_Combined_kW_Hour', 'Energy + other cost']
    result2 = result[cols2]

    m2_values = result2.values
    #df2_values.shape

    X2_Fit = m2_values[:,1:3]
    #X_Fit.shape

    Y2_Fit = m2_values[:,3:]
    #Y_Fit.shape

    # prepare model and set parameters
    regr2 = linear_model.LinearRegression()

    # Train the model using the training sets
    regr2.fit(X2_Fit, Y2_Fit)

    df3 = pd.read_excel(open('E&T 5 min interval data_updated.xls','rb'), sheetname=1)
    temp = pd.DatetimeIndex(df3['Time'])

    df3['Date_Time'] = temp
    df3['Hour'] = temp.hour
    df3['kW'] = np.nan

    df3 = df3.drop(['Total kW 1.E & T (kW)', 'Total kW 2.E & T (kW)', 'Time'], axis = 1)

    for i in range(24):
        temp = df1.loc[(df1['Hour'] == i), 'kW'].median()
        df3.loc[df3['Hour'] == i, 'kW'] = temp

    df4 = pd.concat([df3, df1], axis=0)

    df4_values = df4.values
    #df4_values.shape

    X_Model = df4_values[:,1:]
    #X_Model.shape

    Y_hyp1 =  regr1.predict(X_Model)
    Y_hyp2 = regr2.predict(X_Model)

    df4['Cost_W_Demand'] = Y_hyp1
    df4['Cost_WO_Demand'] = Y_hyp2
    df4['Consumed_kW'] = df4['kW']


    df4 = df4.reset_index()

    df4['Solar_kW/m^2'] = 1
    df4['Solar_LUX'] = 1
    df4['Temperature_C'] = 1
    df4['Pressure_HPA'] = 1
    df4['Humidity_%'] = 1
    df4['Wind_Speed_M/S'] = 1
    
    tsConsumed = df4[['Date_Time','Consumed_kW']].values
    tsCostWD = df4[['Date_Time','Cost_W_Demand']].values
    tsCostWOD = df4[['Date_Time','Cost_WO_Demand']].values
    tsSolarP = df4[['Date_Time','Solar_kW/m^2']].values
    tsSolarLux = df4[['Date_Time','Solar_LUX']].values
    tsTemperature = df4[['Date_Time','Temperature_C']].values
    tsPressure = df4[['Date_Time','Pressure_HPA']].values
    tsHumidity = df4[['Date_Time','Humidity_%']].values
    tsWindSpeed = df4[['Date_Time','Wind_Speed_M/S']].values

    tsConsumed = np.apply_along_axis(change_time, axis=1, arr=tsConsumed)
    tsCostWD = np.apply_along_axis(change_time, axis=1, arr=tsCostWD)
    tsCostWOD = np.apply_along_axis(change_time, axis=1, arr=tsCostWOD)
    tsSolarP = np.apply_along_axis(change_time, axis=1, arr=tsSolarP)
    tsSolarLux = np.apply_along_axis(change_time, axis=1, arr=tsSolarLux)
    tsTemperature = np.apply_along_axis(change_time, axis=1, arr=tsTemperature)
    tsPressure = np.apply_along_axis(change_time, axis=1, arr=tsPressure)
    tsHumidity = np.apply_along_axis(change_time, axis=1, arr=tsHumidity)
    tsWindSpeed = np.apply_along_axis(change_time, axis=1, arr=tsWindSpeed)

    red = RedisManager('redis_ryan')
            
    red.setVar('tsConsumed', tsConsumed.tolist())
    red.setVar('tsCostWD', tsCostWD.tolist())
    red.setVar('tsCostWOD', tsCostWOD.tolist())
    red.setVar('tsSolarP', tsSolarP.tolist())
    red.setVar('tsSolarLux', tsSolarLux.tolist())
    red.setVar('tsTemperature', tsTemperature.tolist())
    red.setVar('tsPressure', tsPressure.tolist())
    red.setVar('tsHumidity', tsHumidity.tolist())
    red.setVar('tsWindSpeed', tsWindSpeed.tolist())
