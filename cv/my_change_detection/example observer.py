# example_observer.py
from change_detector import ChangeDetector, Observer
import time
class PrintObserver(Observer):
    """Observer that prints the state changes."""
    def update(self, key, value):
        print(f"State changed: {key} = {value}")

    def reset(self):
        print("Observer state has been reset.")

if __name__ == "__main__":
    # Create a change detector instance
    change_detector = ChangeDetector()

    # Create an observer instance
    print_observer = PrintObserver()

    # Add the observer to the change detector
    change_detector.add_observer(print_observer)

    # Simulate changing state with debounce
    change_detector.set_state("user.name", "Alice", debounce=True)
    change_detector.set_state("user.age", 30, debounce=True)
    change_detector.set_state("user.name", "Bob", debounce=True)

    # Wait for the debounce to finish
    time.sleep(0.3)  # Sleep longer than the debounce delay to ensure notifications are sent

    # Reset the state
    change_detector.reset_state()
