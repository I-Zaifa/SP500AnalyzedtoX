import pandas as pd 
from sklearn.preprocessing import StandardScaler
import os
import glob as glob

def standardizing_the_merged_files():

	def standardizing_the_data(file):

		file_name = file.split("/")[0]
		# print(file_name)
		ticker_name = os.path.basename(file)
		file_name = ticker_name.split("_")[0]
		# print(file_name)
		directory = 'All_Ratios/Risk_analysison_Ratios/standardized_data'

		if not os.path.exists(directory):
			os.makedirs(directory)

		file_name_final = os.path.join(directory, f"{file_name}_standardized_datafile.csv")

		datafile = pd.read_csv(file)

		featues_to_standardize = datafile.columns.tolist()
		# print(featues_to_standardize)

		scaler = StandardScaler()

		try:
			datafile[featues_to_standardize] = scaler.fit_transform(datafile[featues_to_standardize])
			datafile.to_csv(file_name_final, index=False)
		except Exception as e:
			pass # Data didn't contain any rows
		# print(datafile)
		
		
	# Loop over all files. This glob thing is B-E-A-utiful
	file_path = "All_Ratios/Risk_analysison_Ratios/merged_data/*_merged_datafile.csv"
	data_files = glob.glob(file_path)
	for file in data_files:
		standardizing_the_data(file)
	