# 📊 AI Sales Forecasting Dashboard

A complete time series forecasting solution built for real-world retail analytics. This internship project applies machine learning to historical sales data, generating future forecasts using **Facebook Prophet**, and presenting results in a clean and interactive dashboard built with **Plotly Dash**.

---

## 🎯 Project Objective

To help retail businesses like Rossmann plan ahead, manage inventory, and optimize operations through accurate **sales forecasting**. This end-to-end solution cleans and analyzes sales data, applies a forecasting model, and visualizes results with clarity for stakeholders.

---

## ✅ What This Project Does

- Cleans and structures **daily historical sales data** from Rossmann stores.
- Builds **individual Prophet models per store** to account for local trends and seasonality.
- Forecasts **2 years ahead** of daily sales using Facebook Prophet.
- Generates **interactive Dash dashboard** to explore:
  - Actual vs Forecasted sales
  - Store-wise comparisons
  - Trends, spikes, and low seasons
- Outputs:
  - Forecast CSV files per store (`/export`)
  - Forecast visual plots (`/visuals`)

---

## 🛠️ Tools & Technologies Used

| Tool           | Purpose                            |
|----------------|------------------------------------|
| `Python`       | Programming, model training        |
| `Prophet`      | Time series forecasting            |
| `Pandas`       | Data preprocessing                 |
| `Dash`         | Web dashboard visualization        |
| `Matplotlib`   | Static plot export                 |
| `VS Code`      | Development environment            |
| `Git + GitHub` | Version control                    |

---

## 📁 Project Structure

rossmann-forecast-dashboard/
│
├── dashboard/
│ ├── app.py # Dash web dashboard
│ └── data/ # Final actuals and forecast CSVs
│
├── scripts/
│ ├── forecast_rossmann.py # Forecasts all stores using Prophet
│ ├── preprocess_rossmann.py # Preprocessing sales data
│ └── generate_actuals.py # Merges actual sales for visualization
│
├── data/
│ ├── rossmann/
│ │ ├── daily_sales.csv # Main processed time series
│ │ ├── store.csv # Store metadata
│ │ ├── train.csv / test.csv
│
├── export/ # Store-wise forecast output CSVs
├── visuals/ # Plots of forecast per store
├── notebooks/ # Jupyter EDA and modeling
│ └── rossmann_forecast.ipynb
│
├── requirements.txt # Python packages
└── README.md # Project overview (this file)

yaml
Copy
Edit

---

## 🚀 How to Run the Project

### 1. 📦 Install dependencies
Make sure you have Python 3.8+ and run:

```bash
pip install -r requirements.txt
2. ⚙️ Run Forecasting Script
This will generate 2-year forecasts and save plots.

bash
Copy
Edit
python scripts/forecast_rossmann.py
3. 📊 Launch the Dashboard
bash
Copy
Edit
cd dashboard
python app.py
Open http://127.0.0.1:8050 in your browser.

📌 Features
📈 Time Series Forecasting: 2-year prediction using Facebook Prophet

🏪 Per-Store Forecasting: Each store is modeled individually

📊 Interactive Dashboard: Select stores, view forecasts vs actuals

🧠 Business Insights: Spot seasonality, promotions, and trends

💾 Auto-generated Plots & CSVs for analysis or reporting

📈 Sample Use Cases
Retail Analysts: Estimate inventory needs by store

Marketing Teams: Identify high/low seasons

Management: Visualize long-term trends

Consultants: Present data-driven strategy proposals

📦 Dataset Used
Based on the Rossmann Store Sales dataset on Kaggle:

Daily sales data per store

Store metadata, holidays, and promotions

🧠 Business Recommendations (Example)
Stores with consistent holiday dips may benefit from localized promotions.

Some stores show strong year-end surges — stock early.

Underperforming locations identified for operational review.

🧰 Forecasting Techniques
Facebook Prophet:

Captures daily, weekly, and yearly seasonality

Robust to outliers and holiday effects

Cleaned and prepared using pandas, numpy

Trained per store for accurate micro-trend modeling

✨ Sample Dashboard View

📍 Next Steps
Integrate this with Power BI using Python scripts or export CSVs

Explore other models (ARIMA, XGBoost)

Automate dashboard deployment (Render or Heroku)

📚 Resources
Prophet Documentation

Rossmann Kaggle Competition

Dash by Plotly

👨‍💼 About the Internship Task
This project is part of a real-world analytics internship to showcase:

Business-oriented forecasting

Machine learning for sales predictions

Data storytelling for decision makers

yaml
Copy
Edit

---

## ✅ Next Steps

Would you like me to:

1. ✅ Bundle your entire project with this `README.md` into a `.zip`?
2. ✅ Push your code to a GitHub repository for you?
3. ✅ Help you connect Dash to **Power BI** if needed?

Let me know, and I’ll assist immediately.