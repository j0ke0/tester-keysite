import sqlite3
import serial
import time

def main():
    # Connect to SQLite database
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()

    # Function to get the COM port from the database
    def get_com_port():
        cursor.execute("SELECT comment_text FROM comments WHERE id = 1")
        row = cursor.fetchone()
        return row[0] if row else None

    # Get the COM port from the database
    com_port = get_com_port()

    if com_port:
        print("COM port retrieved from database:", com_port)
        # Use com_port to establish serial connection
        ser = serial.Serial(com_port, 9600)
        time.sleep(2.3)
    else:
        print("COM port not found in database. Please set it manually.")

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
            print("Voltage measured on TP1:")
            voltage = ser.readline().strip().decode()  # Read the voltage value from the device
            voltage = float(voltage)  # Convert the voltage value to float
            if 1.100 <= voltage <= 1.300:
                print("Voltage within the range (1.100 - 1.300):", voltage)
            else:
                print("Voltage not within the range (1.100 - 1.300):", voltage)

        elif "dog" in input_text:
            ser.write(b'3')
            time.sleep(1)
            last_pin = 3
            print("Voltage measured on TP2:")
        elif "cat" in input_text:
            ser.write(b'4')
            time.sleep(1)
            last_pin = 4
            print("Voltage measured on TP3:")
        elif "pig" in input_text:
            ser.write(b'5')
            time.sleep(1)
            last_pin = 5
            print("Voltage measured on TP4:")
        elif "rat" in input_text:
            ser.write(b'6')
            time.sleep(1)
            last_pin = 6
            print("Voltage measured on TP5:")
        elif "can" in input_text:
            ser.write(b'7')
            time.sleep(1)
            last_pin = 7
            print("Voltage measured on TP6:")
        elif "lip" in input_text:
            ser.write(b'8')
            time.sleep(1)
            last_pin = 8
            print("Voltage measured on TP7:")
        elif "ton" in input_text:
            ser.write(b'9')
            time.sleep(1)
            last_pin = 9
            print("Voltage measured on TP8:")
        elif "done" in input_text:
            ser.write(b'0')
            last_pin = 0
        if last_pin is not None:
            ser.write(str(last_pin).encode())
            last_pin = None

    if 'ser' in locals():
        ser.close()
    conn.close()

if __name__ == "__main__":
    main()