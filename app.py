from flask import Flask, jsonify, request
from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
#from webdriver_manager.chrome import ChromeDriverManager
import math
import time

app = Flask(__name__)


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=chrome_options)





def getData(rut):
    time.sleep(1)

    #busqueda facturas de compra/venta

    driver.get("https://www4.sii.cl/consdcvinternetui/#/index")

    #configurar el seelct del mes
    select_mes = driver.find_element(By.ID,"periodoMes")

    time.sleep(1)
    select1 = Select(select_mes)
    #select1.select_by_value("11")

    #select del anio
    select_anio = driver.find_element(By.XPATH,'//*[@id="my-wrapper"]/div[2]/div[1]/div[1]/div/div[1]/div/div[3]/div/form/div[2]/select[2]')
    time.sleep(1)
    select2 = Select(select_anio)

    #select del rut
    select_rut = driver.find_element(By.XPATH,'//*[@id="my-wrapper"]/div[2]/div[1]/div[1]/div/div[1]/div/div[3]/div/form/div[1]/select')

    #select2.select_by_value("2023")
    btn_siguiente = driver.find_element(By.XPATH,'//*[@id="my-wrapper"]/div[2]/div[1]/div[1]/div/div[1]/div/div[3]/div/form/div[3]/button')


    btn_seccion_venta = driver.find_element(By.CSS_SELECTOR,'a[ui-sref="venta"]')

    btn_seccion_compra = driver.find_element(By.CSS_SELECTOR,'a[ui-sref="compra"]')

    #Periodos de tiempo buscados
    periodos = [{"anio":"2023","mes":"11"},{"anio":"2023","mes":"12"},{"anio":"2024","mes":"01"}]

    total_facturas_de_venta = 0
    total_facturas_de_compra = 0

    for periodo in periodos:
        #

        time.sleep(1)
        select_rut.send_keys(rut)
        time.sleep(1)
        select1.select_by_value(periodo["mes"])
        time.sleep(1)
        select2.select_by_value(periodo["anio"])

        btn_siguiente.click()
        time.sleep(1)

        try:
            table_body = driver.find_element(By.XPATH,'//*[@id="home"]/table/tbody[2]')
            time.sleep(1)
            rows = table_body.find_elements(By.CSS_SELECTOR,'tr.ng-scope')
            #print('mes ' + periodo["mes"])
            cantidad = 0
            for row in rows:
                #print('fila')
                tipo = row.find_element(By.CSS_SELECTOR,'td[scope="row"]').text
                cols = row.find_elements(By.CSS_SELECTOR,'td.ng-binding')
                col = cols[0].text
                valor = int(col)
                if "(39)" in tipo or "(48)" in tipo or "(35)" in tipo or "(38)" in tipo or "(41)" in tipo:
                    #print("no hay que sumarlo")
                    #cantidad = cantidad
                    pass
                else:
                    cantidad = cantidad + valor

                #cantidad = cantidad + valor
                print({"tipo":tipo,"valor":col,"mes":periodo["mes"],"anio":periodo["anio"]})

            #
            print(f"canntidad final facturas de compra: {cantidad}")
            #print(cantidad)
            periodo["facturas_de_compra"] = cantidad
            total_facturas_de_compra = total_facturas_de_compra + cantidad

        except NoSuchElementException:
            print('no hay nada en facturas de compra')
            periodo["facturas_de_compra"] = 0


        btn_seccion_venta.click()
        time.sleep(3)
        #accion de venta
        try:
            #
            table_body = driver.find_element(By.XPATH,'//*[@id="home"]/table/tbody[2]')
            time.sleep(3)
            rows = table_body.find_elements(By.CSS_SELECTOR,'tr.ng-scope')
            print('mes '+periodo["mes"])
            cantidad = 0
            for row in rows:
                #print('fila')
                tipo = row.find_element(By.CSS_SELECTOR,'td[scope="row"]').text
                cols = row.find_elements(By.CSS_SELECTOR,'td.ng-binding')
                col = cols[0].text
                valor = int(col)
                if "(39)" in tipo or "(48)" in tipo or "(35)" in tipo or "(38)" in tipo or "(41)" in tipo:
                    #print("no hay que sumarlo")
                    #cantidad = cantidad
                    pass
                else:
                    cantidad = cantidad + valor
                #cantidad = cantidad + valor
                print({"tipo":tipo,"valor":col,"mes":periodo["mes"],"anio":periodo["anio"]})

            #print('canntidad final facturas de venta')
            #print(cantidad)
            #resultados.append({"facturasVenta":cantidad})
            print(f"canntidad final facturas de venta: {cantidad}")
            periodo["facturas_de_venta"] = cantidad
            total_facturas_de_venta = total_facturas_de_venta + cantidad


        except NoSuchElementException:
            print('no hay nada en facturas de venta')
            periodo["facturas_de_venta"] = 0

        time.sleep(1)
        btn_seccion_compra.click()



    #print(periodos)


    promedio_facturas_de_compra = total_facturas_de_compra/3
    promedio_facturas_de_compra_redondeado = math.ceil(promedio_facturas_de_compra)
    print(promedio_facturas_de_compra)

    promedio_facturas_de_venta = total_facturas_de_venta/3
    promedio_facturas_de_venta_redondeado = math.ceil(promedio_facturas_de_venta)
    print(promedio_facturas_de_venta)

    """
    print(f"facturas de compra: {total_facturas_de_compra}")
    print(f"promedio facturas de compra: {promedio_facturas_de_compra} / redondeado {promedio_facturas_de_compra_redondeado}")

    print(f"facturas de venta: {total_facturas_de_venta}")
    print(f"promedio facturas de venta: {promedio_facturas_de_venta} / redondeado {promedio_facturas_de_venta_redondeado}")
    """

    time.sleep(1)


    #logica para recopilar

    #Boletas de Honorarios Electrónicas recibidas(INFORMES DE BOLETAS RECIBIDAS)
    driver.get("https://loa.sii.cl/cgi_IMT/TMBCOC_MenuConsultasContribRec.cgi?dummy=1461943244650")
    select_anio = driver.find_element(By.XPATH,'/html/body/div[2]/center/table[3]/tbody/tr[2]/td[2]/div/font/select')
    time.sleep(1)
    select = Select(select_anio)
    select.select_by_value("2023")
    btn = driver.find_element(By.ID,'cmdconsultar124')
    time.sleep(1)
    btn.click()
    promedio_boletas_anuales_recibidas = 0
    promedio_boletas_anuales_recibidas_redondeado = 0
    try:
        boletas_anuales_txt = driver.find_element(By.XPATH,'/html/body/div[3]/center/table[2]/tbody/tr[6]/td/table/tbody/tr[15]/td[2]/font').text
        boletas_anuales = int(boletas_anuales_txt)
        promedio_boletas_anuales_recibidas = boletas_anuales/12
        promedio_boletas_anuales_recibidas_redondeado = math.ceil(promedio_boletas_anuales_recibidas)


    except NoSuchElementException:
        print('no hay')


    driver.get("https://zeus.sii.cl/cvc_cgi/bte/bte_indiv_cons?1")

    select_anio = driver.find_element(By.ID,'ANOA')
    time.sleep(1)
    select = Select(select_anio)
    select.select_by_value("2023")

    btn = driver.find_element(By.XPATH,'/html/body/center[2]/form/table/tbody/tr[2]/td[3]/font/input[1]')
    time.sleep(1)
    btn.click()
    promedio_boletas_anuales_emitidas = 0
    promedio_boletas_anuales_emitidas_redondeado = 0
    try:
        boletas_anuales_txt = driver.find_element(By.XPATH,'/html/body/center[2]/form[1]/table/tbody/tr[15]/td[4]/div/font').text
        boletas_anuales = int(boletas_anuales_txt)
        promedio_boletas_anuales_emitidas = boletas_anuales/12
        promedio_boletas_anuales_emitidas_redondeado = math.ceil(promedio_boletas_anuales_emitidas)

    except NoSuchElementException:
        print('no hay')


    #print({"facturas_de_venta":{"promedio":promedio_facturas_de_venta,"promedio_redondeado":promedio_facturas_de_venta_redondeado},"faturas_de_compra":{"promedio":promedio_facturas_de_compra,"promedio_redondeado":promedio_facturas_de_compra_redondeado},"boletas_recibidas":{"promedio":promedio_boletas_anuales,"promedio_redondeado":promedio_boletas_anuales_redondeado}})
    return{"facturas_de_venta":{"promedio":promedio_facturas_de_venta,"promedio_redondeado":promedio_facturas_de_venta_redondeado},"faturas_de_compra":{"promedio":promedio_facturas_de_compra,"promedio_redondeado":promedio_facturas_de_compra_redondeado},"boletas_recibidas":{"promedio":promedio_boletas_anuales_recibidas,"promedio_redondeado":promedio_boletas_anuales_recibidas_redondeado},"boletas_emitidas":{"promedio":promedio_boletas_anuales_emitidas,"promedio_redondeado":promedio_boletas_anuales_emitidas_redondeado}}



