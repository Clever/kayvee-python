import unittest
import kayvee as kv
import logger
import json
import os
import StringIO

class TestLogger(unittest.TestCase):

  def assertEqualJson(self, a, b):
    """ Given two strings, assert they are the same json dict """
    actual = json.loads(a)
    expected = json.loads(b)
    self.assertEqual(actual, expected)

  def assertNotEqualJson(self, a, b):
    """ Given two strings, assert they are the same json dict """
    actual = json.loads(a)
    expected = json.loads(b)
    self.assertNotEqual(actual, expected)

  def test_constructor(self):
    formatter = lambda data: data["level"] + "." + data["source"] + "." + data["title"]
    outputIO = StringIO.StringIO()
    logObj = logger.Logger("logger-test", logger.LOG_LEVELS["Info"], formatter, outputIO)
    logObj.debug("testlogdebug")
    expected = ""
    self.assertEqual(outputIO.getvalue(), expected)

    logObj.info("testloginfo")
    expected = logger.LOG_LEVELS["Info"] + ".logger-test.testloginfo\n"
    self.assertEqual(outputIO.getvalue(), expected)
    outputIO.close()

  def test_validateLog(self):
    # Explicit validation checks
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logLvl = logObj._validateLogLvl("debug")
    self.assertEqual(logLvl, logger.LOG_LEVELS["Debug"])

    logLvl = logObj._validateLogLvl("Debug")
    self.assertEqual(logLvl, logger.LOG_LEVELS["Debug"])

    logLvl = logObj._validateLogLvl("info")
    self.assertEqual(logLvl, logger.LOG_LEVELS["Info"])
    logLvl = logObj._validateLogLvl("Info")
    self.assertEqual(logLvl, logger.LOG_LEVELS["Info"])

    logLvl = logObj._validateLogLvl("sometest")
    self.assertEqual(logLvl, logger.LOG_LEVELS["Debug"])
    outputIO.close()

  def test_invalidLog(self):
    # Invalid log levels will default to debug
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logObj.setLogLevel("debu")
    logObj.debug("testlogdebug")
    expected = "{\"source\": \"logger-tester\", \"level\": \"" + logger.LOG_LEVELS["Debug"] + "\", \"title\": \"testlogdebug\"}"
    self.assertEqualJson(outputIO.getvalue(), expected)

    # Recreate to clear
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)
    logObj.setLogLevel("sometest")
    logObj.info("testloginfo")
    expected = "{\"source\": \"logger-tester\", \"level\": \"" + logger.LOG_LEVELS["Info"] + "\", \"title\": \"testloginfo\"}"
    self.assertEqualJson(outputIO.getvalue(), expected)
    outputIO.close()

  def test_debug(self):
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logObj.debug("testlogdebug")
    expected = "{\"source\": \"logger-tester\", \"level\": \"" + logger.LOG_LEVELS["Debug"] + "\", \"title\": \"testlogdebug\"}"
    self.assertEqualJson(outputIO.getvalue(), expected)
    outputIO.close()
  def test_debugD(self):
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logObj.debugD("testlogdebug", {"key1":"val1","key2":"val2"})
    expected = "{\"source\": \"logger-tester\", \"level\": \"" + logger.LOG_LEVELS["Debug"] + "\", \"title\": \"testlogdebug\",\"key1\": \"val1\", \"key2\": \"val2\"}"
    self.assertEqualJson(outputIO.getvalue(), expected)
    outputIO.close()

  def test_info(self):
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logObj.info("testloginfo")
    expected = "{\"source\": \"logger-tester\", \"level\": \"" + logger.LOG_LEVELS["Info"] + "\", \"title\": \"testloginfo\"}"
    self.assertEqualJson(outputIO.getvalue(), expected)
    outputIO.close()
  def test_infoD(self):
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logObj.infoD("testloginfo", {"key1":"val1","key2":"val2"})
    expected = "{\"source\": \"logger-tester\", \"level\": \"" + logger.LOG_LEVELS["Info"] + "\", \"title\": \"testloginfo\",\"key1\": \"val1\", \"key2\": \"val2\"}"
    self.assertEqualJson(outputIO.getvalue(), expected)
    outputIO.close()

  def test_warn(self):
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logObj.warn("testlogwarning")
    expected = "{\"source\": \"logger-tester\", \"level\": \"" + logger.LOG_LEVELS["Warning"] + "\", \"title\": \"testlogwarning\"}"
    self.assertEqualJson(outputIO.getvalue(), expected)
    outputIO.close()
  def test_warnD(self):
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logObj.warnD("testlogwarning", {"key1":"val1","key2":"val2"})
    expected = "{\"source\": \"logger-tester\", \"level\": \"" + logger.LOG_LEVELS["Warning"] + "\", \"title\": \"testlogwarning\",\"key1\": \"val1\", \"key2\": \"val2\"}"
    self.assertEqualJson(outputIO.getvalue(), expected)
    outputIO.close()

  def test_error(self):
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logObj.error("testlogerror")
    expected = "{\"source\": \"logger-tester\", \"level\": \"" + logger.LOG_LEVELS["Error"] + "\", \"title\": \"testlogerror\"}"
    self.assertEqualJson(outputIO.getvalue(), expected)
    outputIO.close()
  def test_errorD(self):
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logObj.errorD("testlogerror", {"key1":"val1","key2":"val2"})
    expected = "{\"source\": \"logger-tester\", \"level\": \"" + logger.LOG_LEVELS["Error"] + "\", \"title\": \"testlogerror\",\"key1\": \"val1\", \"key2\": \"val2\"}"
    self.assertEqualJson(outputIO.getvalue(), expected)
    outputIO.close()

  def test_critical(self):
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logObj.critical("testlogcritical")
    expected = "{\"source\": \"logger-tester\", \"level\": \"" + logger.LOG_LEVELS["Critical"] + "\", \"title\": \"testlogcritical\"}"
    self.assertEqualJson(outputIO.getvalue(), expected)
    outputIO.close()
  def test_criticalD(self):
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logObj.criticalD("testlogcritical", {"key1":"val1","key2":"val2"})
    expected = "{\"source\": \"logger-tester\", \"level\": \"" + logger.LOG_LEVELS["Critical"] + "\", \"title\": \"testlogcritical\",\"key1\": \"val1\", \"key2\": \"val2\"}"
    self.assertEqualJson(outputIO.getvalue(), expected)
    outputIO.close()

  def test_counter(self):
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logObj.counter("testlogcounter")
    expected = "{\"source\": \"logger-tester\", \"level\": \"" + logger.LOG_LEVELS["Info"] + "\", \"title\": \"testlogcounter\", \"type\": \"counter\", \"value\": 1}"
    self.assertEqualJson(outputIO.getvalue(), expected)
    outputIO.close()
  def test_counterD(self):
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logObj.counterD("testlogcounter", 2, {"key1":"val1","key2":"val2"})
    expected = "{\"source\": \"logger-tester\", \"level\": \"" + logger.LOG_LEVELS["Info"] + "\", \"title\": \"testlogcounter\",\"type\": \"counter\", \"value\": 2,\"key1\": \"val1\", \"key2\": \"val2\"}"
    self.assertEqualJson(outputIO.getvalue(), expected)
    outputIO.close()

  def test_gauge(self):
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logObj.gauge("testloggauge", 0)
    expected = "{\"source\": \"logger-tester\", \"level\": \"" + logger.LOG_LEVELS["Info"] + "\", \"title\": \"testloggauge\", \"type\": \"gauge\", \"value\": 0}"
    self.assertEqualJson(outputIO.getvalue(), expected)
    outputIO.close()
  def test_gaugeD(self):
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logObj.gaugeD("testloggauge", 4, {"key1":"val1","key2":"val2"})
    expected = "{\"source\": \"logger-tester\", \"level\": \"" + logger.LOG_LEVELS["Info"] + "\", \"title\": \"testloggauge\", \"type\": \"gauge\", \"value\": 4, \"key1\": \"val1\", \"key2\": \"val2\"}"
    self.assertEqualJson(outputIO.getvalue(), expected)
    outputIO.close()

  def test_diffOutput(self):
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logObj.info("testloginfo")
    output1 = outputIO.getvalue()

    outputIO2 = StringIO.StringIO()
    logObj.setOutput(outputIO2)
    logObj.warn("testlogwarning")
    output2 = outputIO2.getvalue()

    self.assertEqualJson(output1, outputIO.getvalue())
    self.assertNotEqualJson(output2, outputIO.getvalue())
    outputIO.close()

  def test_hiddenLogWarning(self):
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)
    logObj.setLogLevel(logger.LOG_LEVELS["Warning"])

    logObj.debug("testlogdebug")
    self.assertEqual(outputIO.getvalue(), "")

    logObj.info("testloginfo")
    self.assertEqual(outputIO.getvalue(), "")

    logObj.warn("testlogwarning")
    self.assertNotEqual(outputIO.getvalue(), "")

    logObj.error("testlogerror")
    self.assertNotEqual(outputIO.getvalue(), "")

    logObj.critical("testlogcritical")
    self.assertNotEqual(outputIO.getvalue(), "")
    outputIO.close()

  def test_hiddenLogCritical(self):
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)
    logObj.setLogLevel(logger.LOG_LEVELS["Critical"])

    logObj.debug("testlogdebug")
    self.assertEqual(outputIO.getvalue(), "")

    logObj.info("testloginfo")
    self.assertEqual(outputIO.getvalue(), "")

    logObj.warn("testlogwarning")
    self.assertEqual(outputIO.getvalue(), "")

    logObj.error("testlogerror")
    self.assertEqual(outputIO.getvalue(), "")

    logObj.critical("testlogcritical")
    self.assertNotEqual(outputIO.getvalue(), "")
    outputIO.close()

  def test_diffFormat(self):
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)
    logObj.setFormatter(lambda data: "\"This is a test\"")
    logObj.warn("testlogwarning")
    self.assertEqual(outputIO.getvalue(), "\"This is a test\"\n")
    outputIO.close()

  def test_multipleLoggers(self):
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    # Same buffer
    logObj2 = logger.Logger("logger-tester2")
    logObj2.setOutput(outputIO)
    logObj.warn("testlogwarning")
    output1 = outputIO.getvalue()
    logObj2.info("testloginfo")
    output2 = outputIO.getvalue()
    self.assertNotEqual(output1, output2)

    # Recreate to clear
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    # Different buffer
    outputIO2 = StringIO.StringIO()
    logObj2.setOutput(outputIO2)
    logObj.warn("testlogwarning")
    logObj2.info("testloginfo")

    loggerExpected = "{\"source\": \"logger-tester\", \"level\": \"" + logger.LOG_LEVELS["Warning"] + "\", \"title\": \"testlogwarning\"}"
    self.assertEqualJson(outputIO.getvalue(), loggerExpected)

    logger2Expected = "{\"source\": \"logger-tester2\", \"level\": \"" + logger.LOG_LEVELS["Info"] + "\", \"title\": \"testloginfo\"}"
    self.assertEqualJson(outputIO2.getvalue(), logger2Expected)
    outputIO.close()
    outputIO2.close()
