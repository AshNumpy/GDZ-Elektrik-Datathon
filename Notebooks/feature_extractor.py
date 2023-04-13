import pandas as pd 
import numpy as np 

weather=pd.read_csv('./Datasets/weather.csv')

def extractor(df, date_col, weather=weather):
    df[date_col] = pd.to_datetime(df[date_col])
    
    # Extracting date features
    df['Saat'] = df[date_col].dt.hour
    df['Aylık Gün'] = df[date_col].dt.day
    df['Yıllık Gün'] = df[date_col].dt.dayofyear
    df['Haftanın günü'] = df[date_col].dt.day_name()
    df['Hafta'] = df[date_col].dt.week
    df['Ay'] = df[date_col].dt.month
    df['Çeyreklik'] = df[date_col].dt.quarter
    df['Yıl'] = df[date_col].dt.year
    
    # Extracting holiday features
    import holidays
    tr_holidays = holidays.Turkey()
    df['Özel Gün'] = df[date_col].apply(lambda x: x in tr_holidays)
    
    # Extracting seasonality features
    def get_season(month):
        if month >= 3 and month <= 5:
            return 'Spring'
        elif month >= 6 and month <= 8:
            return 'Summer'
        elif month >= 9 and month <= 11:
            return 'Autumn'
        else:
            return 'Winter'
    
    df['Mevsim'] = df[date_col].dt.month.apply(get_season)
    
    # Adding weather features
    weather['date'] = pd.to_datetime(weather['date']).dt.date
    df['date_no_time'] = df[date_col].dt.date
    df = pd.merge(df, weather, left_on='date_no_time', right_on='date', how='left')
    df.drop(['date_no_time','date'], axis=1, inplace=True)
    
    # Extracting weekend features
    import datetime
    def is_weekend(date_str):
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        return 1 if date_obj.weekday() >= 5 else 0
    
    df['Hafta Sonu'] = df[date_col].dt.strftime('%Y-%m-%d').apply(is_weekend)
    
    return df

