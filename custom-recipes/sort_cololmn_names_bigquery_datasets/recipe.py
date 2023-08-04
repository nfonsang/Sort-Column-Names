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
bigquery_table_name = get_recipe_config().get("bigqery_table_name", "")

# Get the schema
schema = input_dataset.read_schema()
schema = pd.DataFrame(schema)
sorted_schema = schema.sort_values(by="name")
column_names = sorted_schema.columns.values
names = sorted_schema["name"].values
types = sorted_schema["type"].values

# Create sorted columns while taking care of writing date type to BigQuery
sorted_columns = []
for i in range(len(names)):
    if "originalSQLType" in column_names:
        sql_type = sorted_schema["originalSQLType"].values
        if sql_type[i] == "DATE":
            cast_col_1 = f"CAST(`{names[i]}` as TIMESTAMP) as {names[i]}"
            sorted_columns.append(cast_col_1)
        else:
            sorted_columns.append(names[i])
    elif "originalType" in column_names:
        original_type = sorted_schema["originalType"].values
        if original_type[i] == "DATE":
            cast_col_1 = f"CAST(`{names[i]}` as TIMESTAMP) as {names[i]}"
            sorted_columns.append(cast_col_1)
        else:
            sorted_columns.append(names[i])
    elif types[i] == "date":
        cast_col_1 = f"CAST(`{names[i]}` as TIMESTAMP) as {names[i]}"
        sorted_columns.append(cast_col_1)
    else:
        sorted_columns.append(names[i])

# Extract BQ dataset and BQ project
client = dataiku.api_client()
project = client.get_default_project()
datasets = project.list_datasets()
dataset_name = input_dataset.short_name
for dataset in datasets:
    if dataset["name"]== dataset_name:
        d = dataset


BQ_dataset = d["params"]["schema"]
BQ_project = d["params"]["catalog"]

# Create query table, then create the query
if bigquery_table_name:
    query_table = f"`{BQ_project}.{BQ_dataset}.{bigquery_table_name}`"
    query = 'SELECT ' + ', '.join(f'{c}' for c in sorted_columns) + f' FROM {query_table}'
else:
    BQ_table = d["projectKey"] + d["params"]["table"].split("}")[1]
    query_table = f"`{BQ_project}.{BQ_dataset}.{BQ_table}`"
    query = 'SELECT ' + ', '.join(f'{c}' for c in sorted_columns) + f' FROM {query_table}'

# In-database execution of query
SQLExecutor2.exec_recipe_fragment(output_dataset, query)