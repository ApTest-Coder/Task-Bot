import shutil
import tempfile
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


def start_browser():
    profile = Path(tempfile.mkdtemp(prefix="taskbot-firefox-"))
    options = Options()
    options.profile = str(profile)
    if HEADLESS:
        options.add_argument("-headless")
    if FIREFOX_BINARY:
        options.binary_location = FIREFOX_BINARY
    service = Service(executable_path=GECKODRIVER_PATH) if GECKODRIVER_PATH else Service()
    driver = webdriver.Firefox(service=service, options=options)
    if UBLOCK_XPI:
        driver.install_addon(UBLOCK_XPI, temporary=True)
    return driver, profile


def stop_browser(driver, profile):
    try:
        driver.quit()
    finally:
        shutil.rmtree(profile, ignore_errors=True)


from config import FIREFOX_BINARY, GECKODRIVER_PATH, HEADLESS, UBLOCK_XPI
