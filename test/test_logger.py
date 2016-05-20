import unittest
import kayvee as kv
import kayvee.logger as logger
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

  def test_logger_contruct(self):
    formatter = lambda data: ".".join(data.values())
    outputIO = StringIO.StringIO()
    logObj = logger.Logger("logger-constructor", logger.LOG_LEVELS["Info"], formatter, outputIO, dict(default_field="someval"))
    logObj.debug("testlogdebug")
    expected = ""
    self.assertEqual(outputIO.getvalue(), expected)

    logObj.info("testloginfo")
    expected = "logger-constructor.info.someval.testloginfo\n"
    self.assertEqual(outputIO.getvalue(), expected)
    outputIO.close()

  def test_validateLogLevel(self):
    # Explicit validation checks
    logObj = logger.Logger("logger-validateLogLevel")
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
    logObj = logger.Logger("logger-invalidLog")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logObj.setLogLevel("invalidlog_level")
    logObj.debug("debug-invalidlog")
    expected = "{\"source\": \"logger-invalidLog\", \"level\": \"" + logger.LOG_LEVELS["Debug"] + "\", \"title\": \"debug-invalidlog\"}"
    self.assertEqualJson(outputIO.getvalue(), expected)
    outputIO.close()

    # Recreate to clear
    outputIO = StringIO.StringIO("")
    logObj.setOutput(outputIO)
    logObj.setLogLevel("sometest")
    logObj.info("info-invalidlog")
    expected = "{\"source\": \"logger-invalidLog\", \"level\": \"" + logger.LOG_LEVELS["Info"] + "\", \"title\": \"info-invalidlog\"}"
    self.assertEqualJson(outputIO.getvalue(), expected)
    outputIO.close()

  def test_logFuncs(self):
    logObj = logger.Logger("logger-logFuncs")

    # LOG_LEVEL: (withoutData, withData)
    tests = {
        logger.LOG_LEVELS["Debug"]: (logObj.debug, logObj.debug),
        logger.LOG_LEVELS["Info"]: (logObj.info, logObj.info),
        logger.LOG_LEVELS["Warning"]: (logObj.warn, logObj.warn),
        logger.LOG_LEVELS["Error"]: (logObj.error, logObj.error),
        logger.LOG_LEVELS["Critical"]: (logObj.critical, logObj.critical)
    }

    for log_level in tests:
        outputIO = StringIO.StringIO()
        logObj.setOutput(outputIO)

        simpleLogFunc = tests[log_level][0]
        simpleLogFunc("testlog"+log_level)
        simpleExpected = "{\"source\": \"logger-logFuncs\", \"level\": \"" + log_level + "\", \"title\": \"testlog" + log_level + "\"}"
        self.assertEqualJson(outputIO.getvalue(), simpleExpected)

        outputIO.close()

        outputIO = StringIO.StringIO()
        logObj.setOutput(outputIO)

        addlDataLogFunc = tests[log_level][1]
        addlDataLogFunc("testlog"+log_level, {"key1":"val1","key2":"val2"})
        addlDataExpected = "{\"source\": \"logger-logFuncs\", \"level\": \"" + log_level + "\", \"title\": \"testlog" + log_level + "\",\"key1\": \"val1\", \"key2\": \"val2\"}"
        self.assertEqualJson(outputIO.getvalue(), addlDataExpected)

        outputIO.close()

  def test_counter(self):
    logObj = logger.Logger("logger-counter")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logObj.counter("testlogcounter")
    expected = "{\"source\": \"logger-counter\", \"level\": \"" + logger.LOG_LEVELS["Info"] + "\", \"title\": \"testlogcounter\", \"type\": \"counter\", \"value\": 1}"
    self.assertEqualJson(outputIO.getvalue(), expected)
    outputIO.close()

    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)
    logObj.counter("testlogcounter", 2, {"key1":"val1","key2":"val2"})
    expected = "{\"source\": \"logger-counter\", \"level\": \"" + logger.LOG_LEVELS["Info"] + "\", \"title\": \"testlogcounter\",\"type\": \"counter\", \"value\": 2,\"key1\": \"val1\", \"key2\": \"val2\"}"
    self.assertEqualJson(outputIO.getvalue(), expected)
    outputIO.close()

  def test_gauge(self):
    logObj = logger.Logger("logger-gauge")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logObj.gauge("testloggauge", 0)
    expected = "{\"source\": \"logger-gauge\", \"level\": \"" + logger.LOG_LEVELS["Info"] + "\", \"title\": \"testloggauge\", \"type\": \"gauge\", \"value\": 0}"
    self.assertEqualJson(outputIO.getvalue(), expected)
    outputIO.close()

    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)
    logObj.gauge("testloggauge", 4, {"key1":"val1","key2":"val2"})
    expected = "{\"source\": \"logger-gauge\", \"level\": \"" + logger.LOG_LEVELS["Info"] + "\", \"title\": \"testloggauge\", \"type\": \"gauge\", \"value\": 4, \"key1\": \"val1\", \"key2\": \"val2\"}"
    self.assertEqualJson(outputIO.getvalue(), expected)
    outputIO.close()

  def test_diffOutput(self):
    logObj = logger.Logger("logger-diffOutput")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    logObj.info("info-diffOutput")
    output1 = outputIO.getvalue()

    outputIO2 = StringIO.StringIO()
    logObj.setOutput(outputIO2)
    logObj.warn("warn-diffOutput")
    output2 = outputIO2.getvalue()

    self.assertEqualJson(output1, outputIO.getvalue())
    self.assertNotEqualJson(output2, outputIO.getvalue())
    outputIO.close()
    outputIO2.close()

  def test_hiddenLogWarning(self):
    logObj = logger.Logger("logger-hiddenLogWarning")
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
    logObj = logger.Logger("logger-hiddenLogCritical")
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
    logObj = logger.Logger("logger-diffFormat")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)
    logObj.setFormatter(lambda data: "\"This is a test\"")
    logObj.warn("testlogwarning")
    self.assertEqual(outputIO.getvalue(), "\"This is a test\"\n")
    outputIO.close()

  def test_multipleLoggers(self):
    logObj = logger.Logger("logger-multipleLoggers-1")
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)

    # Same buffer
    logObj2 = logger.Logger("logger-multipleLoggers-2")
    logObj2.setOutput(outputIO)
    logObj.warn("testlogwarning")
    output1 = outputIO.getvalue()
    logObj2.info("testloginfo")
    output2 = outputIO.getvalue()
    self.assertNotEqual(output1, output2)
    outputIO.close()

    # Recreate to clear
    outputIO = StringIO.StringIO()
    logObj.setOutput(outputIO)
    logObj.warn("testlogwarning")

    # Different buffer
    outputIO2 = StringIO.StringIO()
    logObj2.setOutput(outputIO2)
    logObj2.info("testloginfo")

    loggerExpected = "{\"source\": \"logger-multipleLoggers-1\", \"level\": \"" + logger.LOG_LEVELS["Warning"] + "\", \"title\": \"testlogwarning\"}"
    self.assertEqualJson(outputIO.getvalue(), loggerExpected)

    logger2Expected = "{\"source\": \"logger-multipleLoggers-2\", \"level\": \"" + logger.LOG_LEVELS["Info"] + "\", \"title\": \"testloginfo\"}"
    self.assertEqualJson(outputIO2.getvalue(), logger2Expected)
    outputIO.close()
    outputIO2.close()
