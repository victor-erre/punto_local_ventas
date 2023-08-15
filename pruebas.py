import tkinter
from tkinter import ttk
import random
import pandas
import sqlite3
# import time
import datetime


def conexionProyecto():
	conexion = sqlite3.connect("C:/Users/Victo/Documents/programacion/proyectos_propios/punto_local_ventas/BASE_DATOS_PRUEBA.db")
	cursor = conexion.cursor()
	cursor.execute("DELETE FROM SALDOS WHERE COD_FACTURA = (?)", (18,))
	cursor.execute("INSERT INTO SALDOS VALUES (?,?,?,?,?,?)",(int("08"), "CLIENTE OCHO", 18, "SALDADO", 0, str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
	conexion.commit()
	cursor.close()
	conexion.close()

def tkinterTreeview():

	def seleccion(event):
		print("arbol selection: ",arbol.selection(), "arbol item: ", arbol.item(arbol.selection()), "arbol item values: ", arbol.item(arbol.selection())["values"])
		print("\nTIPOS:\n")
		print("arbol selection: ",type(arbol.selection()), "arbol item: ", type(arbol.item(arbol.selection())), "arbol item values: ", type(arbol.item(arbol.selection())["values"]))

	raiz = tkinter.Tk()
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

	for i in range(5):
		arbol.insert("", tkinter.END, iid = nombre[i],text = str(i)+" "+nombre[i],values= [colores[i], random.randint(1,40), "$ "+str(1000*random.randint(10, 30))], tags= ("seleccion_item",))
	arbol.pack(fill=tkinter.BOTH, expand=True)


	raiz.mainloop()

def funcionLambda():

	funcion = lambda y: map(lambda x :x+2, y)
	prueba = funcion([2,3,5,6])
	print(list(prueba))

def pruebaDataFrame():

	nombres = ["victor", "idaly", "jeffrey"]
	apellidos = ["ruiz", "lopez", "quiñonez"]
	edades = [25, 64, 35]
	residencias = ["palmira", "cali", "pereira"]
	df = pandas.DataFrame(data =[[nombres[i], apellidos[i], edades[i], residencias[i]] for i in range(len(nombres))],columns=("nombre", "apellido", "edad", "residencia"))


# cadena = "23 Borrador 2300  ~ 43 sacapuntas 6000     ~ 98 papel 123000 / 2 tijeras 5000"
# print([i.strip() for i in str("~".join(cadena.split("/"))).split("~")])
