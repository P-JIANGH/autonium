# coding=utf-8

"""
判断类代码模板模块

编码/运行前提:

前置变量名            *element*

浏览器驱动变量名       *driver*

Excel驱动变量名       *er*

数据库驱动变量名      *db_conn*

且所需要的包均已在模板中导入，或在返回的字符串中导入
"""


__author__ = 'JIANGH'

from . import Args
from .find import find_element

@Args({
  "mode": "select",
  "target": "text",
})
def assert_element_exist(**params):
  return [
    "element = None"
    "try:",
    "\telement = %s" % find_element(**params),
    "except NoSuchElementException:"
    "  pass"
    "self.assertIsNotNone(element)"
  ]

def assert_format(**params):
  pass

@Args({
  "mode": "select",
  "target": "text",
  "value": "text"
})
def assert_text_value(**params):
  return [
    find_element(**params),
    'self.assertEqual(element.text, {value})'.format(**params)
  ]

def assert_table_value_with_excel(**params):
  # TODO 待实现（生成测试报告结果?）
  pass