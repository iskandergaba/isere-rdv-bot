from os.path import abspath
from time import sleep

from playsound import playsound
from selenium import webdriver

url = "http://www.isere.gouv.fr/booking/create/23012/0"
url_reject = "http://www.isere.gouv.fr/booking/create/23012/2"


class Requestxception(Exception):
    pass


def assert_error(driver):
    if "502 Bad Gateway" in driver.page_source:
        driver.get(url)
        raise Requestxception


def open_browser():
    print("Titre de Séjour Bot")
    driver = webdriver.Firefox()
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
        driver.find_element_by_id("condition").click()
        driver.find_element_by_name("nextButton").click()
        try:
            assert_error(driver)
        except Requestxception:
            driver.refresh()
            continue
        if driver.current_url == url_reject:
            driver.find_element_by_name("finishButton").click()
        else:
            break
    playsound(abspath("silent_hill_siren.mp3"))
    driver.quit()


def main():
    open_browser()


if __name__ == "__main__":
    main()
