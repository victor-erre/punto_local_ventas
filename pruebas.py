import tkinter
from tkinter import ttk
import random

print("PRUEBAS")

def tkinterTreeview():

	def seleccion(event):

		print("arbol selection")
		print(arbol.selection())
		print("arbol item")
		print(arbol.item(arbol.selection()))
		print("values")
		print(arbol.item(arbol.selection())["values"])
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

tkinterTreeview()
