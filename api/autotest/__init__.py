# coding=utf-8

from .common.config_reader import readconfig
import os
log_folder_path = os.path.abspath(readconfig('result', 'log_folder'))
picture_folder_path = os.path.abspath(readconfig('result', 'picture_folder'))

# 如果存放结果的文件夹不存在则新建
if not os.path.exists(os.path.dirname(log_folder_path)):
  os.mkdir(os.path.dirname(log_folder_path))
if not os.path.exists(log_folder_path):
  os.mkdir(log_folder_path)
if not os.path.exists(picture_folder_path):
  os.mkdir(picture_folder_path)
