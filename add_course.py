# system libraries
import os
import sys
import urllib
import time
import random

# recaptcha libraries
import pydub
import speech_recognition as sr

# selenium libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# custom patch libraries
from datetime import datetime
from data import *

# Leave None if you do not want time start. (desired_time = None)
# desired_time = "10:00:00"

# # [courseCode, sectionCode, categoryCode]
# lessonList = [
#     ['6510141', '1', 'NONTECHNICAL ELECTIVE'],
#     ['6510242', '1', 'NONTECHNICAL ELECTIVE'],
#     ['6510242', '2', 'NONTECHNICAL ELECTIVE']
# ]

"""
COURSE CATEGORIES (for selection option):
MUST = 1
RESTRICTED ELECTIVE = 2
FREE ELECTIVE = 3
TECHNICAL ELECTIVE = 4
NONTECHNICAL ELECTIVE = 5
NOT INCLUDED = 6
"""
"""
COURSE CATEGORIES (for reading radio value):
MUST = 1
RESTRICTED ELECTIVE = 4
FREE ELECTIVE = 5
TECHNICAL ELECTIVE = 7
NONTECHNICAL ELECTIVE = 8
NOT INCLUDED = 9
"""

# category_dic = {'1': 'MUST', '4': 'RESTRICTED ELECTIVE', '5': 'FREE ELECTIVE', '7': 'TECHNICAL ELECTIVE', '8': 'NONTECHNICAL ELECTIVE', '9': 'NOT INCLUDED'}
option_dic = {'MUST': '1', 'RESTRICTED ELECTIVE': '2', 'FREE ELECTIVE': '3',
              'TECHNICAL ELECTIVE': '4', 'NONTECHNICAL ELECTIVE': '5', 'NOT INCLUDED': '6'}


def start_process(driver, wait, countdown_control):
    if start_time:
        time_loop(countdown_control)
    driver.get("https://register.metu.edu.tr")
    wait.until(EC.presence_of_element_located(
        (By.XPATH, '//input[@id="textUserCode"]')))

    wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="textUserCode"]'))).send_keys(metu_username)
    driver.find_element_by_xpath('//input[@id="textPassword"]').send_keys(metu_passw)
    
    print("Login page found...")
    driver.find_element_by_xpath('//input[@name="submitLogin"]').click()


def time_loop(countdown_control):
    print("Entered time loop...")
    desired = list(map(int, start_time.split(":")))
    desired_sec = desired[0]*3600 + desired[1]*60 + desired[2]
    if start_time:
        while 1:
            current_time = datetime.now().strftime("%H:%M:%S")
            lst = list(map(int, current_time.split(":")))
            sec = lst[0]*3600 + lst[1]*60 + lst[2]
            if sec >= desired_sec:
                break
            countdown_control.value = 1
            time.sleep(0.2)
    print("Exiting time loop...")


def recaptcha_control(driver):
    element = driver.find_element_by_id("recaptcha-anchor")
    print("Recapctha Checkmark =", element.get_attribute('aria-checked'))
    if element.get_attribute('aria-checked') == "true":
        return True
    else:
        return False


def wait_recaptcha(driver, timeout=5):
    t1 = time.perf_counter()
    element = driver.find_element_by_id("recaptcha-anchor")
    while time.perf_counter() - t1 < timeout:
        if element.get_attribute('aria-checked') == "true":
            break
        time.sleep(0.1)


def recaptcha_solver(driver, control, wait):
    frames = driver.find_elements_by_tag_name("iframe")
    recaptcha_control_frame = None
    recaptcha_challenge_frame = None
    for frame in frames:
        if frame.get_attribute("title") == "reCAPTCHA":
            recaptcha_control_frame = frame
        if frame.get_attribute("title") == "recaptcha challenge" or frame.get_attribute("title") == "reCAPTCHA sorusunun süresi iki dakika sonra dolacak" or frame.get_attribute("title") == "recaptcha challenge expires in two minutes":
            recaptcha_challenge_frame = frame
    if not (recaptcha_control_frame and recaptcha_challenge_frame):
        print("[ERR] Unable to find recaptcha. Abort solver.")
        control.refresh = True
    # switch to recaptcha frame
    frames = driver.find_elements_by_tag_name("iframe")
    driver.switch_to.frame(recaptcha_control_frame)

    # click on checkbox to activate recaptcha
    driver.find_element_by_class_name("recaptcha-checkbox-border").click()
    wait_recaptcha(driver, 1)

    if not recaptcha_control(driver):
        # switch to recaptcha audio control frame
        driver.switch_to.default_content()
        frames = driver.find_elements_by_tag_name("iframe")
        driver.switch_to.frame(recaptcha_challenge_frame)

        try:
            # click on audio challenge
            driver.find_element_by_id("recaptcha-audio-button").click()
        except:
            pass

        # switch to recaptcha audio challenge frame
        driver.switch_to.default_content()
        frames = driver.find_elements_by_tag_name("iframe")
        driver.switch_to.frame(recaptcha_challenge_frame)

        wait.until(EC.presence_of_element_located((By.ID, 'audio-source')))
        # get the mp3 audio file
        src = driver.find_element_by_id("audio-source").get_attribute("src")
        print(f"[INFO] Audio src: {src}")

        rand_int = random.randint(0,99999)
        path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), f"sample_{rand_int}.mp3"))
        
        while os.path.exists(path_to_mp3):
            rand_int = random.randint(0,99999)
            path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), f"sample_{rand_int}.mp3"))

        path_to_wav = os.path.normpath(os.path.join(os.getcwd(), f"sample_{rand_int}.wav"))

        # download the mp3 audio file from the source
        urllib.request.urlretrieve(src, path_to_mp3)

        # load downloaded mp3 audio file as .wav
        try:
            sound = pydub.AudioSegment.from_mp3(path_to_mp3)
            sound.export(path_to_wav, format="wav")
            sample_audio = sr.AudioFile(path_to_wav)
        except Exception:
            sys.exit(
                "[ERR] Please run program as administrator or download ffmpeg manually, "
                "https://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/"
            )

        # translate audio to text with google voice recognition
        r = sr.Recognizer()
        with sample_audio as source:
            audio = r.record(source)
        key = r.recognize_google(audio)
        print(f"[INFO] Recaptcha Passcode: {key}")
        # key in results and submit
        audio_section = driver.find_element_by_id("audio-response")
        audio_section.send_keys(key.lower())
        audio_section.send_keys(Keys.ENTER)

        driver.switch_to.default_content()
        frames = driver.find_elements_by_tag_name("iframe")
        driver.switch_to.frame(recaptcha_control_frame)
        wait_recaptcha(driver, 1)

        if not recaptcha_control(driver):
            control.refresh = True
        driver.switch_to.default_content()

        try:
            os.remove(path_to_mp3)
            os.remove(path_to_wav)
        except Exception as e:
            print("ERROR :", "Error occured while removing sound files." , e)
    else:
        driver.switch_to.default_content()
    
    


