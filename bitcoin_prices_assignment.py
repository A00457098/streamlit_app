"""
This program creates an interactive Streamlit app that plots bitcoin prices for
various currencies over the given timeframe and calculates the average price.

@author: Radhika Suri: A00457098
"""

import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime

def get_data(payload: dict):
    
    api_url ='https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
    req=requests.get(api_url, params=payload)
   
    df = None
    if req.status_code == 200:
        json_data = req.json()
        data=json_data['prices']
        df=pd.DataFrame(data,columns=['date','prices'])
        df = pd.DataFrame(json_data['prices'], columns=['Date', currency])
    else:
        print(req.status_code)
    return df


#Step 1: get data

st.header("Bitcoin prices")
days=st.slider("No of days",1,365,90)
currency = st.radio("Currency: ", ('cad', 'usd','inr'))

payload = {'vs_currency': currency, 'days': days, 'interval': 'daily'}

df = get_data(payload)

if df is not None:
    #Step 2: Create dataframe
    #API returns prices and dates (in Unix epoch format). Use pandas to
    #convert the timestamp to human-readable dates
    
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df = df.set_index('Date')
    df_mean = df[currency].mean()
    
    #step3: Plot line chart
    st.line_chart(df[currency])

    str_to_display= f'Average price during this time was: {df_mean} in {currency}'
    st.text(str_to_display)
    
