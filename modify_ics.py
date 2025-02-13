import requests
import re
from icalendar import Calendar, Event

# 定义提取“日”的函数，正则匹配最后的“日”
def extract_day(summary):
    # 正则提取“日”前的部分内容
    match = re.search(r'(\S+日)$', summary)
    if match:
        return match.group(1)  # 返回“日”字前的部分
    return summary  # 如果没有找到“日”，则返回原内容

def modify_ics(url, file_name, summary_modifier=None):
    # 获取 ICS 文件
    response = requests.get(url)
    ics_data = response.content  # 使用 .content 获取字节数据

    # 解析 ICS 文件
    calendar = Calendar.from_ical(ics_data)

    # 修改每个事件
    for component in calendar.walk('vevent'):
        summary = component.get('summary')
        location = component.get('location')

        # 只在 summary 和 location 都存在的情况下修改
        if summary and location:
            # 交换 summary 和 location 的内容
            component['summary'] = location  # 设置新的 summary 为原来的 location
            component['location'] = None  # 清空 location 字段

            # 提取 summary 中的“日”部分，如果指定了 summary_modifier 函数
            if summary_modifier:
                component['summary'] = summary_modifier(summary)  # 修改 summary

    # 保存修改后的 ICS 文件，强制指定 UTF-8 编码
    with open(file_name, 'wb') as f:
        f.write(calendar.to_ical())  # 写入时不需要额外的编码转换

    print(f"ICS file '{file_name}' has been modified successfully.")

# 修改 cal_lunar.ics 文件
modify_ics(
    'https://yangh9.github.io/ChinaCalendar/cal_lunar.ics', 
    'modified_cal_lunar.ics', 
    summary_modifier=lambda summary: extract_day(summary)
)

# 修改 cal_trunkBranch.ics 文件
def trunk_branch_modifier(summary):
    # 提取并保留 `乙丑时 甲子日`
    match = re.search(r'([^\s]+时 [^\s]+日)', summary)
    if match:
        return match.group(1)  # 返回 `乙丑时 甲子日`
    return summary  # 如果没有找到，则返回原内容

modify_ics(
    'https://yangh9.github.io/ChinaCalendar/cal_trunkBranch.ics',
    'modified_cal_trunkBranch.ics',
    summary_modifier=trunk_branch_modifier
)
