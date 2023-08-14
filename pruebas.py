import tkinter
from tkinter import ttk

def interfazTreeview():

	def funcionSeleccion(event):
		print("seleccion  = ",arbol.selection(), "\nItem solo=", arbol.item(arbol.selection()), "\nItem values=", arbol.item(arbol.selection())["values"])
	colores = ["ROJO", "VERDE", "AMARILLO", "ROSADO", "MARRÓN"]
	figura = ["TRIANGULO", "CIRCULO", "CUBO", "CONO", "RECTANGULO"]

	raiz = tkinter.Tk()

	arbol = ttk.Treeview(raiz, columns= ("COLOR", "FIGURA", "NUMERO"), selectmode = tkinter.BROWSE)

	arbol.tag_bind("tag_seleccion", "<<TreeviewSelect>>", funcionSeleccion)

	arbol.column("#0", width=0, stretch=tkinter.NO)
	arbol.column("COLOR", width=15)
	arbol.column("FIGURA", width=15)
	arbol.column("NUMERO", width=15)

	for i in range(5):

		arbol.insert("", tkinter.END, iid = "elemento {}".format(i+1), values=[colores[i], figura[i], i+1], tags=("tag_seleccion",))

	arbol.place(relwidth = 1, relheight = 1)

	raiz.mainloop()

interfazTreeview()