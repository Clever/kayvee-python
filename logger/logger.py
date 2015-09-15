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

# This is a port from kayvee-go/c-log/clog.go
class Logger:
  def __init__(self, source, logLvl=None, formatter=kv.format, output=sys.stderr):
    if not logLvl:
      logLvl = os.environ.get('KAYVEE_LOG_LEVEL')
    self.logLvl = self._validateLogLvl(logLvl)
    self.globals = {}
    self.globals["source"] = source
    self.formatter = formatter
    self.output = output

  def setConfig(self, source, logLvl, formatter, output):
    self.globals["source"] = source
    self.logLvl = self._validateLogLvl(logLvl)
    self.formatter = formatter
    self.output = output

  def _validateLogLvl(self, logLvl):
    if not logLvl:
      return LOG_LEVELS["Debug"]
    else:
      for key, value in LOG_LEVELS.iteritems():
        if logLvl.lower() == value:
          return value
    return LOG_LEVELS["Debug"]

  def setLogLevel(self, logLvl):
    self.logLvl = self._validateLogLvl(logLvl)

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

  def logWithLevel(self, logLvl, data):
    if LOG_LEVEL_ENUM[logLvl] < LOG_LEVEL_ENUM[self.logLvl]:
      return
    data["level"] = logLvl
    for key,value in self.globals.iteritems():
      if key in data:
        continue
      data[key] = value
    logString = self.formatter(data)
    print(logString, file=self.output)
