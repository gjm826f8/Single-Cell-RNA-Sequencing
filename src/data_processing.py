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
def data_process(id_col_name_array, fc_col_name_array, pv_col_name_array):
    df_output_array.clear()

    for i in range(len(file.df_array)):
        df_output = pd.DataFrame()
        for j in file.df_array[i].columns.values:
            if j in id_col_name_array:
                df_output[j] = file.df_array[i][j]
            if j in fc_col_name_array:
                df_output[j] = file.df_array[i][j].round(2)
            if j in pv_col_name_array:
                df_output[j] = file.df_array[i][j].round(3)

            for split_char in split_char_array:
                if split_char in j:
                    str_tmp = j.split(split_char)[j.split(split_char).__len__() - 1]
                    if str_tmp[0:1].strip().isdigit() and str_tmp[0:1].strip() != '0':
                        new_col_name = j[0:j.rindex(split_char)].strip()
                        if new_col_name not in df_output.columns.values:
                            df_output[new_col_name] = file.df_array[i][
                                [col for col in file.df_array[i].columns if new_col_name in col]]\
                                .mean(axis=1, numeric_only=True).round(1)
                            df_output[new_col_name + "_STD"] = file.df_array[i][
                                [col for col in file.df_array[i].columns if new_col_name in col]]\
                                .std(axis=1, numeric_only=True).round(1)
        # df_output.insert(0, "file_name", str(file.df_map[i]).split("\\")[file.df_map[i].split("\\").__len__() - 1])
        df_output.insert(0, "file_name", os.path.split(file.df_map[i])[1])
        df_output_array.append(df_output)

    return df_output_array

def data_filter(id, id_col_name_array):
    warn_msg = ""
    df_filter_array.clear()
    for df in df_output_array:
        for col_name in df.columns.values:
            if col_name in id_col_name_array:
                nan_value_cnt = df[col_name].isnull().sum()
                if nan_value_cnt > 0:
                    warn_msg += df["file_name"][0] + " column [" + col_name + "] has " + str(nan_value_cnt) + " empty values.\n"
                df_filter = df[df[col_name].notnull()]
                df_filter = df_filter[df_filter[col_name].str.lower().str.contains(r'^'+id.lower())]
                df_filter_array.append(df_filter)
                break
    return df_filter_array, warn_msg