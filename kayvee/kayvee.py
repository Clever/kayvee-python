import json

def format(data):
  """ Converts a dict to a string of space-delimited key=val pairs """
  return json.dumps(data, separators=(',', ':'))

def formatLog(source="", level="", title="", data={}):
  """ Similar to format, but takes additional reserved params to promote logging best-practices

  :param level - severity of message - how bad is it?
  :param source - application context - where did it come from?
  :param title - brief description - what kind of event happened?
  :param data - additional information - what details help to investigate?
  """
  # consistently output empty string for unset params, because null values differ by language
  source = "" if source is None else source
  level = "" if level is None else level
  title = "" if title is None else title
  
  if not type(data) is dict:
    data = {}
  data['source'] = source
  data['level'] = level
  data['title'] = title

  return format(data)

# Log Levels
UNKNOWN = "unknown"
CRITICAL = "critical"
ERROR = "error"
WARNING = "warning"
INFO = "info"
TRACE = "trace"
