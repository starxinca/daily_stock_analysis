import argparse
import requests
import os

def main():
    parser = argparse.ArgumentParser(description="PushPlus 汇总推送")
    parser.add_argument("--token", required=True, help="PushPlus Token")
    parser.add_argument("--stocks", required=True, help="股票列表")
    parser.add_argument("--report", required=True, help="汇总报告路径")
    args = parser.parse_args()

    if not os.path.exists(args.report):
        print(f"❌ 报告文件不存在: {args.report}")
        return

    with open(args.report, "r", encoding="utf-8") as f:
        content = f.read()

    payload = {
        "token": args.token,
        "title": f"股票分析汇总 - {args.stocks}",
        "content": content,
        "template": "markdown"  # 支持 markdown 格式
    }

    resp = requests.post("https://www.pushplus.plus/send", json=payload, timeout=15)
    if resp.status_code == 200:
        print("✅ PushPlus 汇总推送成功")
    else:
        print(f"❌ PushPlus 推送失败: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    main()

