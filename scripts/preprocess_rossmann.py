import pandas as pd
import os

def preprocess():
    # Load sales and store data
    sales_path = os.path.join('..', 'data', 'rossmann', 'train.csv')
    store_path = os.path.join('..', 'data', 'rossmann', 'store.csv')
    
    df_sales = pd.read_csv(sales_path, parse_dates=['Date'])
    df_store = pd.read_csv(store_path)

    # ✅ Check Store column exists in both
    if 'Store' not in df_sales.columns or 'Store' not in df_store.columns:
        raise ValueError("❌ 'Store' column missing in input CSV files.")

    # Merge on Store
    df = df_sales.merge(df_store, on='Store', how='left')

    # Filter: Keep only open stores (if column exists)
    if 'Open' in df.columns:
        df = df[df['Open'] == 1]
    else:
        print("⚠️ 'Open' column not found. Skipping store open filter.")

    # Select relevant columns
    df = df[['Store', 'Date', 'Sales']].rename(columns={'Date': 'ds', 'Sales': 'y'})

    # ✅ Print column names to confirm
    print("✅ Columns in final DataFrame:", df.columns.tolist())

    # Save to CSV
    output_dir = os.path.join('..', 'data', 'rossmann')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'daily_sales.csv')
    df.to_csv(output_path, index=False)

    print("✅ daily_sales.csv generated at:", output_path)

if __name__ == '__main__':
    preprocess()
