# coding=utf-8
"""
数据库操作类代码模板模块

编码/运行前提:

前置变量名            *element*

浏览器驱动变量名       *driver*

Excel驱动变量名       *er*

数据库驱动变量名      *db_conn*

且所需要的包均已在模板中导入，或在返回的字符串中导入
"""

from . import Args

@Args({
  'file_path': 'text',
  'sheet_index': 'number',
  'header_range': 'text',
  'data_range': 'text',
  'table_name': 'text'
})
def insert_to_database_from_excel(**params):
  from .excel import select_table_value_from_excel
  return [
    select_table_value_from_excel(**params),
    "db_conn.insert('{table_name}', excel_table_header, excel_table_data)".format(**params)
  ]

