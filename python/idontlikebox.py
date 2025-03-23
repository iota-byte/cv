import tkinter as tk
import threading

# Flag to track window selection status
window_selected = False

def on_window_select(event):
    """Flag when the first window is selected."""
    global window_selected
    window_selected = True
    print("Window 1 selected.")

def task_when_window_selected():
    """A task that is triggered when Window 1 is selected."""
    while True:
        if window_selected:
            print("Executing task in Window 1!")
            # Do some work here
            window_selected = False

def draw_line(event, canvas, start_x, start_y):
    """Draw a straight line from start to current mouse position."""
    canvas.create_line(start_x, start_y, event.x, event.y)
    return event.x, event.y

def start_drawing():
    """Create the second window for drawing."""
    root2 = tk.Tk()
    root2.title("Window 2 - Draw Lines")

    canvas = tk.Canvas(root2, width=400, height=400)
    canvas.pack()

    start_x, start_y = None, None

    def on_click(event):
        nonlocal start_x, start_y
        if start_x is None or start_y is None:
            start_x, start_y = event.x, event.y
        else:
            start_x, start_y = draw_line(event, canvas, start_x, start_y)

    canvas.bind("<Button-1>", on_click)  # Left click to start drawing
    root2.mainloop()

def start_window_1():
    """Create the first window with a task."""
    root1 = tk.Tk()
    root1.title("Window 1")

    # Create a label to display window selection status
    label = tk.Label(root1, text="Select this window to trigger task.")
    label.pack(pady=20)

    # Bind the window selection event
    root1.bind("<FocusIn>", on_window_select)  # Trigger task when window selected

    # Run the window in the background thread to not block the main program
    root1.mainloop()

if __name__ == "__main__":
    # Start the task when the window is selected in a separate thread
    task_thread = threading.Thread(target=task_when_window_selected, daemon=True)
    task_thread.start()

    # Launch the two windows in separate threads
    window1_thread = threading.Thread(target=start_window_1, daemon=True)
    window1_thread.start()

    window2_thread = threading.Thread(target=start_drawing, daemon=True)
    window2_thread.start()

    # Mainloop to keep the main program running
    window1_thread.join()
    window2_thread.join()
