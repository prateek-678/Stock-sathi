import pandas as pd
import plotly.graph_objs as go

def plot_stock_price(df: pd.DataFrame, title: str):
    fig = go.Figure()
    # Ensure 'Datetime' column is actual datetime objects for Plotly
    # yfinance usually returns datetime-indexed data or a 'Datetime' column
    # If 'Datetime' is not the index, it's often already in a suitable format.
    # If it's an index, df.reset_index() in fetch_data.py handles it.

    # Check if 'Datetime' or 'Timestamp' column exists, yfinance varies
    time_column = None
    if 'Datetime' in df.columns:
        time_column = 'Datetime'
    elif 'Timestamp' in df.columns:
        time_column = 'Timestamp'
    # Add more checks if other names are possible e.g. from different intervals/sources

    if time_column:
        x_data = df[time_column]
    else: # Fallback if no recognized time column, though this should not happen with yfinance
        x_data = df.index

    fig.add_trace(go.Scatter(x=x_data, y=df['Close'], mode='lines+markers', name='Close Price',
                             line=dict(color='cyan', width=2), marker=dict(size=5, color='yellow')))

    fig.update_layout(
        title={'text': title, 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top', 'font': {'size': 24, 'color': 'white'}},
        xaxis_title='Time',
        yaxis_title='Price (USD)',
        template='plotly_dark',  # Using a dark theme for better contrast
        height=600,  # Increased height for better visibility
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(100,100,100,0.5)',
            rangeslider=dict(visible=True), # Add a range slider for easier navigation
            type="date" # Ensure x-axis is treated as date
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(100,100,100,0.5)'
        ),
        legend_title_text='Metrics',
        font=dict(
            family="Arial, sans-serif",
            size=14,
            color="white"
        )
    )
    return fig