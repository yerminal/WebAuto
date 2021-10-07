# It can be sent max 4 requests to recaptcha.
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

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

# SETUP AND LAUNCH
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=options, executable_path=r'C:\webdrivers\chromedriver.exe')

wait = WebDriverWait(driver, timeout=10)

print(driver.title)

input("Type to continue...")

print()
for order, lesson in enumerate(lessonList):
    courseCode, sectionCode, categoryCode = lesson[0], lesson[1], lesson[2]
    print(f"{order} | {courseCode} - {sectionCode}")

    driver.find_element_by_xpath('//*[@id="textAddCourseCode"]').clear()
    driver.find_element_by_xpath('//*[@id="textAddCourseCode"]').send_keys(str(courseCode))
    
    driver.find_element_by_xpath('//*[@id="textAddCourseSection"]').clear()
    driver.find_element_by_xpath('//*[@id="textAddCourseSection"]').send_keys(str(sectionCode))

    driver.find_element_by_xpath(f'//*[@id="selectAddCourseCategory"]/option[{categoryCode}]').click()
    
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
    time.sleep(0.4)

    driver.find_element_by_xpath('//input[@name="submitAddCourse"]').click()

print("ALL DONE...")
