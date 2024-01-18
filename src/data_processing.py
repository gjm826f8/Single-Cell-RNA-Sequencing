import pandas as pd
import sys
import os

current_path = os.path.abspath(__file__)
parent_path = os.path.dirname(current_path)
project_root_path = os.path.dirname(parent_path)
sys.path.append(project_root_path)

import src.read_file as file

split_char_array = ['-', '_']
df_output_array = []
df_filter_array = []
def data_process(id_col_name_array, fc_col_name_array):
    df_output_array.clear()

    for i in range(len(file.df_array)):
        df_output = pd.DataFrame()
        for j in file.df_array[i].columns.values:
            if j in id_col_name_array:
                df_output[j] = file.df_array[i][j]
            if j in fc_col_name_array:
                df_output[j] = file.df_array[i][j]

            for split_char in split_char_array:
                if split_char in j:
                    str_tmp = j.split(split_char)[j.split(split_char).__len__() - 1]
                    if str_tmp[0:1].strip().isdigit() and str_tmp[0:1].strip() != '0':
                        new_col_name = j[0:j.rindex(split_char)].strip()
                        if new_col_name not in df_output.columns.values:
                            df_output[new_col_name] = file.df_array[i][
                                [col for col in file.df_array[i].columns if new_col_name in col]].mean(axis=1,
                                                                                                  numeric_only=True)
        df_output_array.append(df_output)

    return df_output_array

def data_filter(id, id_col_name_array):
    df_filter_array.clear()
    for df in df_output_array:
        for col_name in df.columns.values:
            if col_name in id_col_name_array:
                df_filter = df[df[col_name] == id]
                df_filter_array.append(df_filter)
                break
    return df_filter_array