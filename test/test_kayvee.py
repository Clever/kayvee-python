import unittest
import kayvee as kv
import json
import os
from testfixtures import LogCapture
import logging
logger = logging.getLogger("kayvee-test")


class TestKayvee(unittest.TestCase):

  def setup(self):
    pass

  def tearDown(self):
    pass

  def assertEqualJson(self, a, b):
    """ Given two strings, assert they are the same json dict """
    actual = json.loads(a)
    expected = json.loads(b)
    self.assertEquals(actual, expected)

  def test_format(self):
    logger.info("allows empty data")
    data = {}
    actual = kv.format(data)
    expected = '{}'
    self.assertEqual(actual, expected)
    self.assertEqualJson(actual, expected)

    logger.info("stringifies simple dict")
    data = {"a":"b"}
    actual = kv.format(data)
    expected = '{"a":"b"}'
    self.assertEqual(actual, expected)
    self.assertEqualJson(actual, expected)

    logger.info("stringifies arbitrary dict")
    data = {"foo":"bar","hello":{"a":"b"}}
    actual = kv.format(data)
    expected = '{"foo":"bar","hello":{"a":"b"}}'
    self.assertEqual(actual, expected)
    self.assertEqualJson(actual, expected)

  def test_basic_logging(self):
    specs = [
        ("hello", {}),
        ("hello", {"foo":"bar"}),
    ]
    methods = [
      (kv.trace, kv.TRACE, "DEBUG"),
      (kv.info, kv.INFO, "INFO"),
      (kv.warning, kv.WARNING, "WARNING"),
      (kv.warn, kv.WARNING, "WARNING"), # alias for warning
      (kv.error, kv.ERROR, "ERROR"),
      (kv.critical, kv.CRITICAL, "CRITICAL"),
    ]
    for spec in specs:
      for method in methods:
        with LogCapture() as l:
          # determine fn to test and expected output
          fn, expected_kv_level, expected_logging_level = method[0], method[1], method[2]
          msg, data = spec[0], spec[1]

          # call log method
          fn(msg, data)

          # get a dict describing last outputted log
          record = l.records[-1].__dict__
          logger_name = record['name']
          output = record['msg']
          levelname = record['levelname']

          self.assertEqual(logger_name, 'kayvee')
          self.assertEqual(levelname, expected_logging_level)
          self.assertIn(expected_kv_level, output) # verify kv level is in output
          self.assertIn(msg, output) # verify msg is in output
          for k, v in data.iteritems():
            # verify keys and values are in output
            self.assertIn(k, output)
            self.assertIn(v, output)

  def test_metric_logging(self):
    specs = [{
      # counter with default value (1)
      'method' : kv.counter,
      'args': ('my-title',),
      'expected_data' : {'type':'counter', 'title':'my-title', 'value': 1}
    },{
      # counter with non-default value
      'method' : kv.counter,
      'args': ('my-title',5),
      'expected_data' : {'type':'counter', 'title':'my-title', 'value': 5}
    },{
      'method' : kv.gauge,
      'args': ('my-title', 1),
      'expected_data' : {'type':'gauge', 'title':'my-title', 'value': 1}
    }]
    for spec in specs:
      with LogCapture() as l:
        spec['method'](*spec['args'])

        # get data describing last outputted log
        record = l.records[-1].__dict__
        logger_name = record['name']
        output = record['msg']
        levelname = record['levelname']

        for k, v in spec['expected_data'].iteritems():
          self.assertIn(k, output)
          self.assertIn(str(v), output)
