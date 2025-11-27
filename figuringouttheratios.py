import pandas as pd
import glob
import os

def get_ratios_from_bs():

    def get_the_bs_data(file_bs, file_fn, ticker_name):

        datafile_bs = pd.read_csv(file_bs, index_col=0)
        datafile_fn = pd.read_csv(file_fn, index_col=0)

        try:
            current_assets = datafile_bs["Current Assets"]/datafile_bs["Current Liabilities"]
        except Exception as e:
            current_assets = pd.Series([0] * len(datafile_bs), index=datafile_bs.index)
        # print(current_assets.head())

        try:
            quick_ratio = (datafile_bs["Current Assets"] - datafile_bs["Inventory"]) /datafile_bs["Current Liabilities"]
        except Exception as e:
            quick_ratio = pd.Series([0] * len(datafile_bs), index=datafile_bs.index)
        # print("Quick Ratio:\n", quick_ratio)

        try:
            debt_to_equity_ratio = datafile_bs['Total Debt']/datafile_bs["Total Equity Gross Minority Interest"]
        except Exception as e:
            debt_to_equity_ratio = pd.Series([0] * len(datafile_bs), index=datafile_bs.index)
        # print(debt_to_equity_ratio)

        try:
            total_debt_to_total_capitalization_ratio = datafile_bs["Total Debt"]/ datafile_bs["Total Capitalization"]
        except Exception as e:
            total_debt_to_total_capitalization_ratio = pd.Series([0] * len(datafile_bs), index=datafile_bs.index)
        # print(total_debt_to_total_capitalization_ratio)

        try:
            debt_to_assets_ratio = datafile_bs["Total Debt"]/ datafile_bs["Total Assets"]
        except Exception as e:
            debt_to_assets_ratio = pd.Series([0] * len(datafile_bs), index=datafile_bs.index)
        # print(debt_to_assets_ratio)

        try:
            net_debt_to_equity_ratio = datafile_bs["Net Debt"]/ datafile_bs["Total Equity Gross Minority Interest"]
        except Exception as e:
            net_debt_to_equity_ratio = pd.Series([0] * len(datafile_bs), index=datafile_bs.index)
        # print(net_debt_to_equity_ratio)

        try:
            return_on_equity =  datafile_fn["Net Income"]/ datafile_bs["Total Equity Gross Minority Interest"]
        except Exception as e:
            return_on_equity = pd.Series([0] * len(datafile_bs), index=datafile_bs.index)
        
        try:
            return_on_assets =  datafile_fn["Net Income"]/ datafile_bs["Total Assets"]
        except Exception as e:
            return_on_assets = pd.Series([0] * len(datafile_bs), index=datafile_bs.index)
        
        try:    
            return_on_investment =  datafile_fn["Net Income"]/ datafile_bs["Invested Capital"]
        except Exception as e:
            return_on_investment = pd.Series([0] * len(datafile_bs), index=datafile_bs.index)
        # print(return_on_equity, return_on_assets, return_on_investment)
        try:
            gross_profit_margin = datafile_fn["Gross Profit"]/ datafile_fn["Total Revenue"]
        except Exception as e:
            gross_profit_margin = pd.Series([0] * len(datafile_bs), index=datafile_bs.index)

        try:
            asset_turnover = datafile_fn["Total Revenue"] / datafile_bs["Total Assets"]
        except Exception as e:
            asset_turnover = pd.Series([0] * len(datafile_bs), index=datafile_bs.index)

        try:
            inventory_turnover =  datafile_fn["Gross Profit"] / datafile_bs["Inventory"]
        except Exception as e:
            inventory_turnover = pd.Series([0] * len(datafile_bs), index=datafile_bs.index)

        try:
            receivables_turnover =  datafile_fn["Total Revenue"] / datafile_bs["Accounts Receivable"]
        except Exception as e:
            receivables_turnover = pd.Series([0] * len(datafile_bs), index=datafile_bs.index)
        # print(asset_turnover, inventory_turnover, receivables_turnover)

        BigList =  [current_assets, quick_ratio, debt_to_equity_ratio,total_debt_to_total_capitalization_ratio,
            debt_to_assets_ratio,net_debt_to_equity_ratio,return_on_equity,return_on_assets,return_on_investment,
            gross_profit_margin, asset_turnover,inventory_turnover,receivables_turnover]

        savingfile = pd.concat(BigList, axis=1)

        savingfile.columns = ['Current Assets', 'Quick Ratio', 'Debt To Equity Ratio', 'Total Debt To Total Capitalization Ratio',
            'Debt To Assets Ratio', 'Net Debt To Equity Ratio', 'Return On Equity', 'Return On Assets', 
            'Return On Investment', 'Gross Profit Margin', 'Asset Turnover', 'Inventory Turnover', 
            'Receivables Turnover']

        import os

        # Define the folder path
        main_folder_path = 'All_Ratios/ratios'

        # Check if the folder exists, if not, create it
        if not os.path.exists(main_folder_path):
            os.makedirs(main_folder_path)

        savingfile.to_csv(f"All_Ratios/ratios/{ticker_name}_ratios.csv", index=True)

        # return BigList

    folder_path_bs = "maindata/*_balancesheet.csv"
    folder_path_fn = "maindata/*_financials.csv"

    bs_files= glob.glob(folder_path_bs)
    fn_files= glob.glob(folder_path_fn)

    count = 0

    for bs, fn in zip(bs_files, fn_files):
        try:
            file_bs = bs
            file_fn = fn
            filename = os.path.basename(file_bs)
            ticker_name = filename.split('_')[0]
            print(ticker_name)
            get_the_bs_data(file_bs, file_fn, ticker_name=ticker_name)    

        except Exception as e:
            print(f"{ticker_name}: some info not available")
            count += 1

    print(count)

