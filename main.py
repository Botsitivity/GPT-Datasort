from math import comb
from operator import truediv
from xml.etree.ElementInclude import include
import pandas as pd
import os
from os import listdir
from os.path import isfile, join
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.getcwd()
include_columns = eval(os.getenv("INCLUDE_COL_NAMES"))
rename_col = os.getenv("RENAME_COL").lower() == "true"
rename_columns = eval(os.getenv("RENAME_COL_NAMES"))
csv_seperator = os.getenv("SEPARATOR")

if (len(include_columns)!=len(rename_columns) and rename_col): raise Exception("INCLUDE_COL_NAMES length does not match RENAME_COL_NAMES length.")

raw_data_files = [f for f in listdir(f"{BASE_DIR}/raw-data") if (isfile(join(f"{BASE_DIR}/raw-data", f)) and f!="placeholder.txt" )]

combined_data = None

for filename in raw_data_files:
    data = pd.read_csv(f"{BASE_DIR}/raw-data/{filename}", sep=csv_seperator)

    if (type(combined_data)!=pd.DataFrame):
        combined_data = data
    else:
        combined_data = pd.concat([data, combined_data])

for col in combined_data.columns.to_list():
    if col not in include_columns:
        combined_data.drop(col, axis=1, inplace=True)

if (rename_col):
    col = {}
    for i in range(0,len(rename_columns)):
        col[include_columns[i]] = rename_columns[i]
    combined_data.rename(columns=col, inplace=True, errors='raise')

combined_data.to_csv(f"{BASE_DIR}/combined.csv", index=None, header=True)