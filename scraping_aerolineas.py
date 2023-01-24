from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from bs4 import BeautifulSoup

# INICIALIZANCO WEBDRIVER
service = Service(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service)

url = "https://www.aerolineas.com.ar/"



cantidad_meses_disponibles = 1
precios = []



def abrir_pagina():
    driver.get(url)



def setear_tramo_ida():
    input_tramo_ida = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "radio-sbf-from")))
    input_tramo_ida.click()



def setear_aeropuertos(aeropuerto, input_id):
    input_aeropuerto = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, input_id)))
    input_aeropuerto.send_keys(aeropuerto)
    time.sleep(2)
    opciones_origen = driver.find_elements(By.TAG_NAME, "li")
    for opcion in opciones_origen:
        if aeropuerto in opcion.text:
            opcion.click()
            break



def setear_fecha():
    input_fecha = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "input-from-date-1")))
    input_fecha.click()
    date_picker = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "DayPicker-Body")))
    dias = date_picker.find_elements(By.CLASS_NAME, "DayPicker-Day")
    for dia in dias:    #click en primer dia disponible del mes
            if dia.get_attribute("aria-disabled") == "false":
                dia.click()
                break
    time.sleep(3)



def click_buscar():
    button_buscar = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "button-search-flights")))
    button_buscar.click()



def calcular_meses_disponibles():
    global cantidad_meses_disponibles

    input_fecha = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "input-from-date-1")))
    input_fecha.click()

    mes = driver.find_element(By.CLASS_NAME, "DayPicker-Caption").text.split()[0]

    while mes != "DICIEMBRE":
        flecha_siguiente = driver.find_element(By.ID, "next-button")
        flecha_siguiente.click()
        mes = driver.find_element(By.CLASS_NAME, "DayPicker-Caption").text.split()[0]
        time.sleep(0.5)
        cantidad_meses_disponibles += 1



def reiniciar_calendario():
    i=0
    while i<cantidad_meses_disponibles: # vuelvo al primer mes
        driver.find_element(By.ID, "previous-button").click()
        i+=1



def obtener_precios():
    global precios

    ofertas = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.ID, "fdc-available-day"))) 

    for oferta in ofertas:
        precios.append(int(oferta.find_element(By.ID, "fdc-button-price").text))



def abrir_editar_busqueda():
    button_editar_busqueda = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "button-edit-search")))
    button_editar_busqueda.click()



def scraping_aerolineas(origen, destino):
    abrir_pagina()
    setear_tramo_ida()
    calcular_meses_disponibles()
    reiniciar_calendario()
    setear_aeropuertos(origen, "suggestion-input-sb-origin")
    setear_aeropuertos(destino, "suggestion-input-sb-destination")
    setear_fecha()
    click_buscar()
    obtener_precios()
    abrir_editar_busqueda()
    print(precios)

scraping_aerolineas("BUE", "BRC")