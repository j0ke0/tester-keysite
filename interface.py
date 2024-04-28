from colorizer import color_pass, color_fail
from colorizer import find_com_ports
from tkinter import simpledialog
from no_tester_rev2 import main
from tkinter import messagebox
from no_tester import pin
import tkinter as tk
import sqlite3
import os

def another_on_entry_click(event):
    if another_input_text.get() == "Serial or file name":
        another_input_entry.delete(0, tk.END)
        another_input_entry.config(fg='black')

def another_on_entry_leave(event):
    if not another_input_text.get():
        another_input_text.set("Serial or file name")
        another_input_entry.config(fg='grey')

def third_on_entry_click(event):
    if third_input_text.get() == "Provide Comport Number":
        third_input_entry.delete(0, tk.END)
        third_input_entry.config(fg='black')

def third_on_entry_leave(event):
    if not third_input_text.get():
        third_input_text.set("Provide Comport Number")
        third_input_entry.config(fg='grey')

def on_entry_click(event):
    if input_text.get() == "Path":
        input_entry.delete(0, tk.END)
        input_entry.config(fg='black')

def on_entry_leave(event):
    if not input_text.get():
        input_entry.insert(0, "Path")
        input_entry.config(fg='grey')

def button1_click():
    input_text_value = input_entry.get().strip()
    comment_text.delete(1.0, tk.END)  # Remove leading and trailing whitespace

    # Extract directory path from input text
    directory_path = input_text_value
    if not os.path.exists(directory_path):
        comment_text.config(fg='red')
        comment_text.insert(tk.END, "Error: Directory does not exist!")
        return  # Exit the function if the directory does not exist

    # Update the CONSTANT_FILE_PATH to match the input directory path
    global CONSTANT_FILE_PATH
    CONSTANT_FILE_PATH = directory_path

    # Define the file path with the fixed file name
    file_path = os.path.join(directory_path, "noly.txt")

    try:
        # Write input text to a text file in the specified directory, overwriting existing content
        with open(file_path, "w") as file:
            file.write(input_text_value + "\n")
            comment_text.config(fg='black')
            comment_text.insert(tk.END, "File written successfully!")
    except IOError:
        comment_text.config(fg='black')
        comment_text.insert(tk.END, "Error: Could not write to file!")

    # Change button1 color after it's clicked
    button1.config(bg='#D3D3D3')

def button2_click():
    com_ports = find_com_ports()
    if com_ports:
        # Extract the port value from the first COM port found
        port_value = com_ports[0][0]

        # Set the extracted port value to the third_input_text widget
        third_input_text.set(port_value)

        # Clear existing content in comment_text
        comment_text.delete(1.0, tk.END)
        
        # Display COM ports in comment_text
        comment_text.insert(tk.END, "Available COM Ports:\n")
        for port, desc, hwid in com_ports:
            comment_text.insert(tk.END, f"Port: {port}, \nDescription: {desc}, \nHWID: {hwid}\n")
    else:
        # Clear existing content in comment_text
        comment_text.delete(1.0, tk.END)
        comment_text.insert(tk.END, "No COM ports available.")

    # Change button2 color after it's clicked
    button2.config(bg='#D3D3D3')

def button3_click():
    # Get the output file name from the user
    output_file_name = get_output_file_name()
    
    if output_file_name:
        test_result = main()  # Call the main function to run testing procedures
        if test_result:
            try:
                # Extract directory path from input text
                directory_path = input_text.get().strip()
                
                # Ensure that the directory path is not empty
                if directory_path:
                    # Construct the full path to the file
                    file_path = os.path.join(directory_path, output_file_name + ".txt")
                    
                    # Open a file for writing the test results
                    with open(file_path, "w") as file:
                        # Write the test results to the file
                        for result in test_result:
                            file.write(result + "\n")
                    
                    # Notify the user that the test results have been saved
                    comment_text.delete(1.0, tk.END)
                    comment_text.insert(tk.END, f"Path: {file_path}")
                    
                    # Display test summary in comment_text
                    comment_text.insert(tk.END, "\nTest Summary:\n")
                    comment_text.insert(tk.END, "\n".join(test_result))
                    comment_text.insert(tk.END, "\n-------End of test-------\n")
                    
                    # Colorize the text
                    color_pass(comment_text)
                    color_fail(comment_text)
                else:
                    # Notify the user that the directory path is empty
                    comment_text.delete(1.0, tk.END)
                    comment_text.insert(tk.END, "Error: Directory path is empty!")
            except IOError:
                # Handle the case where an error occurs while writing to the file
                comment_text.delete(1.0, tk.END)
                comment_text.insert(tk.END, "Error: Could not write test results to the location!")
        else:
            # Handle the case where there are no test results
            comment_text.delete(1.0, tk.END)
            comment_text.insert(tk.END, "No test results to save.")
    else:
        # Handle the case where no file name was provided
        comment_text.delete(1.0, tk.END)
        comment_text.insert(tk.END, "Error: No serial was provided!")

