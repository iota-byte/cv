import os
import win32pipe
import win32file
import ctypes
import sys

def list_named_pipes():
    # List of named pipes
    pipe_list = []
    
    # Open the pipe directory
    pipe_directory = r'\\.\pipe\\'
    
    try:
        # Use a ctypes call to list the named pipes
        for pipe in os.listdir(pipe_directory):
            pipe_list.append(pipe)

        return pipe_list
    
    except Exception as e:
        print(f"Error accessing pipes: {e}")
        return []

def check_pipe_exists(pipe_name):
    pipes = list_named_pipes()
    
    # Check if the specified pipe exists
    if pipe_name in pipes:
        print(f"Pipe '{pipe_name}' exists.")
    else:
        print(f"Pipe '{pipe_name}' does not exist.")

if __name__ == "__main__":
    check_pipe_exists('myeventlogger')  # Change this to your specific pipe name
