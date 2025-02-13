import requests
from icalendar import Calendar, Event

# 获取 ICS 文件
url = 'https://yangh9.github.io/ChinaCalendar/cal_lunar.ics'
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
        component['summary'] = location  # 设置 summary 为 location
        component['location'] = None  # 清空 location 字段

# 保存修改后的 ICS 文件，强制指定 UTF-8 编码
with open('modified_cal_lunar.ics', 'wb') as f:  # 使用二进制写入
    f.write(calendar.to_ical())  # 写入时不需要额外的编码转换

print("ICS file has been modified successfully.")
