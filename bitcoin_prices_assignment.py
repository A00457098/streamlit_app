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
    else:
        print(req.status_code)
    return df

def plot_line_chart():
    fig, ax = plt.subplots()
    plt.grid()
    ax.plot(df_date, df_prices)
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmax=days)
    # Axis multiplier
    multiplier = 12

    # Set a tick on each integer multiple
    locator = plt.MultipleLocator(multiplier)

    # Set the locator of the major ticker
    ax.xaxis.set_major_locator(locator)

    st.pyplot(fig)

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

    df['date']=pd.to_datetime(df['date'],unit='ms')
    df_date=df['date'].dt.strftime("%d-%b")


    df_prices=df['prices']

    if currency=="usd":
        df['prices'] = df['prices'].apply(lambda x: x/1.2613)
    elif currency=="inr":
        df['prices'] = df['prices'].apply(lambda x: x*60)


    df['date']=df['date'].apply(lambda x:(x-datetime(2022,1,1)).days)
    
    #Step 3: Plot linechart
    plot_line_chart()
    
    #Step4: Calculate mean price

    df_mean = df['prices'].mean()
    str_to_display= f'Average price during this time was: {df_mean} in {currency}'
    st.text(str_to_display)
    









