# coding=utf-8

"""
生成代码，并运行测试

from auto_runner import TestRunner

TestRunner(json_setting).run()
"""

__author__ = 'JIANGH'

__all__ = ['TestRunner']

import unittest, time, types, functools, os, datetime

from . import TestBase, log_result, log_codes_creator, actions
from ..common.config_reader import readconfig
from ..common.log import Logger

class TestRunner:
  """
  测试运行类

  初始化时取得测试名称，logger组件，并将配置信息生成为测试类代码
  """
  def __init__(self, data=None):
    if data == None:
      data = {}
    self.__name = data.get('name')
    self.__logger = Logger(data.get('name'))
    self.__filepath = os.path.join(readconfig('code_generate', 'generate_folder'), '%s.py' % self.__name)
    self.parser(data)

  def create_func(self, func_name, func_settings=None):
    '''
    格式化action代码

    动态调用action获得返回值，根据条件为返回值字符串添加换行符或制表符
    '''
    from .output import (func_template, nop)
    # 获得函数头
    codes = func_template % func_name
    # 若有方法名而无方法体则方法体为pass
    if func_settings == None or func_settings == {}:
      return codes + nop
    for func in func_settings:
      actions_codes = actions.get_action(func.get('action'))(name=self.__name, **func)
      # 当action为数组时，为数组的每个item添加分隔符，并展开为一个字符串
      # 当数组中存在一个多行字符串时，不进行格式化
      if isinstance(actions_codes, list):
        actions_codes = functools.reduce(
          lambda x, y: x + y,   # reduce把数组降级，将数组的每一个元素拼接在一起
          map(                  # map则将固定操作映射给数组中的每一个元素
            lambda code: '\t\t%s\n' % code if not len(code.splitlines()) > 1 else '%s\n' % code,
            actions_codes
          )
        )
        codes = codes + '%s\n' % actions_codes
      else:
      # 当action为一个字符串时，添加分隔符
        if not len(actions_codes.splitlines()) > 1:
          codes = codes + ('\t\t%s\n' % actions_codes)
        else:
          codes = codes + ('%s\n' % actions_codes)
    return codes.expandtabs(2)  # 将制表符展开为两个空格

  def parser(self, data):
    """生成代码"""
    from .output import code_template   # 导入代码模版
    with open(os.path.abspath(self.__filepath), 'w', encoding='utf-8') as codefile:
      if data.get('baseUrl'):   # 有浏览器驱动测试
        # 写入代码模版
        codefile.write(code_template % (self.__name, 'BrowserTestBase'))
        # 绑定浏览器驱动
        codefile.write(('\tdriver_kind = "%s"\n' % readconfig('webdriver', 'browser_kind')).expandtabs(2))
        # 绑定页面URL
        codefile.write(('\ttest_url = "%s"\n' % data.get('baseUrl')).expandtabs(2))
      else:                     # 无浏览器驱动测试
        # 写入代码模版
        codefile.write(code_template % (self.__name, 'TestBase'))
      # 创建测试夹具方法
      codefile.write(self.create_func('setUp', data.get('start')))
      codefile.write(self.create_func('tearDown', data.get('end')))
      # 创建测试方法
      for case in data.get('tests').keys():
        codefile.write(self.create_func(case, data.get('tests').get(case)))

  def run(self):
    """
    运行测试
    """
    # 获取生成代码的全局包路径
    package = os.path.splitext(os.path.abspath(self.__filepath))[0].replace(os.getcwd(), '').replace('\\', '.')[1:]
    # 引入创建后的测试Case代码
    testcase = __import__(package, globals(), locals(), fromlist=[self.__name])
    # unittest读取测试用例
    test = unittest.TestLoader().loadTestsFromTestCase(getattr(testcase, self.__name))
    testsuite = unittest.TestSuite((test, ))
    # 执行测试并返回结果
    result = unittest.TextTestRunner(verbosity=2).run(testsuite)
    # log输出
    log_result(self.__logger.get_logger(self.__name), result)
    # 关闭log
    self.__logger.close()
    # 如果配置文件中delete_after_run设置为true，则测试完成后删除生成的代码
    if readconfig('code_generate', 'delete_after_run').lower() == 'true':
      os.remove(self.__filepath)
    else:
      # 获得文件修改时间
      file_moddified_time = time.strftime('%Y%m%d', time.localtime(os.stat(self.__filepath).st_mtime))
      # 获得文件修改时间与现在时间的时间差
      timesub = datetime.datetime.now() - datetime.datetime.strptime(file_moddified_time, '%Y%m%d')
      # 如果时间差的日数大于等于文件的保留天数则删除文件
      if timesub.days >= int(readconfig('code_generate', 'hold_days')):
        os.remove(self.__filepath)
    return result
