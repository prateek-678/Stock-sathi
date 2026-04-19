def check_price_alert(current_df, threshold=5):
    """
    Compares the latest price with the previous price in a series or
    the opening price if only one distinct price point is available frequently.
    For real-time, this should ideally compare the current price with the price from the PREVIOUS fetch.
    However, the current structure provides the latest dataframe from fetch_data.
    So, we compare the last two points in the current dataframe.
    If the dataframe has only one row (e.g. first fetch or very sparse data),
    we compare 'Close' to 'Open' of that single row.
    """
    if current_df.empty:
        return "ℹ️ Dataframe is empty, cannot check alert."

    if len(current_df) >= 2:
        # Compare the last price with the second to last price
        latest_price = current_df['Close'].iloc[-1]
        previous_price = current_df['Close'].iloc[-2]

        if previous_price == 0: # Avoid division by zero
            return "ℹ️ Previous price is zero, cannot calculate change."

        change_pct = ((latest_price - previous_price) / previous_price) * 100
        comparison_basis = "previous price in series"

    elif len(current_df) == 1:
        # If only one row, compare Close to Open of that row
        latest_price = current_df['Close'].iloc[0]
        open_price = current_df['Open'].iloc[0]

        if open_price == 0: # Avoid division by zero
             return "ℹ️ Opening price is zero, cannot calculate change."

        change_pct = ((latest_price - open_price) / open_price) * 100
        comparison_basis = "opening price of the day/period"

    else: # Should not happen if df is not empty
        return "ℹ️ Insufficient data to calculate change."

    if abs(change_pct) >= threshold:
        direction = "risen" if change_pct > 0 else "fallen"
        return f"🚨 ALERT: Price has {direction} by {change_pct:.2f}% (compared to {comparison_basis}). Latest: ${latest_price:.2f}"
    else:
        return f"✅ STABLE: Price change is {change_pct:.2f}% (compared to {comparison_basis}). Latest: ${latest_price:.2f}"
