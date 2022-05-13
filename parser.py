from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from urllib import response
import requests


url = 'https://applicant.21-school.ru/api/v3/signin'

meeting_url = 'https://applicant.21-school.ru/meet'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0'
}

data = {
    'api_user': {
        'email': 'xyamix1337@gmail.com',
        'password': 'Markertron21!'
    }
}


def get_meetings():
    meetings = []
    session = requests.Session()
    session.headers.update(headers)
    resp = session.post(url, json=data)

    if resp.status_code == 200:
        Auth_Cookie = resp.json()['Authorization']
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(5)
        driver.get(meeting_url)
        driver.add_cookie({'name': 'Authorization', 'value': Auth_Cookie})
        try:
            driver.get(meeting_url)
        except TimeoutException:
            driver.execute_script("window.stop();")
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'main-default-button cookie')]")))
        cookie_button.click()
        elements = driver.find_elements(by=By.CLASS_NAME, value='table__item')
        for element in elements:
            meeting = {}
            info = element.find_elements(
                by=By.CLASS_NAME, value='item__column')
            for index, information in enumerate(info):
                if index == 0:
                    meeting['date'] = information.text
                elif index == 1:
                    meeting['places'] = information.text
            meetings.append(meeting)
        driver.close()
    return meetings
