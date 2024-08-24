import pandas as pd

def get_top_companies():
    file_path = 'All_Ratios/ratioAverages/average.csv'
    datafile = pd.read_csv(file_path)


    high_performance_categories = [
        'Current Assets', 'Quick Ratio', 'Return On Equity', 'Return On Assets', 
        'Return On Investment', 'Gross Profit Margin', 'Asset Turnover', 
        'Inventory Turnover', 'Receivables Turnover'
    ]

    low_performance_categories = [
        'Debt To Equity Ratio', 'Total Debt To Total Capitalization Ratio', 
        'Debt To Assets Ratio', 'Net Debt To Equity Ratio'
    ]

    relevant_columns = ['Ticker'] + high_performance_categories + low_performance_categories
    datafile_filtered = datafile[relevant_columns]

    # Function to rank the symbols
    def rank_symbols(datafile, categories, ascending=True):
        rankings = datafile[categories].apply(pd.to_numeric, errors='coerce').rank(ascending=ascending)
        return rankings

    # Function used here on both elements
    high_rankings = rank_symbols(datafile_filtered, high_performance_categories, ascending=False)
    low_rankings = rank_symbols(datafile_filtered, low_performance_categories, ascending=True)

    # Combing the rankings into a single score for both categories
    datafile_filtered['High_Performance_Score'] = high_rankings.sum(axis=1)
    datafile_filtered['Low_Performance_Score'] = low_rankings.sum(axis=1)

    # Calculate a final score by summing the high performance and low performance scores
    # This may be a bit unconventional approach
    datafile_filtered['Final_Score'] = datafile_filtered['High_Performance_Score'] + datafile_filtered['Low_Performance_Score']

    top_25_symbols = datafile_filtered.sort_values('Final_Score', ascending=False).head(33)

    # Select the main parts only
    final_companies = top_25_symbols[['Ticker', 'Final_Score']]

    import os

    # Define the folder path
    main_folder_path = 'All_Ratios/ratioAverages'

    # Check if the folder exists, if not, create it
    if not os.path.exists(main_folder_path):
        os.makedirs(main_folder_path)   

    # print(final_companies)
    final_companies = pd.DataFrame(final_companies)
    final_companies.to_csv("All_Ratios/ratioAverages/Top Performing Companies by Ratios.csv", index=False)
    final_companies.to_csv("Top Performing Companies by Ratios.csv", index=False)
