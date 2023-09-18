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


