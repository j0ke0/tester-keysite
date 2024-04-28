import sqlite3
import serial
import time


def get_com_port(cursor):
    cursor.execute("SELECT comment_text FROM comments WHERE id = 1")
    row = cursor.fetchone()
    return row[0] if row else None

def send_command(ser, pin):
    ser.write(str(pin).encode())
    time.sleep(.7)

def main():
    try:
        output = []

        # Connect to SQLite database
        conn = sqlite3.connect('comments.db')
        cursor = conn.cursor()

        # Get the COM port from the database
        com_port = get_com_port(cursor)

        if com_port:
            output.append("COM port used: {}".format(com_port))
            # Use com_port to establish serial connection
            ser = serial.Serial(com_port, 9600)
            time.sleep(2.3)
        else:
            output.append("COM port not found in database. Please set it manually.")
            return output

        # Dictionary to hold voltage limits for each action
        voltage_limits = {
            "cow": (1.10, 1.23),  # Example voltage limits for "cow"
            "dog": (1.15, 1.20),  # Example voltage limits for "dog"
            "cat": (1.10, 1.22),  # Example voltage limits for "cat"
            "pig": (1.16, 1.21),  # Example voltage limits for "pig"
            "rat": (1.10, 1.24),  # Example voltage limits for "rat"
            "can": (1.14, 1.19),  # Example voltage limits for "can"
            "lip": (1.00, 1.25),  # Example voltage limits for "lip"
            "ton": (1.21, 1.26),  # Example voltage limits for "ton"
        }

        input_texts = [
            "cow",
            "dog",
            "cat",
            "pig",
            "rat",
            "can",
            "lip",
            "ton"
        ]

        last_pin = None
        messages = []
        for input_text in input_texts:
            if "exit" in input_text.lower():
                break

            actions = {
                "cow": 2,
                "dog": 3,
                "cat": 4,
                "pig": 5,
                "rat": 6,
                "can": 7,
                "lip": 8,
                "ton": 9,
            }

            action = actions.get(input_text.lower())
            if action is not None:
                send_command(ser, action)
                messages.append(" TP{} = 1.1100".format(action))
                last_pin = action

        if last_pin is not None:
            send_command(ser, last_pin)

        # Reset relays
        ser.write(b'Reset')  # Assuming 'Reset' is the command to reset the relays

        # Modify the messages list to append "pass" or "fail" based on voltage value
        for i in range(len(messages)):
            voltage_value = float(messages[i].split()[-1])
            action = input_texts[i].lower()
            low_limit, high_limit = voltage_limits.get(action, (1.19, 1.22))  # Default limits if not specified
            if low_limit <= voltage_value <= high_limit:
                messages[i] += " Pass"
            else:
                messages[i] += " Fail"

        # Return the test summary
        for message in messages:
            output.append(message)

        return output
                
    except sqlite3.Error as e:
        output.append("SQLite error: {}".format(str(e)))
    except serial.SerialException as e:
        output.append("Wrong COM port: {}".format(str(e)))
    finally:
        if 'ser' in locals():
            ser.close()
        if 'conn' in locals():
            conn.close()

        return output


# If this script is executed directly, run the main function
if __name__ == "__main__":
    result = main()
    for line in result:
        print(line)
