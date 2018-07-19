# coding=utf-8

"""
SQL Server数据库连接器

TODO 待实现
"""

__author__ = 'JIANGH'

import pymssql

class MssqlConn(object):
  """
  Class for the adapter for *Microsoft SQL Server* database
  keywords arguments(need):
  | host: the IP address or the name of the host
  | database: the database to connect to
  | user: the user to login
  | password: password of the user
  """
  # TODO 未实现
  def __init__(self, **kwargs):
    pass

  # 关闭连接
  # TODO 未实现
  def close(self):
    pass

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

  # TODO 未实现
  def insert(self, table_name, columns, datalist):
    pass

  # TODO 未实现
  def select(self, sql):
    pass

  # TODO 未实现
  # 删除对象实例时关闭数据库连接，并关闭java虚拟机
  def __del__(self):
    pass
