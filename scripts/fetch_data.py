import yfinance as yf
import pandas as pd
import time

def fetch_stock_data(symbol: str, interval: str, period: str, real_time: bool = False) -> pd.DataFrame:
    """
    Fetches historical or real-time stock data using yfinance.
    For real-time, it fetches the most recent data point.
    """
    ticker = yf.Ticker(symbol)
    if real_time:
        # Fetching the most recent available data for "real-time"
        # yfinance doesn't support true real-time streaming in the free version.
        # We fetch a short period frequently. For 1m interval, get last 2 minutes to ensure we get the latest.
        # If interval is '1m', period should be very short e.g. '1d' and then we take the last row.
        # For intervals like '1h', '1d', the 'real-time' aspect is less granular.
        if interval == "1m":
            df = ticker.history(period="1d", interval="1m") # Fetch 1 day of 1-minute data
        elif interval == "5m":
            df = ticker.history(period="2d", interval="5m") # Fetch 2 days of 5-minute data
        elif interval == "15m":
            df = ticker.history(period="5d", interval="15m")
        else: # Default to historical for other intervals or if real_time logic isn't specific enough
            df = ticker.history(interval=interval, period=period)

        if not df.empty:
            df.reset_index(inplace=True)
            return df # Return the full dataframe, dashboard will pick the latest
        else:
            return pd.DataFrame() # Return empty if no data
    else:
        df = ticker.history(interval=interval, period=period)
        df.reset_index(inplace=True)
        return df

def save_to_csv(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False)

# Example usage
if __name__ == "__main__":
    # Example for historical data
    symbol_hist = "AAPL"
    interval_hist = "1d"
    period_hist = "1mo"
    data_hist = fetch_stock_data(symbol_hist, interval_hist, period_hist, real_time=False)
    if not data_hist.empty:
        print(f"Fetched historical data for {symbol_hist}:")
        print(data_hist.tail())
        save_to_csv(data_hist, "../data/stock_data_historical.csv")
    else:
        print(f"No historical data found for {symbol_hist}")

    # Example for "real-time" data (latest available)
    symbol_rt = "MSFT"
    interval_rt = "1m" # For real-time, 1m is common
    # Period is less relevant for "real-time" mode as we fetch recent data based on interval
    data_rt = fetch_stock_data(symbol_rt, interval_rt, period="1d", real_time=True)
    if not data_rt.empty:
        print(f"\nFetched latest ('real-time') data for {symbol_rt} (interval: {interval_rt}):")
        print(data_rt.tail(1)) # Displaying the very last entry
        save_to_csv(data_rt, f"../data/{symbol_rt}_stock_data_realtime_latest.csv")
    else:
        print(f"No 'real-time' data found for {symbol_rt}")
