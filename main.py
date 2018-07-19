# coding=utf-8

"""
自动化测试的外部主入口
以下为对test_case文件夹的json文件结构的说明：
| name      -> 文件名被用作测试标识，输出log
| baseUrl     -> 测试的页面URL标识
| start       -> 测试夹具：规定每一个测试case开始前的准备工作（可选）
| | action    -> 动作类型标识：click, select, input
| | mode      -> 选择target的模式标识：id, css, xpath, name, text, partial_text
| | target    -> 模式对应下的选择器标识
| | value     -> （可选）输入或比较的值
| end         -> 测试夹具：规定每一个测试case结束后的清理工作（可选）
| tests       -> 测试主体标识
| | case1     -> 'case1'为自定义的case号，内容为该case的全部动作
| | | action  -> 动作类型标识：click, select, input
| | | mode    -> 选择target的模式标识：id, css, xpath, name, text, partial_text
| | | target  -> 模式对应下的选择器标识
| | | value   -> （可选）输入或比较的值
| |
|
"""

__author__ = 'JIANGH'

import sys, os, json, types

from api.autotest.testcodegen.auto_runner import TestRunner
from api.autotest.common.config_reader import readconfig

if __name__ == "__main__":
  json_file = sys.argv[1] + '.json'
  with open(readconfig('case', 'case_folder') + json_file, encoding='utf-8') as f:
    setting = json.load(f)
    TestRunner(setting).run()
