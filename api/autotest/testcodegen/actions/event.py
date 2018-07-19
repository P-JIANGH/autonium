# coding=utf-8

"""
事件类代码模板模块

编码/运行前提:

前置变量名            *element*

浏览器驱动变量名       *driver*

Excel驱动变量名       *er*

数据库驱动变量名      *db_conn*

且所需要的包均已在模板中导入，或在返回的字符串中导入

返回的字符串如果为一个字符串，则需要自己添加好制表符
"""

__author__ = "JIANGH"

from . import Args

@Args({
  "mode": "select",
  "target": "text"
})
def click(**params):
  """点击事件代码模板"""
  from .find import find_element
  return [
    find_element(**params),
    "element.click()"
  ]

@Args({
  "mode": "select",
  "target": "text"
})
def select(**params):
  from .find import find_element
  return [
    find_element(**params),
    "Select(element).select_by_index()"
  ]

@Args({
  "mode": "select",
  "target": "text",
  "value": "text"
})
def input_value(**params):
  from .find import find_element
  return [
    find_element(**params),
    "element.clear()",
    "element.send_keys('{value}')".format(**params)
  ]

@Args({
  "picture_name": "text"
})
def screen_shot(**params):
  from ...common.config_reader import readconfig
  picture_path = readconfig("result", "picture_folder")
  return ["self.driver.save_screenshot('{0}{picture_name}.png')".format(picture_path, **params)]
