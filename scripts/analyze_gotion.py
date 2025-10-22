import sys
import os
import datetime as dt
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

TICKER = '002074.SZ'  # 国轩高科
LOOKBACK_YEARS = 3
OUTPUT_IMG = os.path.join('/workspace/images', 'gotion_trend.png')


def to_series_1d(obj: pd.Series | pd.DataFrame) -> pd.Series:
    """Return a 1-D float Series from a Series/DataFrame (handles MultiIndex columns)."""
    if isinstance(obj, pd.DataFrame):
        ser = obj.iloc[:, 0]
    else:
        ser = obj
    return pd.Series(ser, index=ser.index).astype(float)


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Ensure 1-D Series for OHLC regardless of MultiIndex/DataFrame columns
    close_s = to_series_1d(df['Close'])
    high_s = to_series_1d(df['High'])
    low_s = to_series_1d(df['Low'])

    # MAs
    for win in [5, 10, 20, 50, 100, 200]:
        df[f'MA{win}'] = close_s.rolling(window=win).mean()

    # RSI (14)
    delta = close_s.diff()
    gain = delta.clip(lower=0)
    loss = (-delta).clip(lower=0)
    roll_up = gain.rolling(14).mean()
    roll_down = loss.rolling(14).mean()
    rs = roll_up / (roll_down + 1e-9)
    df['RSI14'] = 100.0 - (100.0 / (1.0 + rs))

    # MACD (12,26,9)
    ema12 = close_s.ewm(span=12, adjust=False).mean()
    ema26 = close_s.ewm(span=26, adjust=False).mean()
    df['MACD'] = ema12 - ema26
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['Hist'] = df['MACD'] - df['Signal']

    # ATR (14)
    prev_close = close_s.shift(1)
    tr1 = high_s - low_s
    tr2 = (high_s - prev_close).abs()
    tr3 = (low_s - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    df['ATR14'] = tr.rolling(14).mean()

    return df


def fetch_data(ticker: str, years: int) -> pd.DataFrame:
    end = dt.datetime.now().date() + dt.timedelta(days=1)
    start = end - dt.timedelta(days=365*years + 5)
    data = yf.download(ticker, start=start.isoformat(), end=end.isoformat(), interval='1d', auto_adjust=False, progress=False)
    if data is None or data.empty:
        raise RuntimeError('下载数据失败，可能是代码错误或网络受限')
    data = data.dropna()
    return data


def summarize(df: pd.DataFrame) -> str:
    # Use robust 1-D access to avoid single-element Series warnings
    price = float(to_series_1d(df['Close']).iloc[-1])
    ma20 = float(to_series_1d(df['MA20']).iloc[-1]) if 'MA20' in df else np.nan
    ma50 = float(to_series_1d(df['MA50']).iloc[-1]) if 'MA50' in df else np.nan
    rsi = float(to_series_1d(df['RSI14']).iloc[-1]) if 'RSI14' in df else np.nan
    macd = float(to_series_1d(df['MACD']).iloc[-1]) if 'MACD' in df else np.nan
    signal = float(to_series_1d(df['Signal']).iloc[-1]) if 'Signal' in df else np.nan

    trend = []
    if not np.isnan(ma20) and price > ma20:
        trend.append('价在MA20上方，短期偏强')
    elif not np.isnan(ma20):
        trend.append('价在MA20下方，短期承压')

    if not np.isnan(ma50) and price > ma50:
        trend.append('价在MA50上方，中期偏强')
    elif not np.isnan(ma50):
        trend.append('价在MA50下方，中期偏弱')

    if not np.isnan(rsi):
        if rsi > 70:
            trend.append('RSI>70，可能超买')
        elif rsi < 30:
            trend.append('RSI<30，可能超卖')
        else:
            trend.append('RSI中性区间')

    if not np.isnan(macd) and not np.isnan(signal):
        if macd > signal:
            trend.append('MACD金叉偏多')
        else:
            trend.append('MACD死叉偏空')

    return '；'.join(trend)


def plot_chart(df: pd.DataFrame, out_path: str):
    plt.figure(figsize=(14, 9))
    ax1 = plt.subplot(3,1,1)
    ax2 = plt.subplot(3,1,2, sharex=ax1)
    ax3 = plt.subplot(3,1,3, sharex=ax1)

    # Price & MAs
    ax1.plot(df.index, df['Close'], label='Close', color='#1f77b4')
    for win, color in [(20,'#ff7f0e'), (50,'#2ca02c'), (200,'#d62728')]:
        col = f'MA{win}'
        if col in df:
            ax1.plot(df.index, df[col], label=col, linewidth=1.2, color=color)
    ax1.set_title('Gotion High-Tech (002074.SZ) - Price & MAs')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)

    # MACD
    ax2.plot(df.index, df['MACD'], label='MACD', color='#9467bd')
    ax2.plot(df.index, df['Signal'], label='Signal', color='#8c564b')
    ax2.bar(df.index, df['Hist'], label='Hist', color=np.where(df['Hist']>=0, '#2ca02c', '#d62728'))
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)

    # RSI
    ax3.plot(df.index, df['RSI14'], label='RSI14', color='#17becf')
    ax3.axhline(70, color='red', linestyle='--', linewidth=0.8)
    ax3.axhline(30, color='green', linestyle='--', linewidth=0.8)
    ax3.legend(loc='upper left')
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=160)


