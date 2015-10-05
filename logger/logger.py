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
  def __init__(self, source, log_level=None, formatter=kv.format, output=sys.stderr):
    if not log_level:
      log_level = os.environ.get('KAYVEE_LOG_LEVEL')
    self.log_level = self._validateLogLevel(log_level)
    self.globals = {}
    self.globals["source"] = source
    self.formatter = formatter
    self.output = output

  def setConfig(self, source, log_level, formatter, output):
    self.globals["source"] = source
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

  def debug(self, title):
    self.debugD(title, {})

  def info(self, title):
    self.infoD(title, {})

  def warn(self, title):
    self.warnD(title, {})

  def error(self, title):
    self.errorD(title, {})

  def critical(self, title):
    self.criticalD(title, {})

  def counter(self, title):
    self.counterD(title, 1, {})

  def gauge(self, title, value):
    self.gaugeD(title, value, {})

  def debugD(self, title, data):
    data["title"] = title
    self.logWithLevel(LOG_LEVELS["Debug"], data)

  def infoD(self, title, data):
    data["title"] = title
    self.logWithLevel(LOG_LEVELS["Info"], data)

  def warnD(self, title, data):
    data["title"] = title
    self.logWithLevel(LOG_LEVELS["Warning"], data)

  def errorD(self, title, data):
    data["title"] = title
    self.logWithLevel(LOG_LEVELS["Error"], data)

  def criticalD(self, title, data):
    data["title"] = title
    self.logWithLevel(LOG_LEVELS["Critical"], data)

  def counterD(self, title, value, data):
    data["title"] = title
    data["value"] = value
    data["type"] = "counter"
    self.logWithLevel(LOG_LEVELS["Info"], data)

  def gaugeD(self, title, value, data):
    data["title"] = title
    data["value"] = value
    data["type"] = "gauge"
    self.logWithLevel(LOG_LEVELS["Info"], data)

  def logWithLevel(self, log_level, data):
    if LOG_LEVEL_ENUM[log_level] < LOG_LEVEL_ENUM[self.log_level]:
      return
    data["level"] = log_level
    for key,value in self.globals.iteritems():
      if key in data:
        continue
      data[key] = value
    logString = self.formatter(data)
    print(logString, file=self.output)
