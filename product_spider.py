from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def fetch_option_value(url):
    driver = webdriver.Chrome()
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.swatchanchor')))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        swatchanchors = soup.select('.swatchanchor')
        for swatchanchor in swatchanchors:
            swatchanchor.click()
            variation_select = driver.find_element_by_css_selector('.variation-select')
            if variation_select:
                print(variation_select.text) 
            else:
                print("Variation select element not found!")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        driver.quit()

url = "https://www.bcf.com.au/p/daiwa-23-td-black-spinning-rod/M675158.html"
fetch_option_value(url)