def button4_click():
    input_text.set("Button 4 Clicked")
    root.destroy()

import tkinter.messagebox as messagebox

def button5_click():
    try:
        pin()
    except Exception as e:
        # Display an error message box with the exception details
        messagebox.showerror("Alert", f"Wrong COM port: {str(e)}")


def button6_click():
    comment_text.delete(1.0, tk.END)
    load_comment()
    color_pass(comment_text)
    color_fail(comment_text)

def button7_click():
    # Clear comment text widget
    comment_text.delete('1.0', tk.END)
    
    # Get the input text (COM port) from third_input_text
    com_port = third_input_text.get()
    
    # Check if the comment contains "COM" as the first three letters
    if com_port[:3].upper() != "COM":
        # Display error message if the condition is not met
        comment_text.insert(tk.END, "Error: Invalid COM Port specified.")
        return
    
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('comments.db')
        cursor = conn.cursor()
        
        # Drop all existing data in the comments table
        cursor.execute('''DELETE FROM comments''')
        
        # Insert comment into database
        cursor.execute("INSERT INTO comments (comment_text) VALUES (?)", (com_port,))
        
        # Fetch all comments from database
        cursor.execute("SELECT comment_text FROM comments")
        comments = cursor.fetchall()
        
        # Display comments in comment text widget
        for comment in comments:
            comment_text.insert(tk.END, comment[0] + "\n")
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        
        # Change button7 color after it's clicked
        button7.config(bg='#D3D3D3')  # Change button color to #D3D3D3 after clicking
    
    except Exception as e:
        # If an error occurs, display the error message
        comment_text.insert(tk.END, f"Error: {e}")
        return

def load_comment():
    try:
        file_name = another_input_text.get()  # Get the file name from another_input_text
        file_path = os.path.join(CONSTANT_FILE_PATH, file_name)  # Construct full file path
        if not file_path.endswith(".txt"):
            file_path += ".txt"  # Append .txt extension if not already present
        with open(file_path, "r") as file:
            comment_content = file.read()
            comment_text.insert(tk.END, comment_content)
    except FileNotFoundError:
        comment_text.config(fg='black')  # Set text color to red
        comment_text.insert(tk.END, "File not found.\n")  # Insert "File not found." with a newline
    except Exception as e:
        comment_text.config(fg='red')  # Set text color to red
        comment_text.insert(tk.END, "Error: Provide a valid PATH.\n")  # Insert error message with a newline

def get_output_file_name():
    # Open a dialog window to get the output file name from the user
    while True:
        output_file_name = simpledialog.askstring("Validating Name", "Scan Serial Number:", parent=root)
        if output_file_name:
            # Check if the output file name starts with "MFP" and has exactly 7 digits
            if output_file_name.startswith("MFP") and output_file_name[3:].isdigit() and len(output_file_name) == 10:
                return output_file_name
            else:
                # Display an error message if the format is incorrect
                messagebox.showerror("Alert", "The format of the serial was incorrect!")
        else:
            # Return None if the user cancels the input
            return None

# Create the main window
root = tk.Tk()
root.title("PCB TESTER")

# Load the logo image
logo_image = tk.PhotoImage(file="C:/Users/joanm/Desktop/Noly/python/logo/logo.png")  # Replace "logo.png" with the path to your image file

# Create a frame to contain the logo
logo_frame = tk.Frame(root)
logo_frame.pack()

