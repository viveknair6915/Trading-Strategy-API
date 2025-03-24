from app import crud
import pandas as pd

def evaluate_strategy():
    # Fetch data from the database
    records = crud.get_all_data()
    if not records:
        return {"error": "No data available"}

    # Convert records into a DataFrame and process the datetime column
    df = pd.DataFrame(records)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.sort_values('datetime', inplace=True)

    # Convert numeric columns to float (and volume to int)
    for col in ["open", "high", "low", "close"]:
        df[col] = df[col].astype(float)
    df["volume"] = df["volume"].astype(int)

    # Define moving average windows
    short_window = 5
    long_window = 20

    # Calculate short-term and long-term moving averages
    df['short_ma'] = df['close'].rolling(window=short_window).mean()
    df['long_ma'] = df['close'].rolling(window=long_window).mean()

    # Generate signals: 1 for buy, -1 for sell, 0 for hold
    df['signal'] = 0
    df.loc[df['short_ma'] > df['long_ma'], 'signal'] = 1
    df.loc[df['short_ma'] < df['long_ma'], 'signal'] = -1

    # Calculate daily returns and strategy returns
    df['returns'] = df['close'].pct_change()
    df['strategy_returns'] = df['returns'] * df['signal'].shift(1)

    # Compute cumulative return from strategy returns
    cumulative_return = (df['strategy_returns'] + 1).cumprod().iloc[-1] - 1

    # Count signals for buy, sell, and hold
    buy_count = (df['signal'] == 1).sum()
    sell_count = (df['signal'] == -1).sum()
    hold_count = (df['signal'] == 0).sum()

    # Prepare dataset for display (selecting key columns)
    table_data = df[["datetime", "open", "high", "low", "close", "volume", "signal"]].to_dict(orient="records")

    return {
        "cumulative_return": cumulative_return,
        "buy_signals": int(buy_count),
        "sell_signals": int(sell_count),
        "hold_signals": int(hold_count),
        "dataset": table_data
    }