def main():
    df = fetch_data(TICKER, LOOKBACK_YEARS)
    df = compute_indicators(df)
    summary = summarize(df)
    # Additional metrics for context
    close_s = to_series_1d(df['Close'])
    high_s = to_series_1d(df['High'])
    low_s = to_series_1d(df['Low'])
    vol_s = to_series_1d(df['Volume']) if 'Volume' in df else pd.Series(index=df.index, dtype=float)
    price = float(close_s.iloc[-1])
    ma20 = float(to_series_1d(df['MA20']).iloc[-1]) if 'MA20' in df else np.nan
    ma50 = float(to_series_1d(df['MA50']).iloc[-1]) if 'MA50' in df else np.nan
    rsi = float(to_series_1d(df['RSI14']).iloc[-1]) if 'RSI14' in df else np.nan
    macd = float(to_series_1d(df['MACD']).iloc[-1]) if 'MACD' in df else np.nan
    signal = float(to_series_1d(df['Signal']).iloc[-1]) if 'Signal' in df else np.nan
    atr = float(to_series_1d(df['ATR14']).iloc[-1]) if 'ATR14' in df else np.nan
    atr_pct = (atr / price * 100.0) if (not np.isnan(atr) and price > 0) else np.nan
    # 52-week metrics (~252 trading days)
    lookback_1y = 252 if len(close_s) >= 252 else len(close_s)
    high_52w = float(high_s.tail(lookback_1y).max()) if lookback_1y > 0 else np.nan
    low_52w = float(low_s.tail(lookback_1y).min()) if lookback_1y > 0 else np.nan
    # Volume metrics
    vol_last = int(vol_s.iloc[-1]) if len(vol_s) else 0
    vol_ma20 = float(vol_s.rolling(20).mean().iloc[-1]) if len(vol_s) else np.nan
    vol_ratio = (vol_last / vol_ma20) if (vol_ma20 and not np.isnan(vol_ma20) and vol_ma20 > 0) else np.nan
    plot_chart(df, OUTPUT_IMG)
    print('SUMMARY::' + summary)
    print('METRICS::' + (
        f"price={price:.2f};MA20={ma20:.2f};MA50={ma50:.2f};RSI14={rsi:.1f};"
        f"MACD={macd:.3f};Signal={signal:.3f};ATR14={atr:.3f};ATR%={atr_pct:.2f};"
        f"52W_H={high_52w:.2f};52W_L={low_52w:.2f};VOL={vol_last};VOL_MA20={vol_ma20:.0f};VOL_RATIO={vol_ratio:.2f}"
    ))


if __name__ == '__main__':
    main()
