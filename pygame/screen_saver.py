import threading
import subprocess

class BlankScreen:

    def __init__(self, timeout=600):
        # how long before screen blanks in seconds
        self.blank_screen_timeout = timeout
        print("Screen blank timeout is", self.blank_screen_timeout, "seconds")
        
        self.blank_timer_cond = threading.Condition()
        self.blank_timer_running = False
        self.blank_screen = True
    
    def blank_screen_timer(self):
        print("Start blank screen timer")

        self.blank_timer_running = True

        while self.blank_timer_running:
            self.blank_timer_cond.acquire()
            self.blank_timer_cond.wait(self.blank_screen_timeout)
            # print("blank screen timer woke up")
            if self.blank_screen:
                bl_status = self.status()
                if bl_status != "1":
                    self.on()
            self.blank_screen = True
            self.blank_timer_cond.release()
        
        print("End blank screen timer")

    def stop_timer(self):
        print("Stopping blank screen timer")
        self.blank_timer_cond.acquire()
        print("Stop blank screen timer got lock")
        self.blank_screen = False
        self.blank_timer_running = False
        self.blank_timer_cond.notify()
        self.blank_timer_cond.release()
        print("Stop blank screen timer done")
        
    def reset_timer(self):
        self.blank_timer_cond.acquire()
        self.blank_screen = False
        self.blank_timer_cond.notify()
        self.blank_timer_cond.release()
        
    def start_timer(self):
        thread = threading.Thread(target = self.blank_screen_timer,
                                  args = ())
        thread.start()

    def status(self):
        # file contains 0 if scr is on, 1 if off
        # /sys/class/backlight/rpi_backlight/bl_power
        blank_file = '/sys/class/backlight/rpi_backlight/bl_power'
        try:
            with open(blank_file, 'r') as f:
                bl_status = f.read(1)
                print("bl_status %s" % bl_status)
                return bl_status
        except FileNotFoundError:
            pass
        return "error"
    
    
    # Using a script to wrap call to:
    #
    # sudo sh -c echo 1 > /sys/class/backlight/rpi_backlight/bl_power
    #
    # Tried stuff like:
    #
    #  subprocess.call(['sudo', 'sh', '-c' 'echo 1 > /sys/class/backlight/rpi_backlight/bl_power'])
    #
    # Maybe add a /bin/sh instead of just sh?  scripts needed a /bin/sh.
    # Or set shell arg thingy to true?

    def off(self):
        """Turn off screen saver.
        This means turning the screen on.
        """
        print("off(): Turning screen on")
        bl_status = self.status()
        if bl_status == "1":
            subprocess.call(["/home/pi/bin/scr-on.sh"])

    def on(self):
        """Turn on screen saver.
        This means turning the screen off.
        """
        print("on(): Turning screen off")
        bl_status = self.status()
        if bl_status == "0":
            subprocess.call(["/home/pi/bin/scr-off.sh"])
