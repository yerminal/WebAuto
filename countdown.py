import time
import datetime
 
def countdown(s, countdown_control, restart_process_warning):
    total_seconds = s
    while 1:
        while total_seconds > 0:
            time.sleep(1)
            total_seconds -= 1
            
            if countdown_control.value == 1:
                total_seconds = s
                countdown_control.value = 0

            if total_seconds != s and total_seconds % 5 == 0:
                print("\nRestart Timeout:", str(datetime.timedelta(seconds = total_seconds)) + "\n")
        
        total_seconds = s
        restart_process_warning.value -= 1
        print("restart_process_warning:", restart_process_warning.value)