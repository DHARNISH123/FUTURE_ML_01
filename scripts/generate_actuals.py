import pandas as pd

# Load the Rossmann train dataset
df = pd.read_csv("data/rossmann/train.csv", parse_dates=["Date"])

# Group by date and sum the sales
daily_sales = df.groupby("Date")["Sales"].sum().reset_index()

# Rename columns to match Prophet's expected format
daily_sales.rename(columns={"Date": "ds", "Sales": "y"}, inplace=True)

# Save to actuals.csv in the same folder as forecast
daily_sales.to_csv("data/actuals.csv", index=False)

print("✅ actuals.csv generated successfully!")
