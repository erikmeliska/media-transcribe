import time
import Quartz  # PyObjC dependency
import psutil
import os

MINIMUM_IDLE_TIME = 0.1  # minutes
MIN_IDLE_PERCENTAGE = 60  # percentage

def get_idle_time():
    """ Returns system idle time in seconds """
    idle_time = Quartz.CGEventSourceSecondsSinceLastEventType(Quartz.kCGEventSourceStateHIDSystemState, Quartz.kCGAnyInputEventType)
    return idle_time

def is_notebook_on_power():
    """ Check if the notebook is running on battery. """
    if hasattr(psutil, "sensors_battery"):
        battery = psutil.sensors_battery()
        if battery:
            return battery.power_plugged
    return False

def is_fullscreen_app_active():
    """ Check if the active application is running in fullscreen mode. """
    main_display = Quartz.CGMainDisplayID()
    display_bounds = Quartz.CGDisplayBounds(main_display)
    display_width = display_bounds.size.width
    display_height = display_bounds.size.height

    active_window = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements, Quartz.kCGNullWindowID)
    for window in active_window:
        if window.get('kCGWindowLayer') == 0:
            window_bounds = window['kCGWindowBounds']
            window_width = window_bounds['Width']
            window_height = window_bounds['Height']
            if window_width == display_width and window_height == display_height:
                return True
    return False

def is_cpu_sufficiently_idle(min_idle_percentage=MIN_IDLE_PERCENTAGE):
    """ Check if the CPU is at least a certain percentage idle. """
    return psutil.cpu_percent(1) <= (100 - min_idle_percentage)

def can_perform_task():
    """ Check if conditions are met to perform a task. """
    idle_for_some_time = get_idle_time() >= MINIMUM_IDLE_TIME * 60
    fullscreen_not_active = not is_fullscreen_app_active()
    cpu_idle = is_cpu_sufficiently_idle()

    return idle_for_some_time and fullscreen_not_active and cpu_idle

# Example usage
# if can_perform_task():
#     print("Conditions met to perform the task")

# # loop checking for idle time, when idle, use system say command to announce status idle
# while True:
#     print(is_notebook_on_battery())
#     print(psutil.sensors_battery())
#     if can_perform_task():
#         print("Conditions met to perform the task")
#         # os.system("say 'Spúšťam úlohu na pozadí'")
#         time.sleep(10)
#     else:
#         print("Conditions not met to perform the task")
#         # os.system("say 'Nemôžem vykonať úlohu'")
#         time.sleep(10)


