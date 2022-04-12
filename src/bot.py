import notify2

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from requests import get
from os.path import abspath
from time import sleep
from playsound import playsound

url = "http://www.isere.gouv.fr/booking/create/23012/0"
url_reject = "http://www.isere.gouv.fr/booking/create/23012/2"

notification = notify2.Notification("Summary111",
                "Some body text111",
            #  "notification-message-im"   # Icon name
            )
notification.set_urgency(notify2.URGENCY_CRITICAL)

notification_reject = notify2.Notification("Summary",
                "Some body text",
            #  "notification-message-im"   # Icon name
            )

class Requestxception(Exception):
    pass

def assert_error(driver):
    if "502 Bad Gateway" in driver.page_source:
        driver.get(url)
        raise Requestxception

def open_browser():
    notify2.init("Titre de Séjour Bot")
    driver = webdriver.Firefox(executable_path=abspath("geckodriver"))
    driver.get(url)
    assert_error(driver)
    driver.execute_script("javascript:accepter()")
    while True:
        sleep(600)
        try:
            assert_error(driver)
        except Requestxception:
            driver.refresh()
            continue
        driver.find_element_by_id('condition').click()
        driver.find_element_by_name('nextButton').click()
        try:
            assert_error(driver)
        except Requestxception:
            driver.refresh()
            continue
        if driver.current_url == url_reject:
            # notification_reject.show()
            driver.find_element_by_name('finishButton').click()
        else:
            notification.show()
            break
    playsound(abspath("silent_hill_siren.mp3"))
    # driver.quit()

def main():
    print(open_browser())

if __name__ == "__main__":
    main()
