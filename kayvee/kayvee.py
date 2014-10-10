import json

def format(data):
  """ Converts a dict to a string of space-delimited key=val pairs """
  val_formatter = lambda v: json.dumps(v, separators=(',', ':'))
  pairs = map(lambda key: "{key}={val}".format(key=key, val=val_formatter(data[key])), data.keys())
  return " ".join(sorted(pairs))

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

  reserved = "{} {} {}".format(
    format({"source": source}),
    format({"level": level}),
    format({"title": title})
  )
  if type(data) is dict and len(data.keys()) > 0:
    return "{} {}".format(reserved, format(data))
  else:
    return reserved

# Log Levels
UNKNOWN = "unknown"
CRITICAL = "critical"
ERROR = "error"
WARNING = "warning"
INFO = "info"
TRACE = "trace"
