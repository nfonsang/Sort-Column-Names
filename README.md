# Description 
This plugin contains different tools for preparing your data

# How to Set up
When installing the plugin in DSS, you will be prompted to build its code environment. Note that this plugin requires one of these Python versions:  Python 3.6, Python 3.7, Python 3.8, Python 3.9, Python 3.10, Python 3.11.

# How to Use
- In your DSS project flow, click on a dataset to select it, then click on the DataPrep-Add-ons plugin on the right panel in the plugin recipe section.
- select the component you need for your data preparation and proceed until you create and run the recipe.

# Plugin Components
This plugin currently has two components:
## Sort Column Names for any Dataset
This recipe component can use any DSS dataset as input. The recipe runs just like a Python recipe. Hence the recipe component can run using a local execution or containerized execution. 
## Sort Column Names - SQL Datasets Only
This recipe component can use only an SQL dataset as input. The recipe is executed with the SQL execution engine. The SQL execution engine could be more efficient for larger datasets than the DSS local execution engine. 

# License
This plugin is distributed under the [Apache License version 2.0.](https://github.com/nfonsang/DataPrep-Add-ons/blob/main/LICENSE)
	
