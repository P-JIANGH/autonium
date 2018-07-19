# coding=utf-8

"""
Log输出器
"""

__author__ = 'JIANGH'

import logging, time, threading
from .config_reader import readconfig

# 设定log等级
LEVEL = getattr(logging, readconfig('result', 'log_level'), logging.NOTSET)

"""
设定log信息格式，可设置参数如下，引用自python的文档：
%(name)s            Name of the logger (logging channel)
%(levelno)s         Numeric logging level for the message (DEBUG, INFO,
                    WARNING, ERROR, CRITICAL)
%(levelname)s       Text logging level for the message ("DEBUG", "INFO",
                    "WARNING", "ERROR", "CRITICAL")
%(pathname)s        Full pathname of the source file where the logging
                    call was issued (if available)
%(_filename)s        _filename portion of pathname
%(module)s          Module (name portion of _filename)
%(lineno)d          Source line number where the logging call was issued
                    (if available)
%(funcName)s        Function name
%(created)f         Time when the LogRecord was created (time.time()
                    return value)
%(asctime)s         Textual time when the LogRecord was created
%(msecs)d           Millisecond portion of the creation time
%(relativeCreated)d Time in milliseconds when the LogRecord was created,
                    relative to the time the logging module was loaded
                    (typically at application startup time)
%(thread)d          Thread ID (if available)
%(threadName)s      Thread name (if available)
%(process)d         Process ID (if available)
%(message)s         The result of record.getMessage(), computed just as
                    the record is emitted
"""
FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'
# 全局设置
logging.basicConfig(level=LEVEL, format=FORMAT)

class Logger():

  """
  将logger实例存于dict中，键为线程ID

  取得配置好的logger。TODO: SocketHandler待添加

  可以同时输出到控制台和文件中去
  
  文件名格式：YYYYMMDDHHMMSS-%(name).log
  """
  __logger_dict = {}

  def __init__(self, filename):
    self.thread_id = threading.get_ident()
    from ..testcodegen import time_format
    # 设置文件全路径
    _filepath = readconfig('result', 'log_folder')
    # 使用时间戳设置文件名
    self.__filename = _filepath + time.strftime(time_format, time.localtime(time.time())) + '-' + filename + '.log'
    self.__logger = self.init_logger(filename)

  def init_logger(self, name):
    # 如果当前线程没有logger对象则新建实例
    if self.__logger_dict.get(self.thread_id) == None:
      _log_creator = logging.getLogger(name=name)
      # socket = logging.handlers.SocketHandler TODO
      # 创建文件输出处理器
      _console = logging.FileHandler(filename=self.__filename, mode='w', encoding='utf-8')
      # 设置文件输出处理器的格式，使用FORMAT全局变量进行统一
      _console.setFormatter(logging.Formatter(FORMAT))
      _log_creator.addHandler(_console)
      self.__logger_dict[self.thread_id] = _log_creator
      print('在线程%d新建一个Logger' % self.thread_id)
    else:
      _log_creator = self.__logger_dict.get(self.thread_id)
      _log_creator.name = name
    return _log_creator

  @property
  def log_path(self):
    return self.__filename

  def get_logger(self, name=None):
    if not name == None:
      self.__logger.name = name
    return self.__logger

  def close(self):
    for handler in self.__logger.handlers:
      self.__logger.removeHandler(handler)
    self.__logger = None
    self.__logger_dict.pop(self.thread_id)
