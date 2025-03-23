import unittest
import time
import threading
import difflib
from change_detector import ChangeDetector, Observer

class TestObserver(Observer):
    """A test observer that captures state changes."""
    def __init__(self):
        self.changes = []

    def update(self, key, value):
        self.changes.append((key, value))

    def reset(self):
        self.changes = []  # Clear changes on reset

class TestChangeDetector(unittest.TestCase):
    def setUp(self):
        """Set up a ChangeDetector and a TestObserver before each test."""
        self.change_detector = ChangeDetector()
        self.observer = TestObserver()
        self.change_detector.add_observer(self.observer)

    @classmethod
    def setUpClass(cls):
        """Print the initial and modified script names and summary of changes."""
        cls.print_script_names()
        cls.compare_scripts()

    @staticmethod
    def print_script_names():
        """Print the names of the initial and modified scripts."""
        initial_script_name = "initial_change_detector.py"
        modified_script_name = "modified_change_detector.py"
        
        print(f"Initial Script: {initial_script_name}")
        print(f"Modified Script: {modified_script_name}")

    @staticmethod
    def compare_scripts():
        """Compare initial and modified scripts and print changes."""
        initial_script_content = '''
class ChangeDetector:
    def __init__(self):
        self._state = {}
        self._observers = []

    def set_state(self, key, value):
        """Set the state and notify observers."""
        self._state[key] = value
        self.notify_observers(key, value)

    def get_state(self, key):
        """Get the current state for the given key."""
        return self._state.get(key, None)

    def add_observer(self, observer):
        """Add an observer that will be notified on state changes."""
        self._observers.append(observer)

    def notify_observers(self, key, value):
        """Notify all observers about the state change."""
        for observer in self._observers:
            observer.update(key, value)

class Observer:
    """Base class for observers that will react to state changes."""
    def update(self, key, value):
        raise NotImplementedError("Observer must implement the update method.")
        '''
        
        modified_script_content = '''
class ChangeDetector:
    def __init__(self):
        self._state = {}
        self._observers = []
        self._pending_updates = {}
        self._debounce_timeout = None
        self._debounce_delay = 0.2  # 200 milliseconds debounce time

    def set_state(self, key, value, debounce=False):
        """Set the state and notify observers if the value has changed."""
        keys = key.split('.')
        old_value = self._get_nested_state(keys)

        self._set_nested_state(keys, value)

        if old_value != value:  # Only notify if the value has changed
            if debounce:
                self._pending_updates[key] = value
                self._start_debounce()
            else:
                self.notify_observers(key, value)

    def _set_nested_state(self, keys, value):
        """Set the state value for nested keys."""
        state = self._state
        for key in keys[:-1]:
            if key not in state:
                state[key] = {}
            state = state[key]
        state[keys[-1]] = value

    def get_state(self, key):
        """Get the current state for the given key."""
        keys = key.split('.')
        value = self._get_nested_state(keys)
        return value if value != {} else None  # Return None if the value is an empty dict

    def _get_nested_state(self, keys):
        """Get the state value for nested keys."""
        state = self._state
        for key in keys:
            state = state.get(key, {})
        return state

    def add_observer(self, observer):
        """Add an observer that will be notified on state changes."""
        self._observers.append(observer)

    def notify_observers(self, key, value):
        """Notify all observers about the state change."""
        for observer in self._observers:
            observer.update(key, value)

    def _start_debounce(self):
        """Start a debounce timer for pending updates."""
        if self._debounce_timeout is not None:
            self._debounce_timeout.cancel()  # Cancel previous timeout

        self._debounce_timeout = threading.Timer(self._debounce_delay, self._flush_pending_updates)
        self._debounce_timeout.start()

    def _flush_pending_updates(self):
        """Flush the pending updates and notify observers."""
        for key, value in self._pending_updates.items():
            self.notify_observers(key, value)
        self._pending_updates.clear()

    def reset_state(self):
        """Reset the state to an empty dictionary."""
        self._state.clear()
        for observer in self._observers:
            observer.reset()

class Observer:
    """Base class for observers that will react to state changes."""
    def update(self, key, value):
        raise NotImplementedError("Observer must implement the update method.")

    def reset(self):
        """Reset the observer's state (if needed)."""
        pass
        '''

        # Compare scripts using difflib
        initial_lines = initial_script_content.strip().splitlines()
        modified_lines = modified_script_content.strip().splitlines()
        diff = difflib.ndiff(initial_lines, modified_lines)

        added_lines = []
        removed_lines = []

        for line in diff:
            if line.startswith('+ '):
                added_lines.append(line[2:])
            elif line.startswith('- '):
                removed_lines.append(line[2:])

        if added_lines:
            print("Changes detected: Added lines:")
            for line in added_lines:
                print(f"  + {line}")

        if removed_lines:
            print("Changes detected: Removed lines:")
            for line in removed_lines:
                print(f"  - {line}")

    def test_initial_state(self):
        """Test that the initial state is empty."""
        self.assertEqual(self.change_detector.get_state("count"), None)

    def test_set_nested_state(self):
        """Test setting nested state values."""
        self.change_detector.set_state("user.name", "Alice")
        self.change_detector.set_state("user.age", 30)
        self.assertEqual(self.change_detector.get_state("user.name"), "Alice")
        self.assertEqual(self.change_detector.get_state("user.age"), 30)

    def test_set_state_notifies_observer(self):
        """Test that setting state notifies the observer."""
        self.change_detector.set_state("count", 1)
        self.assertEqual(self.observer.changes, [("count", 1)])

    def test_set_state_no_duplicate_notification(self):
        """Test that setting the same state does not notify again."""
        self.change_detector.set_state("count", 1)
        self.change_detector.set_state("count", 1)  # No change, should not notify
        self.assertEqual(self.observer.changes, [("count", 1)])

    def test_debounce_updates(self):
        """Test that debounce works as expected."""
        self.change_detector.set_state("count", 1, debounce=True)
        self.change_detector.set_state("count", 2, debounce=True)
        self.change_detector.set_state("count", 3, debounce=True)

        # Wait for debounce delay
        time.sleep(0.3)  # Sleep longer than the debounce delay to ensure notifications are sent

        self.assertEqual(self.observer.changes, [("count", 3)])  # Only the last change should be notified

    def test_reset_state(self):
        """Test that the reset functionality works."""
        self.change_detector.set_state("count", 1)
        self.change_detector.reset_state()
        self.assertEqual(self.observer.changes, [])  # No changes should be captured after reset

if __name__ == '__main__':
    unittest.main()
