from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# INICIALIZANCO WEBDRIVER
option = webdriver.ChromeOptions()

option.add_argument("window-size=1100,1080")
# option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")

service = Service(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=option)

url = "https://www.aerolineas.com.ar/"


# destinos_argentina = [
#     {"lugar": "San Martín de los Andes" , "codigo": "CPC"},
#     {"lugar": "Bahía Blanca" , "codigo": "BHI"},
#     {"lugar": "Bariloche" , "codigo": "BRC"},
#     {"lugar": "Calafate" , "codigo": "FTE"},
#     {"lugar": "Catamarca" , "codigo": "CTC"},
#     {"lugar": "Comodoro Rivadavia" , "codigo": "CRD"},
#     {"lugar": "Corrientes" , "codigo": "CNQ"},
#     {"lugar": "Rio Cuarto" , "codigo": "RCU"},
#     {"lugar": "Córdoba" , "codigo": "COR"},
#     {"lugar": "Santiago del Estero" , "codigo": "SDE"},
#     {"lugar": "Mar del Plata" , "codigo": "MDQ"},
#     {"lugar": "Esquel" , "codigo": "EQS"},
#     {"lugar": "Santa fe" , "codigo": "SFN"},
#     {"lugar": "Formosa" , "codigo": "FMA"},
#     {"lugar": "Rio Gallegos" , "codigo": "RGL"},
#     {"lugar": "Villa Gesell" , "codigo": "VLG"},
#     {"lugar": "Rio Grande" , "codigo": "RGA"},
#     {"lugar": "Rio Hondo" , "codigo": "RHD"},
#     {"lugar": "Puerto Iguazú" , "codigo": "IGR"},
#     {"lugar": "San Juan" , "codigo": "UAQ"},
#     {"lugar": "Jujuy" , "codigo": "JUJ"},
#     {"lugar": "La Rioja" , "codigo": "IRJ"},
#     {"lugar": "San Luis" , "codigo": "LUQ"},
#     {"lugar": "Puerto Madryn" , "codigo": "PMY"},
#     {"lugar": "Malargue" , "codigo": "LGS"},
#     {"lugar": "Mendoza" , "codigo": "MDZ"},
#     {"lugar": "Villa Mercedes" , "codigo": "VME"},
#     {"lugar": "Merlo" , "codigo": "RLO"},
#     {"lugar": "Neuquén" , "codigo": "NQN"},
#     {"lugar": "Paraná" , "codigo": "PRA"},
#     {"lugar": "Posadas" , "codigo": "PSS"},
#     {"lugar": "San Rafael" , "codigo": "AFA"},
#     {"lugar": "Resistencia" , "codigo": "RES"},
#     {"lugar": "Santa Rosa" , "codigo": "RSA"},
#     {"lugar": "Rosario" , "codigo": "ROS"},
#     {"lugar": "Salta" , "codigo": "SLA"},
#     {"lugar": "Trelew" , "codigo": "REL"},
#     {"lugar": "Tucumán" , "codigo": "TUC"},
#     {"lugar": "Ushuaia" , "codigo": "USH"},
#     {"lugar": "Viedma" , "codigo": "VDM"}
#     ]

destinos_argentina = [
    {"lugar": "San Martín de los Andes" , "codigo": "CPC"},
    {"lugar": "Bariloche" , "codigo": "BRC"},
    {"lugar": "Calafate" , "codigo": "FTE"},
    {"lugar": "Cordoba" , "codigo": "COR"},
    {"lugar": "Esquel" , "codigo": "EQS"},
    {"lugar": "Rio Gallegos" , "codigo": "RGL"},
    {"lugar": "Rio Grande" , "codigo": "RGA"},
    {"lugar": "Rio Hondo" , "codigo": "RHD"},
    {"lugar": "Puerto Iguazu" , "codigo": "IGR"},
    {"lugar": "Puerto Madryn" , "codigo": "PMY"},
    {"lugar": "Malargue" , "codigo": "LGS"},
    {"lugar": "Mendoza" , "codigo": "MDZ"},
    {"lugar": "Neuquen" , "codigo": "NQN"},
    {"lugar": "Posadas" , "codigo": "PSS"},
    {"lugar": "San Rafael" , "codigo": "AFA"},
    {"lugar": "Trelew" , "codigo": "REL"},
    {"lugar": "Ushuaia" , "codigo": "USH"},
    {"lugar": "Viedma" , "codigo": "VDM"}
    ]

