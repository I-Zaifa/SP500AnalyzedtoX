from companydata import get_sp500
from macroeconomic_data import get_macroeconomic_data
from figuringouttheratios import get_ratios_from_bs
from analyze_the_stocks import analyze_the_stocks
from dividends_analyzed import get_all_dividend_data
from ratioAverages import get_ratio_averages
from the_top_ones import get_top_companies
from trendyratioAverages import get_trendy_averages
from the_top_trendy_ones import get_top_trendy_companies
from merging_the_data import merge_ratio_me_files
from standardizing_merged_files import standardizing_the_merged_files
from risk_analysis_on_ratios import getting_R2_for_ratios

# For Forcing Sequential Execution. (Some function within a function was running first)
sp500_done = False
me_done = False
ratios_done = False
stocks_done = False
divs_done = False
avgs_done = False
merge_done = False
r2_done = False



# Enforcing sequential execution
if not sp500_done:
    get_sp500()
    print("\n\n\nDONE WITH 500\n\n\n")
    sp500_done = True

if sp500_done and not me_done:
    try: 
        get_macroeconomic_data()
        print("\n\n\nDONE WITH ME\n\n\n")
    except Exception as e:
        print("You didn't get the API key from fredapi website. SO the code will just skip this part work work with the csv already available. If it isn't, then many things will not give results.")
    me_done = True

if me_done and not ratios_done:
    get_ratios_from_bs()
    print("\n\n\nDONE WITH RATIOS\n\n\n")
    ratios_done = True

if ratios_done and not stocks_done:
    analyze_the_stocks()
    print("\n\n\nDONE WITH STOCKS\n\n\n")
    stocks_done = True

if stocks_done and not divs_done:
    get_all_dividend_data()
    print("\n\n\nDONE WITH DIVS\n\n\n")
    divs_done = True

if divs_done and not avgs_done:
    get_ratio_averages()
    get_top_companies()
    print("\n\n\nDONE WITH AVGS\n\n\n")
    avgs_done = True

if avgs_done and not merge_done:
    merge_ratio_me_files()
    standardizing_the_merged_files()
    print("\n\n\nDONE WITH MERGE AND STANDARDIZATION\n\n\n")
    merge_done = True

if merge_done and not r2_done:
    getting_R2_for_ratios()
    print("\n\n\nDONE WITH R2\n\n\n")
    r2_done = True

