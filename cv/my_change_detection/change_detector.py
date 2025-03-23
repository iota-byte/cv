import threading
import time
import difflib
import os

class Observer:
    """An observer that gets notified about changes."""
    def notify(self, changes):
        """Notify the observer of changes."""
        print(f"\nChanges detected:")
        if changes['added']:
            print("Added lines:")
            for line in changes['added']:
                print(f"  + {line.strip()}")
        if changes['removed']:
            print("Removed lines:")
            for line in changes['removed']:
                print(f"  - {line.strip()}")


class ChangeDetector:
    def __init__(self, file_path, observer):
        self.file_path = file_path
        self.previous_content = self.read_file()
        self.lock = threading.Lock()
        self.keep_running = True
        self.observer = observer

    def read_file(self):
        """Read the content of the file."""
        with open(self.file_path, 'r') as file:
            return file.readlines()

    def monitor_changes(self):
        """Continuously monitor the file for changes."""
        while self.keep_running:
            time.sleep(1)  # Check for changes every second
            current_content = self.read_file()
            self.detect_changes(current_content)

    def detect_changes(self, current_content):
        """Detect changes between previous and current content."""
        with self.lock:
            diff = difflib.ndiff(self.previous_content, current_content)
            added_lines = []
            removed_lines = []

            for line in diff:
                if line.startswith('+ '):
                    added_lines.append(line[2:])
                elif line.startswith('- '):
                    removed_lines.append(line[2:])

            if added_lines or removed_lines:
                changes = {
                    'added': added_lines,
                    'removed': removed_lines
                }
                self.observer.notify(changes)
                
                # Update the previous content
                self.previous_content = current_content

    def stop(self):
        """Stop the monitoring thread."""
        self.keep_running = False


class Modifier:
    def __init__(self, file_path):
        self.file_path = file_path

    def modify_file(self):
        """Modify the file after a delay."""
        time.sleep(5)  # Wait 5 seconds before modifying
        with open(self.file_path, 'a') as file:
            file.write("\n# New line added by Modifier\n")
        
        time.sleep(2)  # Wait before stopping


def main():
    script_name = 'example_script.py'
    
    # Create a sample script if it doesn't exist
    if not os.path.exists(script_name):
        with open(script_name, 'w') as f:
            f.write("# Initial content\n")

    # Create an observer and the ChangeDetector
    observer = Observer()
    change_detector = ChangeDetector(script_name, observer)
    modifier = Modifier(script_name)

    # Start the change tracking thread
    tracker_thread = threading.Thread(target=change_detector.monitor_changes)
    tracker_thread.start()

    # Start the modifier thread
    modifier_thread = threading.Thread(target=modifier.modify_file)
    modifier_thread.start()

    # Wait for the modifier thread to finish
    modifier_thread.join()

    # Stop the change detector
    change_detector.stop()

    # Wait for the change tracker to finish
    tracker_thread.join()

if __name__ == '__main__':
    main()
