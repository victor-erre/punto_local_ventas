import tkinter as tk
from tkinter import ttk
import random
import pandas as pd
import sqlite3
# import time
import datetime
import numpy
import calendar
import locale
import re
from PIL import Image, ImageTk


def conexionProyecto():
	# conexion = sqlite3.connect("C:/Users/Victo/Documents/programacion/proyectos_propios/punto_local_ventas/BASE_DATOS_PRUEBA.db")
	conexion = sqlite3.connect("C:/Users/Victo/Documents/programacion/proyectos_propios/punto_local_ventas/base_datos_p1.db")
	cursor = conexion.cursor()
	cursor.execute("DROP TABLE IF EXISTS PRUEBA")
	# cursor.execute("""CREATE TABLE PRUEBA (
	# 			PRUEBA1 VARCHAR(12) NOT NULL,
	# 			PRUEBA2 VARCHAR(20) DEFAULT "PRUEBA DOS",
	# 			PRUEBA3 INTEGER NOT NULL,
	# 			PRUEBA4 INTEGER NOT NULL,
	# 			PRUEBA5 INTEGER GENERATE ALWAYS (PRUEBA3 - PRUEBA4),
	# 			PRIMARY KEY (PRUEBA1)
	# 	)""")
	# cursor.execute("INSERT INTO PRUEBA(PRUEBA1, PRUEBA3, PRUEBA4) VALUES (?)", ('ENSAYO 1', 4000, 3500))
	conexion.commit()
	cursor.close()
	conexion.close()
	# cursor.execute("DELETE FROM SALDOS WHERE COD_FACTURA = (?)", (18,))
	# cursor.execute("INSERT INTO SALDOS VALUES (?,?,?,?,?,?)",(int("08"), "CLIENTE OCHO", 18, "SALDADO", 0, str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
	# cursor.execute("SELECT * FROM INVENTARIO_PAPELERIA WHERE CODIGO = (?)", ("PA078", ))
	# try:
	# 	# saldos = cursor.fetchall()
	# 	saldos = cursor.fetchone()
	# 	print(saldos)
	# 	print(type(saldos))
	# 	# print(sum([i[0] for i in saldos]))
	# except ValueError as e:
	# 	print(e)
	# except AttributeError as ae:
	# 	print(ae)
	# conexion.commit()
	# cursor.close()
	# conexion.close()

# conexionProyecto()


def tkinterTreeview():

	def seleccion(event):
		print("arbol selection: ",arbol.selection(), "arbol item: ", arbol.item(arbol.selection()), "arbol item values: ", arbol.item(arbol.selection())["values"])
		print("\nTIPOS:\n")
		print("arbol selection: ",type(arbol.selection()), "arbol item: ", type(arbol.item(arbol.selection())), "arbol item values: ", type(arbol.item(arbol.selection())["values"]))

	def borrarElementoUnitario():
		arbol.delete(arbol.selection()[0])

	def borrarElementos():
		arbol.delete(*arbol.get_children())
		#arbol.delete('1', 'end')

	def imprimirElementos():
		print(arbol.get_children())

	def crearElementos():

		for i in range(5):
			arbol.insert("", tkinter.END, iid = nombre[i],text = str(i)+" "+nombre[i],values= [colores[i], random.randint(1,40), "$ "+str(1000*random.randint(10, 30))], tags= ("seleccion_item",))
			arbol.insert(nombre[i], tkinter.END, text="prueba"+str(i), values = [0, 1, 2])
		arbol.pack(fill=tkinter.BOTH, expand=True)

	def validarNumero(elemento):
		print(elemento)
		if elemento=="" or elemento.isalpha() and len(elemento)<11:
			# vbleControl.set(elemento)
			etiqueta["text"] = elemento
			return True
		else:
			return False

	raiz = tkinter.Tk()
	vbleControl = tkinter.StringVar()
	etiqueta = tkinter.Label(raiz, text = "", bg = "red")
	etiqueta.pack()
	entrada = tkinter.Entry(raiz, width=30, bg="gray", textvariable=vbleControl)
	entrada.config(validate = "key" ,validatecommand = (entrada.register(validarNumero), '%P'))
	# entrada.config(validate = "key", validatecommand = (entrada.register(validarNumero), '%P'))
	entrada.pack()
	raiz.geometry("600x600")
	arbol = ttk.Treeview(raiz, columns=("COLOR", "CANTIDAD", "PRECIO"), selectmode=tkinter.BROWSE)


	arbol.tag_bind("seleccion_item", "<<TreeviewSelect>>", seleccion)

	arbol.heading("#0", text="COLUMNA DEFECTO")
	arbol.heading("COLOR", text="COLOR")
	arbol.heading("CANTIDAD", text="CANTIDAD")
	arbol.heading("PRECIO", text="PRECIO")

	arbol.column("#0", stretch=tkinter.NO)
	arbol.column("COLOR", width=12)
	arbol.column("CANTIDAD", width=8)
	arbol.column("PRECIO", width=8)

	colores = ["amarilo", "rojo", "verde", "morado", "blanco"]
	nombre = ["primero", "segundo", "tercero", "cuarto", "quinto"]

	crearElementos()

	tkinter.Button(raiz, width = 12, text= "BORRAR ELEMENTO", command=borrarElementoUnitario).pack()
	tkinter.Button(raiz, width = 12, text= "VER ELEMENTOS", command=imprimirElementos).pack()
	tkinter.Button(raiz, width = 12, text= "REINICIAR TREEVIEW", command=borrarElementos).pack()

	raiz.mainloop()



