from fredapi import Fred
import pandas as pd
import datetime


def get_macroeconomic_data():

    # Request it from the FRED website. Replace it with your own (signup is required)
    # Writing a code to make it easier to initiatlize the key
    with open('fred_api_key_file.txt', 'r') as file:
        fred_api_key = file.read()
        fred_api_key = fred_api_key.replace(' ', '')

    api_key = fred_api_key
    fred = Fred(api_key=api_key)

    # Indicators Required
    indicators = {
        'GDP': 'GDP',
        'Inflation': 'CPIAUCNS', # The Consumer Price Index for All Urban Consumers 
        'Unemployment': 'UNRATE',
        'CCI': 'UMCSENT' # Consumer Confidence Index
    }


    # Define the date range for the past 11 years
    end_date = datetime.datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.datetime.today() - pd.DateOffset(years=11)).strftime('%Y-%m-%d')

    # Fetch data and store in a dictionary
    data = {}
    for name, series_id in indicators.items():
        print(f"Fetching data for {name}...")
        data[name] = fred.get_series(series_id, start_date, end_date)


    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(data)

    import os

    main_folder_path = 'macroindicators'

    # Check if the folder exists, if not, create it
    if not os.path.exists(main_folder_path):
        os.makedirs(main_folder_path)

    df.to_csv('macroindicators/macroeconomic_data.csv', index=True)

    print("Data collection finished for M.E Data, mi amigo")


