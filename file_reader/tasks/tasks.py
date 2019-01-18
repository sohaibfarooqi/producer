import csv, time
from celery import group, signature, Celery, uuid
from celery.utils.log import get_task_logger
from .config import CeleryConfig

celery_app = Celery("file_reader")
celery_app.config_from_object(CeleryConfig)

logger = get_task_logger(__name__)

class Producer(celery_app.Task):
  """
  Producer class is responsible for reading input file and
  creating a `group` of tasks. Each group element represent
  a row plus some other identification data like timestamps
  and group_id. Each group element is sent to attached broker
  in a specified queue.
  """
  name = 'producer'

  def run(self, file, consumer='consumer', queue='test', header_rows=0, column_map={'name': 0, 'email': 1}, sep=','):
    """
    Main task body. It will create a group of task that will
    run in parallel. Each group element is a single file row.
    Malformed rows i.e. rows which doesn't comply with input
    schema are ignored.

    Params:
    -------
      - file(str): Name of input file.
      - consumer(str): Celery task that will consume the data.
      - queue(str): Name of destination queue.
      - header_rows(int): Number of rows of header of csv file.
      - column_map(dict): Indicate column labels.
      - sep(str): CSV seperator.

    Raises:
    ------
      - StopIteration: In case file is empty or header rows are less
      than specified in params
    """
    logger.info("Processing file: {}".format(file))

    self.group_id = uuid()
    data = open(file, 'r')
    reader = csv.reader(data, delimiter=sep)

    reader = self._skip_headers(reader, header_rows)

    base_obj = {
      "parent_task_id": self.group_id,
      "timestamp": time.time()
    }
    grouped_task = list()
    for index, row in enumerate(reader):
      try:
        obj = {
            **self._parse_row(row, column_map),
            **base_obj
        }
        grouped_task.append(signature(consumer, kwargs=obj, queue=queue))
      except IndexError:
        logger.error("Malformed row at index: {}".format(index))

    if grouped_task:
      workflow = group(grouped_task)
      return workflow.apply_async(task_id=self.group_id)

  def on_failure(self, exc, task_id, args, kwargs, einfo):
    """
    In celery task this function gets invoked when a task gets `failed`.
    For arguments we can identify the task and get retrieve any extra
    parameters passed to this function
    """
    logger.error("task: {} with group-id: {} failed. error trace: {}".format(self.group_id, task_id, exc))

  def on_success(self, retval, task_id, args, kwargs):
    """
    In celery task this function gets invoked when a task execute successfully.
    """
    logger.info("task: {} with group-id: {} is successful".format(self.group_id, task_id))

  def _skip_headers(self, reader, header_rows):
    [next(reader) for _ in range(header_rows)]
    return reader

  def _parse_row(self, row, column_map):
    return {k:row[val] for k, val in column_map.items()}

celery_app.tasks.register(Producer())

