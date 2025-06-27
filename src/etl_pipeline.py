import pandas as pd
from pathlib import Path
from utils import get_data

# Build absolute path to the CSV file
PROJECT_ROOT = Path(__file__).resolve().parent.parent
csv_path = PROJECT_ROOT / "data" / "original_data.csv"

# Loading CDNOW dataset
cdnow = get_data(csv_path)

# Stop pipeline if file is missing
if cdnow is None:
    raise FileNotFoundError(f"ETL stopped: Could not find dataset at {csv_path}")

# Create sales table - includes original customer_id
sales_data = pd.DataFrame({
    'customer_id': cdnow['customer_id'],
    'country': cdnow['country'],
    'date': cdnow['date'],
    'product_id': cdnow['product_id']
})

# Creating product table - includes sample price from original data
product_data = pd.DataFrame({
    'product_id': cdnow['product_id'],
    'quantity': cdnow['quantity'],
    'price': cdnow['price'],
    'category': cdnow['product_category']
})

# Converting the DataFrame to csv files
output_dir = PROJECT_ROOT / "data"
sales_data.to_csv(output_dir / "sales.csv", index=False)
product_data.to_csv(output_dir / "products.csv", index=False)

print("✅ ETL process completed. CSVs saved to:", output_dir)
