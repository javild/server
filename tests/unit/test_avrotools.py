"""
Tests the avrotools module
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

import ga4gh.avrotools as avrotools
import ga4gh.protocol as protocol


class TestSchemaTool(unittest.TestCase):
    """
    Tests the SchemaTool
    """
    def testNonProtocolElement(self):
        # Throws an exception when class_ is not a subclass of ProtocolElement
        with self.assertRaises(avrotools.SchemaToolException):
            avrotools.SchemaTool(object).getInvalidFields({})

    def testLessFields(self):
        # Throws an exception when there are fields missing from the jsonDict
        for class_ in protocol.getProtocolClasses():
            tool = avrotools.SchemaTool(class_)
            with self.assertRaises(avrotools.SchemaToolException):
                tool.getInvalidFields({})

    def testMoreFields(self):
        # Throws an exception when there are extra fields in the jsonDict
        for class_ in protocol.getProtocolClasses():
            jsonDict = class_().toJsonDict()
            jsonDict['extra'] = 'extra'
            tool = avrotools.SchemaTool(class_)
            with self.assertRaises(avrotools.SchemaToolException):
                tool.getInvalidFields(jsonDict)

    @unittest.skipIf(protocol.version.startswith("0.6"), "")
    def testGeneratedObjects(self):
        # Test that generated objects pass validation
        for class_ in protocol.getProtocolClasses():
            tool = avrotools.SchemaTool(class_)
            generatedInstance = tool.getTypicalInstance()
            jsonDict = generatedInstance.toJsonDict()
            returnValue = tool.getInvalidFields(jsonDict)
            self.assertEqual(returnValue, {})
