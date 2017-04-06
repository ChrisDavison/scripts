import unittest
from utility import *

class TestUtility(unittest.TestCase):
    @unittest.skip("Not implemented.")
    def testChooseValidIndexFromList(self):
        pass

    @unittest.skip("Not implemented.")
    def testChooseInvalidIndexFromList(self):
        pass

    @unittest.skip("Not implemented.")
    def testChooseFromEmptyList(self):
        pass

    @unittest.skip("Not implemented.")
    def testChooseFiltered(self):
        pass

    @unittest.skip("Not implemented.")
    def testInsertionIntoTimeseries(self):
        pass

    @unittest.skip("Not implemented.")
    def testConversionOfADCValues(self):
        pass

    @unittest.skip("Not implemented.")
    def testMeanDurationOfTimestamps(self):
        """Determine the average difference between timestamps."""
        pass

    @unittest.skip("Not implemented.")
    def testMostPrevalentValueInList(self):
        """Can find the most prevalent value in a list."""
        self.assertEqual(False, True)

    @unittest.skip("Not implemented.")
    def testMostPrevalentValueInListWithMulitplePrevalent(self):
        """Return the 'lesser' value if multiple values are 'most prevalent'"""
        self.assertEqual(False, True)

    def testParsingADCValues(self):
        """Convert a raw ADC value for a given sensitivity and precision."""
        precision = 8 # 8 bit sensor
        sensitivity = 1 / 2 # +- 1g
        self.assertEqual(1.0, from_adc(256, precision, sensitivity))

    def testParsingADCValuesNoPrecision(self):
        """Cannot convert ADC value without a precision."""
        self.assertRaises(Exception, from_adc, 1)

    def testParsingADCValuesNoSensitivity(self):
        """Cannot convert ADC value without a sensitivity."""
        self.assertRaises(Exception, from_adc, 1)
