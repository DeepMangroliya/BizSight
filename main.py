import argparse
import yaml
import os
from pathlib import Path
from src.utils import write_file_s3, gcp_feed_data
from src.data_analysis_ext import process

# Resolve project root dynamically
PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"

# Parse task argument
args = argparse.ArgumentParser(
    description="Provides some information on the job to process"
)
args.add_argument(
    "-t", "--task", type=str, required=True,
    help="This will point to a task location in the config.yaml file. \
          Then it will follow the steps for this specific task."
)
args = args.parse_args()

# Load the config file
with open(CONFIG_PATH, "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# Fetch the export configuration
config_export = config[args.task]["export"]
export_cfg = config_export[0]["export"]

# Run data process function
df = process()

if df is None:
    raise Exception("❌ DataFrame returned is None. Check your query or DB connection.")

if df is None:
    raise Exception("❌ DataFrame is None. Check your DB, query, or process function.")

# Export result based on config
if export_cfg["host"] == "s3":
    write_file_s3(df, export_cfg["bucket_name"], export_cfg["object_name"])
elif export_cfg["host"] == "gsheet":
    gcp_feed_data(export_cfg["spread_sheet_id"], export_cfg["worksheet_name"], df)
