from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def open_browser():
    brave_path = "/snap/bin/brave"
    chrome_options = Options()
    chrome_options.binary_location = brave_path
    chrome_options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.google.com/travel/flights")
    return driver

if __name__ == "__main__":
    driver = open_browser()
    # The browser is now open and navigated to the flights page
    # print(driver.title)