from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
import time


def close_modal(driver: ChromeDriver) -> None:
    close_button = driver.find_element(By.XPATH, """// *[ @ id = "PromoteSignUpPopUp"] / div[2] / i""")
    close_button.click()


def extract_table_html(driver: ChromeDriver) -> str:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table_element = soup.find('table', {'id': 'eventHistoryTable733'})
    table_html = str(table_element)
    return table_html


def click_show_more_button_multiple_times(url: str, output_filename: str, num_clicks: int) -> None:
    driver = webdriver.Chrome()
    driver.get(url)
    for _ in range(num_clicks):
        try:
            show_more_button = driver.find_element(By.ID, "showMoreHistory733")
            show_more_button.click()

            time.sleep(2)
        except:
            close_modal(driver)
            time.sleep(2)

    table_html = extract_table_html(driver)

    with open(output_filename, 'w', encoding='utf-8') as html_file:
        html_file.write(table_html)
    driver.quit()


url = "https://ru.investing.com/economic-calendar/cpi-733"
output_filename = "output.html"
num_clicks = 60


click_show_more_button_multiple_times(url=url, output_filename=output_filename, num_clicks=num_clicks)
