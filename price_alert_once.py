#!/usr/bin/env python3
import time
import yfinance as yf
import pandas as pd

SYMBOL = '002156.SZ'
LEVELS = {}

# Fetch recent data for short-term indicators (ensure enough bars for ATR14/SMA20)
t = yf.Ticker(SYMBOL)
df_short = t.history(period='3mo', interval='1d', auto_adjust=False)
if df_short is None or df_short.empty:
    print('No data for short period')
    raise SystemExit(1)

# Fetch longer data for accurate 52-week high
df_long = t.history(period='1y', interval='1d', auto_adjust=False)
if df_long is None or df_long.empty:
    df_long = df_short

close = float(df_short['Close'].iloc[-1])
sma20 = float(df_short['Close'].rolling(20).mean().iloc[-1])
hi_52w = float(df_long['Close'].rolling(252).max().fillna(df_long['Close'].max()).iloc[-1])

# ATR(14) on short data
high = df_short['High']
low = df_short['Low']
prev_close = df_short['Close'].shift(1)
tr = pd.concat([(high-low).abs(), (high-prev_close).abs(), (low-prev_close).abs()], axis=1).max(axis=1)
atr = float(tr.ewm(span=14, adjust=False).mean().iloc[-1])

LEVELS['close'] = close
LEVELS['sma20'] = sma20
LEVELS['hi_52w'] = hi_52w
LEVELS['guard'] = close - atr

print('Snapshot:', LEVELS)

# Simple one-shot checks
alerts = []
if close < sma20:
    alerts.append(f'Close fell below SMA20: {close:.2f} < {sma20:.2f}')
if close > hi_52w * 0.99:
    alerts.append(f'Close near 52w high: {close:.2f} vs {hi_52w:.2f}')
if close < LEVELS['guard']:
    alerts.append(f'Close below ATR guard: {close:.2f} < {LEVELS["guard"]:.2f}')

if alerts:
    print('\n'.join(alerts))
else:
    print('No alerts triggered.')
