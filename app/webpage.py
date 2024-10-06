import sys
import os
import streamlit as st
from datetime import datetime

current_path = os.path.abspath(__file__)
parent_path = os.path.dirname(current_path)
project_root_path = os.path.dirname(parent_path)
sys.path.append(project_root_path)

from src.read_file import getFileFromPath, get_sheetnames_xlsx, read_file, get_file_sheet_map, df_map
from src.data_processing import data_process, data_filter, df_filter_array
from src.config import read_config, write_config
from src.output_file import export_file



st.sidebar.header("Filter by Gene/Protein ID")

file_path_array, id_array, fc_array, pv_array = read_config()

# Initialization
if "reload_file" not in st.session_state:
    st.session_state.reload_file = False
def change_file_path():
    st.session_state.reload_file = True

file_path_select = st.sidebar.selectbox(
        "Folder Path", file_path_array, on_change=change_file_path
    )
if file_path_select == "Enter yourself":
    file_path_input = st.sidebar.text_input(
        "Please enter the folder path", "", on_change=change_file_path
    )
    file_path = file_path_input
    if len(file_path_input) != 0 and file_path_input not in file_path_array:
        write_config("filepath", file_path_input)
        file_path_array.append(file_path_input)
else:
    file_path_input = st.sidebar.text_input(
        "Please enter the folder path", "", disabled=True
    )
    file_path = file_path_select

export_file_path_input = st.sidebar.text_input(
        "Export File Name", "Output"
    )
if st.sidebar.button("Export Data"):
    rst_msg = export_file(file_path, export_file_path_input)
    st.sidebar.info(rst_msg)

st.sidebar.header("Files' Name List:")

multiselect_key = 0
if file_path:
    if st.session_state.reload_file:
        file_name_array = getFileFromPath(st, file_path)
        st.session_state.file_name_array = file_name_array
    else:
        file_name_array = st.session_state.file_name_array

    sheet_select_map = {}
    with st.sidebar.form("files and sheet form"):
        for file_name in file_name_array:
            if st.session_state.reload_file:
                sheet_array = get_sheetnames_xlsx(file_name)
                st.session_state[file_name] = sheet_array
            else:
                sheet_array = st.session_state[file_name]
            sheet_select = st.multiselect(file_name, sheet_array, default=sheet_array, key=file_name+"\\"+str(multiselect_key))
            sheet_select_map[file_name] = sheet_select
            multiselect_key += 1
        # Every form must have a submit button.
        submitted = st.form_submit_button("Read Data")
        if submitted:
            sheet_count = get_file_sheet_map(sheet_select_map)
            read_file(file_path)
            # display sheet number read
            st.write('Last read file sheet number:', str(sheet_count))
            # displays time
            st.write('Last read data time:', str(datetime.now()))
    st.session_state.reload_file = False

    # display selected sheet number
    # selected_sheet_count = 0
    # for key in sheet_select_map:
    #     print(sheet_select_map)
    #     selected_sheet_count += len(sheet_select_map[key])
    # st.sidebar.write('Selected file sheet number:', str(selected_sheet_count))


col1, col2 = st.columns(2)

with col2:
    new_id_col_name = st.text_input(
        "Enter a new ID column name", ""
    )
if len(new_id_col_name) != 0 and new_id_col_name not in id_array:
    write_config("id", new_id_col_name)
    id_array.append(new_id_col_name)
with col1:
    id_col_name = st.multiselect(
        "Gene/Protein ID column name", id_array
    )

with col2:
    new_fc_col_name = st.text_input(
        "Enter a new Fold Change column name", ""
    )
if len(new_fc_col_name) != 0 and new_fc_col_name not in fc_array:
    write_config("fc", new_fc_col_name)
    fc_array.append(new_fc_col_name)
with col1:
    fc_col_name = st.multiselect(
        "Fold Change column name", fc_array
    )

with col2:
    new_pv_col_name = st.text_input(
        "Enter a new P-Value column name", ""
    )
if len(new_pv_col_name) != 0 and new_pv_col_name not in pv_array:
    write_config("pv", new_pv_col_name)
    pv_array.append(new_pv_col_name)
with col1:
    pv_col_name = st.multiselect(
        "P-Value column name", pv_array
    )

id = st.text_input(
    "Gene/Protein ID (Not case sensitive)(Unique Value or Prefix, ex. Cetn4 / Cetn)",""
)

if st.button("Filter Dataset", type="primary"):
    if len(id_col_name) == 0:
        st.error("Please indicate Gene/Protein ID column name")
    # if len(fc_col_name) == 0:
    #     st.error("Please indicate Fold Change column name")
    if len(id) == 0:
        st.error("Please indicate Gene/Protein ID")
    data_process(id_col_name, fc_col_name, pv_col_name)
    df_array, warn_msg = data_filter(id, id_col_name)
    st.info(warn_msg)


for idx in range(len(df_filter_array)):
    # st.markdown("###" + df_map + "###")
    st.write(df_filter_array[idx])