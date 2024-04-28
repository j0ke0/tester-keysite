import tkinter as tk
import os
import serial.tools.list_ports
import serial
import time


def color_pass(comment_text):
    start_idx = "1.0"
    while True:
        start_idx = comment_text.search("Pass", start_idx, stopindex=tk.END)
        if not start_idx:
            break
        end_idx = f"{start_idx}+{len('Pass')}c"
        comment_text.tag_add("pass_tag", start_idx, end_idx)
        comment_text.tag_config("pass_tag", foreground="green", font=("Arial", 10, "bold"))
        start_idx = end_idx

def color_fail(comment_text):
    start_idx = "1.0"
    while True:
        start_idx = comment_text.search("Fail", start_idx, stopindex=tk.END)
        if not start_idx:
            break
        end_idx = f"{start_idx}+{len('Fail')}c"
        comment_text.tag_add("fail_tag", start_idx, end_idx)
        comment_text.tag_config("fail_tag", foreground="red", font=("Arial", 10, "bold"))
        start_idx = end_idx

def find_com_ports():
    com_ports = []
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        com_ports.append((port, desc, hwid))
    return com_ports

if __name__ == "__main__":
    available_ports = find_com_ports()
    if available_ports:
        print("Available COM Ports:")
        for port, desc, hwid in available_ports:
            print(f"Port: {port}, Description: {desc}, HWID: {hwid}")
    else:
        print("No COM ports available.")



def initialize_serial_port(port='COM3', baudrate=9600, delay=1):
    ser = serial.Serial(port, baudrate)
    time.sleep(delay)
    return ser
