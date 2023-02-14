import multiprocessing as mp
import countdown
import test_recaptcha
import time

if __name__ == "__main__":
    
    # creating Value of int data type
    countdown_control = mp.Value('i', 0)
    restart_process_warning = mp.Value('i', 1)
    
    # creating new process
    p1 = mp.Process(target=countdown.countdown, args=(30, countdown_control, restart_process_warning, ))
    p2 = mp.Process(target=test_recaptcha.main, args=(countdown_control, restart_process_warning, ))

    p1.start()
    p2.start()
    print("Processes started...\n")
    while 1:
        if restart_process_warning.value == 0:
            print("\nRESTARTING...\n")

            TIMEOUT = 10 
            start = time.time()
            while time.time() - start <= TIMEOUT:
                if not p2.is_alive():
                    break
                time.sleep(.1)
            else:
                p2.terminate()
                p2.join()

            p2 = mp.Process(target=test_recaptcha.main, args=(countdown_control, restart_process_warning, ))
            p2.start()

            restart_process_warning.value = 1
            countdown_control.value = 1
        else:
            if not p2.is_alive():
                break
        time.sleep(.8)
    p1.terminate()

