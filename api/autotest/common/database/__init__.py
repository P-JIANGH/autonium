# coding=utf-8

__author__ = 'JIANGH'

class DBType():
  ORACLE = 'oracle'
  SQLITE = 'sqlite'
  MSSQL = 'sqlserver'
  MYSQL = 'mysql'
  POSTGRE = 'postgresql'

from ...common.config_reader import readconfig
from ...common.log import Logger

_logger = Logger('DBAdapter').get_logger()

class DBAdapter(object):
  def __init__(self):
    self.logger = _logger
    self.type = readconfig('database', 'type')
    self.server = readconfig('database', 'host')
    self.database = readconfig('database', 'database')
    self.user = readconfig('database', 'user')
    self.password = readconfig('database', 'password')
    self.logger.info('connect: type:%s, host:%s, schame:%s, user: %s' % (self.type, self.server, self.database, self.user))

  @property
  def connector(self):
    """
    判断数据库种类，依照种类返回连接池
    引入数据库驱动类库失败时，log输出error
    connent()方法失败时返回空
    TODO 之后需要修改成log输出：请确认数据库参数 之类的
    """
    dbtype = self.type
    try:
      if dbtype == DBType.MSSQL:
        from .mssql_connector import MssqlConn
        return MssqlConn(host=self.server, database=self.database, user=self.user, password=self.password)

      elif dbtype == DBType.MYSQL:
        from .mysql_connector import MysqlConn
        return MysqlConn(host=self.server, db=self.database, user=self.user, passwd=self.password)

      elif dbtype == DBType.ORACLE:
        from .oracle_connector import OracleConn
        return OracleConn(host=self.server, database=self.database, user=self.user, password=self.password)

      elif dbtype == DBType.POSTGRE:
        from .postgresql_connector import PostgreConn
        return PostgreConn(host=self.server, database=self.database, user=self.user, password=self.password)

      else:
        raise Exception('Could not find the TYPE of database')
    except ImportError:
      self.logger.error('Could not find the DRIVER of database')

  def select(self, sql):
    return self.connector.select(sql)

  def insert(self, table_name, columns, datalist):
    return self.connector.insert(table_name, columns, datalist)

  def close(self):
    return self.connector.close()
