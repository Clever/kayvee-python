import json
import logging
import os

# Logger
logger = logging.getLogger('kayvee')
logger.setLevel(os.environ.get('KAYVEE_LOG_LEVEL', logging.DEBUG)) # default to show all logs
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

def set_level(level):
  """ Set logging level. Only logs >= this level will be outputted.

  :param level - log level
  """
  logger.setLevel(level)
setLevel = set_level # alias to match logging.Logger interface


# Kayvee-specific (cross-language) log levels
UNKNOWN = "unknown"
CRITICAL = "critical"
ERROR = "error"
WARNING = "warning"
INFO = "info"
TRACE = "trace"

# Kayvee-specific metric types
COUNTER = 'counter'
GAUGE = 'gauge'

# Allow including default key-val pairs
default_values = {}
def set_default_value(key, val):
  """ Sets a default key-val. This key=val will be included it all logs.
  This may be overriden by the specific log's data. """
  default_values
  default_values[key] = val

def unset_default_value(k):
  """ Unsets a default key-val. """
  default_values
  if default_values.get(k):
    del default_values[k]

# Formatters
def format(data):
  """ Converts a dict to stringified json """
  for k, v in default_values.iteritems():
    # user's logged data may override default_values
    data[k] = data.get(k, v)

  return json.dumps(data, separators=(',', ':'))

# Log at specific log levels
def trace(msg, data={}):
  data['msg'] = msg
  data['level'] = TRACE
  logger.debug(format(data))

def info(msg, data={}):
  data['msg'] = msg
  data['level'] = INFO
  logger.info(format(data))

def warning(msg, data={}):
  data['msg'] = msg
  data['level'] = WARNING
  logger.warning(format(data))
warn = warning # alias to match logging.Logger interface

def error(msg, data={}):
  data['msg'] = msg
  data['level'] = ERROR
  logger.error(format(data))

def critical(msg, data={}):
  data['msg'] = msg
  data['level'] = CRITICAL
  logger.critical(format(data))

# Log metrics
def counter(title, value = 1, data = {}):
  data['source'] = data.get('source', 'unknown')
  data['title'] = title
  data['value'] = value
  data['level'] = INFO
  data['type'] = COUNTER
  logger.info(format(data))

def gauge(title, value, data = {}):
  data['title'] = title
  data['value'] = value
  data['level'] = INFO
  data['type'] = GAUGE
  logger.info(format(data))
