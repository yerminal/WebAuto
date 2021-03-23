from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import winsound
import getpass
import pickle, os
from fake_useragent import UserAgent

# PARAMETERS
metu_username = ''  # Your METU username - eXXXXXX - e204849
metu_password = ''  # Your METU password

priorList = [63, 61, 13, 14, 15, 90]

duration = 1000  # milliseconds
freq = 440  # Hz

def start_process(driver, wait):
    driver.get("https://register.metu.edu.tr")
    wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="textUserCode"]'))).send_keys(metu_username)
    driver.find_element_by_xpath('//input[@id="textPassword"]').send_keys(metu_password)
    driver.find_element_by_xpath('//input[@name="submitLogin"]').click()


# SETUP AND LAUNCH
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
#options.add_argument(f"user-data-dir=C:\\Users\\{getpass.getuser()}\\AppData\\Local\\Google\\Chrome\\User Data")
ua = UserAgent()
userAgent = ua.random
#options.add_argument(f'user-agent={userAgent}')

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, executable_path=r'C:\WebDrivers\chromedriver.exe')
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

wait = WebDriverWait(driver, 10)
start_process(driver, wait)

"""WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()"""

"""
driver.find_element_by_xpath('//input[@name="submitChangeCourse"]/option[4]').click()
driver.find_element_by_xpath("//input[@value='2360120|12|1']").click()
"""

done = False
while not done:
    try:
        while not done:
            for i in priorList:
                driver.find_element_by_xpath(
                    '//*[@id="single_content"]/form/table[3]/tbody/tr[1]/td/table/tbody/tr[8]/td[1]/input').click()
                driver.find_element_by_xpath('//*[@id="textChangeCourseSection"]').clear()
                driver.find_element_by_xpath('//*[@id="textChangeCourseSection"]').send_keys(str(i))
                driver.find_element_by_xpath(
                    '//*[@id="single_content"]/form/div[2]/div/center/fieldset/div/table/tbody/tr[2]/td[2]/input').click()
                if driver.find_element_by_xpath(
                        '//*[@id="single_content"]/form/table[3]/tbody/tr[1]/td/table/tbody/tr[8]/td[5]').text == str(i):
                    done = True
                    break
                time.sleep(0.2)
    except:
        print("Restarting...")
        start_process(driver, wait)

for _ in range(100):
    winsound.Beep(freq, duration)
    time.sleep(1)