# Create a label to display the logo
logo_label = tk.Label(logo_frame, image=logo_image)
logo_label.pack()

# Create a frame to contain the input boxes
input_frame = tk.Frame(root, pady=8)
input_frame.pack()

# Create the input box
input_text = tk.StringVar()
input_entry = tk.Entry(input_frame, textvariable=input_text, fg='grey', bg='#B0C4DE', justify="center")
input_entry.grid(row=0, column=0, padx=15, ipadx=30)  # Use grid() for alignment
input_entry.insert(0, "Path")  # Set the placeholder text
input_entry.bind('<FocusIn>', on_entry_click)
input_entry.bind('<FocusOut>', on_entry_leave)

# Create the third StringVar variable
third_input_text = tk.StringVar()
third_input_entry = tk.Entry(input_frame, textvariable=third_input_text, fg='grey', bg='#B0C4DE', justify="center")
third_input_entry.grid(row=0, column=1, padx=6, ipadx=10)  # Use grid() for alignment
third_input_entry.insert(0, "Provide Comport Number")  # Set the placeholder text
third_input_entry.bind('<FocusIn>', third_on_entry_click)
third_input_entry.bind('<FocusOut>', third_on_entry_leave)

# Create another StringVar variable
another_input_text = tk.StringVar()
another_input_entry = tk.Entry(input_frame, textvariable=another_input_text, fg='grey', bg='#B0C4DE', justify="center")
another_input_entry.grid(row=0, column=2,padx=15, ipadx=30)  # Use grid() for alignment
another_input_entry.insert(0, "Serial or file name")  # Set the placeholder text
another_input_entry.bind('<FocusIn>', another_on_entry_click)
another_input_entry.bind('<FocusOut>', another_on_entry_leave)

# Create a frame to contain the buttons
button_frame = tk.Frame(root)
button_frame.pack()

# Create the buttons
button1 = tk.Button(button_frame, text="Log Address Save", command=button1_click, width=13, bg='#D3D3D3')  # Set background color to blue
button1.grid(row=0, column=0, padx=15, pady=10)
button1.config(bg='#FF5733')

button2 = tk.Button(button_frame, text="Check Comports", command=button2_click, width=13, bg='#D3D3D3')  # Set background color to green
button2.grid(row=0, column=1, padx=15, pady=10)
button2.config(bg='#FF5733')

# Create the "Save Comport" button
button7 = tk.Button(button_frame, text="Save Comport", command=button7_click, width=13, bg='#D3D3D3')  # Set initial background color to #FF5733
button7.grid(row=0, column=2, padx=15, pady=10)  # Adjust row and column as needed
button7.config(bg='#FF5733')

# Add the new button next to button2
button6 = tk.Button(button_frame, text="Open Log File ", command=button6_click, width=13, bg='#D3D3D3')  # Set background color and text accordingly
button6.grid(row=0, column=3, padx=15, pady=10)  # Adjust row and column as needed

# Create a frame for the comment box
comment_frame = tk.Frame(root)
comment_frame.pack(pady=10)

comment_text = tk.Text(comment_frame, width=69, height=15, bg='#B0C4DE')
comment_text.pack()

# Create a frame to contain the buttons
button_frame = tk.Frame(root)
button_frame.pack()

# Create the "Run Testing" button
button3 = tk.Button(button_frame, text="Run Testing", command=button3_click, width=10, bg='#D3D3D3', font=('Arial', 10, 'bold'))  # Set background color to red and make text bold
button3.grid(row=0, column=1, padx=25, pady=10)

# Create the "Exit" button
button4 = tk.Button(button_frame, text="Exit", command=button4_click, width=10, bg='#D3D3D3', font=('Arial', 10, 'bold'))
button4.grid(row=0, column=2, padx=15, pady=10)  # Adjust row and column as needed

# Create the additional button
button5 = tk.Button(button_frame, text="Program Ready", command=button5_click, width=12, bg='#D3D3D3', font=('Arial', 10, 'bold'))
button5.grid(row=0, column=0, padx=15, pady=10)  # Adjust row and column as needed

# Start the Tkinter event loop
root.mainloop()