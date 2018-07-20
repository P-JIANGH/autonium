# coding=utf-8

"""
自动化测试的外部主入口
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
