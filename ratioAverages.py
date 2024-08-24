import pandas as pd
import glob as glob
import os


def get_ratio_averages():

	folder_path = "All_Ratios/ratios/*_ratios.csv"
	datafiles = glob.glob(folder_path)
	# print(datafiles)

	final_files_list = []

	def get_the_averages(file):
		# print(file)
		datafile = pd.read_csv(file, index_col=0)
		datafile = datafile.drop(datafile.index[-1])
		# print(datafile)
		ticker_name = os.path.basename(file)
		ticker_name = ticker_name.split("_")[0]
		# print(ticker_name)

		averages = datafile.mean()
		# print(averages)

		finalfile = pd.DataFrame(averages).transpose()
		finalfile.insert(0, "Ticker", ticker_name)

		return finalfile
		# finalfile.to_csv("average.csv", index=False)


	for file in datafiles:
		result = get_the_averages(file)	
		final_files_list.append(result)

    import os

    # Define the folder path
    main_folder_path = 'All_Ratios/ratioAverages'

    # Check if the folder exists, if not, create it
    if not os.path.exists(main_folder_path):
        os.makedirs(main_folder_path)	

	combine_for_csv = pd.concat(final_files_list, ignore_index=True)
	combine_for_csv.to_csv("All_Ratios/ratioAverages/average.csv", index=False)

