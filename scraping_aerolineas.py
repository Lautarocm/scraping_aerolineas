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
option = webdriver.ChromeOptions()

option.add_argument("window-size=1100,1080")
# option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")

service = Service(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=option)

url = "https://www.aerolineas.com.ar/"



cantidad_meses_disponibles = 0

precios = []



def abrir_pagina():
    driver.get(url)



def setear_tramo_ida():
    input_tramo_ida = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "radio-sbf-from")))
    input_tramo_ida.click()



def setear_aeropuertos(aeropuerto, input_id):
    input_aeropuerto = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, input_id)))
    input_aeropuerto.send_keys(aeropuerto)
    time.sleep(1)
    opciones_origen = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.TAG_NAME, "li")))
    for opcion in opciones_origen:
        if aeropuerto in opcion.text:
            opcion.click()
            break



def abrir_calendario():
    input_fecha = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "input-from-date-1")))
    input_fecha.click()



def setear_fecha():
    dias = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "DayPicker-Day")))
    for dia in dias:    #click en primer dia disponible del mes
            if dia.get_attribute("aria-disabled") == "false":
                dia.click()
                break



def click_buscar():
    button_buscar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "button-search-flights")))
    button_buscar.click()



def calcular_meses_disponibles():
    global cantidad_meses_disponibles

    input_fecha = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "input-from-date-1")))
    input_fecha.click()

    meses_contados = []

    mes = driver.find_element(By.CLASS_NAME, "DayPicker-Caption").text.split()[0]

    while mes not in meses_contados:
        meses_contados.append(mes)
        flecha_siguiente = driver.find_element(By.ID, "next-button")
        flecha_siguiente.click()
        mes = driver.find_element(By.CLASS_NAME, "DayPicker-Caption").text.split()[0]
    
    cantidad_meses_disponibles = len(meses_contados)
    print(meses_contados)



def reiniciar_calendario():
    i=0
    while i<cantidad_meses_disponibles: # vuelvo al primer mes
        driver.find_element(By.ID, "previous-button").click()
        i+=1



def obtener_precios():
    global precios
    try:
        ofertas = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, "fdc-available-day")))
        mes = driver.find_element(By.ID, "fdc-month").text
        anio = driver.find_element(By.ID, "header-title").text.split()[4]
        for oferta in ofertas:
            dia = oferta.find_element(By.ID, "fdc-button-day").text
            
            precio = int(oferta.find_element(By.ID, "fdc-button-price").text)
            obj_oferta = {
                "dia": dia,
                "mes": mes,
                "anio": anio,
                "precio": precio
            }
            precios.append(obj_oferta)
    except:
        print("nada")
        pass



def abrir_editar_busqueda():
    button_editar_busqueda = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "button-edit-search")))
    button_editar_busqueda.click()
    time.sleep(1)



def elegir_siguiente_mes():
    flecha_siguiente = driver.find_element(By.ID, "next-button")
    flecha_siguiente.click()



def buscar_resto_del_anio():
    i=1
    while i<cantidad_meses_disponibles:
        abrir_editar_busqueda()
        abrir_calendario()
        elegir_siguiente_mes()
        setear_fecha()
        click_buscar()
        obtener_precios()
        i+=1
        time.sleep(1)




def scraping_aerolineas(origen, destino):
    abrir_pagina()
    setear_tramo_ida()
    calcular_meses_disponibles()
    reiniciar_calendario()
    setear_aeropuertos(origen, "suggestion-input-sb-origin")
    setear_aeropuertos(destino, "suggestion-input-sb-destination")
    abrir_calendario()
    setear_fecha()
    click_buscar()
    obtener_precios()
    buscar_resto_del_anio()
    precios_ordenados = sorted(precios, key=lambda d: d['precio'])
    print(*precios_ordenados, sep = "\n")

scraping_aerolineas("BUE", "BCN")