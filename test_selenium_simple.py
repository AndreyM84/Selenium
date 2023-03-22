from selenium import webdriver
from selenium.webdriver.common.by import By

# driver = webdriver.Chrome(executable_path="C:\\Users\\User\\PycharmProjects\\pythonProject\\Selenium\\chromedriver.exe")

driver = webdriver.Chrome(executable_path="C:/Users/User/PycharmProjects/pythonProject/Selenium/chromedriver.exe")

import time


def test_search_example(selenium):
    """ Search some phrase in google and make a screenshot of the page. """

    # Open google search page:
    selenium.get('https://google.com')

    time.sleep(5)  # just for demo purposes, do NOT repeat it on real projects!

    # Find the field for search text input:
    search_input = selenium.find_element(By.NAME, "q")

    # Enter the text for search:
    search_input.clear()
    search_input.send_keys('my first selenium test for Web UI!')

    time.sleep(5)  # just for demo purposes, do NOT repeat it on real projects!

    # Click Search:
    search_button = selenium.find_element(By.NAME, 'btnK')
    search_button.click()

    time.sleep(5)  # just for demo purposes, do NOT repeat it on real projects!

    # Make the screenshot of browser window:
    selenium.save_screenshot('result.png')
