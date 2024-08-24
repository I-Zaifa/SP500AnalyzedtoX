# Metrics, Ratios, Analysis, R2 Scores and others
# Please Read the Documentation.PDF


_(First of all, my deepest apologies for the naming conventions and the folder structure and hierarchy mess)_



### I. Outline:
##### This project automatically takes all the stocks on the s&p500 index as of August, 2024 and does various sorts of analysis on them. These are given as output in the form of csv’s and can also be accessed through flask. The details on all the files are listed below.
##### 

### II. Dependencies Used

    Pandas
    Flask
    yFinance
    FredAPI
    NumPy
    Glob
    Scikit-Learn

### III. Main Methodology & Process

##### 1. Data Collection

    A list of 500 tickers corresponding to the S&P 500 is provided to the yFinance library.
    The data spans from January 2013 to January 2023 (Daily Data) and includes:
        Opening Prices
        Closing Prices
        Volume
        Dividends (quarterly or yearly)
        Stock Splits
    Financial statements (balance sheet, financials, cash flow) were also collected (Yearly Data of 5 years) and saved as CSV files.
    Macroeconomic data was downloaded using the FredAPI, covering indicators such as GDP, Unemployment, Inflation, and CCI over the same 10-year period (Quarterly Data).

###### 2. Stock Metrics Analysis

    Average Stock Price over the past ten years
    Yearly Stock Trend (number of years with increase vs decrease)
    Average Returns (mean)
    Standard Deviation (average deviation from the mean)
    Covariance (Stock, Market) using 'IRX' ticker (US Treasury Bills) as a market proxy
    Variance of each stock
    Beta Calculation (Covariance / Variance) to assess stock performance relative to the market
    R2 Score using a Random Forest Regressor (RFR) based on 10-year averages with macroeconomic indicators as independent variables.

###### 3. Dividend Analysis

    Dividends per Year
    Latest Dividend Paid ($) per Share
    Years Without Dividends (non-cumulative, over 10 years)
    Trend in Dividend Payments (increasing or decreasing)
    Average Dividend Payment
    Dividend Yield (average dividend per year / average stock price)
    Price to Earnings Ratio
    Free Cash (in millions $) to assess the company's ability to cover dividends.

###### 4. Ratio Analysis

Ratios were computed based on balance sheets, financials, and cash flow statements, including:

    Current Assets
    Quick Ratio
    Debt to Equity Ratio
    Total Debt to Total Capitalization Ratio
    Debt to Assets Ratio
    Net Debt to Equity Ratio
    Return on Equity
    Return on Assets
    Return on Investment
    Gross Profit Margin
    Asset Turnover
    Inventory Turnover
    Receivables Turnover

###### 5. Averages & Risk Analysis

    Average Ratios were calculated for each stock over the 5-year period, saved to a single file for ease of comparison.
    Risk Analysis was performed on all ratios, with R2 Scores calculated for each ratio to show the influence of macroeconomic indicators. The results were averaged and saved separately.

###### 6. Flask API

    The SIMPLE_FLASK_API.py script provides a simple Flask API with the to compare various ticks and numerous metrics and analyses. It is straightforward presentation in tables.
    
![Flask1]([https://myoctocat.com/assets/images/base-octocat.svg](https://github.com/I-Zaifa/SP500AnalyzedtoX/blob/main/Flask1.jpg))

!Flask2]([https://myoctocat.com/assets/images/base-octocat.svg](https://github.com/I-Zaifa/SP500AnalyzedtoX/blob/main/Flask2.jpg))    

### IV. All Files Included
##### Main Files to Run:

    MAIN.py: Executes the entire process.
    TICKER_LOOKER.py: For specific ticker lookups.
    SIMPLE_FLASK_API.py: Provides the Flask API.
    Fred_api_key_file.txt: For FredAPI key input.
