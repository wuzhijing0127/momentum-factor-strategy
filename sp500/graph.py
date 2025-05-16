import pandas as pd
import matplotlib.pyplot as plt

def plotspy():
    # Load dataset
    spy_df = pd.read_csv("SPY_with_daily_returns.csv", parse_dates=["Date"])

    # Drop rows with missing return values
    spy_df = spy_df.dropna(subset=["daily_return_pct"])

    # Calculate cumulative return
    spy_df['cumulative_return'] = (1 + spy_df['daily_return_pct'] / 100).cumprod() - 1

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(spy_df['Date'], spy_df['cumulative_return'] * 100, label='Cumulative Return (%)', color='blue')
    plt.title("SPY Cumulative Return Over Time")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return (%)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

def plot_spy_1mon():
    spy_df = pd.read_csv("SPY_with_daily_returns.csv", parse_dates=["Date"])
    spy_df = spy_df.dropna(subset=["daily_return_pct"])

    # Calculate SPY cumulative return
    spy_df['cumulative_return_spy'] = (1 + spy_df['daily_return_pct'] / 100).cumprod() - 1

    # Resample SPY to monthly to align with portfolio data
    spy_monthly = spy_df.set_index('Date').resample('MS').last().reset_index()

    # Load portfolio data
    portfolio_df = pd.read_csv("combined_momentum_portfolio_results.csv", parse_dates=["formation_month"])
    portfolio_df['return_factor'] = 1 + portfolio_df['portfolio_return'] / 100
    portfolio_df['cumulative_return_portfolio'] = portfolio_df['return_factor'].cumprod() - 1
    portfolio_df.rename(columns={'formation_month': 'Date'}, inplace=True)

    # Merge the two datasets on date
    combined = pd.merge(portfolio_df[['Date', 'cumulative_return_portfolio']],
                        spy_monthly[['Date', 'cumulative_return_spy']],
                        on='Date', how='inner')

    # Plot the results
    plt.figure(figsize=(12, 6))
    plt.plot(combined['Date'], combined['cumulative_return_portfolio'] * 100, label='Momentum Portfolio', linewidth=2)
    plt.plot(combined['Date'], combined['cumulative_return_spy'] * 100, label='SPY ETF', linestyle='--')
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return (%)")
    plt.title(" Momentum Portfolio (1 month, top5 stocks) vs SPY")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