destinos_españa = [
    {"lugar": "Alicante", "codigo": "ALC"},
    {"lugar": "Asturias", "codigo": "OVD"},
    {"lugar": "Barcelona", "codigo": "BCN"},
    {"lugar": "Bilbao", "codigo": "BIO"},
    {"lugar": "Canarias", "codigo": "LPA"},
    {"lugar": "Coruna", "codigo": "LCG"},
    {"lugar": "Mallorca", "codigo": "PMI"},
    {"lugar": "Fuerteventura", "codigo": "FUE"},
    {"lugar": "Ibiza", "codigo": "IBZ"},
    {"lugar": "Lanzarote", "codigo": "ACE"},
    {"lugar": "Madrid", "codigo": "MAD"},
    {"lugar": "Mahon", "codigo": "MAH"},
    {"lugar": "Malaga", "codigo": "AGP"},
    {"lugar": "Sevilla", "codigo": "SVQ"},
    {"lugar": "Tenerife sur", "codigo": "TFS"},
    {"lugar": "Tenerife 2", "codigo": "TFN"},
    {"lugar": "Tenerife 3", "codigo": "TCI"},
    {"lugar": "Valencia", "codigo": "VLC"},
    {"lugar": "Vigo", "codigo": "VGO"}
]

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
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "react-autosuggest__suggestions-list")))
    opciones_origen = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.TAG_NAME, "li")))
    for opcion in opciones_origen:
        if aeropuerto in opcion.text:
            opcion.click()
            break



def abrir_calendario():
    input_fecha = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "input-from-date-1")))
    input_fecha.click()



def setear_fecha():
    calendario = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "DayPicker")))
    dias = WebDriverWait(calendario, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "DayPicker-Day")))
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

    mes = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "DayPicker-Caption"))).text.split()[0]

    while mes not in meses_contados:
        meses_contados.append(mes)

        flecha_siguiente = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "next-button")))
        flecha_siguiente.click()
        mes = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "DayPicker-Caption"))).text.split()[0]
    
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



def obtener_precios(destino):
    global precios

    try:
        WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.ID, "fdc-from-box")))
        ofertas = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.ID, "fdc-available-day")))
        mes = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "fdc-month"))).text
        anio = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "header-title"))).text.split()[4]
        for oferta in ofertas:
            dia = oferta.find_element(By.ID, "fdc-button-day").text
            
            precio = int(oferta.find_element(By.ID, "fdc-button-price").text)
            obj_oferta = {
                "dia": dia,
                "mes": mes,
                "anio": anio,
                "destino": destino,
                "precio": precio
            }
            precios.append(obj_oferta)
    except:
        WebDriverWait(driver, 0.5).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "styled__UnavailableFlightDateErrorContainer-sc-1sduzq6-3"), "No tenemos vuelos disponibles"))
        print("no hay vuelos")



def abrir_editar_busqueda():
    try:
        button_editar_busqueda = WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.ID, "button-edit-search")))
        button_editar_busqueda.click()
    except:
        pass



def elegir_siguiente_mes():
    flecha_siguiente = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "next-button")))
    flecha_siguiente.click()



def buscar_resto_del_anio(destino):
    i=1
    while i<cantidad_meses_disponibles:
        abrir_editar_busqueda()
        setear_tramo_ida()
        abrir_calendario()
        elegir_siguiente_mes()
        setear_fecha()
        click_buscar()
        esperar_data()
        obtener_precios(destino)
        i+=1
    
    



def mostrar_resultados():
    precios_ordenados = sorted(precios, key=lambda d: d['precio'])
    print(*precios_ordenados, sep = "\n")



def guardar_vuelos():
    precios_ordenados = sorted(precios, key=lambda d: d['precio'])
    vuelos = open("vuelos", 'w')
    vuelos.write(str(precios_ordenados))



def scraping_aerolineas(aeropuerto_origen, aeropuerto_destino, destino):
    abrir_pagina()
    setear_tramo_ida()
    if cantidad_meses_disponibles == 0:
        calcular_meses_disponibles()
        reiniciar_calendario()
    setear_aeropuertos(aeropuerto_origen, "suggestion-input-sb-origin")
    setear_aeropuertos(aeropuerto_destino, "suggestion-input-sb-destination")
    abrir_calendario()
    setear_fecha()
    click_buscar()
    esperar_data()
    obtener_precios(destino)
    buscar_resto_del_anio(destino)

for destino in destinos_españa:
    scraping_aerolineas("BUE", destino["codigo"], destino["lugar"])

# scraping_aerolineas("BUE", "IGR", "Iguazu")

guardar_vuelos()