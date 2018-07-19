# coding=utf-8

"""
查找类代码模板模块

编码/运行前提:

前置变量名            *element*

浏览器驱动变量名       *driver*

Excel驱动变量名       *er*

数据库驱动变量名      *db_conn*

且所需要的包均已在模板中导入，或在返回的字符串中导入
"""

__author__ = 'JIANGH'

from . import ModeType, Args

@Args({
  "mode": "select",
  "target": "text"
})
def find_element(**params):
  """选择一个画面元素"""
  mode = params.get("mode")
  if mode == ModeType.CSS_SELECTOR:
    return "element = self.driver.find_element_by_css_selector('{target}')".format(**params)
  elif mode == ModeType.NAME:
    return "element = self.driver.find_element_by_name('{target}')".format(**params)
  elif mode == ModeType.CLASS:
    return "element = self.driver.find_element_by_class_name('{target}')".format(**params)
  elif mode == ModeType.XPATH:
    return "element = self.driver.find_element_by_xpath('{target}')".format(**params)
  elif mode == ModeType.INNER_TEXT:
    return "element = self.driver.find_element_by_link_text('{target}')".format(**params)
  elif mode == ModeType.PARTIAL_TEXT:
    return "element = self.driver.find_element_by_partial_link_text('{target}')".format(**params)
  else:
    return "element = self.driver.find_element_by_id('{target}')".format(**params)

@Args({
  "mode": "select",
  "target": "text"
})
def find_elements(**params):
  """选择多个画面元素"""
  mode = params.get('mode')
  if mode == ModeType.CSS_SELECTOR:
    return "element = self.driver.find_elements_by_css_selector('{target}')".format(**params)
  elif mode == ModeType.CLASS:
    return "element = self.driver.find_elements_by_class_name('{target}')".format(**params)
  elif mode == ModeType.NAME:
    return "element = self.driver.find_elements_by_name('{target}')".format(**params)
  elif mode == ModeType.XPATH:
    return "element = self.driver.find_elements_by_xpath('{target}')".format(**params)
  elif mode == ModeType.INNER_TEXT:
    return "element = self.driver.find_elements_by_link_text('{target}')".format(**params)
  elif mode == ModeType.PARTIAL_TEXT:
    return "element = self.driver.find_elements_by_partial_link_text('{target}')".format(**params)
  else:
    return "element = self.driver.find_elements_by_id('{target}')".format(**params)

@Args({
  "target": "text"
})
def select_frame(**params):
  """切换Frame"""
  return [
    'self.driver.switch_to.default_content()',
    "self.driver.switch_to.frame('{target}')".format(**params)
  ]

@Args({
  "header_selector": "text",
  "data_selector": "text",
  "except_column_indexs": "text",
})
def select_table_value_from_page(**params):
  """从画面上选择出一个列表的数据"""
  return """\
    with open('../script_lib/parse_table_value.js', encoding='utf-8') as file:
      script = file.read()
      header = driver.execute_script(script, '{header_selector}')[0]
      result = driver.execute_script(script, '{data_selector}')
      input_indexs = '{except_column_indexs}'
      except_column_indexs = sorted([int(d.replace(' ', '')) for d in input_indexs.split(',')])
      page_data = format_to_df(result, columns=header)
      for col in except_column_indexs:
        del page_data[header[col]]
  """.format(**params)
