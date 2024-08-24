import pandas as pd
import glob
import os
import numpy as np
import math

def market_returns():
    """Calculating the market returns using Close price of each stock on the list"""
    
    files_pattern = 'maindata/*_historical.csv'
    # List all files matching the pattern
    files = glob.glob(files_pattern)
    # print(f"Found files: {files}")

    omega_list = []

    for file in files:
        datafile = pd.read_csv(file)
        datafile['Date'] = pd.to_datetime(datafile['Date'], errors='coerce', utc=True)
        datafile['Year'] = datafile["Date"].dt.year
        avg_stocks_per_year = datafile.groupby('Year')['Close'].mean()

        avg_stocks_count = avg_stocks_per_year.shape[0]
        average_returns_list_decimal = [] # not %
        for num in range(avg_stocks_count -1):
            upper_num = num + 1
            average_returns_list_decimal.append((avg_stocks_per_year.iloc[upper_num]-avg_stocks_per_year.iloc[num]) /avg_stocks_per_year.iloc[num])
        # print(average_returns_list_decimal) 
        omega_list.append(average_returns_list_decimal)
    # print(omega_list)

    lenght_of_lists = [len(sublist) for sublist in omega_list]
    avg_len_of_lists = sum(lenght_of_lists) / len(lenght_of_lists)
    avg_len_of_lists = math.ceil(avg_len_of_lists)
    # print(avg_len_of_lists)

    filtered_list = []
    for item in omega_list:
        if len(item) == avg_len_of_lists:
            filtered_list.append(item)

    omega_list = filtered_list        

    
    np_array = np.array(omega_list)
    np_averages = np.mean(np_array, axis=0)
    market_averages = np_averages.tolist()
    
    return market_averages
        

