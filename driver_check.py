import os
import sys
from patch import download_latest_chromedriver, webdriver_folder_name
from selenium import webdriver

def delay(waiting_time=5):
    driver.implicitly_wait(waiting_time)

if __name__ == "__main__":
    while True:
        try:
            # create chrome driver
            path_to_chromedriver = os.path.normpath(
                os.path.join(os.getcwd(), webdriver_folder_name, "chromedriver.exe")
            )
            driver = webdriver.Chrome(executable_path=path_to_chromedriver)
            delay(0.5)
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
    driver.close()
    driver.quit()
    print("\nDone...\n'chromedriver.exe' is properly working.\n")