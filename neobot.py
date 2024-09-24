import os
import ssl
import tempfile

import whisper
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

CAPTCHA_COUNT = 10
FETCH_INTERVAL = 30
CAPTCHA_IMAGE_ID = "captchaFR_CaptchaImage"
CPATCHA_AUDIO_ID = "BDC_CaptchaSoundAudio_captchaFR"
CPATCHA_AUDIO_BUTTON_ID = "captchaFR_SoundLink"
CPATCHA_TEMP_PATH = os.path.join(tempfile.gettempdir(), "captchaFR")
WHISPER_MODEL = "medium"
URL = (
    "https://www.rdv-prefecture.interieur.gouv.fr/rdvpref/reservation/demarche/3762/cgu"
)


def get_captcha_image(driver):
    return WebDriverWait(driver, 10).until(
        expected_conditions.visibility_of_element_located((By.ID, CAPTCHA_IMAGE_ID))
    )


def get_audio_blob_uri(driver):
    audio_button = WebDriverWait(driver, 10).until(
        expected_conditions.visibility_of_element_located(
            (By.ID, CPATCHA_AUDIO_BUTTON_ID)
        )
    )
    audio_button.click()
    return (
        WebDriverWait(driver, 10)
        .until(
            expected_conditions.presence_of_element_located((By.ID, CPATCHA_AUDIO_ID))
        )
        .get_attribute("src")
    )


def transcribe_audio_file(model, audio_filepath):
    result = model.transcribe(audio_filepath, language="fr")
    text = result["text"]
    text = (
        text.replace(" ", "")
        .replace("–", "")
        .replace("-", "")
        .replace(",", "")
        .replace(".", "")
        .upper()
    )
    return text


def main():
    # Monkypatch to bypass Self-signed SSL certificate crap problems in enterprise
    ssl._create_default_https_context = ssl._create_unverified_context

    # Create data path
    datapath = os.path.abspath("data")
    os.makedirs(datapath, exist_ok=True)
    os.makedirs(CPATCHA_TEMP_PATH, exist_ok=True)

    # Load Whisper model
    model = whisper.load_model(WHISPER_MODEL)

    # Setup a Firefox web driver
    options = Options()
    options.add_argument("--headless")
    options.set_preference("media.volume_scale", "0.0")
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", CPATCHA_TEMP_PATH)
    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(FETCH_INTERVAL)

    # Retrieve Cpatcha images
    for _ in range(CAPTCHA_COUNT):
        try:
            driver.get(URL)
            image_element = get_captcha_image(driver)
            image = image_element.screenshot_as_png

        except WebDriverException as _:
            print(
                "Failed to retrieve captcha image. Retrying in {} seconds...".format(
                    FETCH_INTERVAL
                )
            )

        # A hack for saving the sound files
        try:
            # The get call will block for FETCH_INTERVAL seconds, effectively casusing
            # the equivalent of sleep(FETCH_INTERVAL)
            audio_blob_uri = get_audio_blob_uri(driver)
            driver.get(audio_blob_uri)
        except WebDriverException as _:
            pass
        for file in os.listdir(CPATCHA_TEMP_PATH):
            if file.endswith(".wav"):
                filepath = os.path.join(CPATCHA_TEMP_PATH, file)
                text = transcribe_audio_file(model, filepath)
                os.remove(filepath)
                with open(
                    os.path.join(datapath, "{}.png".format(text)), "wb"
                ) as image_file:
                    image_file.write(image)

    # Clean up
    driver.quit()


main()
