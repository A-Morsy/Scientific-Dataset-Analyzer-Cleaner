# Biodiversity Data Analysis Pipeline

## Description
A comprehensive Python pipeline for analyzing, cleaning, and visualizing biodiversity data from the Centre for Plant Medicine Research (CPMR) dataset.



## Table of Contents

### Prerequisites

Python 3.x

Required Python packages:

```
install pandas numpy matplotlib scipy scikit-learn
```

### Usage

Run the scripts in the following order:

Initial data quality analysis:

```
 data_quality_analyzer.py
```
Generate initial visualizations:

```
 data_visual.py
```
Clean the dataset:

```
 data_cleaner.py
```
Analyze cleaned data:

```
 data_analyzer.py
 ```


Pipeline Steps
1. Data Quality Analysis

Script: data_quality_analyzer.py

Purpose: Analyzes raw data quality

Output: Console report of data quality issues

2. Initial Visualization

Script: data_visual.py

Purpose: Creates initial data visualizations

Output: Distribution plots and heatmaps

3. Data Cleaning

Script: data_cleaner.py

Purpose: Cleans and preprocesses data

Output: cleaned_dataset.csv


4. Final Analysis

Script: data_analyzer.py

Purpose: Analyzes cleaned data

Output: Visualizations in cleaned_data_plots/


## Output Files
Cleaned Data

cleaned_dataset.csv

Visualizations
Located in cleaned_data_plots/:

taxonomic_diversity.png

iucn_distribution.png

temporal_distribution.png

geographic_distribution.png

data_completeness.png



Analysis Reports

Data Quality Metrics

Missing value analysis

Duplicate detection

Data type validation

Format consistency checks

## Biodiversity Analysis

Taxonomic distribution

Conservation status (IUCN)

Temporal patterns

Geographic distribution

Data completeness