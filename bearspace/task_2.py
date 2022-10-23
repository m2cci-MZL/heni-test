from __future__ import annotations

import re

import pandas
import pandas as pd
from numpy import NaN

dim_df = pd.read_csv(
    '/home/mehdi/Downloads/Data_Engineer_Scraping_test_-_17-06-21/candidateEvalData/dim_df_correct.csv',
)
df = pandas.DataFrame(columns=['rawDim', 'height', 'width', 'depth'])


def parse_data(index, raw_string: str):
    parsed_values: list = []
    height, width, depth = None, None, None

    # uncomment if you'd like to use 3.10 match-case
    # match _index:
    #     case 0 | 4:
    #         parsed_values = re.findall(r"\d+", raw_string)
    #     case 1:
    #         parsed_values = re.findall(r"\d+,?\d", raw_string)
    #     case 2:
    #         parsed_values = re.findall(r"\d+\.\d", raw_string)
    #     case 3:
    #         parsed_values = re.findall(r"(?<=[Image:\s])\d+\.\d", raw_string)
    if index in (0, 4):
        parsed_values = re.findall(r'\d+', raw_string)
    elif index == 1:
        parsed_values = re.findall(r'\d+,?\d', raw_string)
    elif index == 2:
        parsed_values = re.findall(r'\d+\.\d', raw_string)
    elif index == 3:
        parsed_values = re.findall(r'(?<=[Image:\s])\d+\.\d', raw_string)

    if len(parsed_values) == 2:
        height, width = parsed_values
    else:
        height, width, depth = parsed_values

    return height, width, depth


raw_dict: dict[str, str] = {}
for i, row in dim_df.iterrows():
    raw_dim = row.get('rawDim')
    h, w, d = parse_data(i, raw_dim)
    raw_dict.setdefault(
        i, {'rawDim': raw_dim, 'height': h, 'width': w, 'depth': d},
    )

df = pandas.DataFrame(data=raw_dict.values())
print(df.fillna(NaN))
