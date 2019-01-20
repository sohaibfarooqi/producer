import csv

import celery
import pytest

from producer import Producer


def test_header_rows(file_with_header):
  """
  Test Producer class with header rows parameter values.
  """
  p = Producer()
  header = 1
  total_rows = sum(1 for row in csv.reader(file_with_header))
  file_with_header.seek(0)
  reader = p._skip_headers(file_with_header, header_rows=header)
  out_rows = sum(1 for row in reader)
  assert total_rows == (out_rows + header)

def test_column_map(file_with_header):
  """
  Test Producer class with custom column mappings of csv files.
  """
  p = Producer()
  reader = csv.reader(file_with_header)
  column_map = {'name': 1, 'email': 2}
  for line in reader:
    with pytest.raises(IndexError):
      p._parse_row(line, column_map=column_map)

def test_seperator(file_with_seperator):
  """
  Test Producer class with custom CSV seperator.
  """
  p = Producer()
  task_id = p.s(file_with_seperator, sep='|').apply_async()
  assert isinstance(task_id, celery.result.EagerResult)

def test_successful_execution(custom_file_format):
  """
  Test valid CSV file with all three parameters.
  """
  p = Producer()
  sep = '|'
  header = 1
  column_map = {'email': 0, 'name': 1}
  task_id = p.s(custom_file_format, header_rows=header, column_map=column_map, sep='|').apply_async()
  assert isinstance(task_id, celery.result.EagerResult)
