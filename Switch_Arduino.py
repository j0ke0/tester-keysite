import serial
import time
import sys
import pyvisa as visa
from voltage import voltages, preset

# Connect to Arduino via serial port
ser = serial.Serial('COM16', 9600)  # Replace 'COM16' with your Arduino's port
last_pin = None  # Variable to keep track of the last pin set high
time.sleep(1)

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

def main():
    input_texts = [
        "cow",
        "dog",
        "cat",
        "pig",
        "rat",
        "can",
        "lip",
        "ton",
        "done"
    ]

    for input_text in input_texts:
        if "exit" in input_text.lower():
            break

        if "cow" in input_text:
            ser.write(b'2')
            time.sleep(1)
            last_pin = 2
            voltage = voltages()
            print("Voltage measured on TP1:", voltage)
        elif "dog" in input_text:
            ser.write(b'3')
            time.sleep(1)
            last_pin = 3
            voltage = voltages()
            print("Voltage measured on TP2:", voltage)
        elif "cat" in input_text:
            ser.write(b'4')
            time.sleep(1)
            last_pin = 4
            voltage = voltages()
            print("Voltage measured on TP3:", voltage)
        elif "pig" in input_text:
            ser.write(b'5')
            time.sleep(1)
            last_pin = 5
            voltage = voltages()
            print("Voltage measured on TP4:", voltage)
        elif "rat" in input_text:
            ser.write(b'6')
            time.sleep(1)
            last_pin = 6
            voltage = voltages()
            print("Voltage measured on TP5:", voltage)
        elif "can" in input_text:
            ser.write(b'7')
            time.sleep(1)
            last_pin = 7
            voltage = voltages()
            print("Voltage measured on TP6:", voltage)
        elif "lip" in input_text:
            ser.write(b'8')
            time.sleep(1)
            last_pin = 8
            voltage = voltages()
            print("Voltage measured on TP7:", voltage)
        elif "ton" in input_text:
            ser.write(b'9')
            time.sleep(1)
            last_pin = 9
            voltage = voltages()
            print("Voltage measured on TP8:", voltage)
        elif "done" in input_text:
            ser.write(b'0')
            last_pin = 0
        if last_pin is not None:
            # Send command to Arduino to turn off the last pin
            ser.write(str(last_pin).encode())
            last_pin = None

# Call the main function
if __name__ == "__main__":
    main()
    
preset()