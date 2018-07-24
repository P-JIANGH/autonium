# coding=utf-8

__author__ = 'JIANGH'

__all__ = ['config_reader', 'log']

import tablib as tl
import json

# 几种数据类型转换的共通方法
def format_to_df(data, columns=None):
  """将数据转换为Dataset类型"""
  return tl.Dataset(*data, headers=columns)

def format_to_dict(data, columns=None):
  """将数据转换为键值对"""
  return json.loads(format_to_df(data, columns).json)

def format_to_json_unicode(data, columns=None):
  """将数据转换为json，中文字符为unicode"""
  return format_to_df(data, columns).json

def format_to_json(data, columns=None):
  """将数据转换为json"""
  return format_to_json_unicode(data, columns).encode().decode('unicode-escape')
