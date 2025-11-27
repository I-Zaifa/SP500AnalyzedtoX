import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import glob as glob
import os

def getting_R2_for_ratios():

    def random_forest_regression(file):
        datafile = pd.read_csv(file)
        
        ticker_name = os.path.basename(file)
        ticker_name = ticker_name.split("_")[0]
        SYMBL = ticker_name.split("_")[0]


        y_values = datafile.columns[1:-4].tolist() # Ratios
        x_values = datafile.columns[-4:].tolist() # M.E Indicators
        results = {}

        X = datafile[x_values]

        feature_importance_sum = np.zeros(len(x_values))
        r2_score_sum = 0

        for ratio in y_values:
            y = datafile[ratio].values

            model = RandomForestRegressor(n_estimators=700)
            model.fit(X, y)

            r2_score = round(model.score(X,y), 5) # r2 score
            r2_score_sum += r2_score
            
            # This gives feature importance for each category
            feature_importances = model.feature_importances_
            feature_importances = np.round(feature_importances, 5)

            results[ratio] = {r2_score}

            # This sums up the features weights for all categories. ()
            feature_importance_sum += feature_importances

        num_of_ratios = len(y_values)
        r2_score_avg = r2_score_sum/num_of_ratios
        feature_importance_avg = np.round(feature_importance_sum/num_of_ratios, 5)
        fixed_result_dict = {key: next(iter(value)) for key, value in results.items()}
        indicator_dict = {indicator: avg for indicator, avg in zip(x_values, feature_importance_avg)}

        final_dict = {**fixed_result_dict, **indicator_dict}

        final_dataframe = pd.DataFrame([final_dict])
        final_dataframe.insert(0, 'Ticker', SYMBL)

        # This is basically the sum of the R2 score
        final_metric = pd.DataFrame([{'Ticker': [SYMBL], "R2_Sum": r2_score_avg, **indicator_dict}])
        return final_dataframe, final_metric

        

    ### This approach basically gives us the R2 score for each category and the
    ### feeature value of the ME indicators for each category is also given seperatly for
    ### each category but it is all summed up for easier interpretation. 
    ## Otherwise the detail would be too much. Feel free to manipulate the data if it is needed


    file_path = "All_Ratios/Risk_analysison_Ratios/standardized_data/*_standardized_datafile.csv"
    dataframe_list = []
    dataframe_list_final = []
    data_files = glob.glob(file_path)
    for file in data_files:
        print(file, "\n")
        result_seperate, result_final = random_forest_regression(file)
        dataframe_list.append(result_seperate)
        dataframe_list_final.append(result_final)

    # All the stuff in between the concat and csv save is just handling empty cells and/or 0 values

    merged_df = pd.concat(dataframe_list, ignore_index=True)
    merged_df = merged_df.replace("", np.nan)
    merged_df = merged_df[(merged_df != 0).any(axis=1)]
    merged_df = merged_df.dropna(how='all')
    merged_df.to_csv("All_Ratios/Risk_analysison_Ratios/analyzed_metrics_individual_r2.csv", index=False)



    ### Sum of all categories' r2 score and their ME indicators' featues value

    merged_df_final = pd.concat(dataframe_list_final, ignore_index=True)
    merged_df_final = merged_df_final.replace("", np.nan)
    merged_df_final = merged_df_final.dropna(subset=[merged_df_final.columns[1]])
    merged_df_final.to_csv("All_Ratios/Risk_analysison_Ratios/Final_R2_Aggregate.csv", index=False)


# getting_R2_for_ratios()