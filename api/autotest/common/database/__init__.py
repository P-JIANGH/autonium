# coding=utf-8

__author__ = 'JIANGH'

class DBType():
  """定义了数据库类型的常量类"""
  ORACLE = 'oracle'
  SQLITE = 'sqlite'
  MSSQL = 'sqlserver'
  MYSQL = 'mysql'
  POSTGRE = 'postgresql'

from ...common.config_reader import readconfig
from ...common.log import Logger

_logger = Logger('DBAdapter').get_logger()

class DBAdapter(object):
  """
  数据库适配器工厂类

  读取配置文件中的数据库相关的参数

  根据类型生成适配数据库的连接池
  """
  def __init__(self):
    self.type = readconfig('database', 'type')
    self.server = readconfig('database', 'host')
    self.database = readconfig('database', 'database')
    self.user = readconfig('database', 'user')
    self.password = readconfig('database', 'password')
    _logger.info('connect: type:%s, host:%s, schame:%s, user: %s' % (self.type, self.server, self.database, self.user))

  @property
  def connector(self):
    """
    判断数据库种类，依照种类返回连接池
    引入数据库驱动类库失败时，log输出error
    connent()方法失败时返回空
    """
    dbtype = self.type
    try:
      # SQL Server
      if dbtype == DBType.MSSQL:
        from .mssql_connector import MssqlConn
        return MssqlConn(host=self.server, database=self.database, user=self.user, password=self.password)

      # MySQL
      elif dbtype == DBType.MYSQL:
        from .mysql_connector import MysqlConn
        return MysqlConn(host=self.server, db=self.database, user=self.user, passwd=self.password)

      # Oracle
      elif dbtype == DBType.ORACLE:
        from .oracle_connector import OracleConn
        return OracleConn(host=self.server, database=self.database, user=self.user, password=self.password)

      # PostgreSQL
      elif dbtype == DBType.POSTGRE:
        from .postgresql_connector import PostgreConn
        return PostgreConn(host=self.server, database=self.database, user=self.user, password=self.password)

      # 这几种类型之外的情况报错
      else:
        raise Exception('Could not find the TYPE of database')
    except ImportError:
      _logger.error('Could not find the DRIVER of database')
