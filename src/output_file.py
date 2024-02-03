import pandas as pd
import sys
import os

current_path = os.path.abspath(__file__)
parent_path = os.path.dirname(current_path)
project_root_path = os.path.dirname(parent_path)
sys.path.append(project_root_path)

import src.data_processing as df_process

def export_file(file_path, export_file_path_input):
    output_file_data = pd.DataFrame()

    if file_path == "":
        return "Empty File Path (Skip export process)"
    if file_path[-1] != '\\':
        file_path = file_path + '\\'
    if len(df_process.df_filter_array) == 0:
        return "Empty Dataset (No need to export)"
    if export_file_path_input == "":
        return "Please Indicate Export File Name"

    output_file_name = file_path + export_file_path_input + ".xlsx"
    if os.path.isfile(output_file_name):
        return "File Already Exist (Ignore export operation)"

    output_file_data = pd.concat(df_process.df_filter_array)
    output_file_data.to_excel(output_file_name, index=False, header=True)
    return "Export Succeed. File Path:" + output_file_name
