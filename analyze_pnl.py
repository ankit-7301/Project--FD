# Task: Drawdown with respect to Fixed Deposit (FD)
# Objective: To measure account drawdown (DD) and drawdown streak (DDS) with respect to a fixed deposit (FD) rate using a daily PnL time series.

import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('daily_pnl.csv', parse_dates=['date'])

# Initialize variables
initial_balance = 100000
fd_rate = 0.0001 #daily 0.01 % return  
data['balance'] = initial_balance + data['pnl'].cumsum()

# Calculate the FD-adjusted balance
data['fd_balance'] = initial_balance * ((1 + fd_rate) ** data.index)
data['adjusted_balance'] = data['balance'] - data['fd_balance']

# Calculate the peak and drawdown
data['peak'] = data['adjusted_balance'].cummax()
data['drawdown'] = data['peak'] - data['adjusted_balance']
data['drawdown_percent'] = data['drawdown'] / data['peak']

# Compute the drawdown streak (DDS)
data['in_dd'] = data['drawdown'] > 0
data['dds'] = data['in_dd'].astype(int).groupby((data['in_dd'] != data['in_dd'].shift()).cumsum()).cumsum()

# Calculate maximum drawdown and maximum DDS
max_dd = data['drawdown'].max()
max_dds = data['dds'].max()

# Calculate profit streak stats
data['profit_streak'] = (data['pnl'] > 0).astype(int).groupby((data['pnl'] <= 0).astype(int).cumsum()).cumsum()
profit_streak_stats = data['profit_streak'].describe()

# Calculate drawdown streak stats
drawdown_streak_stats = data['dds'].describe()

# Print results
print(f"Maximum Drawdown (w.r.t FD): {max_dd}")
print(f"Maximum Drawdown Streak (DDS, w.r.t FD): {max_dds}")
print("\nDrawdown Streak Stats:")
print(drawdown_streak_stats)
print("\nProfit Streak Stats:")
print(profit_streak_stats)

# Plot the equity curve
plt.figure(figsize=(14, 7))
plt.plot(data['date'], data['balance'], label='Account Balance')
plt.plot(data['date'], data['fd_balance'], label='FD Balance', linestyle='--')
plt.xlabel('Date')
plt.ylabel('Balance')
plt.title('Equity Curve')
plt.legend()
plt.grid(True)

# Save the plot
output_path = 'equity_curve.png'
plt.savefig(output_path)
plt.close()

# Generate a link to the graph
import urllib.parse
file_url = urllib.parse.quote(output_path)
graph_link = f"file://{file_url}"
print(f"Equity curve graph saved. Open the graph from this link: {graph_link}")

# Save to CSV for further analysis if needed
data.to_csv('output_with_stats.csv', index=False)