def plot_1mon():

    # Load momentum portfolio data
    portfolio_df = pd.read_csv("combined_momentum_portfolio_results.csv", parse_dates=["formation_month"])

    # Calculate cumulative return
    portfolio_df['return_factor'] = 1 + portfolio_df['portfolio_return'] / 100
    portfolio_df['cumulative_return'] = portfolio_df['return_factor'].cumprod() - 1

    # Rename for plotting
    portfolio_df.rename(columns={'formation_month': 'Date'}, inplace=True)

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(portfolio_df['Date'], portfolio_df['cumulative_return'] * 100, label='Momentum Portfolio Cumulative Return', color='green')
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return (%)")
    plt.title("Momentum Portfolio(1 month, top 5 stocks)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

def plot_spy_top10():
    # === Load and process SPY data ===
    spy_df = pd.read_csv("SPY_cleaned.csv", parse_dates=["Date"])

    # Calculate daily return percentage and drop first NaN row
    spy_df['daily_return_pct'] = spy_df['Close'].pct_change() * 100
    spy_df = spy_df.dropna(subset=["daily_return_pct"])

    # Calculate cumulative return
    spy_df['cumulative_return_spy'] = (1 + spy_df['daily_return_pct'] / 100).cumprod() - 1

    # Resample to monthly (start of month) to match portfolio dates
    spy_monthly = spy_df.set_index('Date').resample('MS').last().reset_index()

    # === Load and process momentum portfolio data ===
    portfolio_df = pd.read_csv("mom10_comb.csv", parse_dates=["formation_month"])
    portfolio_df['return_factor'] = 1 + portfolio_df['portfolio_return'] / 100
    portfolio_df['cumulative_return_portfolio'] = portfolio_df['return_factor'].cumprod() - 1
    portfolio_df.rename(columns={"formation_month": "Date"}, inplace=True)

    # === Merge both datasets on 'Date' ===
    combined_df = pd.merge(
        portfolio_df[['Date', 'cumulative_return_portfolio']],
        spy_monthly[['Date', 'cumulative_return_spy']],
        on="Date",
        how="inner"
    )

    # === Plot ===
    plt.figure(figsize=(12, 6))
    plt.plot(combined_df['Date'], combined_df['cumulative_return_portfolio'] * 100,
            label='Momentum Portfolio', linewidth=2)
    plt.plot(combined_df['Date'], combined_df['cumulative_return_spy'] * 100,
            label='SPY ETF', linestyle='--')
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return (%)")
    plt.title("Momentum Portfolio(1 month, top 10 stock) vs SPY")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

def plot_top10():
    # Load the momentum portfolio data
    portfolio_df = pd.read_csv("mom10_comb.csv", parse_dates=["formation_month"])

    # Calculate cumulative return
    portfolio_df['return_factor'] = 1 + portfolio_df['portfolio_return'] / 100
    portfolio_df['cumulative_return'] = portfolio_df['return_factor'].cumprod() - 1

    # Rename for plotting
    portfolio_df.rename(columns={'formation_month': 'Date'}, inplace=True)

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(portfolio_df['Date'], portfolio_df['cumulative_return'] * 100, label='Momentum Portfolio', color='green')
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return (%)")
    plt.title("Momentum Portfolio(top 10 stocks, 1 month)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

def plot_spy_6mon():
    # === Load and process momentum portfolio ===
    portfolio_df = pd.read_csv("mom_res_comb.csv", parse_dates=["formation_month"])

    # Calculate cumulative return
    portfolio_df['return_factor'] = 1 + portfolio_df['portfolio_return'] / 100
    portfolio_df['cumulative_return_portfolio'] = portfolio_df['return_factor'].cumprod() - 1
    portfolio_df.rename(columns={'formation_month': 'Date'}, inplace=True)

    # === Load and process SPY data ===
    spy_df = pd.read_csv("SPY_cleaned.csv", parse_dates=["Date"])
    spy_df['daily_return_pct'] = spy_df['Close'].pct_change() * 100
    spy_df = spy_df.dropna(subset=["daily_return_pct"])
    spy_df['cumulative_return_spy'] = (1 + spy_df['daily_return_pct'] / 100).cumprod() - 1

    # Resample SPY to monthly frequency (start of month)
    spy_monthly = spy_df.set_index('Date').resample('MS').last().reset_index()

    # === Merge datasets by date ===
    combined_df = pd.merge(
        portfolio_df[['Date', 'cumulative_return_portfolio']],
        spy_monthly[['Date', 'cumulative_return_spy']],
        on='Date',
        how='inner'
    )

    # === Plot cumulative returns ===
    plt.figure(figsize=(12, 6))
    plt.plot(combined_df['Date'], combined_df['cumulative_return_portfolio'] * 100, label='Momentum Portfolio', linewidth=2)
    plt.plot(combined_df['Date'], combined_df['cumulative_return_spy'] * 100, label='SPY ETF', linestyle='--')
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return (%)")
    plt.title("Momentum Portfolio(top 10 stocks, 6 month) vs SPY")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

def plot_6mon():

    # Load momentum portfolio data
    portfolio_df = pd.read_csv("mom_res_comb.csv", parse_dates=["formation_month"])

    # Calculate cumulative return
    portfolio_df['return_factor'] = 1 + portfolio_df['portfolio_return'] / 100
    portfolio_df['cumulative_return'] = portfolio_df['return_factor'].cumprod() - 1

    # Rename for plotting
    portfolio_df.rename(columns={'formation_month': 'Date'}, inplace=True)

    # Plot cumulative return
    plt.figure(figsize=(12, 6))
    plt.plot(portfolio_df['Date'], portfolio_df['cumulative_return'] * 100,
            label='Momentum Portfolio', color='blue', linewidth=2)
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return (%)")
    plt.title("Momentum Portfolio(top 10 stocks, 6 month)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

def plot_12mon_spy():


    # === Load and process momentum portfolio ===
    portfolio_df = pd.read_csv("res_12_comb.csv", parse_dates=["formation_month"])

    # Calculate cumulative return
    portfolio_df['return_factor'] = 1 + portfolio_df['portfolio_return'] / 100
    portfolio_df['cumulative_return_portfolio'] = portfolio_df['return_factor'].cumprod() - 1
    portfolio_df.rename(columns={'formation_month': 'Date'}, inplace=True)

    # === Load and process SPY data ===
    spy_df = pd.read_csv("SPY_cleaned.csv", parse_dates=["Date"])
    spy_df['daily_return_pct'] = spy_df['Close'].pct_change() * 100
    spy_df = spy_df.dropna(subset=["daily_return_pct"])
    spy_df['cumulative_return_spy'] = (1 + spy_df['daily_return_pct'] / 100).cumprod() - 1

    # Resample SPY to monthly frequency (start of month)
    spy_monthly = spy_df.set_index('Date').resample('MS').last().reset_index()

    # === Merge datasets on date ===
    combined_df = pd.merge(
        portfolio_df[['Date', 'cumulative_return_portfolio']],
        spy_monthly[['Date', 'cumulative_return_spy']],
        on='Date',
        how='inner'
    )

    # === Plot cumulative returns ===
    plt.figure(figsize=(12, 6))
    plt.plot(combined_df['Date'], combined_df['cumulative_return_portfolio'] * 100, label='Momentum Portfolio', linewidth=2)
    plt.plot(combined_df['Date'], combined_df['cumulative_return_spy'] * 100, label='SPY ETF', linestyle='--')
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return (%)")
    plt.title("Momentum Portfolio (top 10 stocks, 12 month) vs SPY")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

def plot_12mon():

    # Load the momentum portfolio data
    portfolio_df = pd.read_csv("res_12_comb.csv", parse_dates=["formation_month"])

    # Calculate cumulative return
    portfolio_df['return_factor'] = 1 + portfolio_df['portfolio_return'] / 100
    portfolio_df['cumulative_return'] = portfolio_df['return_factor'].cumprod() - 1

    # Rename for plotting
    portfolio_df.rename(columns={'formation_month': 'Date'}, inplace=True)

    # Plot cumulative return
    plt.figure(figsize=(12, 6))
    plt.plot(portfolio_df['Date'], portfolio_df['cumulative_return'] * 100,
            label='Momentum Portfolio (12-Month)', color='purple', linewidth=2)
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return (%)")
    plt.title("Momentum Portfolio(top 10 stocks, 12 month)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()


# plotspy()
# plot_1mon()
# plot_spy_1mon()
# plot_top10()
# plot_spy_6mon()
# plot_6mon()
# plot_12mon_spy()
# plot_12mon()
plot_spy_top10()