# coding=utf-8

"""
Oracle数据库连接器
本例使用 python -> jvm -> oracle
直连实现，不需要安装Oracle Instant Client客户端
"""

__author__ = 'JIANGH'

import jpype, os
from jpype import java, JavaException, JClass, JPackage
from . import _logger
from ..config_reader import readconfig
# 执行jar位置路径
jar_path = readconfig('database', 'jarpath')

def log_java_exception(exception):
  _logger.error('\n'.join([line for line in exception.stacktrace().splitlines() if not line == '']))

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
    jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % jar_path, "-Djdbc.drivers=oracle.jdbc.OracleDriver")
    DriverManager = java.sql.DriverManager
    try:
      self.connector = DriverManager.getConnection(url)
      self.connector.setAutoCommit(False)
    except JavaException as e:
      _logger.error('Oracle Driver: Cannot Connected to the DataBase')
      log_java_exception(e)
      self.connector = None
      raise e
    else:
      _logger.info('Oracle Driver: Connect Success')

  # 关闭连接
  def close(self):
    if self.connector:
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
    # 测试请求数据库
    testSql = 'select {cols} from "{table_name}" where rownum = 1'.format(
      cols=', '.join(columns), table_name=table_name
    )
    # 获取目标表的列定义
    try:
      preStat = self.connector.prepareStatement(testSql)
      testResult = preStat.executeQuery()
      columnsTypeList = [testResult.getMetaData().getColumnType(jpype.JInt(i + 1)) for i in range(len(columns))]
    except JavaException as e:
      _logger.error('Oracle Driver: Error In Execute Test SQL')
      log_java_exception(e)
      self.close()
      raise e

    # 生成SQL模板
    insert_sql_template = 'insert into "{table_name}" ({cols}) values ({placeholders})'.format(
      table_name=table_name, cols=', '.join(columns), placeholders=', '.join(['? ' for i in range(len(columns))])
    )
    result = 0
    try:
      for row in datalist:
        preStat = self.connector.prepareStatement(insert_sql_template)
        paramList = []
        for i, data in enumerate(row):
          if data == None:
            preStat.setNull(jpype.JInt(i + 1), columnsTypeList[i])
            paramList.append(None)
          else:
            param_class = self.__switchType(columnsTypeList[i])
            param = self.__prepareParam(param_class, data)
            if param_class.getSimpleName() == "Integer":
              methodName = 'setInt'
            else:
              methodName = 'set' + param_class.getSimpleName()
            getattr(preStat, methodName)(jpype.JInt(i + 1), param)
            paramList.append(str(param._pyv))
        _logger.info("\nExecute: " + insert_sql_template + "\nParams: " + ', '.join(paramList))
        result = result + preStat.executeUpdate()
    except JavaException as e:
      _logger.error("Oracle Driver: SQL Error in execute insert")
      log_java_exception(e)
      self.connector.rollback()
      self.close()
      raise e
    else:
      self.connector.commit()
      _logger.info("Oracle Driver: Insert %d rows into %s" % (result, table_name))

  def __switchType(self, code):
    Types = java.sql.Types
    if (code == Types.VARCHAR or
      code == Types.CHAR or
      code == Types.NCHAR or
      code == Types.NVARCHAR or
      code == Types.LONGNVARCHAR or
      code == Types.LONGVARCHAR):
      return java.lang.Class.forName('java.lang.String')
    elif code == Types.INTEGER:
      return java.lang.Class.forName('java.lang.Integer')
    elif code == Types.BIGINT:
      return java.lang.Class.forName('java.lang.Long')
    elif code == Types.BOOLEAN:
      return java.lang.Class.forName('java.lang.Boolean')
    elif code == Types.NUMERIC or code == Types.DECIMAL:
      return java.lang.Class.forName('java.math.BigDecimal')
    elif code == Types.DOUBLE:
      return java.lang.Class.forName('java.lang.Double')
    elif code == Types.FLOAT:
      return java.lang.Class.forName('java.lang.Float')
    elif code == Types.DATE:
      return java.lang.Class.forName('java.sql.Date')
    elif code == Types.TIME or code == Types.TIME_WITH_TIMEZONE:
      return java.lang.Class.forName('java.sql.Time')
    elif code == Types.TIMESTAMP or code == Types.TIMESTAMP_WITH_TIMEZONE:
      return java.lang.Class.forName('java.sql.Timestamp')
    else:
      return java.lang.Class.forName('java.lang.String')

  def __prepareParam(self, param_class, data):
    if data == None: return None
    try:
      if param_class.getSimpleName() == 'BigDecimal':
        return java.math.BigDecimal(jpype.JString(str(data)))
      elif param_class.getSimpleName() == 'String':
        return jpype.JString(str(data))
      elif param_class.getSimpleName() == 'Integer':
        return java.lang.Integer(jpype.JString(str(data))).intValue()
      else:
        return param_class.getMethod('valueOf', java.lang.Class.forName('java.lang.String')).invoke(None, jpype.JString(str(data)))
    except JavaException as e:
      _logger.error("Oracle Driver: SQL Error in prepare Params")
      log_java_exception(e)
      self.close()
      raise e

  def select_with_header(self, sql):
    '''选取数据并返回表头
    返回值1: 数据表（二维列表）
    返回值2: 表头列表'''
    pass

  def select(self, sql):
    result_list = []
    try:
      preStat = self.connector.prepareStatement(sql)
      query_result = preStat.executeQuery()
      columnCounts = query_result.getMetaData().getColumnCount()
      while columnCounts > 0 and query_result.next():
        result_list_item = []
        for i in range(columnCounts):
          result_list_item.append(query_result.getObject(jpype.JInt(i + 1))._pyv)
        result_list.append(result_list_item)
    except JavaException as e:
      _logger.error("Oracle Driver: SQL Error in Query Select")
      log_java_exception(e)
      self.close()
      raise e
    else:
      return result_list

  # 删除对象实例时关闭数据库连接，并关闭java虚拟机
  def __del__(self):
    self.close()
    if jpype.isJVMStarted:
      jpype.shutdownJVM()
