import pandas as pd
import glob
import os
import numpy as np

def get_all_dividend_data():


    def get_dividend_data(historical, financial, cashflow, file_path_new):
        datafile = pd.read_csv(historical, header=0)
        datafile_fn = pd.read_csv(financial, header=0)
        datafile_cf = pd.read_csv(cashflow, header=0)

        ticker_name = historical.split('_')[0]
        ticker = ticker_name.split('\\')[1]
        # print(ticker)

        # Extracting the yearly element
        datafile["Date"] = pd.to_datetime(datafile['Date'], errors='coerce', utc=True)
        datafile["Year"] = datafile['Date'].dt.year
        # print(datafile["Year"])
        yearly_data = datafile.groupby("Year")

        # How many dividends paid per year
        dividends_count = yearly_data['Dividends'].apply( lambda x : ( x > 0).sum() )
        dividends_count = dividends_count.mean()
        dividends_count = round(dividends_count,2)
        # print(dividends_count)

        # Checking the lastest dividend value paid out
        latest_year = datafile['Year'].max()
        latest_year_data = yearly_data.get_group(latest_year)
        latest_dividend = latest_year_data["Dividends"].max()
        # print(latest_dividend)

        # Check to see if any years skipped for paying dividends (deferred or retained)
        dividends_averages = yearly_data['Dividends'].apply(lambda x: x[x>0].mean()) # Excluding 0 values
        dividends_averages = round(dividends_averages, 4)
        # print(dividends_averages.iloc[0])

        skipped_years = 0
        upp = 0
        number_of_rows = dividends_averages.shape[0]
        # print(number_of_rows)

        for ity in range(number_of_rows):
            if np.isnan(dividends_averages.iloc[upp]):
                upp += 1
                skipped_years +=1
        # print(skipped_years)
        
        

        # Increase in the % of the dividends from year to year
        div_percent_change = dividends_averages.pct_change() * 100
        div_percent_change_mean = round(div_percent_change.mean(),4)
        percent_up_or_down = "Increasing" if div_percent_change_mean >= div_percent_change.max() else "Decreasing"
        # print(percent_up_or_down)

        # 10 year avg of dividends paid out
        all_year_div_avg = round(dividends_averages.mean(), 2)
        # print(all_year_div_avg)

        ##################################

        # Calculating Dividend Yield in %

        stock_average_yearly = yearly_data['Close'].apply(lambda x: x[x>0].mean())
        # print(stock_average_yearly)
        dividend_yield =  round((dividends_averages /stock_average_yearly) * 100, 4)
        dividend_yield = round(dividend_yield.mean(), 2)
        # print(dividend_yield)

        # Calculating Price-to-Earnings Ratio for 5 years

        EPS_mean = datafile_fn["Basic EPS"].mean()
        num_years = datafile_fn.shape[0]
        N = -1
        collection = 0
        for year in range(num_years):
            collection += stock_average_yearly.iloc[N]
            N -= 1

        price_to_earnings = round((collection / num_years), 2) # to get the aveage of the stocks only for the number of years that the EPS data is available
        # print(price_to_earnings) 

        # Free Cash Flow to see if dividends can be covered (In millions)
        free_cash_flow = datafile_cf["Free Cash Flow"].mean()
        free_cash_flow = free_cash_flow / 1000000
        # print(free_cash_flow)


        results_dict = {}
        results_dict = {
            'Ticker (10Y Data)': [ticker],
            'Dividends Count (Per Year)': [dividends_count],
            'Latest Dividend': [latest_dividend],
            'Years Dividend Unpaid': [skipped_years],
            'Dividend Percentage Increasing Or Decreasing': [percent_up_or_down],
            'All Years Avg Dividend': [all_year_div_avg],
            'Dividend Yield (%)': [dividend_yield],
            'Price-to-Earnings Ratio': [price_to_earnings],
            'Free Cash Flow (Million $)': [free_cash_flow]
        }

        import os

        # Define the folder path
        main_folder_path = 'All_Stock/dividends_etc'

        # Check if the folder exists, if not, create it
        if not os.path.exists(main_folder_path):
            os.makedirs(main_folder_path)

        pd.DataFrame(results_dict).to_csv(file_path_new, mode='a', header=not pd.io.common.file_exists(file_path_new), index=False)

        # return results_dict

    file_path_new = "All_Stock/dividends_etc/dividends_analysis.csv"
    if os.path.exists(file_path_new):
        os.remove(file_path_new)

    file_path_hist = glob.glob("maindata/*_historical.csv")
    file_path_fn = glob.glob("maindata/*_financials.csv")
    file_path_cf = glob.glob("maindata/*_cashflow.csv")

    count_dankula = 1
    for file_path_hist, file_path_fn, file_path_cf in zip(file_path_hist, file_path_fn, file_path_cf):
        try:
            get_dividend_data(historical=file_path_hist, financial=file_path_fn, cashflow=file_path_cf, file_path_new=file_path_new)
        except Exception as e:
            # print("Screw Count:", count_dankula)
            print(f"Error: {e}")
            count_dankula += 1 

# get_all_dividend_data()            