# coding=utf-8

"""
Excel文件读取器

TODO 图像处理模块待定，若实现，可以实现图片剪裁
"""

__author__ = 'JIANGH'

import xlwings as xw
import contextlib
from PIL import Image
# from difflib import get_close_matches

class ExcelReader():
  """
  使用方法如下：
  Example:

  > er = ExcelReader()

  > with er.read(file_path) as reader:
  >   reader.open_sheet(sheet_index=2)
  >   reader.read_value('B4:B8')
  >   reader.read_data_to_table('B5')
  >   reader.read_data_to_right('B5')
  >   reader.insert_picture(picture_path, 'E4', percent='50%')
  """
  def __init__(self):
    """
    Excel读取器
    不可见的形式打开Excel应用
    使用with er.read(file_path) as reader:的方式
    打开一个Excel工作簿
    """
    self.excel_app = xw.App(visible=False)
    self.__pid = self.excel_app.pid   # 备用属性，出现进程不干净的情况时使用
    self.excel_book = None
    self.excel_sheet = None
    self.number_handler = lambda num: int(num) if num == int(num) else num

  # 使用上下文管理，强制使用with句，操作完自动close
  @contextlib.contextmanager
  def open_excel(self, excel_path):
    self.excel_book = self.excel_app.books.open(excel_path)
    yield self
    self.close()

  def open_sheet(self, sheet_index):
    """打开指定Sheet"""
    if sheet_index == None:
      raise Exception('Param Error!')
    self.excel_sheet = self.excel_book.sheets[sheet_index]
    return self

  def write_value(self, value, start_range, end_range=None):
    """向单元格或单元格范围写入数据"""
    self.excel_sheet.range(start_range).options(numbers=self.number_handler).value = value
    return self

  def read_value(self, start_range, end_range=None):
    """读取单元格或单元格范围数据"""
    return self.excel_sheet.range(start_range, end_range).options(numbers=self.number_handler).value

  def read_header(self, start_range):
    """指定起始点，拓展向右读取数据"""
    return self.excel_sheet.range(start_range).options(numbers=self.number_handler, expand='right').value

  def read_table(self, start_range):
    """指定起始点，拓展向右下读取表格数据"""
    return self.excel_sheet.range(start_range).options(numbers=self.number_handler, expand='table').value

  def insert_picture(self, picture_path, point, percent=None, width=None, height=None):
    """
    向指定单元格插入图片，可以指定宽高或百分比（缩放）
    For Example:
    >>> insert_picture('path', 'E4') # for default size
    >>> insert_picture('path', 'E4', percent='30%')
    >>> insert_picture('path', 'E4', width=100)
    >>> insert_picture('path', 'E4', height=100)
    >>> insert_picture('path', 'E4', width=100, height=100)
    """
    rng = self.excel_sheet.range(point)
    image_width, image_height = Image.open(picture_path).size
    if percent: # 指定百分比的情况
      per = int(percent.replace('%', '')) / 100
      w, h = image_width * per, image_height * per
    else:       # 指定宽高的情况
      w, h = width, height
    # 插入图片
    self.excel_sheet.pictures.add(picture_path, left=rng.left, top=rng.top, width=w, height=h)
    return self

  def close(self):
    self.excel_book.save()
    self.excel_book.close()
    self.excel_app.quit()

  def __del__(self):
    if xw.apps.count > 0:
      self.excel_app.quit()
