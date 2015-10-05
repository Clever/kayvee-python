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

  def test_validateLogLevel(self):
    # Explicit validation checks
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    # Test case-insensitive in log level name
    log_level = logObj._validateLogLevel("debug")
    self.assertEqual(log_level, logger.LOG_LEVELS["Debug"])
    log_level = logObj._validateLogLevel("Debug")
    self.assertEqual(log_level, logger.LOG_LEVELS["Debug"])

    # Test non-default log levels
    log_level = logObj._validateLogLevel("info")
    self.assertEqual(log_level, logger.LOG_LEVELS["Info"])
    log_level = logObj._validateLogLevel("critical")
    self.assertEqual(log_level, logger.LOG_LEVELS["Critical"])
    # TODO: add for each possible level

    # Test sets level to debug if given invalid log level
    log_level = logObj._validateLogLevel("sometest")
    self.assertEqual(log_level, logger.LOG_LEVELS["Debug"])
    outputIO.close()

  def test_invalidLog(self):
    # Invalid log levels will default to debug
    logObj = logger.Logger("logger-tester")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logObj.setLogLevel("invalidlog_level")
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

  def test_logFuncs(self):
    logObj = logger.Logger("logger-tester")

    # LOG_LEVEL: (simpleLogFunc, addlDataLogFunc)
    tests = {
        logger.LOG_LEVELS["Debug"]: (logObj.debug, logObj.debugD),
        logger.LOG_LEVELS["Info"]: (logObj.info, logObj.infoD),
        logger.LOG_LEVELS["Warning"]: (logObj.warn, logObj.warnD),
        logger.LOG_LEVELS["Error"]: (logObj.error, logObj.errorD),
        logger.LOG_LEVELS["Critical"]: (logObj.critical, logObj.criticalD)
    }

    for log_level in tests:
        outputIO = StringIO.StringIO()
        logObj.setOutput(outputIO)

        simpleLogFunc = tests[log_level][0]
        simpleLogFunc("testlog"+log_level)
        simpleExpected = "{\"source\": \"logger-tester\", \"level\": \"" + log_level + "\", \"title\": \"testlog" + log_level + "\"}"
        self.assertEqualJson(outputIO.getvalue(), simpleExpected)

        outputIO = StringIO.StringIO()
        logObj.setOutput(outputIO)

        addlDataLogFunc = tests[log_level][1]
        addlDataLogFunc("testlog"+log_level, {"key1":"val1","key2":"val2"})
        addlDataExpected = "{\"source\": \"logger-tester\", \"level\": \"" + log_level + "\", \"title\": \"testlog" + log_level + "\",\"key1\": \"val1\", \"key2\": \"val2\"}"
        self.assertEqualJson(outputIO.getvalue(), addlDataExpected)

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