# texto = "Mi dirección de correo es ejemplo@email.com y otra dirección es otra@example.com"
# patron = r'\w+@\w+\.\w+'

# coincidencias = re.findall(patron, texto)
# for coincidencia in coincidencias:
#     print(coincidencia)
# tkinterTreeview()


# def identificar_elemento(event):
#     item_id = tree.identify("item", event.x, event.y)
#     column_id = tree.identify("column", event.x, event.y)
#     heading_id = tree.identify("heading", event.x, event.y)

#     print(f"Identificado Item: {item_id}")
#     print(f"Identificado Columna: {column_id}")
    # print(f"Identificado Encabezado: {heading_id}")

# root = tk.Tk()
# root.geometry("400x300")

# tree = ttk.Treeview(root, columns=("Columna1", "Columna2"))
# tree.heading("#1", text="Encabezado 1")
# tree.heading("#2", text="Encabezado 2")

# tree.insert("", "end", text="Item 1", values=("Valor 1.1", "Valor 1.2"))
# tree.insert("", "end", text="Item 2", values=("Valor 2.1", "Valor 2.2"))

# tree.pack()

# # Configura un evento para identificar elementos cuando haces clic derecho en el Treeview.
# tree.bind("<<TreeviewSelect>>", identificar_elemento)

# root.mainloop()


def actualizar_celda(event):
    # Obtener la fila y la columna de la celda editada
    fila, columna = treeview.index(treeview.focus()), treeview.identify_column(event.x)

    # Verificar que la celda editada sea válida
    if fila and columna:
        # Actualizar el valor en el DataFrame
        nuevo_valor = treeview.item(fila)["values"][columna]
        df.loc[fila, columna] = nuevo_valor

def actualizar_interfaz():
    # Actualizar el Treeview para que refleje los cambios en el DataFrame
    treeview.delete(*treeview.get_children())
    for indice, fila in df.iterrows():
        treeview.insert("", "end", values=fila.tolist())



def funcionLambda():

	funcion = lambda y: map(lambda x :x+2, y)
	prueba = funcion([2,3,5,6])
	print(list(prueba))

def pruebaDataFrame():

	nombres = ["victor", "idaly", "jeffrey", "hector"]
	apellidos = ["ruiz", "lopez", "quiñonez", "perea"]
	edades = [25, 64, 35, 54]
	residencias = ["palmira", "cali", "pereira", "quiddo"]

	df1 = pd.DataFrame(columns = ["nombre", "apellido", "edad", "residencia"])
	df2 = pd.DataFrame(data =[[nombres[i], apellidos[i], edades[i], residencias[i]] for i in range(len(nombres))],columns=("nombre", "apellido", "edad", "residencia"), index=[f"Elemento {i}" for i in range(1,len(nombres)+1)])

	df1 = pd.concat([df1, df2])

	for i, j in df1.iterrows():
		if re.search("ct", j.at["nombre"]):
			print(i,j, sep="\n++++++\n", end="\n\n")

		
	# print(df1)
	# if "nombre" in df1.columns:
	# 	df1 = df1.drop("nombre", axis=1)
	# print(df1)
	# if "pruebas" in df1.columns:
	# 	print("entramos en el condicional")
	# print(df2.index)	

# pruebaDataFrame()



class MiApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Crear un Frame
        self.frameOpciones = tk.Frame(self)
        self.frameOpciones.pack()

        # Cargar la imagen y redimensionarla
        lista = Image.open("lista.png")
        lista.thumbnail((20, 20))
        icon_lista = ImageTk.PhotoImage(lista)

        # Crear un botón con la imagen y la función de comando
        btnLista = tk.Button(self.frameOpciones, text="pureba", command=self.mostrar_lista_codigos)
        btnLista.place(relx=0.2, rely=0.07)

    def mostrar_lista_codigos(self):
        # Define la función que se ejecutará cuando se haga clic en el botón
        print("Mostrar lista Codigos")

# if __name__ == '__main__':
#     app = MiApp()
#     app.mainloop()


