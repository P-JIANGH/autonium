from django.db import models

# Create your models here.
class Case(models.Model):
  case_name = models.CharField(primary_key=True, max_length=50)
  base_url = models.CharField(max_length=200)
  start_action_id = models.CharField(max_length=50)
  end_action_id = models.CharField(max_length=50)
  test_id = models.CharField(max_length=50)
  test_name = models.CharField(max_length=50)

class Test(models.Model):
  test_id = models.CharField(primary_key=True, max_length=50)
  action_id = models.CharField(max_length=50)

class Action(models.Model):
  action_id = models.CharField(primary_key=True, max_length=50)
  action = models.CharField(max_length=20)
  mode = models.CharField(max_length=20)
  target = models.CharField(max_length=200)
  value = models.CharField(max_length=100)