def check_lesson(driver, control):
    for i in [x.get_attribute('value').split("|") for x in driver.find_elements_by_name("radio_courseList")]:
        if i[0] in [x[0] for x in lessonList]:
            lessonNumber = 0
            while lessonNumber < len(lessonList):
                if i[0] == lessonList[lessonNumber][0]:
                    lessonList.pop(lessonNumber)
                    continue
                lessonNumber += 1
            if control.control_number != 0:
                control.control_number -= 1


class ControlTemp:
    def __init__(self) -> None:
        self.refresh = False
        self.control_number = 0


def main(countdown_control, restart_process_warning):
    # download latest chromedriver, please ensure that your chrome is up to date
    control = ControlTemp()
    path_to_chromedriver = os.path.normpath(
        os.path.join(os.getcwd(), "webdriver", "chromedriver")
    )
    # options = webdriver.ChromeOptions()
    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # driver = webdriver.Chrome(options=options, executable_path=path_to_chromedriver)
    driver = webdriver.Chrome(executable_path=path_to_chromedriver)
    wait = WebDriverWait(driver, timeout=3)

    # print(driver.title)
    # input("Type to continue...")

    while 1:
        try:
            if restart_process_warning.value == 0:
                print("\nadd_course.py KILLED.\n")
                driver.close()
                driver.quit()
                return -1
            start_process(driver, wait, countdown_control)
            try:
                WebDriverWait(driver, 1).until(EC.presence_of_element_located(
                    (By.XPATH, '//input[@name="submitAddCourse"]')))
            except Exception as e:
                if "chrome not reachable" in str(e):
                    restart_process_warning.value = 0
                print("ERROR :", e)

            while 1:
                check_lesson(driver, control)
                if control.control_number >= len(lessonList):
                    control.control_number = 0
                for order in list(range(len(lessonList)))[control.control_number:]:
                    control.control_number = order
                    lesson = lessonList[order]
                    courseCode, sectionCode, categoryCode = lesson[0], lesson[1], option_dic[lesson[2]]
                    print(f"\n{order} | {courseCode} - {sectionCode}")

                    try:
                        WebDriverWait(driver, 1).until(EC.presence_of_element_located(
                            (By.XPATH, '//input[@name="submitAddCourse"]')))
                    except Exception as e:
                        print(e)

                    driver.find_element_by_xpath(
                        '//*[@id="textAddCourseCode"]').clear()
                    driver.find_element_by_xpath(
                        '//*[@id="textAddCourseCode"]').send_keys(str(courseCode))

                    driver.find_element_by_xpath(
                        '//*[@id="textAddCourseSection"]').clear()
                    driver.find_element_by_xpath(
                        '//*[@id="textAddCourseSection"]').send_keys(str(sectionCode))

                    if categoryCode != '1':
                        driver.find_element_by_xpath(
                            f'//*[@id="selectAddCourseCategory"]/option[{categoryCode}]').click()

                    recaptcha_solver(driver, control, wait)

                    if control.refresh:
                        control.refresh = False
                        break
                    driver.find_element_by_xpath(
                        '//input[@name="submitAddCourse"]').click()
                    countdown_control.value = 1

                control.control_number = 0

            if len(lessonList) == 0:
                break

        except Exception as e:
            if len(lessonList) == 0:
                break
            if "chrome not reachable" in str(e):
                restart_process_warning.value = 0
            print("ERROR:", e)
        if len(lessonList) == 0:
            break
    driver.close()
    driver.quit()
    print("\nALL DONE...")
    return 0


if __name__ == "__main__":
    main()
