
# Python-Arcaea-Library
本Python包是一个用于处理Arcaea谱面 (*.aff) 相关的包，您可以使用此包编写您自己的Arcaea谱面工具。



# 更新日志
> **v1.0.0 - 2023-8-15**
- 上传到GitHub
- 修复algorithm中处理计算Arc坐标相关函数错误的将SineOut和SineIn互相反着使用的问题

> **v1.1.0 - 2023-10-16**
- 添加了获取timingGroup事件列表的方法
  - logicChart.getTimingGroupEvents(`int` idx)
  - logicChart.getTimingGroupEventsUnchecked(`int` idx)
- 在timingGroup中添加了获取指定事件的方法
  - timingGroup.getEventsByType(`class` t, `bool` toList)
  - timingGroup.getEventsIterableByType(`class` t)
  - timingGroup.getEventsBy(`lambda` t, `bool` toList)
  - timingGroup.getEventsIterableBy(`lambda` t)

> **v1.2.0 - 2024-08-04**
- 修复了部分缓动类型使用了错误函数的问题
- 修复了camera缓动描述错误的问题=
- 添加了一些获取事件的方法
  - timingGroup.getEventsInRange(`int` t, `int` et)
  - timingGroup.getEventsInRangeWithType(`int` t, `int` et, `class|tuple` ft)
  - timingGroup.getEventAtTiming(`int` t, `class|tuple` ft)

> **v1.3.0 - 2024-11-26**
- 对任意类型的 Arc 进行支持

# 使用例

读取谱面与保存谱面
```python
from arclib.logicChart import *

# 读取谱面
chart_path = 'input.aff'
with open(chart_path, 'r') as f:
    chart = logicChart(f.readlines())

# 保存谱面
chart = logicChart() # 这里因为是用于测试所以新建一个谱面
chart_path = 'output.aff'
with open(chart_path, 'w') as f:
    f.write(str(chart))
```
---

获取指定timinggroup中的所有事件
```python
group_id = 0
# 获取组0 (基准组) 中的所有事件
base_group_events = chart.getTimingGroupEvents(group_id) 
```

