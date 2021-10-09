# system libraries
import os
import sys
import urllib
import time

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
from patch import download_latest_chromedriver, webdriver_folder_name

# [courseCode, sectionCode, categoryCode]
lessonList = [
    ['6390211', '1', '1'],
    ['5670201', '1', '1'],
    ['5670213', '7', '1'],
    ['2360260', '1', '1'],
    ['5700230', '4', '2']
]

"""
COURSE CATEGORIES:
MUST = 1
RESTRICTED ELECTIVE = 2
FREE ELECTIVE = 3
TECHNICAL ELECTIVE = 4
NONTECHNICAL ELECTIVE = 5
NOT INCLUDED = 6
"""

def delay(waiting_time=5):
    driver.implicitly_wait(waiting_time)

def recaptcha_control():
    element = driver.find_element_by_id("recaptcha-anchor")
    print("Checkmark =", element.get_attribute('aria-checked'))
    if element.get_attribute('aria-checked') == "true":
        return True
    else:
        return False

def wait_recaptcha(timeout=5):
    t1 = time.perf_counter()
    element = driver.find_element_by_id("recaptcha-anchor")
    while time.perf_counter() - t1 < timeout:
        if element.get_attribute('aria-checked') == "true":
            break
        time.sleep(0.1)

def recaptcha_solver():
    frames = driver.find_elements_by_tag_name("iframe")
    recaptcha_control_frame = None
    recaptcha_challenge_frame = None
    for frame in frames:
        if frame.get_attribute("title") == "reCAPTCHA":
            recaptcha_control_frame = frame
        if frame.get_attribute("title") == "recaptcha challenge":
            recaptcha_challenge_frame = frame
    if not (recaptcha_control_frame and recaptcha_challenge_frame):
        print("[ERR] Unable to find recaptcha. Abort solver.")
        exit()
    # switch to recaptcha frame
    frames = driver.find_elements_by_tag_name("iframe")
    driver.switch_to.frame(recaptcha_control_frame)

    # click on checkbox to activate recaptcha
    driver.find_element_by_class_name("recaptcha-checkbox-border").click()
    wait_recaptcha(2)

    if not recaptcha_control():
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

        # get the mp3 audio file
        src = driver.find_element_by_id("audio-source").get_attribute("src")
        print(f"[INFO] Audio src: {src}")

        path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))
        path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "sample.wav"))

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
        # driver.find_element_by_id("recaptcha-verify-button").click()
        driver.switch_to.default_content()
        frames = driver.find_elements_by_tag_name("iframe")
        driver.switch_to.frame(recaptcha_control_frame)
        wait_recaptcha()
        driver.switch_to.default_content()
    else:
        driver.switch_to.default_content()
if __name__ == "__main__":
    # download latest chromedriver, please ensure that your chrome is up to date
    while True:
        try:
            # create chrome driver
            path_to_chromedriver = os.path.normpath(
                os.path.join(os.getcwd(), webdriver_folder_name, "chromedriver.exe")
            )
            options = webdriver.ChromeOptions()
            options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            driver = webdriver.Chrome(options=options, executable_path=path_to_chromedriver)
            wait = WebDriverWait(driver, timeout=10)
            delay(1)
            break
        except Exception:
            # patch chromedriver if not available or outdated
            try:
                driver
            except NameError:
                is_patched = download_latest_chromedriver()
            else:
                is_patched = download_latest_chromedriver(
                    driver.capabilities["version"]
                )
            if not is_patched:
                sys.exit(
                    "[ERR] Please update the chromedriver.exe in the webdriver folder according to your chrome version:"
                    "https://chromedriver.chromium.org/downloads"
                )

    print(driver.title)
    input("Type to continue...")

    for order, lesson in enumerate(lessonList):
        courseCode, sectionCode, categoryCode = lesson[0], lesson[1], lesson[2]
        print(f"\n{order} | {courseCode} - {sectionCode}")
        
        driver.find_element_by_xpath('//*[@id="textAddCourseCode"]').clear()
        driver.find_element_by_xpath('//*[@id="textAddCourseCode"]').send_keys(str(courseCode))
        
        driver.find_element_by_xpath('//*[@id="textAddCourseSection"]').clear()
        driver.find_element_by_xpath('//*[@id="textAddCourseSection"]').send_keys(str(sectionCode))

        if categoryCode != '1':
            driver.find_element_by_xpath(f'//*[@id="selectAddCourseCategory"]/option[{categoryCode}]').click()

        recaptcha_solver()

        driver.find_element_by_xpath('//input[@name="submitAddCourse"]').click()
        
    print("\nALL DONE...")
