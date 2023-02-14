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


def start_process(driver):
    driver.get("https://www.google.com/recaptcha/api2/demo")


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


def recaptcha_solver(driver, wait, countdown_control):
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

        if recaptcha_control(driver):
            countdown_control.value = 1
        driver.switch_to.default_content()
        try:
            os.remove(path_to_mp3)
            os.remove(path_to_wav)
        except Exception as e:
            print("ERROR :", "Error occured while removing sound files." , e)
    else:
        driver.switch_to.default_content()

def main(countdown_control, restart_process_warning):
    path_to_chromedriver = os.path.normpath(
        os.path.join(os.getcwd(), "webdriver", "chromedriver")
    )
    # options = webdriver.ChromeOptions()
    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # driver = webdriver.Chrome(options=options, executable_path=path_to_chromedriver)
    driver = webdriver.Chrome(executable_path=path_to_chromedriver)
    wait = WebDriverWait(driver, timeout=3)


    counter = 0
    while counter < 20:
        try:
            if restart_process_warning.value == 0:
                print("\ntest_recaptcha.py KILLED.\n")
                driver.close()
                driver.quit()
                return -1
            start_process(driver)
            time.sleep(3)
            recaptcha_solver(driver, wait, countdown_control)
        except Exception as e:
            print("ERROR :", e)
        counter += 1
        print("\nCounter:", counter, "\n")
        
    driver.close()
    driver.quit()
    print("\nALL DONE...")
    return 0

# if __name__ == "__main__":
#     main()
