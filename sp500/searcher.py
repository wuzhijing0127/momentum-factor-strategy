import yfinance as yf
import pandas as pd

tickers_to_check = ['AABA']
start_date = '2004-03-01'
end_date = '2004-03-31'

results = []

for ticker in tickers_to_check:
    try:
        data = yf.download(
            tickers=ticker,
            start=start_date,
            end=end_date,
            interval='1mo',
            auto_adjust=True,
            progress=False
        )

        if not data.empty:
            results.append({
                'ticker': ticker,
                'status': '✅ Data found',
                'date': data.index[0].strftime('%Y-%m-%d'),
                'close': data['Close'].iloc[0]
            })
        else:
            results.append({
                'ticker': ticker,
                'status': '❌ No data returned',
                'date': None,
                'close': None
            })

    except Exception as e:
        results.append({
            'ticker': ticker,
            'status': f'❌ Error: {e}',
            'date': None,
            'close': None
        })

# Save to CSV
df_results = pd.DataFrame(results)
df_results.to_csv("missing_ticker_check_2004-03.csv", index=False)
print("✅ Saved results to missing_ticker_check_2004-03.csv")
