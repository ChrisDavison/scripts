import pytest
from prelude.utility import *

@pytest.mark.skip(reason="Not implemented.")
def testChooseValidIndexFromList():
    pass

@pytest.mark.skip(reason="Not implemented.")
def testChooseInvalidIndexFromList():
    pass

@pytest.mark.skip(reason="Not implemented.")
def testChooseFromEmptyList():
    pass

@pytest.mark.skip(reason="Not implemented.")
def testChooseFiltered():
    pass

@pytest.mark.skip(reason="Not implemented.")
def testInsertionIntoTimeseries():
    pass

@pytest.mark.skip(reason="Not implemented.")
def testConversionOfADCValues():
    pass

@pytest.mark.skip(reason="Not implemented.")
def testMeanDurationOfTimestamps():
    """Determine the average difference between timestamps."""
    pass

@pytest.mark.skip(reason="Not implemented.")
def testMostPrevalentValueInList():
    """Can find the most prevalent value in a list."""
    assert False == True

@pytest.mark.skip(reason="Not implemented.")
def testMostPrevalentValueInListWithMulitplePrevalent():
    """Return the 'lesser' value if multiple values are 'most prevalent'"""
    assert False == True

def testParsingADCValues():
    """Convert a raw ADC value for a given sensitivity and precision."""
    precision = 8 # 8 bit sensor
    sensitivity = 1 / 2 # +- 1g
    assert 1.0 == from_adc(256, precision, sensitivity)

@pytest.mark.skip(reason="Not implemented.")
def testParsingADCValuesNoPrecision():
    """Cannot convert ADC value without a precision."""
    with pytest.raises(Exception):
        from_adc(1)

@pytest.mark.skip(reason="Not implemented.")
def testParsingADCValuesNoSensitivity():
    """Cannot convert ADC value without a sensitivity."""
    with pytest.raises(Exception):
        from_adc(1)
