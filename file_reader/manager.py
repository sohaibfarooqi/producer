import csv
from celery import chain

class TaskManager:
  """
  TaskManager class is a convenient interface to
  schedule celery task. It facilitate with specifying
  meta data about the input file, performing sanity check
  and executing celery task which process the input file.
  """
  def __init__(self, header_rows=1,
    column_map={'name': 0, 'email': 1}, sep=','):
    """
    Class constructor.

    Params:
    -------
      - header_rows(int): Number of rows of header of csv file.
      - column_map(dict): Indicate column labels.
      - sep(str): Csv seperator.
    """
    self.header_rows = header_rows
    self.column_map = column_map
    self.sep = sep

  def execute(self, file):
    """
    Main method to initiate file processing. This
    method first check if file is empty. If it is not
    it will submit the file to celery task processing
    flow.

    Params:
    ------
      - file(str): Name of input file

    Returns:
    --------
      - task_id(str): Task id of celery task.

    Raises:
    -------
      - RuntimeError: If file is empty.
    """
    if self._is_file_empty(file) is True:
      raise RuntimeError("Received Empty File")

    task_id = uuid()
    task = submit_file(file, task_id, self.header_rows, self.column_map, self.sep)
    task.apply_async(task_id=chain_id)
    return task_id

  def _is_file_empty(self, file):
    """
    This method checks whether file is empty of not.

    Params:
    -------
      - file(str): Name of input file.

    Returns:
    -------
      - is_empty(bool): Indicate whether file is empty of not
    """
    is_empty = False
    try:
      next(csv.reader(open(file, 'r'), sep=self.sep))
    except StopIteration:
      is_empty = True
    return is_empty
