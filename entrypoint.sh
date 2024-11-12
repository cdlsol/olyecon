#!/bin/bash
set -e  # Exit on error

echo "Starting ETL process..."
python /app/python/extract_data.py \
  --user root \
  --password root \
  --host pgdatabase \
  --port 5432 \
  --db olympics24db \
  --table olyecon \
  --csv_path /app/olympics-economics.csv

if [ $? -eq 0 ]; then
    echo "ETL process completed successfully"
    echo "Starting Shiny app..."
    exec python -m shiny run --host 0.0.0.0 --port 35603 --reload /app/python/app.py
else
    echo "ETL process failed"
    exit 1
fi