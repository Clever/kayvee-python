from __future__ import print_function
import os
import sys
import kayvee as kv

LOG_LEVELS = {
  "Debug":    "debug",
  "Info":     "info",
  "Warning":  "warning",
  "Error":    "error",
  "Critical": "critical",
}

LOG_LEVEL_ENUM = {
  "debug":    0,
  "info":     1,
  "warning":  2,
  "error":    3,
  "critical": 4,
}

# This is a port from kayvee-go/logger/logger.go
class Logger:
  def __init__(self, source, log_level=None, formatter=kv.format, output=sys.stderr, default_fields=None):
    if not log_level:
      log_level = os.environ.get('KAYVEE_LOG_LEVEL')
    self.log_level = self._validateLogLevel(log_level)
    self.default_fields = {}
    if default_fields is not None:
        for key, value in default_fields.iteritems():
            self.default_fields[key] = default_fields[key]
    self.default_fields["source"] = source
    self.formatter = formatter
    self.output = output

  def setConfig(self, source, log_level, formatter, output):
    self.default_fields["source"] = source
    self.log_level = self._validateLogLevel(log_level)
    self.formatter = formatter
    self.output = output

  def _validateLogLevel(self, log_level):
    if not log_level:
      return LOG_LEVELS["Debug"]
    else:
      for key, value in LOG_LEVELS.iteritems():
        if log_level.lower() == value:
          return value
    return LOG_LEVELS["Debug"]

  def setLogLevel(self, log_level):
    self.log_level = self._validateLogLevel(log_level)

  def setFormatter(self, formatter):
    self.formatter = formatter

  def setOutput(self, output):
    self.output = output

  def debug(self, title, data=None):
    data = data if data else {}
    data["title"] = title
    self.logWithLevel(LOG_LEVELS["Debug"], data)

  def info(self, title, data=None):
    data = data if data else {}
    data["title"] = title
    self.logWithLevel(LOG_LEVELS["Info"], data)

  def warn(self, title, data=None):
    data = data if data else {}
    data["title"] = title
    self.logWithLevel(LOG_LEVELS["Warning"], data)

  def error(self, title, data=None):
    data = data if data else {}
    data["title"] = title
    self.logWithLevel(LOG_LEVELS["Error"], data)

  def critical(self, title, data=None):
    data = data if data else {}
    data["title"] = title
    self.logWithLevel(LOG_LEVELS["Critical"], data)

  def counter(self, title, value=1, data=None):
    data = data if data else {}
    data["title"] = title
    data["value"] = value
    data["type"] = "counter"
    self.logWithLevel(LOG_LEVELS["Info"], data)

  def gauge(self, title, value, data=None):
    data = data if data else {}
    data["title"] = title
    data["value"] = value
    data["type"] = "gauge"
    self.logWithLevel(LOG_LEVELS["Info"], data)

  def logWithLevel(self, log_level, data):
    if LOG_LEVEL_ENUM[log_level] < LOG_LEVEL_ENUM[self.log_level]:
      return
    data["level"] = log_level
    for key,value in self.default_fields.iteritems():
      if key in data:
        continue
      data[key] = value
    logString = self.formatter(data)
    self.output.write(logString + "\n")
