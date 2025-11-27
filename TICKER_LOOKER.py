# THis file can be used to look up the various metrics of many different tickers for comparison
import pandas as pd
import os

def search_tickers_in_files(file_paths, tickers, output_file):
    with open(output_file, 'w') as f:
        for file_path in file_paths:
            try:
                datafile = pd.read_csv(file_path)
    
                matched_rows = pd.DataFrame()
                for ticker in tickers:
                    for column in datafile.columns:
                        if datafile[column].astype(str).str.contains(ticker, case=False, na=False).any():
                            matched_rows = pd.concat([matched_rows, datafile[datafile[column].astype(str).str.contains(ticker, case=False, na=False)]])
                print(matched_rows)
                
                if not matched_rows.empty:
                    # Write file name to the output file
                    f.write(f"File: {os.path.basename(file_path)}\n")
                    # f.write("\n")
                    matched_rows.to_csv(f, index=False)
                    f.write("\n")  

                
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

# File paths from other folders
file_paths = [
    'All_Ratios/ratioAverages/average.csv',
    'All_Ratios/Risk_analysison_Ratios/analyzed_metrics_individual_r2.csv',
    'All_stock/dividends_etc/dividends_analysis.csv',
    'All_Stock/stock_metrics/stocks_analyzed.csv',
    'All_Ratios/ratiotrendyAverages/trendyaverage.csv'
]

tickers = input("Enter the tickers to search for, separated by commas: ").split(',')
tickers = [ticker.strip() for ticker in tickers]  # Remove any extra spaces
# tickers = ["AAPL", "NVDA", "PEP", "KO", "AMZN"] #Example
output_file = "Results_For_Tickers.csv"


search_tickers_in_files(file_paths, tickers, output_file)
