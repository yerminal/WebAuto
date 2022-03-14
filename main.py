import multiprocessing
import countdown
import add_course
import os
import time

def start_chrome():
    os.system("/usr/bin/google-chrome --remote-debugging-port=9222 --user-data-")

def killall_chrome():
    os.system("killall chrome")

if __name__ == "__main__":
    isInOnce = False
    # creating Value of int data type
    countdown_control = multiprocessing.Value('i', 0)
    restart_process_warning = multiprocessing.Value('i', 2)
    # creating new process
    p1 = multiprocessing.Process(target=countdown.countdown, args=(0, 30, countdown_control, restart_process_warning, ))
    p2 = multiprocessing.Process(target=add_course.main, args=(countdown_control, restart_process_warning, ))
    p3 = multiprocessing.Process(target=start_chrome)
    p4 = multiprocessing.Process(target=killall_chrome)
    p4.start()
    p4.join()
    # starting process
    p3.start()
    p1.start()
    p2.start()
    print("Processes started...\n")
    while 1:
        # print("restart_process_warning:", restart_process_warning.value)
        if restart_process_warning.value == 1 and not isInOnce:
            print("\nRESTARTING add_course.py...\n")
            p2.terminate()
            p2 = multiprocessing.Process(target=add_course.main, args=(countdown_control, restart_process_warning, ))
            p2.start()
            isInOnce = True
        elif restart_process_warning.value == 0:
            isInOnce = False
            p1.terminate()
            p2.terminate()
            p3.terminate()
            time.sleep(3)
            print("\nRESTARTING COMPLETELY...\n")
            p1 = multiprocessing.Process(target=countdown.countdown, args=(30, countdown_control, restart_process_warning, ))
            p2 = multiprocessing.Process(target=add_course.main, args=(countdown_control, restart_process_warning, ))
            p3 = multiprocessing.Process(target=start_chrome)
            p4 = multiprocessing.Process(target=killall_chrome)
            p4.start()
            p4.join()
            # starting process
            p3.start()
            p1.start()
            p2.start()
            restart_process_warning.value = 2
        else:
            if not p2.is_alive():
                break
        time.sleep(0.8)

    p1.terminate()
    p2.terminate()
    p3.terminate()