import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
from dataiku import SQLExecutor2

# Import the helpers for custom recipes
from dataiku.customrecipe import get_input_names_for_role
from dataiku.customrecipe import get_output_names_for_role
from dataiku.customrecipe import get_recipe_config

# Get input SQL dataset
input_dataset_name = get_input_names_for_role('input_dataset')[0]
input_dataset = dataiku.Dataset(input_dataset_name)

# Get input output dataset
output_dataset_name = get_output_names_for_role('output_dataset')[0]
output_dataset = dataiku.Dataset(output_dataset_name)

my_table = input_dataset.project_key + "_" + input_dataset.short_name

schema = input_dataset.read_schema()
columns = [col["name"] for col in schema]
sorted_cols = sorted(columns)

query = 'SELECT ' + ', '.join(f'"{c}"' for c in sorted_cols) + f' FROM "{my_table}"'

# Write recipe outputs
SQLExecutor2.exec_recipe_fragment(output_dataset, query)
