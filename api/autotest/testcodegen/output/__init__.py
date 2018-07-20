# coding=utf-8

# 文件头模板
code_template = """\
# coding=utf-8

__author__ = 'robot'

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
import unittest, time, re, os

from .. import TestBase
from .. import BrowserTestBase
from ...common import (format_to_df, format_to_dict)
from ...common.log import Logger
from ...common.database import DBAdapter
from ...common.excel_reader import ExcelReader
from ...common.config_reader import readconfig

er = ExcelReader()
db_conn = DBAdapter().connector

'''
Next is the Code Generator Created:
'''
class %s(%s):

"""

# 方法定义模板
func_template = "\tdef %s(self):\n".expandtabs(2)

# 空指令模版
nop = '\t\tpass\n\n'.expandtabs(2)
