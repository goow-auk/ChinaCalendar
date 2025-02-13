import requests
import re
from icalendar import Calendar, Event

# 定义提取时和日的函数，去掉『』符号及其他多余字符
def format_summary(summary):
    # 清理掉 '『』' 和任何换行符
    cleaned_summary = summary.replace('『', '').replace('』', '').strip()
    
    # 正则提取时和日的部分
    match = re.search(r'([^\s]+时 [^\s]+日)', cleaned_summary)
    if match:
        return match.group(1)  # 只返回提取出的“时”和“日”
    
    return cleaned_summary  # 如果没有找到匹配的内容，返回原内容

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

            # 使用传入的 summary_modifier 函数修改 summary
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
    summary_modifier=lambda summary: format_summary(summary)
)

# 修改 cal_trunkBranch.ics 文件
modify_ics(
    'https://yangh9.github.io/ChinaCalendar/cal_trunkBranch.ics',
    'modified_cal_trunkBranch.ics',
    summary_modifier=lambda summary: format_summary(summary)
)
