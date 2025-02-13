import requests
import re
from icalendar import Calendar, Event

# 获取 ICS 文件
url = 'https://yangh9.github.io/ChinaCalendar/cal_lunar.ics'
response = requests.get(url)
ics_data = response.content  # 使用 .content 获取字节数据

# 解析 ICS 文件
calendar = Calendar.from_ical(ics_data)

# 定义提取“日”的函数，正则匹配最后的“日”
def extract_day(summary):
    # 正则提取“日”前的部分内容
    match = re.search(r'(\S+日)$', summary)
    if match:
        return match.group(1)  # 返回“日”字前的部分
    return summary  # 如果没有找到“日”，则返回原内容

# 修改每个事件
for component in calendar.walk('vevent'):
    summary = component.get('summary')
    location = component.get('location')

    # 只在 summary 和 location 都存在的情况下修改
    if summary and location:
        # 提取summary中的“日”部分
        new_summary = extract_day(summary)
        component['summary'] = new_summary  # 设置新的 summary
        component['location'] = None  # 清空 location 字段

# 保存修改后的 ICS 文件，强制指定 UTF-8 编码
with open('modified_cal_lunar.ics', 'wb') as f:
    f.write(calendar.to_ical())  # 写入时不需要额外的编码转换

print("ICS file has been modified successfully.")
