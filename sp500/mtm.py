import yfinance as yf
import pandas as pd
from datetime import timedelta

# Load and preprocess the historical S&P 500 component data
df = pd.read_csv("S&P 500 Historical Components & Changes(03-10-2025).csv")
df['date'] = pd.to_datetime(df['date'])
monthly_components = df.set_index('date').resample('M').last()

# Select the first month for testing
sample_date = monthly_components.index[50]
ticker_string = monthly_components.loc[sample_date, 'tickers']
tickers = ticker_string.split(',')[:]  # Use only first 5 tickers to test

# Broaden the date range in case of non-trading days
start_date = (sample_date - timedelta(days=7)).strftime('%Y-%m-%d')
end_date = (sample_date + pd.offsets.MonthEnd(1) + timedelta(days=7)).strftime('%Y-%m-%d')

# Validate tickers and download data
valid_tickers = []
invalid_tickers = []

for ticker in tickers:
    try:
        # Test downloading data for each ticker
        data = yf.download(
            tickers=ticker,
            start=start_date,
            end=end_date,
            interval='1mo',
            group_by='ticker',
            auto_adjust=True,
            progress=False
        )
        if not data.empty:
            valid_tickers.append(ticker)
        else:
            invalid_tickers.append(ticker)
    except Exception as e:
        print(f"Error with ticker {ticker}: {e}")
        invalid_tickers.append(ticker)

print(f"Valid tickers: {valid_tickers}")
print(f"Invalid tickers: {invalid_tickers}")

# Download data for valid tickers only
price_data = yf.download(
    tickers=valid_tickers,
    start=start_date,
    end=end_date,
    interval='1mo',
    group_by='ticker',
    auto_adjust=True,
    progress=True
)

print(price_data.isna().sum())
cleaned_data = price_data.dropna(axis=1, how='all')
# Save invalid tickers to a log file
with open("invalid_tickers.log", "w") as log_file:
    for ticker in invalid_tickers:
        log_file.write(f"{ticker}\n")
# Display prices — last available price for the month will be used later
output_filename = f"monthly_prices_{sample_date.strftime('%Y-%m')}.csv"
price_data.to_csv(output_filename)
print(f"Monthly prices saved to: {output_filename}")


# ✅ Step 1: Extract Close prices from cleaned_data
close_prices = pd.DataFrame({
    ticker: cleaned_data[ticker]['Close']
    for ticker in cleaned_data.columns.levels[0]
    if 'Close' in cleaned_data[ticker]
})

# ✅ Step 2: Calculate 1-month returns
monthly_returns = close_prices.pct_change().dropna()

# ✅ Step 3: Identify top 5 stocks based on the first month's returns
formation_date = monthly_returns.index[0]
returns_at_formation = monthly_returns.loc[formation_date]
top_5 = returns_at_formation.sort_values(ascending=False).head(5)

print("📈 Top 5 Momentum Stocks Based on", formation_date.strftime('%Y-%m-%d'))
print(top_5)

# ✅ Step 4: Calculate portfolio return in the next month
if len(monthly_returns.index) >= 2:
    next_month_date = monthly_returns.index[1]
    next_month_returns = monthly_returns.loc[next_month_date, top_5.index]
    portfolio_return = next_month_returns.mean()

    print(f"\n📊 Portfolio return from {formation_date.strftime('%Y-%m')} to {next_month_date.strftime('%Y-%m')}: {portfolio_return:.2%}")
else:
    print("⚠️ Not enough data to compute next month's return.")