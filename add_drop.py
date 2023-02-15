# system libraries
import os
import sys
import time
from datetime import datetime

# selenium libraries
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from data import *

# Leave None if you do not want time start. (desired_time = None)
desired_time = "10:00:00"

# Usage: [courseCode, categoryName, sectionList]
lessonList = [
    ['3110210', 'NONTECHNICAL ELECTIVE', ['3']]
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
    wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="textUserCode"]'))).send_keys(metu_username)
    driver.find_element_by_xpath('//input[@id="textPassword"]').send_keys(metu_passw)
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
        driver.close()
        driver.quit()
        sys.exit("[ERR] Check whether all your courses in lessonList are in your current courses.")
    
    for lesson_now in filtered_table:
        lesson_code, section_code = lesson_now[0], lesson_now[1]
        seclist = [x for x in lessonList if x[0] == lesson_code][0][2]
        
        try:
            index = seclist.index(section_code)
            seclist = seclist[:index]
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
    path_to_chromedriver = os.path.normpath(
        os.path.join(os.getcwd(), "webdriver", "chromedriver")
    )
    driver = webdriver.Chrome(executable_path=path_to_chromedriver)
    wait = WebDriverWait(driver, timeout=3)

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

    driver.close()
    driver.quit()
    print("\nALL DONE...")
    
