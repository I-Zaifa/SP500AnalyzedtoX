import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import glob as glob

def calculate_r2_score(datafile):
    stock_df = datafile
    stock_df["Date"] = pd.to_datetime(stock_df['Date'], errors='coerce', utc=True)
    stock_df["Year"] = stock_df['Date'].dt.year
    yearly_data = stock_df.groupby("Year")

    stock_df = yearly_data["Close"].mean()
    # print(stock_df)
    # Load the macroeconomic data
    macro_df = pd.read_csv("macroindicators/macroeconomic_data.csv")
    macro_df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)

    # Grouping the indicators by the years and taking the averages for their values
    macro_df["Date"] = pd.to_datetime(macro_df["Date"])
    macro_df["Year"] = macro_df['Date'].dt.year

    macro_df = macro_df.groupby("Year").mean()

    # Merge the dataframes on the 'Year' column
    merged_df = pd.merge(stock_df, macro_df, on='Year')
    
    # Define features (independent variables) and target (dependent variable)
    X = merged_df[['GDP', 'Inflation', 'Unemployment', 'CCI']]
    y = merged_df['Close']
    
    # RFR
    rf_regressor = RandomForestRegressor(n_estimators=1000)
    rf_regressor.fit(X, y)
    y_pred = rf_regressor.predict(X)
    
    # Calculate R2
    r2 = r2_score(y, y_pred)
    
    return r2

