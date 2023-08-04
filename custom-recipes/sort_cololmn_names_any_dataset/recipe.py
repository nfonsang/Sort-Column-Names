import dataiku
import pandas as pd, numpy as np

# Import the helpers for custom recipes
from dataiku.customrecipe import get_input_names_for_role
from dataiku.customrecipe import get_output_names_for_role
from dataiku.customrecipe import get_recipe_config

# Get input dataset
input_dataset_name = get_input_names_for_role('input_dataset')[0]
input_dataset = dataiku.Dataset(input_dataset_name)

# Get input output dataset
output_dataset_name = get_output_names_for_role('output_dataset')[0]
output_dataset = dataiku.Dataset(output_dataset_name)

input_dataset_df = input_dataset.get_dataframe()
sorted_columns_data_df = input_dataset_df[sorted(input_dataset_df.columns)]

# Write recipe outputs
output_dataset.write_with_schema(sorted_columns_data_df)