import yfinance as yf
import pandas as pd
import numpy as np
from datetime import timedelta

# Load and preprocess historical S&P 500 data
df = pd.read_csv("sp500_2.csv")
df['date'] = pd.to_datetime(df['date'])
monthly_components = df.set_index('date').resample('M').last()

results = []

# Loop through every month except the last (so we can look at the following month)
for i in range(len(monthly_components) - 1):
    sample_date      = monthly_components.index[i]
    next_month_date  = monthly_components.index[i+1]
    print(f"\n📅 Processing: {sample_date.strftime('%Y-%m')}")

    # ——————————————————————————————
    # 1) Build ticker list for this formation month
    ticker_string = monthly_components.iloc[i]['tickers']
    if not isinstance(ticker_string, str) or pd.isna(ticker_string) or ticker_string.strip()=="":
        print(f"⚠️ No tickers for {sample_date.strftime('%Y-%m')}, skipping.")
        continue
    tickers = list(set(ticker_string.split(',')))
    
    valid_tickers   = []
    invalid_tickers = []

    # 2) Validate each ticker by attempting a tiny download
    start_date = (sample_date - timedelta(days=7)).strftime('%Y-%m-%d')
    end_date   = (next_month_date + pd.offsets.MonthEnd(1) + timedelta(days=7)).strftime('%Y-%m-%d')

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
            else:
                invalid_tickers.append(ticker)
        except Exception as e:
            print(f"⚠️ Error with ticker {ticker}: {e}")
            invalid_tickers.append(ticker)

    print(f"✅ Valid:   {len(valid_tickers)} tickers")
    print(f"⚠️ Invalid: {len(invalid_tickers)} tickers")


    if not valid_tickers:
        print("⏭️  No valid tickers this month, skipping.")
        continue

    # ——————————————————————————————
    # 3) Bulk-download all valid tickers for this two‐month window
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

    # 4) Extract the 'Close' prices into a clean DataFrame
    close_prices = pd.DataFrame()

    if not price_data.empty:
        for ticker in valid_tickers:
            # Only process tickers that are present in cleaned_data columns
            if (ticker,) in price_data.columns:
                if 'Close' in price_data[ticker]:
                    close_prices[ticker] = price_data[ticker]['Close']
                else:
                    print(f"⚠️ 'Close' not found for {ticker}")
            else:
                print(f"⚠️ {ticker} missing from cleaned_data (likely failed download)")

    # ——————————————————————————————
    # 5) Compute month-over-month returns and pick the top 5
    monthly_returns = close_prices.pct_change().dropna()

    if monthly_returns.empty or len(monthly_returns) < 2:
        print("⏭️  Not enough data for returns calculation, skipping.")
        continue

    formation_date = monthly_returns.index[0]
    returns_at_formation = monthly_returns.loc[formation_date]
    top_5 = returns_at_formation.sort_values(ascending=False).head(5)
    print(f"📈 Top 5 at {formation_date.strftime('%Y-%m')}: {top_5.index.tolist()}")
    print(top_5)

    # 6) Compute equal-weighted return in the next month
    next_month_date = monthly_returns.index[1]
    next_returns = monthly_returns.loc[next_month_date, top_5.index]
    portfolio_return = next_returns.mean()

    # 7) Store the result
    results.append({
        "formation_month": formation_date.strftime('%Y-%m'),
        "top_5":             ",".join(top_5.index),
        "portfolio_return":  portfolio_return
    })

# ——————————————————————————————
# Finalize and save
results_df = pd.DataFrame(results)
results_df.to_csv("momentum_portfolio_results_2.csv", index=False)
print("\n✅ Done! Saved to momentum_portfolio_results.csv")
