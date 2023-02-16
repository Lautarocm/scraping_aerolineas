from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
import time
from destinos import destinos_argentina_filtrados
from destinos import destinos_españa

# INICIALIZANCO WEBDRIVER
options = Options()

options.add_argument("window-size=1100,1080")
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
# option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")

service = Service(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)

url = "https://www.aerolineas.com.ar/"



input_origen_id = "suggestion-input-sb-origin"
input_destino_id = "suggestion-input-sb-destination"

cantidad_meses_disponibles = 0
aeropuerto_origen = "BUE"
aeropuerto_destino = ""
ciudad = ""
iteracion = 0
precios = []


ignored_exceptions=(NoSuchElementException, StaleElementReferenceException)


def abrir_pagina():
    driver.get(url)



def setear_tramo_ida():
    input_tramo_ida = WebDriverWait(driver, 60, ignored_exceptions=ignored_exceptions).until(EC.element_to_be_clickable((By.ID, "radio-sbf-from")))
    input_tramo_ida.click()



def setear_aeropuertos():
    input_origen = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, input_origen_id)))
    input_destino = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, input_destino_id)))    

    if input_origen.get_attribute("value") == "":
        input_origen.send_keys(aeropuerto_origen)
        lista_opciones = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "react-autosuggest__suggestions-list")))
        opciones = WebDriverWait(lista_opciones, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "react-autosuggest__suggestion")))
        for opcion in opciones:
            if aeropuerto_origen in opcion.text:
                opcion.click()
                break
    
    if input_destino.get_attribute("value") == "":
        input_destino.send_keys(aeropuerto_destino)
        lista_opciones = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "react-autosuggest__suggestions-list")))
        opciones = WebDriverWait(lista_opciones, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "react-autosuggest__suggestion")))
        for opcion in opciones:
            if aeropuerto_destino in opcion.text:
                opcion.click()
                break



def abrir_calendario():
    try:
        input_fecha = WebDriverWait(driver, 5, ignored_exceptions=ignored_exceptions).until(EC.element_to_be_clickable((By.ID, "input-from-date-1")))
        input_fecha.click()
    except:
        input_fecha = WebDriverWait(driver, 5, ignored_exceptions=ignored_exceptions).until(EC.element_to_be_clickable((By.ID, "input-from-date-1")))
        input_fecha.click()


def setear_fecha():
    calendario = WebDriverWait(driver, 5, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.CLASS_NAME, "DayPicker")))
    dias = WebDriverWait(calendario, 5, ignored_exceptions=ignored_exceptions).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "DayPicker-Day")))
    for dia in dias:    #click en primer dia disponible del mes
            if dia.get_attribute("aria-disabled") == "false":
                dia.click()
                break
    


def click_buscar():
    button_buscar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "button-search-flights")))
    button_buscar.click()



def calcular_meses_disponibles():
    global cantidad_meses_disponibles

    input_fecha = WebDriverWait(driver, 5, ignored_exceptions=ignored_exceptions).until(EC.element_to_be_clickable((By.ID, "input-from-date-1")))
    input_fecha.click()

    meses_contados = []

    mes = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "DayPicker-Caption"))).text.split()[0]

    while mes not in meses_contados:
        meses_contados.append(mes)

        flecha_siguiente = WebDriverWait(driver, 5, ignored_exceptions=ignored_exceptions).until(EC.element_to_be_clickable((By.ID, "next-button")))
        flecha_siguiente.click()
        mes = WebDriverWait(driver, 5, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.CLASS_NAME, "DayPicker-Caption"))).text.split()[0]
    
    cantidad_meses_disponibles = len(meses_contados)



def reiniciar_calendario():
    i=0
    while i<cantidad_meses_disponibles: # vuelvo al primer mes
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "previous-button"))).click()
        i+=1



def esperar_data():
    try:
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME, "ResultsLoader__ResultsLoaderWrapper-abrvrg-0")))
        WebDriverWait(driver,60).until_not(EC.presence_of_element_located((By.CLASS_NAME, "ResultsLoader__ResultsLoaderWrapper-abrvrg-0")))
    except:
        pass



def detectar_pagina_oops():
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "oops-title")))
    boton_inicio = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "button-oops-back")))
    boton_inicio.click()
    buscar_despues_de_pagina_oops()



def buscar_despues_de_pagina_oops():
    global iteracion

    iteracion += 1
    setear_tramo_ida()
    setear_aeropuertos()
    abrir_calendario()
    for i in range(iteracion):
        elegir_siguiente_mes()
    setear_fecha()
    time.sleep(1)
    click_buscar()
    esperar_data()
    obtener_precios()
    while iteracion < len(cantidad_meses_disponibles):
        break




def obtener_precios():
    global precios
    global iteracion

    try:
        WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.ID, "fdc-from-box"))) #esperar que aparezca el calendario con precios
        ofertas = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.ID, "fdc-available-day")))
        mes = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "fdc-month"))).text
        anio = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "header-title"))).text.split()[4]
        for oferta in ofertas:
            dia = oferta.find_element(By.ID, "fdc-button-day").text
            precio = int(oferta.find_element(By.ID, "fdc-button-price").text)
            dict_oferta = {
                "dia": dia,
                "mes": mes,
                "anio": anio,
                "destino": ciudad,
                "precio": precio
            }
            precios.append(dict_oferta)
            iteracion += 1
    except:
        try:
            WebDriverWait(driver, 0.5).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "styled__UnavailableFlightDateErrorContainer-sc-1sduzq6-3"), "No tenemos vuelos disponibles"))
            print("no hay vuelos")
        except:
            detectar_pagina_oops()



def abrir_editar_busqueda():
    try:
        button_editar_busqueda = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "button-edit-search")))
        button_editar_busqueda.click()
    except:
        pass



def elegir_siguiente_mes():
    WebDriverWait(driver, 5, ignored_exceptions=ignored_exceptions).until(EC.element_to_be_clickable((By.ID, "next-button"))).click()



def buscar_meses_siguientes():
    i=1
    while i<cantidad_meses_disponibles:
        abrir_editar_busqueda()
        setear_tramo_ida()
        setear_aeropuertos()
        abrir_calendario()
        elegir_siguiente_mes()
        setear_fecha()
        click_buscar()
        esperar_data()
        obtener_precios()
        i+=1
    


def mostrar_resultados():
    precios_ordenados = sorted(precios, key=lambda d: d['precio'])
    print(*precios_ordenados, sep = "\n")



def guardar_vuelos():
    precios_ordenados = sorted(precios, key=lambda d: d['precio'])
    vuelos = open("vuelos.txt", 'w')
    vuelos.write(str(precios_ordenados).replace("}, ", "}\n").replace("[", "").replace("]", "").replace("{", "").replace("}", "").replace("'", ""))



def scraping_aerolineas():
    abrir_pagina()
    setear_tramo_ida()
    calcular_meses_disponibles()
    reiniciar_calendario()
    setear_aeropuertos()
    abrir_calendario()
    setear_fecha()
    click_buscar()
    esperar_data()
    obtener_precios()
    buscar_meses_siguientes()



for destino in destinos_españa:
    aeropuerto_destino = destino["codigo"]
    ciudad = destino["ciudad"]
    scraping_aerolineas()

# scraping_aerolineas()

guardar_vuelos()