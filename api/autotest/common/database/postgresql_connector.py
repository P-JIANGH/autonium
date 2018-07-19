# coding=utf-8

"""
PostgreSQL 数据库连接器
"""

__author__ = 'JIANGH'

import psycopg2, contextlib
from psycopg2 import sql
from functools import reduce
from . import _logger

class PostgreConn(object):
  """
  Class for the adapter for *Postgresql* database

  keywords arguments(need):\n
  | host: the IP address or the name of the host\n
  | database: the database to connect to\n
  | user: the user to login\n
  | password: password of the user
  """
  def __init__(self, **kwargs):
    # 连接数据库
    try:
      self.connector = psycopg2.connect(**kwargs)
      cursor = self.connector.cursor()
      # 测试数据库连接
      self.execute("select 1")
      _logger.info('连接数据库成功！')
      cursor.close()
    except Exception:
      _logger.error('连接数据库失败！')
      cursor.close()

  def close(self):
    _logger.info('关闭数据库连接！')
    self.connector.close()

  @contextlib.contextmanager
  def execute(self, sql, params=None):
    """强制使用上下文管理，使用with语句调用execute方法，
    with后会自动调用close方法"""
    _logger.debug("Execute: %s; params: %s" % (sql, params))
    cursor = self.connector.cursor()
    cursor.execute(sql, params)
    yield cursor
    cursor.close()

  def callproc(self, procname, params=None):
    cursor = self.connector.cursor()
    cursor.callproc(procname, params)
    return cursor

  def get_all_tables(self):
    '''获取所有表表名'''
    sql_str = "select table_name from information_schema.columns where table_schema = 'public'"
    return self.select(sql_str)

  def get_tablelayout(self, table_name):
    '''获取指定表的表结构'''
    sql_str = "select * from information_schema.columns where table_schema = 'public' and table_name = %s"
    return self.select(sql_str, table_name)

  def get_columns_def_of_table(self, table_name):
    '''获取指定表的列名列表'''
    sql_str = "select column_name from information_schema.columns where table_schema = 'public' and table_name = %s"
    return reduce(lambda x, y: [*x, *y], self.select(sql_str, table_name), list())

  def get_pk_of_table(self, table_name):
    '''获取指定表的主键列表'''
    sql_str = "select column_name from information_schema.key_column_usage where table_name = %s order by ordinal_position"
    return reduce(lambda x, y: [*x, *y], self.select(sql_str, table_name), list())

  def insert(self, table_name, columns, datalist):
    """向表中插入数据
    位置参数：表名，列名列表，数据表格（二维列表）
    """
    # 格式化sql模板
    format_sql = sql.SQL("insert into {table_name} ({cols}) values ({datas})").format(
      table_name=sql.Identifier(table_name),
      cols=sql.SQL(', ').join(map(sql.Identifier, columns)),
      datas=sql.SQL(', ').join(sql.Placeholder() * len(columns))
    )
    try:
      # 执行多个sql并插入数据
      print('Execute: %s' % format_sql.as_string(self.connector))
      cursor = self.connector.cursor()
      rowcount = cursor.executemany(format_sql, datalist)
      cursor.close()
    except Exception as e:
      # 异常时回滚
      self.connector.rollback()
      _logger.error(e)
      _logger.error('rollback')
      raise e
    else:
      # 无异常时提交
      self.connector.commit()
      _logger.info('insert %d rows' % (rowcount if not rowcount == None else 0))

  def select(self, sql, *params):
    '''选取数据'''
    with self.execute(sql, params) as cursor:
      return cursor.fetchall()

  def select_with_header(self, sql):
    """选取数据并返回表头
    返回值1: 数据表（二维列表）
    返回值2: 表头列表
    """
    with self.execute(sql) as cursor:
      header = [column.name for column in cursor.description]
      return cursor.fetchall(), header

  # def update(self):
  #   pass

  # def delete(self):
  #   pass

  # 删除对象实例时关闭数据库连接
  def __del__(self):
    self.close()
