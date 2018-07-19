# coding=utf-8

__author__ = 'JIANGH'

__all__ = [
  'judge', 'event', 'find', 'excel', 'database',
  'ModeType', 'Args',
  'get_action', 'get_actions_def'
]

class ModeType():
  """选择器模式枚举"""
  ID = 'id'
  CLASS = 'class'
  CSS_SELECTOR = 'css'
  XPATH = 'xpath'
  NAME = 'name'
  INNER_TEXT = 'text'
  PARTIAL_TEXT = 'partial_text'

class Args(object):
  """装饰器\n
  标记函数需要哪些参数（拓展用：执行前检查参数名和数目正不正确等）\n
  For example:\n
  @arg({
    'arg': {require type of this arg},
    'mode': None #None for default (or select type)
    'index': 'number' #for create a vaildator
  })
  """
  def __init__(self, args):
    self.__args = args

  def __call__(self, func):
    return self.decorator(func)

  def decorator(self, func):
    import functools
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      return func(*args, **kwargs)
    wrapper.args = self.__args
    return wrapper

def get_action(action_name):
  """
  根据action_name字符串取得对应方法，取不到时抛出异常
  """
  from . import event, find, judge, excel, database
  package_group = [event, find, judge, excel, database]
  for action_package in package_group:
    if getattr(action_package, action_name, None):
      return getattr(action_package, action_name, None)
  raise Exception('Could not find the action of %s' % action_name)

def get_actions_def():
  """
  取得所有action的签名定义，dict形式\n
  key为action_name\n
  value为参数及类型\n
  """
  def is_action(module, action_name):
    '''判断一个名称是否是模块中的action'''
    if len(action_name) < 1: return False
    return action_name[0] != '_' and isinstance(getattr(module, action_name, None), types.FunctionType)

  import types
  from . import event, find, judge, excel, database
  package_group = [event, find, judge, excel, database]
  all_actions = {}
  for module in package_group:
    all_actions = {**all_actions, **{fn: getattr(getattr(module, fn), 'args', None) for fn in dir(module) if is_action(module, fn)}}
  return all_actions
