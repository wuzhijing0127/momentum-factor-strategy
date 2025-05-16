import yfinance as yf
import pandas as pd
import numpy as np
from datetime import timedelta

# Load and preprocess historical S&P 500 data
df = pd.read_csv("sp500_2.csv")
df['date'] = pd.to_datetime(df['date'])
monthly_components = df.set_index('date').resample('M').last()

results = []

# Loop every 6 months instead of monthly
for i in range(0, len(monthly_components) - 13, 12):  # Ensure at least one month after for return
    sample_date = monthly_components.index[i]
    next_month_date = monthly_components.index[i + 12 + 1]  # Next month after 6-month interval
    print(f"\n📅 Processing: {sample_date.strftime('%Y-%m')}")

    # 1) Build ticker list
    ticker_string = monthly_components.iloc[i]['tickers']
    if not isinstance(ticker_string, str) or pd.isna(ticker_string) or ticker_string.strip()=="":
        print(f"⚠️ No tickers for {sample_date.strftime('%Y-%m')}, skipping.")
        continue
    tickers = list(set(ticker_string.split(',')))

    valid_tickers = []
    invalid_tickers = []

    # Define download window
    start_date = (sample_date - timedelta(days=7)).strftime('%Y-%m-%d')
    end_date = (next_month_date + pd.offsets.MonthEnd(1) + timedelta(days=7)).strftime('%Y-%m-%d')

    # 2) Validate tickers
    for ticker in tickers:
        try:
            data = yf.download(
                tickers=ticker,
                start=start_date,
                end=end_date,
                interval='1mo',
                progress=False,
                auto_adjust=True
            )
            if not data.empty:
                valid_tickers.append(ticker)
        except Exception as e:
            print(f"⚠️ Error with ticker {ticker}: {e}")

    print(f"✅ Valid: {len(valid_tickers)} tickers")

    if not valid_tickers:
        print("⏭️ No valid tickers this period, skipping.")
        continue

    # 3) Download prices
    price_data = yf.download(
        tickers=valid_tickers,
        start=start_date,
        end=end_date,
        interval='1mo',
        group_by='ticker',
        auto_adjust=True,
        progress=False,
        threads=True
    )

    close_prices = pd.DataFrame()

    if not price_data.empty:
        for ticker in valid_tickers:
            try:
                close_prices[ticker] = price_data[ticker]['Close']
            except:
                print(f"⚠️ Could not extract 'Close' for {ticker}")

    # 4) Compute monthly returns
    monthly_returns = close_prices.pct_change().dropna()

    if monthly_returns.empty or len(monthly_returns) < 2:
        print("⏭️ Not enough return data, skipping.")
        continue

    formation_date = monthly_returns.index[0]
    returns_at_formation = monthly_returns.loc[formation_date]
    top_10 = returns_at_formation.sort_values(ascending=False).head(10)
    print(f"📈 Top 10 at {formation_date.strftime('%Y-%m')}: {top_10.index.tolist()}")

    # 5) Compute portfolio return in the next month
    next_month_return_date = monthly_returns.index[1]  # Next month
    next_returns = monthly_returns.loc[next_month_return_date, top_10.index]
    portfolio_return = next_returns.mean()

    results.append({
        "formation_month": formation_date.strftime('%Y-%m'),
        "top_10": ",".join(top_10.index),
        "portfolio_return": portfolio_return
    })

# Finalize and save
results_df = pd.DataFrame(results)
results_df.to_csv("res_12_2.csv", index=False)
print("\n✅ Done! Saved to res_12_2.csv")
