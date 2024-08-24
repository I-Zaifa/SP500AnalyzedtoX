import pandas as pd
import numpy as np 
import yfinance as yf
from datetime import datetime, timedelta
from market_return import market_returns
import os 
import glob as glob
from r2_score_calculator import calculate_r2_score

def analyze_the_stocks():

    # I don't know how else to handle a confusion with the headers
    file_path_new = "All_Stock/stock_metrics/stocks_analyzed.csv"
    if os.path.exists(file_path_new):
        os.remove(file_path_new)

    def get_stock_metrics(historical):

        datafile = pd.read_csv(historical, header=0)

        ticker_name = historical.split('\\')[-1]
        ticker = ticker_name.split('_')[0]

        print(ticker)

        # Extracting the yearly element
        datafile["Date"] = pd.to_datetime(datafile['Date'], errors='coerce', utc=True)
        datafile["Year"] = datafile['Date'].dt.year
        yearly_data = datafile.groupby("Year")

        # Avg stocks per year and then their mean
        avg_stocks_per_year = yearly_data["Close"].mean()
        avg_stocks_all_time = round(avg_stocks_per_year.mean(),2)
        # print(avg_stocks_all_time)
        # print(avg_stocks_per_year)

        # Increase or decrease over time
        uptown, downtown = 0 , 0
        for stock in avg_stocks_per_year:
            if stock >= avg_stocks_all_time:
                uptown += 1
            else:
                downtown += 1   

        up_or_down = "Increasing" if uptown > downtown else "Decreasing"
        # print(up_or_down)

        # Avg % increase or decrease overtime
        avg_stocks_count = avg_stocks_per_year.shape[0]
        average_current = 0
        average_returns_list = [] # %
        average_returns_list_decimal = [] # not %
        for num in range(avg_stocks_count -1):
            upper_num = num + 1
            average_returns_list.append(((avg_stocks_per_year.iloc[upper_num]-avg_stocks_per_year.iloc[num]) /avg_stocks_per_year.iloc[num]) * 100)
            average_returns_list_decimal.append((avg_stocks_per_year.iloc[upper_num]-avg_stocks_per_year.iloc[num]) /avg_stocks_per_year.iloc[num])
            average_current += ((avg_stocks_per_year.iloc[upper_num]-avg_stocks_per_year.iloc[num]) /avg_stocks_per_year.iloc[num]) * 100
        total_percent_average = round(average_current/(avg_stocks_count -1), 2) 
        # print(total_percent_average)
        # print(average_returns_list_decimal)   

        ## Sharpe Ratio
        # These are borth applied to the % returns nor the actual stocks (I have a degree in finance ffs)
        std_deviation_of_returns = round(np.std(average_returns_list),2)
        mean_of_returns = round(np.mean(average_returns_list),2) # in %
        # print(mean_of_returns, " ", std_deviation_of_returns)

        sharpe_ratio = (mean_of_returns - lastest_rfr_rate) / std_deviation_of_returns
        # print(sharpe_ratio)

        # Calculating the Beta
        returns_df = pd.DataFrame({'Stock': average_returns_list_decimal, 'Market': market_return_list}).dropna()
        covariance_matrix = np.cov(returns_df['Stock'], returns_df['Market'])
        covariance = round(covariance_matrix[0,1],4)
        variance = round(np.var(returns_df["Stock"]),4)
        # print(covariance_matrix, ' ', covariance, ' ', variance)
        beta = round((covariance / variance), 2)
        # print(beta)

        # Calculate r2_score (imports from another file)
        r2_score = calculate_r2_score(datafile)

        results_dict = {}
        results_dict = {
            'Ticker': [ticker],
            'Avg Stock Price All Time': [avg_stocks_all_time],
            'Stock Trend': [up_or_down],
            'Average Returns % (Mean)': [total_percent_average],
            'Standard Deviation': [std_deviation_of_returns],
            'Cov (Stock, Market)': [covariance],
            'Variance (Market)': [variance],
            'Beta': [beta],
            'R2_score (Indicators: GDP, Inf, Unemp, CCI)': [r2_score]
        }

        # print(results_dict)

        import os

        # Define the folder path
        main_folder_path = 'All_Stock/stock_metrics'

        # Check if the folder exists, if not, create it
        if not os.path.exists(main_folder_path):
            os.makedirs(main_folder_path)

        file_path_new = "All_Stock/stock_metrics/stocks_analyzed.csv"
        pd.DataFrame(results_dict).to_csv(file_path_new, mode='a', header=not pd.io.common.file_exists(file_path_new), index=False)




    # Check Risk-Free Rate of US Treasury Bill (Annual)
    ticker_rfr = 'IRX'
    ticker_rfr_data = yf.download(ticker_rfr)
    # pd.DataFrame(ticker_rfr_data).to_csv("All_Stocks/stock_metrics/US Treasury Bills Data.csv", index=False) # If you want to save to a csv file all the 25 year data
    lastest_rfr_rate = round(ticker_rfr_data['Close'].iloc[-360:].mean(),4)
    lastest_rfr_rate = lastest_rfr_rate * 100 # converting to %
    # print(lastest_rfr_rate)

    market_return_list = market_returns()
    market_return_list = [0.2402976592440206, 0.1378557810111676, 0.059002345278998725, 0.23215942293895206, 0.1589180120846856, 0.10679000923590636, 0.09093529767685665, 0.4020466063337753, 0.01979404388508514, 0.05165180374682059]

    lastest_rfr_rate = 0.1031 * 100
    # print(lastest_rfr_rate)
    file_path_hist = glob.glob("maindata/*_historical.csv")

    count_dankula = 1
    for filed in file_path_hist:
        try:
            get_stock_metrics(historical=filed)
        except Exception as e:
            print("Screw Count:", count_dankula)
            count_dankula += 1 



# analyze_the_stocks()