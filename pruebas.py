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
	# cursor.execute("DELETE FROM SALDOS WHERE COD_FACTURA = (?)", (18,))
	# cursor.execute("INSERT INTO SALDOS VALUES (?,?,?,?,?,?)",(int("08"), "CLIENTE OCHO", 18, "SALDADO", 0, str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
	cursor.execute("SELECT SALDO FROM SALDOS WHERE NOMBRE_CLIENTE = (?)", ("cliente nueve",))
	try:
		saldos = cursor.fetchall()
		print(saldos)
		print(sum([i[0] for i in saldos]))
	except:
		print("ERROR")
	conexion.commit()
	cursor.close()
	conexion.close()

def tkinterTreeview():

	def seleccion(event):
		print("arbol selection: ",arbol.selection(), "arbol item: ", arbol.item(arbol.selection()), "arbol item values: ", arbol.item(arbol.selection())["values"])
		print("\nTIPOS:\n")
		print("arbol selection: ",type(arbol.selection()), "arbol item: ", type(arbol.item(arbol.selection())), "arbol item values: ", type(arbol.item(arbol.selection())["values"]))

	def borrarElementoUnitario():
		arbol.delete(arbol.selection()[0])

	def borrarElementos():
		arbol.delete(*arbol.get_children())

	def imprimirElementos():
		print(arbol.get_children())

	def crearElementos():

		for i in range(5):
			arbol.insert("", tkinter.END, iid = nombre[i],text = str(i)+" "+nombre[i],values= [colores[i], random.randint(1,40), "$ "+str(1000*random.randint(10, 30))], tags= ("seleccion_item",))
			arbol.insert(nombre[i], tkinter.END, text="prueba"+str(i), values = [0, 1, 2])
		arbol.pack(fill=tkinter.BOTH, expand=True)

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

	crearElementos()

	tkinter.Button(raiz, width = 12, text= "BORRAR ELEMENTO", command=borrarElementoUnitario).pack()
	tkinter.Button(raiz, width = 12, text= "VER ELEMENTOS", command=imprimirElementos).pack()
	tkinter.Button(raiz, width = 12, text= "REINICIAR TREEVIEW", command=borrarElementos).pack()




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
	print(df.iloc[1, 2])

def tratamientoCadenas():

	frase  = "esta / es la frase ~ que estamos ~colocando de / prueba"
	divisionPorCaracter = "~".join(frase.split("/")).split("~")
	print(divisionPorCaracter)

# tkinterTreeview()
import tkinter as tk
from tkinter import ttk

def insert_child():
    selected_item = tree.selection()
    if selected_item:
        new_item = ("", "Hija de María", "$500")
        tree.insert(selected_item, "end", values=new_item)

import tkinter as tk
from tkinter import ttk

def insert_child(item_id):
    new_item = ("", "Registro Hijo", "$500")
    tree.insert(item_id, "end", values=new_item)

root = tk.Tk()
root.title("TreeView con Registros Jerárquicos")

tree = ttk.Treeview(root, columns=('CODIGO', 'NOMBRE', 'SALDO'), show='headings')

tree.heading('CODIGO', text='CODIGO')
tree.heading('NOMBRE', text='NOMBRE')
tree.heading('SALDO', text='SALDO')

tree.column('CODIGO', width=80)
tree.column('NOMBRE', width=150)
tree.column('SALDO', width=80)

data = [
    ("001", "Padre 1", "$1000"),
    ("002", "Padre 2", "$1500")
]

for item in data:
    parent = tree.insert("", "end", values=item)
    tree.insert(parent, "end", values=("1", "Hijo 1", "$500"))
    tree.insert(parent, "end", values=("2", "Hijo 2", "$700"))

tree.bind("<Button-1>", lambda event: insert_child(tree.identify_row(event.y)))

tree.pack()

root.mainloop()
