# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import winsound
import os

link = "https://www.kaggle.com/yerminal/yolor-d6"
"""
wait.until(EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']"))):
    time.sleep(1)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
"""

def start_process(driver, wait):
    driver.get("https://www.youtube.com/")
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="header-logo"]/a/iron-icon')))
    action = ActionChains(driver)
    action.key_down(Keys.CONTROL).send_keys('\ue039').key_up(Keys.CONTROL).perform()
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ok"]'))).click()
# SETUP AND LAUNCH
os.system("whoami")
os.system('cmd /k "chrome --remote-debugging-port=9222 --user-data-"')
time.sleep(5)
options = webdriver.ChromeOptions()
# options.add_argument("start-maximized")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# options.add_argument("user-data-dir="+ "C:\\Users\\" + os.getlogin() + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
driver = webdriver.Chrome(options=options, executable_path=r'C:\webdrivers\chromedriver.exe')

wait = WebDriverWait(driver, timeout=10)
print(driver.title)
# driver.get("https://harith-sankalpa.medium.com/connect-selenium-driver-to-an-existing-chrome-browser-instance-41435b67affd")
start_process(driver, wait)
""
"""WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()"""

"""
driver.find_element_by_xpath('//input[@name="submitChangeCourse"]/option[4]').click()
driver.find_element_by_xpath("//input[@value='2360120|12|1']").click()
"""

# done = False
# while not done:
#     try:
#         while not done:
#             for i in priorList:
#                 driver.find_element_by_xpath(
#                     f'//input[@value="{courseCode}|{sectionCode}|{categoryCode}"]').click()
#                 driver.find_element_by_xpath('//*[@id="textChangeCourseSection"]').clear()
#                 driver.find_element_by_xpath('//*[@id="textChangeCourseSection"]').send_keys(str(i))
#                 driver.find_element_by_xpath(
#                     '//input[@name="submitChangeSection"]').click()
#                 if driver.find_element_by_xpath(
#                         f'//*[@id="single_content"]/form/table[3]/tbody/tr[1]/td/table/tbody/tr[{orderOfCourse+1}]/td[5]').text == str(i):
#                     done = True
#                     break
#                 time.sleep(0.2)
#
#     except:
#         print("Restarting...")
#         start_process(driver, wait)
#
# for _ in range(100):
#     winsound.Beep(freq, duration)
#     time.sleep(1)
