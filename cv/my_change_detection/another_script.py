from change_detector import ChangeDetector, Observer

class LoggingObserver(Observer):
    def update(self, key, value):
        print(f"Log: {key} changed to {value}")

change_detector = ChangeDetector()
logger = LoggingObserver()
change_detector.add_observer(logger)

change_detector.set_state("username", "Alice")
change_detector.set_state("username", "Bob")  # This will trigger the log