@app.route('/')
def index():
    return 'Hola Asesor'



@app.route('/api/facturacion', methods=['POST'])
def scraping_facturas():
    datos = request.json
    rut = datos["rut"]
    password = datos["password"]

    #driver = iniciar_chrome()
    driver.get("https://zeusr.sii.cl//AUT2000/InicioAutenticacion/IngresoRutClave.html?https://misiir.sii.cl/cgi_misii/siihome.cgi")
    try:


        ruter_input =  driver.find_element(By.ID, "rutcntr")
        ruter_input.send_keys(rut)

        pass_input = driver.find_element(By.ID, "clave")
        pass_input.send_keys(password)

        btn_ingreso = driver.find_element(By.ID, "bt_ingresar")
        btn_ingreso.click()

        try:
            alert = driver.switch_to.alert
            alert.dismiss()
        except:
            pass

        try:
            alert = driver.switch_to.alert
            alert.dismiss()
        except:
            pass

        try:
            driver.find_element(By.ID, "titulo")
            print("login fallido!!!")
            return {"failed":True,"message":"loginn fallido"}

        except NoSuchElementException:
            try:
                try:
                    modal = driver.find_element(By.CSS_SELECTOR, 'div.modal-dialog')

                    if modal:
                        # Si hay un modal, hacer clic en el botón de cierre
                        btn_cierre_modal = driver.find_element(By.XPATH, '//*[@id="ModalEmergente"]/div/div/div[3]/button')
                        btn_cierre_modal.click()
                except:
                    pass

                time.sleep(1)

                try:
                    modal = driver.find_element(By.ID,'myMainCorreoVigente')
                    if modal.is_displayed():
                        driver.execute_script("arguments[0].style.display = 'none';", modal)

                except:
                    pass

                time.sleep(1)

                data = getData(rut)

                return data

                #return {"failed":False,"datos":{"nombre":nombre,"direccion":direccion,"mail":mail,"mail2":mail2}}

            except NoSuchElementException:

                boton_siguiente = driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div/p[2]/a[1]')
                boton_siguiente.click()
                try:
                    try:
                        alert = driver.switch_to.alert
                        alert.dismiss()
                    except:
                        pass

                    try:
                        alert = driver.switch_to.alert
                        alert.dismiss()
                    except:
                        pass

                    try:
                        modal = driver.find_element(By.CSS_SELECTOR, 'div.modal-dialog')

                        if modal:
                            # Si hay un modal, hacer clic en el botón de cierre
                            btn_cierre_modal = driver.find_element(By.XPATH, '//*[@id="ModalEmergente"]/div/div/div[3]/button')
                            btn_cierre_modal.click()
                    except:
                        pass

                    time.sleep(1)

                    try:
                        modal = driver.find_element(By.ID,'myMainCorreoVigente')
                        if modal.is_displayed():
                            driver.execute_script("arguments[0].style.display = 'none';", modal)
                    except:
                        pass

                    time.sleep(1)

                    data = getData(rut)

                    return data

                except NoSuchElementException:
                    print('keseste erroooor!!')
                    return {"failed":True,"message":"Error desconocido"}

    except Exception as e:
        print (e)
        return jsonify({"error": "Error en el proceso de obtención de datos de facturación"}), 500



if __name__ == "__main__":
    app.run(debug=True)
