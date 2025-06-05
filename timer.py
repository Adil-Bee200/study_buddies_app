import threading
import time

class FocusTimer:
    def __init__(self, on_complete_callback, on_tick_callback):
        self.on_complete = on_complete_callback
        self.on_tick = on_tick_callback
        self.is_running = False
        self.remaining_time = 25 * 60  # 25 mins is default
        self.total_time = 25 * 60
        self.timer_thread = None
        self._stop_event = threading.Event()

        self.start_time = None
        self.running = False

    ## Effects: Sets the timer duration in minutes
    def set_duration(self, minutes):
        if not self.is_running:
            self.total_time = minutes * 60
            self.remaining_time = self.total_time
    
    ## Effects: Start the timer
    def start(self, minutes=None):
        if self.is_running:
            return False
        
        if minutes is not None:
            self.set_duration(minutes)
        
        self.is_running = True
        self._stop_event.clear()
        self.timer_thread = threading.Thread(target=self._run_timer, daemon=True)
        self.timer_thread.start()
        return True
    
    ## Effects: Stop the timer
    def stop(self):
        if self.is_running:
            self.is_running = False
            self._stop_event.set()
            if self.timer_thread and self.timer_thread.is_alive():
                self.timer_thread.join(timeout=1.0)
    
    ## Effects: Reset the timer to its initial state
    def reset(self):
        self.stop()
        self.remaining_time = self.total_time
    
    ## Effects: Internal loop for timer (on its own thread)
    def _run_timer(self):
        while self.is_running and self.remaining_time > 0:
            if self._stop_event.wait(timeout=1.0):
                break
            
            if self.is_running:
                self.remaining_time -= 1
                if self.on_tick:
                    self.on_tick()
        
        # Timer completed or stopped
        if self.is_running and self.remaining_time <= 0:
            # Timer completed successfully
            self.is_running = False
            if self.on_complete:
                self.on_complete()   # call the success callback
        else:
            self.is_running = False  # Timer was stopped early
        
    ## Effects: Get the current progress as a percentage (0-100)
    def get_progress_percentage(self):
        if self.total_time == 0:
            return 100
        return ((self.total_time - self.remaining_time) / self.total_time) * 100
    
    ## Effects: Get remaining time in minutes (rounded up)
    def get_remaining_minutes(self):
        return (self.remaining_time + 59) // 60
    
    ## Effects: Get elapsed time in minutes
    def get_elapsed_minutes(self):
        return (self.total_time - self.remaining_time) // 60
