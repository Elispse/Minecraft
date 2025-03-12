BLOCK_CHANGED = "block_changed"

class EventDispatcher:
    def __init__(self):
        self.listeners = {}

    def register_listener(self, event_type, listener):
        """Register a listener for a specific event type."""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def dispatch_event(self, event_type, *args, **kwargs):
        """Trigger all listeners for a specific event type."""
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                listener(*args, **kwargs)