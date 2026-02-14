#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime
import requests

# 获取环境变量
STOCK_LIST = os.getenv("STOCK_LIST", "600519,300750").split(",")
PUSHPLUS_TOKEN = os.getenv("PUSHPLUS_TOKEN", "")

REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)
SUMMARY_FILE = os.path.join(REPORT_DIR, "summary.md")

lines = []
lines.append(f"# 每日股票分析汇总 ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")

for stock in STOCK_LIST:
    lines.append(f"## 股票 {stock}")
    lines.append(f"- 最新价格: 模拟数据")
    lines.append(f"- 日内涨跌: 模拟数据")
    lines.append(f"- 分析结论: 模拟结论")
    lines.append("")  # 空行分隔每只股票

# 写入 summary.md
with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ 已生成汇总文件: {SUMMARY_FILE}")

# PushPlus 一次性推送
if PUSHPLUS_TOKEN:
    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        content = f.read().replace("\n", "%0A")
    url = f"http://www.pushplus.plus/send?token={PUSHPLUS_TOKEN}&title=每日股票分析&content={content}"
    try:
        resp = requests.get(url)
        print(f"✅ PushPlus 推送成功: {resp.text}")
    except Exception as e:
        print(f"⚠️ PushPlus 推送失败: {e}")
else:
    print("⚠️ 未配置 PUSHPLUS_TOKEN，推送跳过")
