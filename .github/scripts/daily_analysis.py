# scripts/daily_analysis.py
import os, datetime, json, base64, requests
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
from ta.momentum import RSIIndicator
from ta.trend import MACD

stocks = os.getenv("STOCK_LIST","600519").split(",")
today = datetime.datetime.now().strftime("%Y-%m-%d")
ALERT_THRESHOLD = 3.0
os.makedirs("charts", exist_ok=True)
os.makedirs("reports", exist_ok=True)

stock_imgs, stock_info, alert_stocks = {}, {}, []

for s in stocks:
    try:
        df = yf.Ticker(s+".SS").history(period="20d")
        if df.empty: continue
        macd = MACD(df['Close']).macd()
        rsi = RSIIndicator(df['Close']).rsi()
        df['MACD'] = macd
        df['RSI'] = rsi
        chart_file = f"charts/{s}_kline.png"
        mpf.plot(df, type='candle', style='charles', savefig=chart_file)
        stock_imgs[s] = chart_file
        last_close = df['Close'].iloc[-1]
        prev_close = df['Close'].iloc[-2]
        change_pct = round((last_close-prev_close)/prev_close*100,2)
        stock_info[s] = {"close": last_close, "change": change_pct, "MACD": round(macd.iloc[-1],2), "RSI": round(rsi.iloc[-1],2)}
        if abs(change_pct) >= ALERT_THRESHOLD:
            alert_stocks.append(s)
    except:
        continue

# PushPlus 汇总推送
push_token = os.getenv("PUSHPLUS_TOKEN")
if push_token:
    content = "📊 今日股票汇总分析\n\n"
    for s,v in stock_info.items():
        mark = " ⚠️" if s in alert_stocks else ""
        content += f"- {s}: 收盘{v['close']} 涨跌{v['change']}% MACD{v['MACD']} RSI{v['RSI']}{mark}\n"
    data = {"token": push_token,"title":"📈 每日股票分析","content":content,"template":"markdown"}
    try:
        r = requests.post("http://www.pushplus.plus/send", json=data)
        print("✅ PushPlus 推送成功:", r.text)
    except Exception as e:
        print("⚠️ PushPlus 推送失败:", e)

