import pandas as pd
import os
import glob as glob
def merge_ratio_me_files():

	def merge_the_files(file):

		ticker_name = os.path.basename(file)
		file_name = ticker_name.split("_")[0]
		# print(file_name)
		directory = 'All_Ratios/Risk_analysison_Ratios/merged_data'

		if not os.path.exists(directory):
			os.makedirs(directory)

		file_name_final = os.path.join(directory, f"{file_name}_merged_datafile.csv")
		# print(file_name_final)

		ratios_datafile = pd.read_csv(file).dropna()
		ratios_datafile.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)

		macro_datafile = pd.read_csv("macroindicators/macroeconomic_data.csv").dropna()
		macro_datafile.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)


		# Get the actual years available in the ratios files

		ratios_datafile["Date"] = pd.to_datetime(ratios_datafile["Date"])
		ratios_datafile["Year"] = ratios_datafile['Date'].dt.year

		the_years_ratios = ratios_datafile.groupby("Year").mean() # Taking mean here doesn't make a difference as the gruop contains only one value
		the_years_ratios.reset_index(inplace=True)

		# Grouping the indicators by the years and taking the averages for their values
		macro_datafile["Date"] = pd.to_datetime(macro_datafile["Date"])
		macro_datafile["Year"] = macro_datafile['Date'].dt.year

		yearly_averages_ME = macro_datafile.groupby("Year").mean()
		yearly_averages_ME.reset_index(inplace=True)

		# Merge all the ratios and the m.e indicators into a single file based on their years with ratios file serving as the basis
		merged_datafile = pd.merge(the_years_ratios, yearly_averages_ME, on="Year", how='left')
		merged_datafile = merged_datafile.drop(columns=['Date_x','Date_y'])
		merged_datafile.reset_index(drop=True, inplace=True)
		merged_datafile.to_csv(file_name_final, index=False)

	file_path = "All_Ratios/ratios/*_ratios.csv"
	data_files = glob.glob(file_path)
	for file in data_files:
		merge_the_files(file)
