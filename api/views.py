# coding=utf-8

__author__ = 'JIANGH'

"""Create By Django-app"""

import sys, os, json
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def get_message(request):
  response = JsonResponse({ 'data': 1 }, safe=False)
  return response

def run_test(request):
  from api.autotest.testcodegen.auto_runner import TestRunner
  from api.autotest.common.config_reader import readconfig
  json_file = 'test_oa.json' # TODO
  with open(readconfig('case', 'case_folder') + json_file, encoding='utf-8') as f:
    setting = json.load(f)
    result = TestRunner(setting).run()
  response = JsonResponse(result)
  return response

def get_cases(request):
  pass

def get_modes(request):
  from .autotest.testcodegen.actions import ModeType
  return JsonResponse({ 'data': [str.lower(mode) for mode in dir(ModeType) if mode[0] != '_'] })

def get_actions(request):
  from .autotest.testcodegen.actions import get_actions_def
  # print(result)
  return JsonResponse({ 'data': get_actions_def() })

def save_config(request):
  print(request)
