import time

class FocusTimer:
    def __init__(self, duration):
        self.duration = duration  # seconds
        self.start_time = None
        self.running = False

    def start(self):
        self.start_time = time.time()
        self.running = True

    def stop(self):
        self.running = False

    def time_remaining(self):
        if not self.running or self.start_time is None:
            return self.duration
        elapsed = time.time() - self.start_time
        return max(0, int(self.duration - elapsed))

    def is_finished(self):
        return self.time_remaining() <= 0
