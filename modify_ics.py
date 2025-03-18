import requests
import re
from icalendar import Calendar

def format_summary(summary):
    """
    清理 summary 字符串，提取包含“时”和“日”的部分。
    """
    cleaned_summary = summary.replace('『', '').replace('』', '').strip()
    match = re.search(r'([^\s]+时 [^\s]+日)', cleaned_summary)
    return match.group(1) if match else cleaned_summary

def modify_ics(url, file_name, summary_modifier=None):
    """
    下载并修改 ICS 文件，将 location 赋值给 summary，并最终删除 location 字段。
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        ics_data = response.content
    except requests.RequestException as e:
        print(f"Error fetching ICS file: {e}")
        return

    try:
        calendar = Calendar.from_ical(ics_data)
        for component in calendar.walk('vevent'):
            summary = component.get('summary')
            location = component.get('location')

            if summary and location:
                component['summary'] = summary_modifier(summary) if summary_modifier else location
            
            # 删除 location 字段
            if 'location' in component:
                del component['location']

        with open(file_name, 'wb') as f:
            f.write(calendar.to_ical())
        print(f"ICS file '{file_name}' has been modified successfully.")
    except Exception as e:
        print(f"Error processing ICS file: {e}")

# 处理 cal_lunar.ics
modify_ics(
    'https://yangh9.github.io/ChinaCalendar/cal_lunar.ics',
    'modified_cal_lunar.ics',
    summary_modifier=format_summary
)

# 处理 cal_trunkBranch.ics
modify_ics(
    'https://yangh9.github.io/ChinaCalendar/cal_trunkBranch.ics',
    'modified_cal_trunkBranch.ics',
    summary_modifier=format_summary
)
