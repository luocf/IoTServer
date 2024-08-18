from datetime import datetime

def format_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

# 其他工具函数
