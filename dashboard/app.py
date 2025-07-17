import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import os

# Paths
EXPORT_DIR = os.path.join("..", "export")
ACTUALS_PATH = os.path.join("data", "actuals.csv")

# Load all forecasts
forecast_files = [f for f in os.listdir(EXPORT_DIR) if f.startswith("forecast_store_") and f.endswith(".csv")]
forecast_list = [pd.read_csv(os.path.join(EXPORT_DIR, f), parse_dates=['ds']) for f in forecast_files]
forecast = pd.concat(forecast_list, ignore_index=True)

# Load actuals
actuals = pd.read_csv(ACTUALS_PATH, parse_dates=['ds'])

# Clean
forecast['Store'] = forecast['Store'].astype(str)
actuals['Store'] = actuals['Store'].astype(str)

# Merge actuals and forecast
merged = pd.merge(forecast, actuals, on=["ds", "Store"], how="left")
merged['Month'] = merged['ds'].dt.to_period('M').astype(str)
merged['Year'] = merged['ds'].dt.year

# App initialization
app = dash.Dash(__name__)
app.title = "Rossmann Forecast Dashboard"

app.layout = html.Div([
    html.H2("📊 Rossmann Sales Forecast Dashboard", style={'textAlign': 'center', 'color': '#007bff'}),

    html.Div([
        dcc.Dropdown(
            id='store-dropdown',
            options=[{'label': s, 'value': s} for s in sorted(merged['Store'].unique())],
            value=merged['Store'].unique()[0],
            clearable=False,
            style={'width': '300px'}
        ),
        html.Div(style={'display': 'inline-block', 'marginLeft': '40px'}, children=[
            html.Label("📅 Date Range"),
            dcc.DatePickerRange(
                id='date-picker',
                start_date=merged['ds'].min(),
                end_date=merged['ds'].max()
            )
        ]),
        html.Div(style={'display': 'inline-block', 'marginLeft': '40px'}, children=[
            html.Label("🌓 Theme"),
            dcc.RadioItems(
                id='theme-toggle',
                options=[
                    {'label': 'Light', 'value': 'light'},
                    {'label': 'Dark', 'value': 'dark'}
                ],
                value='light',
                labelStyle={'display': 'inline-block', 'marginRight': '10px'}
            )
        ]),
    ], style={'padding': '20px'}),

    html.Div([
        html.Button("⬇️ Download Forecast", id="download-button"),
        dcc.Download(id="download-forecast")
    ], style={'padding': '10px'}),

    html.Div(id='insight-cards', style={'display': 'flex', 'gap': '20px', 'justify-content': 'center'}),

    dcc.Graph(id='sales-forecast-graph'),
    html.Div(id="metrics", style={'textAlign': 'center', 'padding': '10px'}),

    html.Div([
        dcc.Graph(id='monthly-comparison'),
        dcc.Graph(id='yearly-comparison')
    ], style={'display': 'flex', 'gap': '40px', 'padding': '20px'}),

    html.Footer("© 2025 Rossmann Forecast", style={'textAlign': 'center', 'fontSize': '12px', 'padding': '20px', 'color': '#aaa'})
])


@app.callback(
    Output('insight-cards', 'children'),
    Input('store-dropdown', 'value')
)
def update_insights(store):
    df = merged[merged['Store'] == str(store)]
    last30 = df[df['ds'] >= df['ds'].max() - pd.Timedelta(days=30)]
    avg_actual = round(last30['y'].mean(), 2) if not last30['y'].isna().all() else 0
    avg_forecast = round(last30['yhat'].mean(), 2)
    trend = "📈 Upward" if avg_forecast > avg_actual else "📉 Downward"
    return [
        html.Div([html.H4("Avg Actual (30d)"), html.P(f"{avg_actual:,.0f}")],
                 style={'backgroundColor': '#e3f2fd', 'padding': '15px', 'borderRadius': '8px'}),
        html.Div([html.H4("Avg Forecast (30d)"), html.P(f"{avg_forecast:,.0f}")],
                 style={'backgroundColor': '#e8f5e9', 'padding': '15px', 'borderRadius': '8px'}),
        html.Div([html.H4("Trend"), html.P(trend)],
                 style={'backgroundColor': '#fff3e0', 'padding': '15px', 'borderRadius': '8px'})
    ]


@app.callback(
    Output('sales-forecast-graph', 'figure'),
    Output('metrics', 'children'),
    Output('monthly-comparison', 'figure'),
    Output('yearly-comparison', 'figure'),
    Input('store-dropdown', 'value'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('theme-toggle', 'value')
)
def update_graphs(store, start_date, end_date, theme):
    df = merged[(merged['Store'] == str(store)) &
                (merged['ds'] >= pd.to_datetime(start_date)) &
                (merged['ds'] <= pd.to_datetime(end_date))]

    template = 'plotly_dark' if theme == 'dark' else 'plotly_white'

    fig1 = go.Figure([
        go.Scatter(x=df['ds'], y=df['yhat'], name='Forecast', line=dict(color='blue')),
        go.Scatter(x=df['ds'], y=df['y'], name='Actual', line=dict(color='black')),
        go.Scatter(x=df['ds'], y=df['yhat_upper'], name='Upper Bound', line=dict(width=0)),
        go.Scatter(x=df['ds'], y=df['yhat_lower'], fill='tonexty', name='Lower Bound',
                   line=dict(width=0), fillcolor='rgba(173,216,230,0.3)')
    ])
    fig1.update_layout(title="Forecast vs Actual", template=template)

    y_true = df['y'].dropna()
    y_pred = df.loc[y_true.index, 'yhat']
    mae = mean_absolute_error(y_true, y_pred) if not y_true.empty else 0
    rmse = np.sqrt(mean_squared_error(y_true, y_pred)) if not y_true.empty else 0
    metrics = f"MAE: {mae:,.2f} | RMSE: {rmse:,.2f}"

    monthly = df.groupby('Month').agg({'y': 'sum', 'yhat': 'sum'}).reset_index()
    fig2 = go.Figure([
        go.Bar(x=monthly['Month'], y=monthly['y'], name='Actual'),
        go.Bar(x=monthly['Month'], y=monthly['yhat'], name='Forecast')
    ])
    fig2.update_layout(title="Monthly Comparison", barmode='group', template=template)

    yearly = df.groupby('Year').agg({'y': 'sum', 'yhat': 'sum'}).reset_index()
    fig3 = go.Figure([
        go.Bar(x=yearly['Year'], y=yearly['y'], name='Actual'),
        go.Bar(x=yearly['Year'], y=yearly['yhat'], name='Forecast')
    ])
    fig3.update_layout(title="Yearly Comparison", barmode='group', template=template)

    return fig1, metrics, fig2, fig3


@app.callback(
    Output("download-forecast", "data"),
    Input("download-button", "n_clicks"),
    prevent_initial_call=True
)
def download_forecast(n_clicks):
    return dcc.send_file(os.path.join(EXPORT_DIR, forecast_files[0]))


if __name__ == '__main__':
    app.run(debug=True)
