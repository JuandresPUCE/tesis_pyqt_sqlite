from PyQt6.QtWidgets import *
import json
import logging
import os
import shutil

class Servicios:
    def __init__(self, parent=None):
        self.parent = parent  # Guardar referencia al widget padre
        self.mensaje = "Metodos comunes del controlador"
    
    # refactor mostrar datos en tabla
    def mostrar_datos_en_tabla(self, tabla, datos, columnas, descripcion_nombre_tabla=None, no_mostrar_aviso=None):
        try:
            # Definir la tabla
            self.tabla = tabla
            self.tabla.clearContents()
            self.tabla.setRowCount(0)

            # Verificar que hay datos
            if datos:
                self.tabla.setRowCount(len(datos))
                self.tabla.setColumnCount(len(columnas))

                for fila, dato in enumerate(datos):
                    for columna, columna_nombre in enumerate(columnas):
                        self.tabla.setItem(fila, columna, QTableWidgetItem(str(getattr(dato, columna_nombre))))

            else:
                self.tabla.setRowCount(0)
                if not no_mostrar_aviso:
                    # Usar descripcion_nombre_tabla si se proporciona, de lo contrario usar un mensaje genérico
                    mensaje = f"No se encontraron registros de {descripcion_nombre_tabla} en la base de datos." if descripcion_nombre_tabla else "No se encontraron registros en la base de datos."
                    QMessageBox.information(self.parent, "No hay registros", mensaje, QMessageBox.StandardButton.Ok)

        except AttributeError as ae:
            print(f"Error de atributo: {ae}")
            QMessageBox.critical(self.parent, "Error", f"Error al mostrar datos: {ae}", QMessageBox.StandardButton.Ok)
        except Exception as e:
            print(f"Error inesperado: {e}")
            QMessageBox.critical(self.parent, "Error", f"Error inesperado al mostrar datos: {e}", QMessageBox.StandardButton.Ok)


    #mostar tablas
    def mostrar_datos_tabla_arrhenius(self, tabla_datos_arrhenius, resultados, no_mostrar_aviso=None):
        columnas = ["id", "nombre_caso", "id_nombre_data_salida", "id_nombre_data", "fecha", "temperatura", "reciproco_temperatura_absoluta", "constante_cinetica", "logaritmo_constante_cinetica", "energia_activacion_r", "r_utilizada", "energia_activacion", "constante_cinetica_0", "logaritmo_constante_cinetica_0", "detalles"]
        self.mostrar_datos_en_tabla(tabla_datos_arrhenius, resultados, columnas, descripcion_nombre_tabla="Datos Arrhenius", no_mostrar_aviso=no_mostrar_aviso)
    
    def mostrar_datos_tabla_salida(self, tabla_datos_salida, resultados, no_mostrar_aviso=None):
        columnas = ["id", "nombre_data_salida", "fecha", "id_nombre_data", "id_condiciones_iniciales", "id_registro_unidades", "r_utilizada", "nombre_data", "nombre_reaccion", "delta_n_reaccion", "epsilon_reactivo_limitante", "tipo_especie", "especie_quimica", "constante_cinetica", "orden_reaccion", "modelo_cinetico", "tipo_calculo", "detalles"]
        self.mostrar_datos_en_tabla(tabla_datos_salida, resultados, columnas, descripcion_nombre_tabla="Datos de Salida", no_mostrar_aviso=no_mostrar_aviso)
    
    def mostrar_condiciones_iniciales(self, condiciones_iniciales_tabla, condiciones, no_mostrar_aviso=None):
        columnas = ["id", "temperatura", "tiempo", "presion_total", "presion_parcial", "fraccion_molar", "especie_quimica", "tipo_especie", "detalle", "nombre_data"]
        self.mostrar_datos_en_tabla(condiciones_iniciales_tabla, condiciones, columnas, descripcion_nombre_tabla="Condiciones Iniciales", no_mostrar_aviso=no_mostrar_aviso)
    
    def mostrar_datos_tabla(self, tabla_datos_cineticos, resultados, no_mostrar_aviso=None):
        columnas = ["id", "tiempo", "concentracion", "otra_propiedad", "conversion_reactivo_limitante", "tipo_especie", "id_condiciones_iniciales", "nombre_data", "nombre_reaccion", "especie_quimica"]
        self.mostrar_datos_en_tabla(tabla_datos_cineticos, resultados, columnas, descripcion_nombre_tabla="Datos Cinéticos", no_mostrar_aviso=no_mostrar_aviso)

    def mostrar_reacciones(self, reacciones_tabla, reacciones, no_mostrar_aviso=None):
        columnas = ["id", "especie_quimica", "formula", "coeficiente_estequiometrico", "detalle", "tipo_especie", "nombre_reaccion"]
        self.mostrar_datos_en_tabla(reacciones_tabla, reacciones, columnas, descripcion_nombre_tabla="Reacciones", no_mostrar_aviso=no_mostrar_aviso)
    
    def mostrar_registros(self, registro_datos_tabla, registros, no_mostrar_aviso=None):
        columnas = ["id", "nombre_data", "fecha", "detalle"]
        self.mostrar_datos_en_tabla(registro_datos_tabla, registros, columnas, descripcion_nombre_tabla="Registros Experimentales", no_mostrar_aviso=no_mostrar_aviso)
    
    def mostrar_unidades(self, unidades_tabla, unidades, no_mostrar_aviso=None):
        columnas = ["id", "presion", "temperatura", "tiempo", "concentracion", "energia", "r", "nombre_data"]
        self.mostrar_datos_en_tabla(unidades_tabla, unidades, columnas, descripcion_nombre_tabla="Unidades", no_mostrar_aviso=no_mostrar_aviso)
    
    #seleccionar informacion de la tabla
    def seleccionar_datos(self, tabla, columnas):
        seleccionar_fila = tabla.currentRow()
        if seleccionar_fila != -1:
            datos = {}
            for i, columna in enumerate(columnas):
                datos[columna] = tabla.item(seleccionar_fila, i).text().strip()
            return datos
        return None
    
    def seleccionar_datos_visuales(self, tabla, columnas, elementos_visuales, excluir_id=None):
        seleccionar_fila = tabla.currentRow()
        if seleccionar_fila != -1:
            datos = {}
            for i, columna in enumerate(columnas):
                datos[columna] = tabla.item(seleccionar_fila, i).text().strip()

            # Excluir 'id' de los elementos visuales por defecto
            if excluir_id is None or excluir_id:
                columnas_visuales = columnas[1:]
            else:
                columnas_visuales = columnas

            for columna, elemento_visual in zip(columnas_visuales, elementos_visuales):
                elemento_visual.setText(datos[columna])

            return datos
        return None
    
    def limpiar_elementos_visuales(self, elementos_visuales):
        for elemento in elementos_visuales:
            try:
                elemento.clear()
            except AttributeError:
                print(f"El elemento {elemento} no esta presente.")

    #funciones refactorizadas
    def borrar_elemento(self, tabla, borrar_resultado, mensaje_confirmacion, mensaje_exito, mensaje_error, metodo_consultar, metodo_refescar, metodo_buscar):
        fila_seleccionada = tabla.currentRow()
        if fila_seleccionada != -1:
            opcion_seleccionada = QMessageBox.question(self.parent, "Eliminar elemento", mensaje_confirmacion, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if opcion_seleccionada == QMessageBox.StandardButton.Yes:
                if borrar_resultado:
                    QMessageBox.information(self.parent, "Información", mensaje_exito, QMessageBox.StandardButton.Ok)
                    metodo_consultar()
                    metodo_refescar()
                    metodo_buscar()
                else:
                    QMessageBox.information(self.parent, "Información", mensaje_error, QMessageBox.StandardButton.Ok)
    
    # desplegar en combo box
    def desplegar_datos_combo_box_catalogo(self, combo_box, elementos,mensaje_error,tipo_elemento_catalogo):
        try:
            combo_box.clear()
            combo_box.addItem("Seleccione una opción",-1)
            combo_box.addItem("otro") # Agregar la opción "otro" al final de la lista
            if elementos:
                for elemento in elementos:
                    combo_box.addItem(str(elemento.get(tipo_elemento_catalogo)), str(elemento.get("id")))
            else:
                QMessageBox.information(self.parent, "No hay elementos", mensaje_error, QMessageBox.StandardButton.Ok)
        except Exception as e:
            #print(f"Error inesperado: {e}")
            QMessageBox.critical(self.parent, "Error", f"Error inesperado al mostrar elementos: {e}", QMessageBox.StandardButton.Ok)

        
    def desplegar_datos_combo_box(self, combo_box, elementos,mensaje_error):

        try:
            combo_box.clear()
            combo_box.addItem("Seleccione una opción",-1)
            if elementos:
                for elemento in elementos:
                    combo_box.addItem(str(elemento.nombre_data), str(elemento.id))
            else:
                QMessageBox.information(self.parent, "No hay elementos", mensaje_error, QMessageBox.StandardButton.Ok)
        except Exception as e:
            #print(f"Error inesperado: {e}")
            QMessageBox.critical(self.parent, "Error", f"Error inesperado al mostrar elementos: {e}", QMessageBox.StandardButton.Ok)


    def cargar_datos_json_box(self, archivo, catalogo, combo_box, tipo_elemento_catalogo):
        try:
            with open(archivo, 'r') as f:
                data = json.load(f)
                self.desplegar_datos_combo_box_catalogo(combo_box, data.get(catalogo, []), "No se encontraron datos en el archivo JSON.", tipo_elemento_catalogo)
        except FileNotFoundError:
            QMessageBox.critical(self.parent, "Error", f"No se encontró el archivo {archivo}", QMessageBox.StandardButton.Ok)
        except json.JSONDecodeError:
            QMessageBox.critical(self.parent, "Error", f"Error al leer el archivo {archivo}", QMessageBox.StandardButton.Ok)

    def cargar_datos_json_box_group_box(self, archivo, catalogo, combo_box, tipo_elemento_catalogo, group_box):
            try:
                with open(archivo, 'r') as f:
                    data = json.load(f)
                    elementos = data.get(catalogo, [])

                    # Limpiar el combo_box antes de insertar nuevos datos
                    combo_box.clear()
                    combo_box.addItem("Seleccione una opción",-1)
                    combo_box.addItem("otro") # Agregar la opción "otro" al final de la lista
                    
                    # Insertar los valores en el combo_box
                    for elemento in elementos:
                        combo_box.addItem(str(elemento[tipo_elemento_catalogo]), elemento)

                    # Conectar la señal de cambio de índice para actualizar el título del group_box
                    combo_box.currentIndexChanged.connect(lambda: self.actualizar_titulo_group_box(combo_box, group_box))


                    # Actualizar el título del group_box con el primer elemento (si existe)
                    if elementos:
                        self.actualizar_titulo_group_box(combo_box, group_box)
                    else:
                        group_box.setTitle("No se encontraron datos en el archivo JSON.")
            except FileNotFoundError:
                QMessageBox.critical(self.parent, "Error", f"No se encontró el archivo {archivo}", QMessageBox.StandardButton.Ok)
            except json.JSONDecodeError:
                QMessageBox.critical(self.parent, "Error", f"Error al leer el archivo {archivo}", QMessageBox.StandardButton.Ok)

    def actualizar_titulo_group_box(self, combo_box, group_box):
        try:
            index = combo_box.currentIndex()
            if index != -1:
                elemento = combo_box.itemData(index)
                if isinstance(elemento, dict):
                    unidades = elemento.get('unidades', 'No se encontraron unidades')
                    group_box.setTitle(f"R ({unidades})")
                elif elemento == "otro":
                    group_box.setTitle("R (Otro)")
                else:
                    group_box.setTitle("R (Seleccione una opción)")
            else:
                group_box.setTitle("R")
        except Exception as e:
            # Manejar cualquier excepción inesperada
            QMessageBox.critical(self.parent, "Error", f"Error al actualizar el título del GroupBox: {e}", QMessageBox.StandardButton.Ok)
            group_box.setTitle("R (Error)")

    def actualizar_titulo_group_box_generico(self, combo_box, group_box, default_title="R", error_title="R (Error)", not_found_title="R (Seleccione una opción)", other_title="R (Otro)", units_not_found="No se encontraron unidades"):
        try:
            index = combo_box.currentIndex()
            if index != -1:
                elemento = combo_box.itemData(index)
                if isinstance(elemento, dict):
                    unidades = elemento.get('unidades', units_not_found)
                    group_box.setTitle(f"{default_title} ({unidades})")
                elif elemento == "otro":
                    group_box.setTitle(other_title)
                else:
                    group_box.setTitle(not_found_title)
            else:
                group_box.setTitle(default_title)
        except Exception as e:
            # Manejar cualquier excepción inesperada
            QMessageBox.critical(self.parent, "Error", f"Error al actualizar el título del GroupBox: {e}", QMessageBox.StandardButton.Ok)
            group_box.setTitle(error_title)


    def actualizar_lineedit(self, combo_box, line_edit, sin_ocultar=None):
        try:
            current_text = combo_box.currentText()
            if current_text == "Seleccione una opción":
                line_edit.clear()
                if not sin_ocultar:
                    line_edit.hide()
            else:
                line_edit.setText(current_text)
                if current_text == "otro":
                    line_edit.show()
                    line_edit.setText(current_text)
                else:
                    if not sin_ocultar:
                        line_edit.hide()
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Error inesperado al actualizar el line edit: {e}", QMessageBox.StandardButton.Ok)

    def validar_ruta(self, ruta):
        # Verifica si la ruta es una ruta de archivo válida
        return os.path.isfile(ruta)

    
    def cargar_configuracion_json(self, archivo, catalogo):
        try:
            # Intenta abrir y leer el archivo principal
            with open(archivo, 'r') as f:
                configuracion = json.load(f)
                
                # Verificar si la clave catalogo está en la configuración
                if catalogo in configuracion:
                    valor = configuracion[catalogo]
                    
                    # Validar si el valor es una ruta de archivo válida
                    if self.validar_ruta(valor):
                        return valor
                    else:
                        raise ValueError(f"El valor de '{catalogo}' en el archivo {archivo} no es una ruta válida.")
                else:
                    raise KeyError(f"La clave '{catalogo}' no se encontró en el archivo {archivo}")
                
        except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError) as e:
            print(str(e))
            print(f"Intentando cargar archivo de configuración temporal...")
            return self.cargar_configuracion_json_temporal(catalogo)
    
    def cargar_configuracion_json_temporal(self, catalogo):
        #QMessageBox.warning(self.parent, "Advertencia", "No se pudo cargar la configuración principal. Intentando cargar la configuración temporal.", QMessageBox.StandardButton.Ok)
        dir_db_temp = r"config\config_temp.json"
        
        try:
            with open(dir_db_temp, 'r') as f:
                configuracion = json.load(f)
                
                # Verificar si la clave catalogo está en la configuración
                if catalogo in configuracion:
                    return configuracion[catalogo]
                else:
                    raise KeyError(f"La clave '{catalogo}' no se encontró en el archivo de configuración temporal {dir_db_temp}")
                
        except FileNotFoundError:
            raise Exception(f"No se encontró el archivo de configuración temporal {dir_db_temp}")
        except json.JSONDecodeError:
            raise Exception(f"Error al leer el archivo de configuración temporal {dir_db_temp}")
        except KeyError as e:
            raise Exception(str(e))
    
    def respaldar_db(self):
        config_path = r"config\config.json"
        config_temp_path = r"config\config_temp.json"
        
        # Intentar cargar la ruta de la base de datos desde ambos archivos de configuración
        db_path = None
        title = ""
        try:
            if os.path.isfile(config_path):
                db_path = self.cargar_configuracion_json(config_path, "db_path")
                title = "Guardar Respaldo - Base de Datos Principal"
            if not db_path and os.path.isfile(config_temp_path):
                db_path = self.cargar_configuracion_json(config_temp_path, "db_path")
                title = "Guardar Respaldo - Base de Datos Temporal"
        except Exception as e:
            print(str(e))

        if not db_path:
            QMessageBox.warning(self.parent, "Advertencia", "No se encontró una ruta de base de datos válida en los archivos de configuración.", QMessageBox.StandardButton.Ok)
            return

        if not os.path.isfile(db_path):
            QMessageBox.critical(self.parent, "Error", "El archivo de base de datos especificado no existe.")
            return

        respaldo_file, _ = QFileDialog.getSaveFileName(self.parent, title, "", "SQLite Files (*.db)")
        
        if respaldo_file:
            try:
                shutil.copyfile(db_path, respaldo_file)
                QMessageBox.information(self.parent, "Respaldo Completo", "El respaldo de la base de datos se ha realizado con éxito.")
            except Exception as e:
                QMessageBox.critical(self.parent, "Error", f"No se pudo realizar el respaldo: {str(e)}")


        
    def cambiar_configuracion_db(self):
        # Abre un diálogo para seleccionar el nuevo archivo de base de datos
        fileName, _ = QFileDialog.getOpenFileName(self.parent, "Selecciona el nuevo archivo de base de datos", "", "All Files (*);;SQLite Files (*.db)")
        if fileName:
            self.actualizar_configuracion_db(fileName)

    def nueva_configuracion_db(self):
        # Abre un diálogo para seleccionar o crear un nuevo archivo de base de datos
        fileName, _ = QFileDialog.getSaveFileName(self.parent, "Guardar como...", "", "SQLite Files (*.db)")
        if fileName:
            # Crear el archivo si no existe
            try:
                if not os.path.exists(fileName):
                    open(fileName, 'w').close()
                # Luego actualiza el archivo de configuración
                self.actualizar_configuracion_db(fileName)
            except Exception as e:
                QMessageBox.critical(self.parent, "Error", f"No se pudo crear el archivo de base de datos: {str(e)}")

    def actualizar_configuracion_db(self, nueva_ruta):
            # Define la ruta completa al archivo config.json dentro de la carpeta config
            config_path = os.path.join(os.getcwd(), 'config', 'config.json')
            
            # Actualiza el archivo JSON con la nueva ruta
            config = {"db_path": nueva_ruta}
            
            try:
                with open(config_path, "w") as f:
                    json.dump(config, f)
                QMessageBox.information(self.parent, "Configuración Actualizada", "La ruta de la base de datos ha sido actualizada.")
            except Exception as e:
                QMessageBox.critical(self.parent, "Error", f"No se pudo actualizar la configuración: {str(e)}")

    def actualizar_valor_celda(self, tabla, manejador, fila, columna):
        try:
            item = tabla.item(fila, columna)
            if item is None:
                logging.warning("La celda está vacía o fuera de los límites de la tabla")
                return

            nuevo_valor = item.text().strip()

            if nuevo_valor == '':
                logging.warning("Error: el valor ingresado está vacío.")
                return

            # Verificar el tipo de datos esperado según el encabezado de la columna
            header_text = tabla.horizontalHeaderItem(columna).text().lower()
            columnas_a_convertir = ['temperatura', 'tiempo', 'presion_total', 'presion_parcial', 'fraccion_molar',
                                    'concentracion', 'otra_propiedad', 'conversion_reactivo_limitante', 'coeficiente_estequiometrico', 'r']

            if header_text in columnas_a_convertir:
                # Verificar si el valor puede convertirse a float
                try:
                    nuevo_valor = float(nuevo_valor)
                except ValueError:
                    logging.error("Error: el valor ingresado no es un número válido.")
                    return

            # Obtener el ID del dato a actualizar
            id_item = tabla.item(fila, 0)
            if id_item is None:
                logging.warning("No se encontró el ID en la fila seleccionada")
                return

            id = int(id_item.text().strip())

            # Crear el diccionario de actualización
            nuevo_dato = {header_text: nuevo_valor}

            # Intentar actualizar el dato en la base de datos
            if manejador.actualizar(id, nuevo_dato):
                logging.info(f"Dato con ID {id} actualizado correctamente")
            else:
                logging.error(f"No se pudo actualizar el dato con ID {id}")

        except Exception as e:
            logging.error(f"Error al actualizar el valor de la celda: {e}")
            QMessageBox.critical(self.parent, "Error", f"Se produjo un error al actualizar el valor de la celda: {e}", QMessageBox.StandardButton.Ok)

