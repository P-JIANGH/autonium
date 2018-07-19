# coding=utf-8

"""配置文件读取器"""

__author__ = 'JIANGH'

from configparser import ConfigParser
import os

# 获取工作路径
BASE_DIR = os.getcwd()
cf = ConfigParser()
# 读取配置文件（每次引入包的时候都会重新读取）
cf.read(os.path.join(BASE_DIR, 'config', 'autotest.conf'))

def readconfig(section, option):
  """
  获取特定配置数据

  readconfig('section', 'option')
  """
  return cf.get(section, option)
