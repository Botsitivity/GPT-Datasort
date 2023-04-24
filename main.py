from math import comb
from operator import truediv
from xml.etree.ElementInclude import include
import pandas as pd
import os
from os import listdir
from os.path import isfile, join
from dotenv import load_dotenv
import warnings

warnings.filterwarnings(
    action='ignore',
    message='The error_bad_lines argument has been deprecated',
)

load_dotenv()
BASE_DIR = os.getcwd()
rename_col = os.getenv("RENAME_COL").lower() == "true"
rename_columns = eval(os.getenv("RENAME_COL_NAMES"))
csv_seperator = os.getenv("SEPARATOR")

raw_data_files = [f for f in listdir(f"{BASE_DIR}/raw-data") if (isfile(join(f"{BASE_DIR}/raw-data", f)) and f!="placeholder.txt" )]

for filename in raw_data_files:
    print(filename, end=" - ")
    data = pd.read_csv(f"{BASE_DIR}/raw-data/{filename}", sep=csv_seperator, error_bad_lines=False)

    if (rename_col):
        name1 = data.loc[0, data.columns[0]]
        name2 = data.loc[1, data.columns[0]]

        if (name1 != "Participant" and name2 != "Participant"):
            print(f"{filename} DOES NOT HAVE 'Participant'")

        data.columns = ["name", "line"]

    data.to_csv(f"{BASE_DIR}/output/{filename}", index=None, header=True)
    print("Done")