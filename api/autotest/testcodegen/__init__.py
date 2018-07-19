# coding=utf-8

__author__ = 'JIANGH'


from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
import unittest

from ..common.config_reader import readconfig
DRIVER_PATH = readconfig('webdriver', 'driver')
save_screenshot_path = readconfig('result', 'picture_folder')
time_format = '%Y%m%d%H%M%S'

class TestBase(unittest.TestCase):
  pass

class BrowserTestBase(TestBase):

  """
  生成的测试用例的基类

  在代码模板中标明继承关系
  """

  driver_kind = ''

  test_url = ''

  @classmethod
  def setUpClass(cls):
    """
    类测试夹具

    为所有测试方法的执行做准备

    测试开始的第一步执行
    """
    log_path = readconfig("result", "log_folder")

    if cls.driver_kind == 'ie':
      cls.driver = webdriver.Ie(executable_path=DRIVER_PATH)
    elif cls.driver_kind == 'firefox':
      cls.driver = webdriver.Firefox(executable_path=DRIVER_PATH, log_path=log_path + 'geckodriver.log')
    elif cls.driver_kind == 'chrome':
      cls.driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    else:
      raise WebDriverException(msg="Unkwon Browser")
    cls.driver.implicitly_wait(5)
    cls.driver.maximize_window()
    cls.driver.get(cls.test_url)

  @classmethod
  def tearDownClass(cls):
    """
    测试夹具

    为所有测试方法的结束做清理
    
    测试开始的最后一步执行
    """
    cls.driver.quit()

def log_codes_creator(logger, codes):
  logger.debug('\n' + codes)

def log_debug(logger, content):
  logger.debug(content)

def log_result(logger, result):
  logger.debug('测试结果： %s' % result)
  logger.info('共测试%d个Case，其中%d个成功，%d个失败，%d个错误'% (
    result.testsRun,
    result.testsRun - len(result.failures) - len(result.errors),
    len(result.failures),
    len(result.errors)
  ))
  if len(result.failures) > 0:
    logger.warning("失败原因如下：")
    for failure in result.failures:
      logger.warning(failure)
  if len(result.errors) > 0:
    logger.error("错误信息如下：")
    for error in result.errors:
      for error_detail in error:
        logger.error(error_detail)
