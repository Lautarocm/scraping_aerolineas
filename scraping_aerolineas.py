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



precios = []



def abrir_pagina():
    driver.get(url)



def realizar_busqueda(origen, destino):
    primer_dia_disponible = None

    input_tramo_ida = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "radio-sbf-from")))
    input_origen = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "suggestion-input-sb-origin")))
    input_destino = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "suggestion-input-sb-destination")))
    button_buscar = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "button-search-flights")))

    input_tramo_ida.click()

    input_origen.send_keys(origen)

    time.sleep(2)

    opciones_origen = driver.find_elements(By.TAG_NAME, "li")

    for opcion in opciones_origen:
        if origen in opcion.text:
            opcion.click()
            break
    
    input_destino.send_keys(destino)

    time.sleep(2)

    opciones_destino = driver.find_elements(By.TAG_NAME, "li")

    for opcion in opciones_destino:
        if destino in opcion.text:
            opcion.click()
            break
    
    input_fecha = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "input-from-date-1")))
    input_fecha.click()

    date_picker = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "DayPicker-Body")))
    dias = date_picker.find_elements(By.CLASS_NAME, "DayPicker-Day")
    
    for dia in dias:    #obtengo dias disponibles
        if dia.get_attribute("aria-disabled") == "false":
            primer_dia_disponible = dia
            break

    primer_dia_disponible.click()

    time.sleep(3)

    button_buscar.click()

    

def obtener_precios():
    global precios

    ofertas = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.ID, "fdc-available-day"))) 

    for oferta in ofertas:
        precios.append(int(oferta.find_element(By.ID, "fdc-button-price").text))



def scraping_aerolineas(origen, destino):
    abrir_pagina()
    realizar_busqueda(origen, destino)
    obtener_precios()
    print(precios)

scraping_aerolineas("BUE", "BRC")