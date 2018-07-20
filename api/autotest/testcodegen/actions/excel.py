# coding=utf-8
"""
Excel操作类代码模板模块

编码/运行前提:

前置变量名            *element*

浏览器驱动变量名       *driver*

Excel驱动变量名       *er*

数据库驱动变量名      *db_conn*

excel导出的表头数据   *excel_table_header*

excel导出的表格数据   *excel_table_data*

且所需要的包均已在模板中导入，或在返回的字符串中导入
"""

from . import Args

@Args({
  "file_path": "text",
  "sheet_index": "number",
  "header_range": "text",
  "data_range": "text",
})
def select_table_value_from_excel(**params):
  """return excel_table_data, excel_table_header, excel_df"""
  header_range = params.get('header_range')
  data_range = params.get('data_range')
  # 参数检查
  if not (header_range and data_range):
    raise Exception(
      'insert_to_database_from_excel needs,'
      'header_range and data_range options,'
      'please set it and run one more time!'
      )
  # header参数检查
  if str(header_range).find(':') > -1:
    header_start, header_end = str(header_range).split(':')
    if (len(header_start) > 1 and len(header_end) > 1) and (header_start[1] != header_end[1]):
      raise Exception(
        "the positions of header has wrong,"
        "or, please check if the header only has one line!"
        )
    header_func = "read_value('%s', '%s')" % (header_start, header_end)
  else: header_func = "read_header('%s')" % header_range

  # 数据参数检查
  if str(data_range).find(':') > -1:
    data_start, data_end = str(data_range).split(':')
    data_func = "read_value('%s', '%s')" % (data_start, data_end)
  else: data_func = "read_table('%s')" % data_range
  return """\
    with er.open_excel(r"{file_path}") as reader:
      reader.open_sheet({sheet_index})
      excel_table_data = reader.{0}
      excel_table_header = reader.{1}
      excel_df = format_to_df(excel_table_data, excel_table_header)
  """.format(data_func, header_func, **params)

@Args({
  "file_path": "text",
  "sheet_index": "number",
  "start_range": "text",
  "sql": "text"
})
def insert_to_excel_from_database(**params):
  import re
  pos_dict = re.compile(r'(?P<col>[a-zA-Z]+)(?P<row>[0-9]+)').match(params.get('start_range')).groupdict()
  col_index = pos_dict['col']
  row_index = pos_dict['row']
  return """\
    data = db_conn.select("{sql}")
    with er.open_excel(r"{file_path}") as reader:
      reader.open_sheet({sheet_index})
      for i, d in enumerate(data):
        row_index = str({row} + i)
        reader.write_value(d, ('{col}' + row_index))
  """.format(**params, col=col_index, row=row_index)

@Args({
  "picture_name": "text",
  "file_path": "text",
  "sheet_index": "number",
  "point": "text",
  "width": "number",
  "height": "number",
  "percent": "text"
})
def insert_screenshot_to_excel(**params):
  """
  Before insert any .png file,

  You need open a excel book and open a sheet at first
  """
  from ...common.config_reader import readconfig
  picture_path = readconfig('result', 'picture_folder')
  if params.get('percent'):
    return """\
      with er.open_excel(r"{file_path}") as reader:
        reader.open_sheet({sheet_index})
        reader.insert_picture(r\"{path}{picture_name}.png\", '{point}', percent='{percent}', width={width}, height={height})
    """.format(**params, path=picture_path)
