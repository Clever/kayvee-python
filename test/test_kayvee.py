import unittest
import kayvee as kv
import json
import os

cur_dir = os.path.dirname(__file__)
f = open(os.path.join(cur_dir, "tests.json"))
tests = json.load(f)

class TestKayvee(unittest.TestCase):

  def test_format(self):
    for test in tests['format']:
      print "TEST: {}".format(test['title'])
      actual = kv.format(test['input']['data'])
      expected = test['output']
      self.assertEquals(actual, expected)

  def test_formatLog(self):
    for test in tests['formatLog']:
      print "TEST: {}".format(test['title'])
      actual = kv.formatLog(
        test['input'].get('source', None),
        test['input'].get('level', None),
        test['input'].get('title', None),
        test['input'].get('data', None)
      )
      expected = test['output']
      self.assertEquals(actual, expected)
