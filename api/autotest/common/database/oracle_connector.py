# coding=utf-8

"""
Oracle数据库连接器
本例使用 python -> jvm -> oracle
直连实现，不需要安装Oracle Instant Client客户端
"""

__author__ = 'JIANGH'

import jpype, os
from . import _logger
# 执行jar位置路径
jar_path = os.path.join(os.path.abspath('.'), 'database_driver', 'oracle_connector.jar')

class OracleConn(object):
  """
  Class for the adapter for *Oracle* database

  keywords arguments(need):\n
  | host: the IP address or the name of the host\n
  | database: the database to connect to\n
  | user: the user to login\n
  | password: password of the user
  """
  def __init__(self, **kwargs):
    # 拼接URL
    url = "jdbc:oracle:thin:{user}/{password}@{host}:{database}".format(**kwargs)
    # 开启java虚拟机
    jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % jar_path)
    # 获取驱动类
    OracleConnector = jpype.JClass('cn.com.transcosmos.OracleConnector')
    # 传入URL并实例化
    self.connector = OracleConnector(url)
    # 调用connect方法
    self.connector.connect()

  # 关闭连接
  def close(self):
    self.connector.close()

  # TODO 未实现
  def execute(self, sql, params=None):
    '''执行sql'''
    pass

  # TODO 未实现
  def callproc(self, procname, params=None):
    pass

  # TODO 未实现
  def get_all_tables(self):
    '''获取所有表表名'''
    pass

  # TODO 未实现
  def get_tablelayout(self, table_name):
    '''获取指定表的表结构'''
    pass

  # TODO 未实现
  def get_columns_def_of_table(self, table_name):
    '''获取指定表的列名列表'''
    pass

  # TODO 未实现
  def get_pk_of_table(self, table_name):
    pass

  def insert(self, table_name, columns, datalist):
    """向表中插入数据
    位置参数：表名，列名列表，数据表格（二维列表）
    """
    columns_list_ = jpype.java.util.ArrayList()
    columns_list_.addAll(columns)

    _data_list = jpype.java.util.ArrayList()
    _data_list_item = jpype.java.util.ArrayList()
    for item in datalist:
      _data_list_item.addAll(item)
      _data_list.add(_data_list_item)
      _data_list_item = jpype.java.util.ArrayList()

    return self.connector.insert(table_name, columns_list_, _data_list)

  def select_with_header(self, sql):
    '''选取数据并返回表头
    返回值1: 数据表（二维列表）
    返回值2: 表头列表'''
    _result_list_map = list(self.connector.select(sql))
    if len(_result_list_map) > 0:
      key_list = list(_result_list_map[0].keySet().toArray())

    result_list = []
    for result_map in _result_list_map:
      result_row = []
      for key in key_list:
        result_row.append(result_map.get(key))
      result_list.append(result_row)
    return result_list, key_list

  def select(self, sql):
    return self.select_with_header(sql)[0]

  # 删除对象实例时关闭数据库连接，并关闭java虚拟机
  def __del__(self):
    self.close()
    jpype.shutdownJVM()