def pruebaSeries():

	serie = pandas.Series(data = ("victor", "alfonso", "ruiz", 23), index = ("nombre", "segundonombre", "apellido", "edad"), name = "prueba")
	serie.loc["edad"] +=1

# pruebaSeries()
def tratamientoCadenas():

	frase  = "esta / es la frase ~ que estamos ~colocando de / prueba"
	divisionPorCaracter = "~".join(frase.split("/")).split("~")
	print(divisionPorCaracter)

def tkinterListbox():

	raiz = tkinter.Tk()
	raiz.geometry("500x500+300+50")

	listaPrueba = tkinter.Listbox(raiz, selectmode="none")
	listaPrueba.insert("end", "Ésta es la primera línea.")
	listaPrueba.insert("end", "Ahora continúo con la segunda línea.")
	listaPrueba.insert("end", "Finalizamos con la tercera línea.")
	listaPrueba.insert("end", "Ésta es la cuarta línea.")
	listaPrueba.insert("end", "Ahora continúo con la quinta línea.")
	listaPrueba.insert("end", "Finalmente la sexta línea.")
	listaPrueba.place(relx=0.3, rely=0.1, relwidth=.69, relheight=.1)

	scroll = tkinter.Scrollbar(listaPrueba, orient=tkinter.VERTICAL)
	scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)

	raiz.mainloop()
	
def puntoMilConSimbolo(numero):
		'''
		Función para asignarle el punto que indica mil (si lo tiene) y ubicar el símbolo de peso a la izquierda de la cifra.
		'''
		if len(numero)<=3:
			return "$ {}".format(numero)
		else:
			transformado = list(numero)
			puntos = len(numero) // 3 
			residuo = len(numero) % 3
			contador = -3

			# insertamos los puntos en el lugar indicado.
			# Si el residuo es cero quiere decir que la cantidad de numeros no es múltiplo de 3 y por ende podemos agregarlos en la posicion -3
			# si es el punto que indica mil, sino le vamos aumentando -4 cada vez. Si el residuo es cero (ES múltiplo de 3) entonces le quitamos
			# una unidad a la variable puntos, ya que si tenemos ejemplo 350, 349.000, y asi susesivamente, no podemos poner punto antes de las centenas, centenas de mil, ..
			if residuo!=0:
				for i in range(puntos):
					transformado.insert(contador, ".")
					contador-=4
			else:
				for i in range(puntos-1):
					transformado.insert(contador, ".")
					contador-=4
			return "$ {}".format("".join(transformado))

def procesar_numero(numero):
    if numero < 0:
        # Lanzar una excepción personalizada
        raise ValueError("El número no puede ser negativo.")
    
    # El procesamiento continúa aquí
    resultado = numero * 2
    return resultado

def manejoErrores():
	try:
		valor = 23 + ["hola", "bro"]
	except ValueError as e:
		print(e)
	except TypeError as t:
		print(t)
		return
	print("fin del intento")

def modificarFuncion(funcion):

	def modificadora(var1, var2, *args, **kwargs):
	# def modificadora( *args, **kwargs):

		conexion = sqlite3.connect("C:/Users/Victo/Documents/programacion/proyectos_propios/punto_local_ventas/BASE_DATOS_PRUEBA.db")
		cursor = conexion.cursor()
		args = ["hola", "mi perro"]
		kwargs = {"conexion":conexion, "cursor":cursor}
		funcion(var1, var2, *args, **kwargs)
		conexion.commit()
		cursor.close()
		conexion.close()
	

	return modificadora


@modificarFuncion
def funcionPrueba( var1, var2, *args, **kwargs):
	print(var1)
	print(args)
	print(kwargs)
	cursor = kwargs["cursor"]
	conexion = kwargs["conexion"]
	cursor.execute("SELECT COD_FACTURA FROM SALDOS")
	prueba = cursor.fetchall()

	# Devuelve los valores que deseas
	return 



def extractoBancolombia():

	vble = """34.00
	"""

	suma = float()
	for i in vble.split("\n"):
		if len(i)>0 and i[0]=="-":
			continue
		else:
			# print(i.replace(".00", "").replace(",", ""))
			# tipo = i.replace(".00", "").replace(",", "")
			# print(tipo, "--->>",type(tipo))
			suma+=float(i.replace(".00", "").replace(",", ""))


import tkinter as tk
from tkinter import ttk

def actualizar_treeview():
    # Borrar todas las filas existentes en el Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Insertar las filas actualizadas
    for elemento in elementos_lista:
        tree.insert("", "end", values=(elemento,))

# Función para manejar eventos de modificación de la lista
def modificar_lista():
    # Aquí puedes modificar la lista según las necesidades del usuario
    # Por ejemplo, agregar o eliminar elementos
    elementos_lista.append("Nuevo Elemento")
    actualizar_treeview()

