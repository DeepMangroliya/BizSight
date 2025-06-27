#!/bin/bash

# load data from csv files into a database
echo "Creating raw database......."
python src/database.py -dbn True -db "raw"

# normalize and clean data, and upload to database
echo "Creating table & uploading data......."
python src/database.py -db "raw" -t "upload-to-database"

echo "Running ETL......."
python src/etl_pipeline.py

echo "Creating processed database......."
python src/database.py -dbn True -db "refined"

echo "Creating table & uploading data......."
python src/database.py -db "refined" -t "cleaned-upload-to-database"

# train and evaluate machine learning models
echo "Extracting data & uploading to S3......."
python main.py -t "data_analysis_ext"

echo "Running modelling & uploading to gsheet......."
python main.py -t "modeling"
