from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup


service = Service(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service)

url = "https://www.aerolineas.com.ar/"

driver.get(url)

def get_search_inputs():
    available_days = []
    input_tramo_ida = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "radio-sbf-from")))
    input_origen = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "suggestion-input-sb-origin")))
    input_destino = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "suggestion-input-sb-destination")))
    time.sleep(3)
    input_tramo_ida.click()
    time.sleep(3)
    input_fecha = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "input-from-date-1")))

    input_fecha.click()
    date_picker = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "DayPicker-Body")))
    days = date_picker.find_elements(By.CLASS_NAME, "DayPicker-Day")
    
    for day in days:    #obtengo dias disponibles
        if day.get_attribute("aria-disabled") == "false":
            available_days.append(day)

    time.sleep(3)

get_search_inputs()