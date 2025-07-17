from prophet import Prophet
import pandas as pd
import os
import matplotlib.pyplot as plt

def forecast_per_store():
    # Load daily sales data
    df_path = os.path.join('..', 'data', 'rossmann', 'daily_sales.csv')
    df = pd.read_csv(df_path, parse_dates=['ds'])

    # Ensure 'Store' column exists
    if 'Store' not in df.columns:
        raise ValueError("❌ 'Store' column not found in daily_sales.csv")

    # Get unique store IDs
    stores = df['Store'].unique()

    # Create output folders
    export_dir = os.path.join('..', 'export')
    visuals_dir = os.path.join('..', 'visuals')
    os.makedirs(export_dir, exist_ok=True)
    os.makedirs(visuals_dir, exist_ok=True)

    # Forecast for each store
    for store in stores:
        df_store = df[df['Store'] == store][['ds', 'y']]

        # Skip if not enough data
        if len(df_store) < 100:
            print(f"⏩ Skipping store {store}: only {len(df_store)} records.")
            continue

        # Fit Prophet model
        model = Prophet(daily_seasonality=True, yearly_seasonality=True, weekly_seasonality=True)
        model.fit(df_store)

        # Forecast 2 years ahead (730 days)
        future = model.make_future_dataframe(periods=730)
        forecast = model.predict(future)

        # Add Store column to forecast
        forecast['Store'] = store

        # Save forecast to CSV (include Store column)
        output_csv = os.path.join(export_dir, f'forecast_store_{store}.csv')
        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'Store']].to_csv(output_csv, index=False)

        # Save forecast plot
        fig1 = model.plot(forecast)
        output_plot = os.path.join(visuals_dir, f'forecast_store_{store}.png')
        fig1.savefig(output_plot)
        plt.close(fig1)

        print(f"✅ Forecast completed for store {store}")

if __name__ == '__main__':
    forecast_per_store()
