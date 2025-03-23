import win32pipe
import win32file
import time

# Define the name of the named pipe
pipe_name = r'\\.\pipe\myeventlogger'

# Create the named pipe
def create_named_pipe():
    print("Creating named pipe...")
    pipe = win32pipe.CreateNamedPipe(
        pipe_name,
        win32pipe.PIPE_ACCESS_DUPLEX,  # Read and write access
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT,
        1,  # Maximum instances
        512,  # Output buffer size
        512,  # Input buffer size
        0,  # Default timeout
        None  # Default security attributes
    )
    print(f"Named pipe created: {pipe_name}")
    return pipe

# Function to write to the pipe
def write_to_pipe(pipe):
    win32pipe.ConnectNamedPipe(pipe, None)  # Wait for a client to connect
    print("Client connected to the pipe.")
    while True:
        message = input("Enter a message to send to the pipe (type 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        win32file.WriteFile(pipe, message.encode())
        print(f"Sent: {message}")

# Main function
def main():
    pipe = create_named_pipe()
    write_to_pipe(pipe)
    win32pipe.DisconnectNamedPipe(pipe)  # Disconnect the pipe
    win32file.CloseHandle(pipe)  # Close the pipe handle
    print("Named pipe closed.")

if __name__ == "__main__":
    main()
