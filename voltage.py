import pyvisa as visa
import time
import os

def voltages():
    rm = visa.ResourceManager()
    v34410A = rm.open_resource('GPIB2::22::INSTR')
    idn = v34410A.query('*IDN?')
    v34410A.write(':SYST:PRES')
    temp_values = v34410A.query_ascii_values(':MEAS:SCAL:VOLT:DC? %s,%s' % ('AUTO', 'MAX'))
    dcVoltage = temp_values[0]
    v34410A.close()
    rm.close()
    return dcVoltage


def preset():
    rm = visa.ResourceManager()
    v34410A = rm.open_resource('GPIB2::22::INSTR')
    time.sleep(0.8)
    v34410A.write(':SYST:PRES')
    v34410A.close()
    rm.close()
    


    


