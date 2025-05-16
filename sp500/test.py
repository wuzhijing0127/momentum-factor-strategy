import yfinance as yf
import pandas as pd
import numpy as np
from datetime import timedelta

# Load and preprocess historical S&P 500 data
df = pd.read_csv("sp500_cleaned.csv")
df['date'] = pd.to_datetime(df['date'])
monthly_components = df.set_index('date').resample('M').last()

# Store results
results = []

# Iterate over each month except the last (since we need t+1 for return)
for i in range(len(monthly_components) - (len(monthly_components)-2)):
    sample_date = monthly_components.index[i]
    next_month_date = monthly_components.index[i + 1]

    print(f"\n📅 Processing: {sample_date.strftime('%Y-%m')}")

    # Extract tickers and clean
    ticker_string = monthly_components.iloc[i]['tickers']
    tickers = list(set(ticker_string.split(',')))[:100]  # Limit to 200 max for API speed

    # Validate tickers before downloading data
    valid_tickers = []
    for ticker in tickers:
        try:
            # Check if the ticker exists in Yahoo Finance
            yf.Ticker(ticker).info  # This will raise an exception if the ticker is invalid
            valid_tickers.append(ticker)
        except Exception:
            print(f"⚠️ Invalid or missing ticker: {ticker}")

    # Proceed only with valid tickers
    if not valid_tickers:
        print(f"⚠️ No valid tickers for {sample_date.strftime('%Y-%m')}")
        continue

    # Date range for two months
    start_date = (sample_date - timedelta(days=7)).strftime('%Y-%m-%d')
    end_date = (next_month_date + pd.offsets.MonthEnd(1) + timedelta(days=7)).strftime('%Y-%m-%d')

    # Download price data for valid tickers
    try:
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
        cleaned_data = price_data.dropna(axis=1, how='all')
        
        # Save cleaned data to a CSV for debugging
        cleaned_data.to_csv(f"cleaned_data_{sample_date.strftime('%Y-%m')}.csv")

        # Extract Close prices safely
        try:
            close_prices = pd.DataFrame()

            # Check if cleaned_data has valid columns
            if not cleaned_data.empty:
                for ticker in cleaned_data.columns.levels[0]:
                    if 'Close' in cleaned_data[ticker]:
                        close_prices[ticker] = cleaned_data[ticker]['Close']
                    else:
                        print(f"⚠️ Missing 'Close' data for ticker: {ticker}")

            # Check if close_prices is empty
            if close_prices.empty:
                print(f"⚠️ No valid 'Close' price data for {sample_date.strftime('%Y-%m')}")
                continue

            # Save close_prices to a CSV for debugging
            close_prices.to_csv(f"close_prices_{sample_date.strftime('%Y-%m')}.csv")
            print(f"✅ Close price columns: {close_prices.columns.tolist()}")
            print(close_prices)

        except Exception as e:
            print(f"⚠️ Error extracting close prices: {e}")
            continue

        # Compute returns
        monthly_returns = close_prices.pct_change().dropna()
        print(f"Monthly returns for {sample_date.strftime('%Y-%m')}:")
        if len(monthly_returns) < 2:
            print("continue  # Not enough data for returns calculation")
            continue  # Not enough data

        formation_date = monthly_returns.index[0]
        next_month_return_date = monthly_returns.index[1]

        returns_at_formation = monthly_returns.loc[formation_date]
        top_5 = returns_at_formation.sort_values(ascending=False).head(5)
        print(f"Top 5 tickers on {formation_date.strftime('%Y-%m')}: {top_5.index.tolist()}")

        # Calculate equal-weighted portfolio return in next month
        next_returns = monthly_returns.loc[next_month_return_date, top_5.index]
        portfolio_return = next_returns.mean()

        results.append({
            "date": formation_date.strftime('%Y-%m'),
            "top_5": ','.join(top_5.index),
            "portfolio_return": portfolio_return
        })
        print(results)

    except Exception as e:
        print(f"⚠️ Error on {sample_date.strftime('%Y-%m')}: {e}")
        continue

# Convert results to DataFrame
results_df = pd.DataFrame(results)
results_df.to_csv("momentum_portfolio_results.csv", index=False)
print("\n✅ Saved all monthly momentum results to momentum_portfolio_results.csv")
