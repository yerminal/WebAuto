# system libraries
import os
import sys
import time
import winsound
# selenium libraries
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# custom patch libraries
from patch import download_latest_chromedriver, webdriver_folder_name
from datetime import datetime

# Leave None if you do not want time start. (desired_time = None)
desired_time = "15:00:00"

# Usage: [courseCode, categoryCode, sectionList]
lessonList = [
    ['5670100', 'MUST', ['4', '12', '3']],
    ['5690105', 'MUST', ['5', '12', '13', '6']]
]

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

category_dic = {'MUST': '1', 'RESTRICTED ELECTIVE': '4', 'FREE ELECTIVE': '5', 'TECHNICAL ELECTIVE': '7', 'NONTECHNICAL ELECTIVE': '8', 'NOT INCLUDED': '9'}
option_dic = {'MUST': '1', 'RESTRICTED ELECTIVE': '2', 'FREE ELECTIVE': '3', 'TECHNICAL ELECTIVE': '4', 'NONTECHNICAL ELECTIVE': '5', 'NOT INCLUDED': '6'}

def start_process():
    if desired_time:
        time_loop()
    driver.get("https://register.metu.edu.tr")
    wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="textUserCode"]')))
    print("Login page found...")
    driver.find_element_by_xpath('//input[@name="submitLogin"]').click()

def time_loop():
    print("Entered time loop...")
    desired = list(map(int, desired_time.split(":")))
    desired_sec = desired[0]*3600 + desired[1]*60 + desired[2]
    while 1:
        current_time = datetime.now().strftime("%H:%M:%S")
        lst = list(map(int, current_time.split(":")))
        sec = lst[0]*3600 + lst[1]*60 + lst[2]
        if sec >= desired_sec:
            break
        time.sleep(0.2)
    print("Exiting time loop...")

def delay(waiting_time=5):
    driver.implicitly_wait(waiting_time)

def check_lesson():
    lessonTable = [x.get_attribute('value').split("|") for x in driver.find_elements_by_name("radio_courseList")]
    desired_lessons = [x[0] for x in lessonList]
    filtered_table = [x for x in lessonTable if x[0] in desired_lessons]
    
    if len(filtered_table) == 0:
        sys.exit("[ERR] Check whether all your courses in lessonList are in your current courses.")
    
    for lesson_now in filtered_table:
        lesson_code, section_code = lesson_now[0], lesson_now[1]
        seclist = [x for x in lessonList if x[0] == lesson_code][0][2]
        
        try:
            index = seclist.index(section_code)
            seclist = seclist[:index]
            winsound.Beep(440, 600)
            print(f"[+] Successfully added {lesson_code} | Section: {section_code}")
            
            for index in range(len(lessonList)):
                lesson = lessonList[index]
                if lesson[0] == lesson_code:
                    lessonList[index][2] = seclist
                    break
        except ValueError:
            pass

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
            wait = WebDriverWait(driver, timeout=3)
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

    while len(lessonList) != 0:
        try:
            start_process()
            try:
                WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//input[@name="submitAddCourse"]')))
            except Exception as e:
                print("ERROR :", e)

            while 1:
                check_lesson()
                for order, lesson in enumerate(lessonList):
                    courseCode, categoryCode, sectionList = lesson[0], category_dic[lesson[1]], lesson[2]
                    option = option_dic[lesson[1]]

                    for sectionCode in sectionList:
                        print(f"\nTrying {courseCode} - {sectionCode}")
                        
                        try:
                            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//input[@name="submitAddCourse"]')))
                        except Exception as e:
                            print("ERROR :", e)

                        lessonTable = [x.get_attribute('value').split("|") for x in driver.find_elements_by_name("radio_courseList")]
                        sectionCode_now = [x[1] for x in lessonTable if x[0] == courseCode][0]

                        driver.find_element_by_xpath(f'//input[@value="{courseCode}|{sectionCode_now}|{categoryCode}"]').click()
                        driver.find_element_by_xpath('//*[@id="textChangeCourseSection"]').clear()
                        driver.find_element_by_xpath('//*[@id="textChangeCourseSection"]').send_keys(str(sectionCode))
                        if categoryCode != '1':
                            driver.find_element_by_xpath(f'//*[@id="selectChangeCourseCategory"]/option[{option}]').click()
                        driver.find_element_by_xpath('//input[@name="submitChangeSection"]').click()

                    if len(lesson[2]) == 0:
                        lessonList.pop(order)

            if len(lessonList) == 0:
                break

        except Exception as e:
            if len(lessonList) == 0:
                break
            print("ERROR:", e, "\nRestarting...")

    print("\nALL DONE...")

    for _ in range(5):
        winsound.Beep(440, 1000)
        time.sleep(1)
