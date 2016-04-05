def from_adc(adc_values, precision, sensitivity):
    """Convert a data series from raw values into units
    given the precision and sensitivy of the sensor.

    adc_values :: 'list-like' object representing ADC values
    precision :: Number of 'bits'
    sensitivity :: Range of sensor for this number of 'bits'"""

    return adc_values * sensitivity / (float(pow(2, precision)) / 2)