# refactor json

    def cargar_datos_json_a_combo_box(self, archivo, combo_box,catalogo):
        try:
            with open(archivo, 'r') as f:
                data = json.load(f)
                self.llenar_combo_box(data.get(catalogo, []), combo_box)
        except FileNotFoundError:
            QMessageBox.critical(self.parent, "Error", f"No se encontró el archivo {archivo}", QMessageBox.StandardButton.Ok)
        except json.JSONDecodeError:
            QMessageBox.critical(self.parent, "Error", f"Error al leer el archivo {archivo}", QMessageBox.StandardButton.Ok)
    
    def llenar_combo_box(self, datos, combo_box):
        combo_box.clear()
        combo_box.addItem("Seleccione una opción")
        for dato in datos:
            combo_box.addItem(dato)
    
    def actualizar_lineedit_desde_combo_box(self, combo_box, line_edit):
        current_text = combo_box.currentText()
        if current_text != "Seleccione una opción":
            line_edit.setText(current_text)
        else:
            line_edit.clear()

    #uso 
    #json_tipo_especie = r"data\tipo_especie.json"
    #self.cargar_datos_json_a_combo_box(json_tipo_especie, self.tipo_especie_rq_box,Tipo_especie_catalogo)

    # En algún lugar donde necesites actualizar el line edit basado en el combo box
    #self.actualizar_lineedit_desde_combo_box(self.tipo_especie_rq_box, self.tipo_especie_rq)


    def agregar_objeto_db(self, objeto, manejador, limpiar_funcion, buscar_funcion):

        try:
            # Asegurarse de que objeto es un diccionario o tiene una forma de iterar sobre sus campos
            if not hasattr(objeto, 'items'):
                raise AttributeError(f"El objeto de tipo '{type(objeto).__name__}' no tiene el método 'items'.")
            # Validar que todos los campos estén llenos
            for campo, valor in objeto.items():
                if not valor:
                    raise ValueError(f"El campo '{campo}' está vacío. Por favor, llénelo.")

            # Intentar agregar el objeto a la base de datos
            agregar_resultado = manejador.agregar(objeto)

            if agregar_resultado:
                QMessageBox.information(self.parent, "Datos agregados correctamente")
                limpiar_funcion()
                buscar_funcion()  # Refrescar la tabla con los nuevos datos
            else:
                QMessageBox.critical(self.parent, "Error", "Hubo un problema al agregar los datos")

        except ValueError as e:
            QMessageBox.warning(self.parent, "Advertencia", f"Datos inválidos o incompletos: {e}")
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Se produjo un error: {e}")

    def validar_convertir_campos(self, columnas, elementos_visuales, tipos):
        datos = {}
        for columna, elemento_visual, tipo in zip(columnas, elementos_visuales, tipos):
            valor = elemento_visual.text().strip()
            if not valor:
                raise ValueError(f"El campo '{columna}' está vacío. Por favor, llénelo.")
            if tipo == int:
                valor = int(valor)
            elif tipo == float:
                valor = float(valor)
            datos[columna] = valor
        return datos
    
    def actualizar_datos_db(self, tabla, columnas, elementos_visuales, tipos, manejador, clase_objeto, limpiar_func, buscar_func):
        try:
            # Obtener el ID del registro seleccionado
            fila_seleccionada = tabla.currentRow()  # O usar la tabla correspondiente
            if fila_seleccionada == -1:
                raise ValueError("Seleccione una fila para actualizar")

            id = int(tabla.item(fila_seleccionada, 0).text().strip())  # Ajustar según tu tabla y modelo

            # Validar y obtener los datos actualizados
            datos = self.validar_convertir_campos(columnas, elementos_visuales, tipos)

            # Intentar actualizar el registro en la base de datos
            actualizar_resultado = manejador.actualizar(id, datos)

            if actualizar_resultado:
                QMessageBox.information(self.parent, "Información", f"{clase_objeto.__name__} actualizado correctamente", QMessageBox.StandardButton.Ok)
                limpiar_func()
                buscar_func()  # Refrescar la tabla con los nuevos datos
            else:
                QMessageBox.critical(self.parent, "Error", f"Hubo un problema al actualizar el {clase_objeto.__name__}", QMessageBox.StandardButton.Ok)

        except ValueError as ve:
            QMessageBox.warning(self.parent, "Advertencia", f"Datos inválidos o incompletos: {ve}", QMessageBox.StandardButton.Ok)

        except Exception as e:
            logging.error(f"Error al actualizar el {clase_objeto.__name__}: {str(e)}")
            QMessageBox.critical(self.parent, "Error", f"Se produjo un error al actualizar el {clase_objeto.__name__}: {e}", QMessageBox.StandardButton.Ok)

    def agregar_datos_db(self, columnas, elementos_visuales, tipos, manejador, clase_objeto, limpiar_func, buscar_func):
        try:
            # Validar y obtener los datos
            datos = self.validar_convertir_campos(columnas, elementos_visuales, tipos)

            # Crear el objeto de la clase correspondiente
            objeto = clase_objeto(**datos)
            print(f"Intentando agregar {clase_objeto.__name__}:", objeto)

            # Intentar agregar el registro a la base de datos
            agregar_resultado = manejador.agregar(objeto)

            if agregar_resultado:
                QMessageBox.information(self.parent, "Información", f"{clase_objeto.__name__} agregado correctamente", QMessageBox.StandardButton.Ok)
                limpiar_func()
                buscar_func()
            else:
                QMessageBox.critical(self.parent, "Error", f"Hubo un problema al agregar el {clase_objeto.__name__} revise el nombre del objeto puede que este deba ser único", QMessageBox.StandardButton.Ok)

        except ValueError as ve:
            QMessageBox.warning(self.parent, "Advertencia", f"Datos inválidos o incompletos: {ve}", QMessageBox.StandardButton.Ok)

        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Se produjo un error al agregar el {clase_objeto.__name__}: {e}", QMessageBox.StandardButton.Ok)
    
    def validar_filtros(self, columnas, elementos_visuales, aplicar_strip=None):
        filtros = {}
        for i, (columna, elemento_visual) in enumerate(zip(columnas, elementos_visuales)):
            if aplicar_strip and aplicar_strip[i]:
                valor = elemento_visual.text().strip()
            else:
                valor = elemento_visual.text()
            if valor:
                filtros[columna] = valor
        return filtros

    def buscar_datos_db(self, columnas, elementos_visuales, aplicar_strip, manejador, mostrar_func, like=False):
        try:
            filtros = self.validar_filtros(columnas, elementos_visuales, aplicar_strip)
            modo_busqueda = "like" if like else "="
            registros = manejador.consultar(filtros, modo_busqueda)
            mostrar_func(registros)
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Se produjo un error al buscar los datos: {e}", QMessageBox.StandardButton.Ok)
