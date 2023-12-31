from tkinter import Frame,BROWSE,NONE, BOTH,X, Y, Listbox, Label, LabelFrame, Checkbutton, Scrollbar, Tk, Text, StringVar,Message, BooleanVar, Entry, Button, messagebox,TOP, OptionMenu, Toplevel, IntVar, NORMAL, RIGHT, LEFT, END, NO, CENTER, YES, HORIZONTAL, VERTICAL, simpledialog
from tkinter import ttk
# POTTER: REGISTRADORA CASIO PCR - T285
import conexiones
#import pandas
import time
import datetime
import matplotlib.pyplot as plt
# import os
# import webbrowser
from selenium import webdriver
from re import match
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import numpy
import locale
	
# Asignamos la hora del sistema en hora local
locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
# from functools import partial

# esta es una prueba inicial
# ***al eliminar un articulo no puede eliminarse sin antes liquidar el stock, entonces preguntar si desea liquidar, si es afirmativa la respuesta
# ...entonces realizar la compra del artículo por el valor actual y ahora si liquidar.

class Conversiones:

	def __init__(self):
		pass

	def puntoMilConSimbolo(self, numero):
		'''
		Función para asignarle el punto que indica mil (si lo tiene) y ubicar el símbolo de peso a la izquierda de la cifra.
		'''
		numero = str(numero)
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


class Validaciones:

	"""
	Para evitar equivocaciones en las cajas de entrada.
	El código ppalmente debe ser dos letras identificando el rubro seguidas de tres dígitos que identifican el artículo.
	El número celular debe tener 10 dígitos, nada de letras.
	"""

	def __init__(self):
		# self.boton = boton
		pass

	def codigoArticulo(self, codigo):
		codigo = codigo.upper()
		if codigo == "":
			return True
		elif len(codigo) <= 2:
			if codigo.isalpha():
				if len(codigo) ==1:
					return codigo in ["P","D"]
				else:
					if codigo[0]=="P" and codigo[1] == "A" or codigo[0] == "D" and codigo[1] == "U":
						return True
					else:
						return False
			else:
				return False
		else:
			if len(codigo) < 6:
				return codigo[2:].isdigit()
			else:
				return False

	def codigoCliente(self, codigo):
		if codigo=="" or codigo.isdigit() and len(codigo)<3:
			return True
		else:
			return False

	# *
	def numeroCelular(self, numero):
		if numero == "":
			return True

		elif len(numero) <= 10:
			return numero.isdigit()
		else:
			return False

	def valorRecarga(self, valor):
		if valor =="":
			return True
		elif len(valor)<6:
			return valor.isdigit()
		else:
			return False

	def codigoServicio(self, codigo):

		if codigo=="" or codigo.isdigit() and len(codigo)<11:
			return True

		else:
			return False

	def soloNumeros(self, valor):

		if valor=="" or valor.isdigit():
			return True
		else:
			return False


class InterfazPrincipal:

	# ***POTTER: funcion para guardar las sugerencias o productos que solicitan y no hay.
	"""
	Interfaz genérica que contiene las operaciones comunes que se hacen en el negocio `PAPELERIA VALERIA`,
	Pago de servicios, recargas, compra de artículos y tareas administrativas.
	"""

	def __init__(self):
		self.raiz = Tk()
		self.raiz.focus_set()
		self.raiz.geometry("400x450+100+100")
		self.raiz.resizable(False,False)

		# creamos dos instancias de clase, para usar sus métodos y atributos.
		self.validaciones = Validaciones()
		self.conversiones = Conversiones()
		self.crearWidgets()
		self.raiz.mainloop()

	def crearWidgets(self):
		
		# CONTENDRÁ 
		self.listaCompra = pd.DataFrame(columns = ["NOMBRE", "PRECIO_UNIT", "CANTIDAD_COMPRA", "SUB_TOTAL", "UTILIDAD"])


		# ++ CREACIÓN WIDGETS; INTERFAZ PRINCIPAL: 

		Label(self.raiz, text=time.strftime("%d de %B")).place(relx=0.15,rely=0.03)
		Label(self.raiz, text="PAPELERÍA VALERIA").place(relx=0.5,rely=0.03)

		Label(self.raiz, text="OPERACIÓN").place(relx=0.05, rely=0.12)
		self.menuOperacion = ttk.Combobox(self.raiz, values = ["SERVICIO_PUBLICO","RECARGA","COMPRA","ADMINISTRACION", "SALDOS"], state="readonly")
		self.menuOperacion.place(relx=0.5,rely=0.12)

		self.frameOpciones = Frame(self.raiz)
		self.frameOpciones.place(rely=0.20, relx=0, relwidth=1, relheight=.80)



		# +++ MANEJO ATAJOS Y EVENTOS INTERFAZ PPAL:

		self.raiz.bind("<Escape>", lambda _ : self.raiz.destroy())
		self.raiz.bind("<Control-z>", lambda _ : self.menuOperacion.current(0))
		self.raiz.bind("<Control-x>", lambda _ : self.menuOperacion.current(1))
		self.raiz.bind("<Control-c>", lambda _ : self.menuOperacion.current(2))
		self.raiz.bind("<Control-v>", lambda _ : self.menuOperacion.current(3))
		self.raiz.bind("<Control-b>", lambda _ : self.menuOperacion.current(4))
		self.menuOperacion.bind("<<ComboboxSelected>>",lambda _:self.cambioOpcion(_))

	def cambioOpcion(self, event):

		# LIMPIEZA DEL FRAME ~OPCIONES~ 
		for i in self.frameOpciones.winfo_children():
			i.destroy()

		if self.menuOperacion.get()=="COMPRA":

			# si el check de ´incluir a saldos´ está activo, se agrega el nombre de la persona que va deber
			@conexiones.decoradorBaseDatos3
			def check(*args, **kwargs):

				cursor = kwargs["cursor"]
				conexion = kwargs["conexion"]
				tipo = args[0]
				if tipo == "SALDO":

					# si selecciona la opcion incluir a saldo, activa casillo cliente nuevo y el entry Uno de codigo cliente
					if self.boolAgregarASaldo.get():

						checkClienteNuevo.place(relx=0.6, rely=0.15)
						lblCodigoCliente.place(relx=0.05, rely=0.27)
						self.entCodigoCliente.place(relx=0.5, rely=0.27)
						validarCodigoCliente = self.entCodigoCliente.register(self.validaciones.codigoCliente)
						self.entCodigoCliente.config(validate="key", validatecommand=(validarCodigoCliente, "%P"))
						lblComentarioCliente.place(relx=0.05, rely=0.5)
						self.txtComentarioCliente.place(relx=0.5, rely=0.5, relwidth=.40, relheight=.08)

					else:

						checkClienteNuevo.place_forget()
						lblCodigoCliente.place_forget()
						self.entCodigoCliente.delete(0,END)
						self.entCodigoCliente.place_forget()
						lblComentarioCliente.place_forget()
						self.txtComentarioCliente.delete("1.0", "end")
						self.txtComentarioCliente.place_forget()

						if self.boolClienteNuevo.get():
							checkClienteNuevo.invoke()

				# si seleccionamos la casilla de nuevo cliente, se crea el entry del nombre al desactivarla se elimina
				elif tipo == "NUEVO":

					if self.boolClienteNuevo.get():
						self.entCodigoCliente.delete(0,END)
						codigo = self.generarCodigoCliente(cursor)
						self.entCodigoCliente.insert(0, codigo)
						self.entCodigoCliente.config(state="readonly")
						lblNombreCliente.place(relx=0.05, rely=0.39)
						self.entNombreCliente.place(relx=0.5, rely=0.39)
					else:
						lblNombreCliente.place_forget()
						self.entNombreCliente.delete(0,END)
						self.entNombreCliente.place_forget()

						self.entCodigoCliente.config(state="normal")
						self.entCodigoCliente.delete(0,END)

			def verificarLongitud(event):

				if len(codigoArticulo.get()) == 5:
					self.anhadirArticulo(codigoArticulo.get().upper())
					codigoArticulo.set("")

			def borrarCompra():
				self.listaCompra.drop(self.listaCompra.index, inplace=True)
				self.cantidadListaCompra.config(text=0)



			codigoArticulo = StringVar()
			codigoCliente = StringVar()
			nombreCliente = StringVar()
			self.facturaImpresa = BooleanVar()
			# comentario = StringVar()
			self.boolAgregarASaldo = BooleanVar()
			self.boolClienteNuevo = BooleanVar()

			facturaImpresa = Checkbutton(self.frameOpciones,text="Imprimir factura", variable = self.facturaImpresa, onvalue=1, offvalue=0)
			facturaImpresa.place(relx=0.3, rely=.03)

			lblCodigo = Label(self.frameOpciones, text="CÓDIGO ARTICULO").place(relx=0.05, rely=0.02)

			entCodigo = Entry(self.frameOpciones, textvariable = codigoArticulo, width=10)
			entCodigo.place(relx=0.50, rely=0.12)
			validarCodigo = entCodigo.register(self.validaciones.codigoArticulo)
			entCodigo.config(validate = "key", validatecommand = (validarCodigo,'%P'))
			entCodigo.bind("<KeyRelease>", lambda _:verificarLongitud(_))

			self.cantidadListaCompra = Label(self.frameOpciones, text = 0, borderwidth=10, font=7)
			self.cantidadListaCompra.place(relx=0.80, rely=0.02)

			self.checkIncluirSaldo = Checkbutton(self.frameOpciones, text = "INCLUIR A SALDO", variable = self.boolAgregarASaldo, onvalue = True, offvalue = False, command=lambda : check("SALDO"))
			self.checkIncluirSaldo.place(relx=0.05, rely=0.15)

			checkClienteNuevo = Checkbutton(self.frameOpciones, text = "CLIENTE NUEVO", variable = self.boolClienteNuevo, onvalue = True, offvalue = False, command=lambda: check("NUEVO"))
			
			lblCodigoCliente = Label(self.frameOpciones, text = "CODIGO CLIENTE")

			self.entCodigoCliente = Entry(self.frameOpciones, textvariable = codigoCliente)


			lblNombreCliente = Label(self.frameOpciones, text="NOMBRE CLIENTE")

			self.entNombreCliente = Entry(self.frameOpciones, textvariable = nombreCliente)

			lblComentarioCliente = Label(self.frameOpciones, text="COMENTARIO (opcional)")

			self.txtComentarioCliente = Text(self.frameOpciones)

			Button(self.frameOpciones,text="BORRAR COMPRA",command=borrarCompra).place(relx=0.42,rely=0.63)

			Button(self.frameOpciones, text="MODIFICAR", command=self.modificarArticulo).place(relx=0.1, rely=0.74)

			Button(self.frameOpciones, text="FINALIZAR", command= self.compra).place(relx=0.45, rely=0.74)

			Button(self.frameOpciones, text= "SALDOS", command=self.interfazSaldos).place(relx=0.80, rely=0.74)


	
		elif self.menuOperacion.get() == "SERVICIO_PUBLICO":

			# ***Aprender validate y validatecommand a profundidad


			def habilitarBtn(event, tipo):

				# *condicionar de acuerdo con el servicio que se vaya a pagar.
				if tipo=="GAS" and len(self.entCodigoServicio.get())==10 or tipo=="ENERGIA" and len(self.entCodigoServicio.get())==9 or tipo=="AGUA" and len(self.entCodigoServicio.get())==8:
					self.btnServicios.config(state="normal") 
					self.btnServicios.invoke()
					self.btnServicios.config(state="disabled")
				else:
					self.btnServicios.config(state="disabled")

					

			valorCodigoServicio = StringVar()

			Label(self.frameOpciones, text= "TIPO SERVICIO").place(relx=0.05, rely=0.02)
			tipoServicio = ttk.Combobox(self.frameOpciones, values =["GAS","ENERGIA","AGUA"], width=8, state="readonly")
			tipoServicio.place(relx=0.50, rely=0.02)
			tipoServicio.current(0)

			Label(self.frameOpciones, text="CÓDIGO FACTURA").place(relx=0.05, rely=0.15)
			self.entCodigoServicio = Entry(self.frameOpciones, textvariable = valorCodigoServicio)
			self.entCodigoServicio.place(relx=0.5, rely=0.15)

			self.btnServicios = Button(self.frameOpciones, text= "PAGAR SERVICIO", command=lambda : self.ejecutar(tipo=tipoServicio.get(), numero=valorCodigoServicio.get()), state = "disabled")
			self.btnServicios.place(relx=0.4, rely=0.65)

			# self.entCodigoServicio.bind("<KeyRelease>", self.validaciones.codigoServicio(tipoServicio.get(), self.entCodigoServicio.get()))
			# validarServicio = self.frameOpciones.register(self.validaciones.codigoServicio(tipo=tipoServicio.get(), boton=self.btnServicios))
			validarServicio = self.frameOpciones.register(self.validaciones.codigoServicio)
			self.entCodigoServicio.config(validate = "key", validatecommand =  (validarServicio,'%P' ))

			tipoServicio.bind("<<ComboboxSelected>>", lambda _: self.entCodigoServicio.delete(0,END))
			self.entCodigoServicio.bind("<KeyRelease>",lambda _ :habilitarBtn(_, tipoServicio.get()))

		elif self.menuOperacion.get()=="RECARGA":

			def habilitarRecarga(event):

				if len(self.entNumeroRecarga.get())==10 and len(self.entValorRecarga.get())>=4:
					btnRecarga["state"]="normal"

				else:

					btnRecarga["state"]="disabled"

			def cambioOperador(event):
				self.entNumeroRecarga.delete(0,END)
				self.entValorRecarga.delete(0, END)


			numeroCelular = StringVar()
			valorRecarga = StringVar()

			Label(self.frameOpciones, text="OPERADOR").place(relx=0.05, rely=0.02)
			tipoOperador = ttk.Combobox(self.frameOpciones, values=["CLARO", "MOVISTAR", "TIGO", "WOM", "VIRGIN", "ETB", "FLASH", "KALLEY"], width=10, state="readonly")
			tipoOperador.place(relx=0.50, rely=0.02)

			Label(self.frameOpciones, text= "NUMERO CELULAR").place(relx=0.05, rely=0.15)
			self.entNumeroRecarga = Entry(self.frameOpciones, textvariable = numeroCelular)
			self.entNumeroRecarga.place(relx=0.5, rely=0.15)
			validarNumero = self.entNumeroRecarga.register(self.validaciones.numeroCelular)
			self.entNumeroRecarga.config(validate = "key", validatecommand = (validarNumero, '%P'))

			Label(self.frameOpciones, text = "VALOR RECARGA").place(relx=0.05, rely=0.28)
			self.entValorRecarga = Entry(self.frameOpciones, textvariable= valorRecarga)
			self.entValorRecarga.place(relx=0.5, rely=0.28)
			validarValorRecarga = self.entValorRecarga.register(self.validaciones.valorRecarga)
			self.entValorRecarga.config(validate = "key", validatecommand = (validarValorRecarga, '%P'))

			btnRecarga = Button(self.frameOpciones, text = "REALIZAR RECARGA", command= lambda : self.ejecutar(numero = numeroCelular.get(), recarga = valorRecarga.get(), tipo = tipoOperador.get()), state="disabled")
			btnRecarga.place(relx=0.4, rely=0.7)

			self.entValorRecarga.bind("<KeyRelease>", lambda _:habilitarRecarga(_))
			tipoOperador.bind("<<ComboboxSelected>>", lambda event:cambioOperador(event))

		elif self.menuOperacion.get()=="ADMINISTRACION":
			InterfazAdministrativa(self.raiz)

		elif self.menuOperacion.get() == "SALDOS":
			self.interfazSaldos()

	@conexiones.decoradorBaseDatos3
	def generarCodigoCliente(*args, **kwargs):
		"""
		CÁLCULA: el código siguiente (cliente nuevo), para que no haya conflicto de clientes
		"""
		cursor = kwargs["cursor"]
		conexion = kwargs["conexion"]
		cursor.execute("SELECT CLIENTE FROM SALDOS")
		return str(len(set([x[0] for x in cursor.fetchall()]))).zfill(2)

	def rescatarSaldos(*args):

		'''
		RETORNA data frame con los clientes que deben. 
		'''
		self = args[0]
		cursor = args[1]

		cursor.execute("SELECT CLIENTE, NOMBRE, CONCEPTO, SALDO, ABONO, COMENTARIO FROM SALDOS")
		saldos = cursor.fetchall()

		# Obtengo los códigos únicos, para listarlos y ordenarlos. 
		codigos = list(set(x[0] for x in saldos))
		codigos.sort()
		df_saldos = pd.DataFrame(data=[[x, "", "", 0, 0, ""] for x in codigos],columns=["CODIGO", "NOMBRE", "CONCEPTO", "SALDO", "ABONO", "COMENTARIO"])

		# ORGANIZO la info de la BBDD en el DataFrame
		for saldo in saldos:

			for indice, data in df_saldos.iterrows():

				if saldo[0] == data.iloc[0]:

					# Si el saldo del moroso NO es cero, agregamos el concepto, de los contrario registramos como saldado.
					# NOTA: sólo debe haber un registro como saldado en la BBDD
					if saldo[3]!=0:

						# si es la primera factura, la agregamos el concepto tal cual.
						if df_saldos.loc[indice,"NOMBRE"]=="":

							df_saldos.loc[indice,"CONCEPTO"]=saldo[2]
							df_saldos.loc[indice,"SALDO"]=saldo[3]

						# si no (es la segunda vez o más), le agregamos un separador.
						else:

							df_saldos.loc[indice,"CONCEPTO"]+="/"+saldo[2]
							df_saldos.loc[indice,"SALDO"]+=saldo[3]

					# si el saldo de la BBDD es cero, le agregamos saldado al concepto.
					# ACLARACIÓN: Solo debe haber un registro como saldado (el cliente no debe nada).
					else:

						df_saldos.loc[indice,"CONCEPTO"]="SALDADO"

					if len(saldo[-1]) >= 3:

								df_saldos.loc[indice, "COMENTARIO"] += saldo[5]

					# el saldo siempre se suma, el nombre y el abono en todos los registros será el mismo
					df_saldos.loc[indice,"NOMBRE"]=saldo[1]
					# df_saldos.loc[indice, "SALDO"]+=saldo[3]
					df_saldos.loc[indice, "ABONO"] = saldo[4]

					# al coincidir el elemento de la lista con el del df, rompemos y continuamos con el siguiente registro de la BBDD
					break

		return df_saldos

	@conexiones.decoradorBaseDatos3
	def interfazSaldos(*args, **kwargs):

		# *FUTURO: Cambiar los íconos internos de las ventanas de dialogo (se decd documents be crear una clase propio heredando de <Toplevel>)
		
		'''
		 MUESTRA la información de los clientes morosos o que han tenido saldo en el negocio.
		 Métodos:
		 	borrarEntradas --> Borra las entradas de ABONO y AGREGAR a saldo.
		 	actualizarDetalle ---> Rellena la información detallada (Panel Derecho) del cliente seleccionado.
		 	abonarSaldo ---> Realiza las modificaciones en la BBDD de acuedo al abono parcial,total o a la suma de saldo nuevo a traves de `interfazSaldos`.
		 	agregarSaldo --> Añade saldo desde esta interfaz y no desde compras.
		'''

		def borrarEntradas():
			entAbonoCliente.delete(0, "end")
			entAgregarSaldo.delete(0, "end")

		@conexiones.decoradorBaseDatos3
		def actualizarDetalle(*args, **kwargs):

			'''
			ACTUALIZACIÓN: de toda la interfaz, luego de abonar, saldar || agregar a la cuenta
			HABILITACIÓN (OPCIONAL): botones y caja de texto (sólo si el cliente debe o lo que es lo mismo, el saldo pendiente sea diferente de 0). 
			<pandas.DataFrame datos> = COLUMNS: "CODIGO" "NOMBRE" "CONCEPTO" SALDO ABONO "COMENTARIO"
			<pandas.Series dato_seleccion> = COLUMNS :["CODIGO" "NOMBRE" "CONCEPTO" SALDO ABONO "COMENTARIO"]
			<list valor_concepto> = [(CANTIDAD "NOMBRE_ARTICULO" PRECIO_TOTAL), ...]
			<list valor_comentario> = ("PRIMERA LINEA", "SEGUNDA LINEA", ...)
			'''
			cursor = kwargs["cursor"]
			conexion = kwargs["conexion"]

			# BORRAMOS ENTRADAS 
			borrarEntradas()

			# DEFINICIÓN DE VARIABLES.
			datos = self.rescatarSaldos(cursor)
			dato_seleccion = datos.iloc[tree.item(tree.selection())["values"][0]]
			valor_concepto = [i.split() for i in dato_seleccion.loc["CONCEPTO"].replace("/","~").split("~")]
			valor_comentario = dato_seleccion.loc["COMENTARIO"].replace("\t","").replace("\n","}").split("}")

			# ACTUALIZCION VALORES.
			tree.item(tree.selection(),values = (dato_seleccion.loc["CODIGO"], dato_seleccion.loc["NOMBRE"], dato_seleccion.loc["CONCEPTO"], self.conversiones.puntoMilConSimbolo(dato_seleccion.loc["SALDO"]- dato_seleccion.loc["ABONO"]), dato_seleccion.loc["ABONO"], dato_seleccion.loc["COMENTARIO"]))
			codigo["text"]=dato_seleccion.loc["CODIGO"]
			nombre["text"]=dato_seleccion.loc["NOMBRE"]

			# ELIMINACIÓN; evitando una remontada, e INSERCCIÓN CONCEPTO (HABILITACION: de botones) .
			concepto.delete(*concepto.get_children())

			if dato_seleccion.loc["SALDO"]!=0: 

				btnSaldarCliente["state"]="normal"
				btnAbonoCliente["state"]="normal"
				entAbonoCliente["state"]="normal"

				for i in valor_concepto:
					concepto.insert("", END, values=i)
					
			else:

				btnAbonoCliente["state"]="disabled"
				entAbonoCliente["state"]="disabled"
				btnSaldarCliente["state"]="disabled"

				concepto.insert("", END, values=["-", "SALDADO", "-"])

			saldoInicial["text"]=self.conversiones.puntoMilConSimbolo(dato_seleccion.loc["SALDO"]) 
			abono["text"]=self.conversiones.puntoMilConSimbolo(dato_seleccion.loc["ABONO"])
			saldoTotal["text"]=self.conversiones.puntoMilConSimbolo(dato_seleccion.loc["SALDO"] - dato_seleccion.loc["ABONO"])

			# ELIMINACIÓN; evitando una remontada, e INSERCCIÓN COMENTARIO
			comentario.delete(0, "end")

			for i in valor_comentario:
				# Agregamos de a 30 caracteres por linea
				for k in range(0, len(i), 30):
					comentario.insert("end", i[k:k+30])
			
			comentario.activate(2)


		@conexiones.decoradorBaseDatos3
		def abonarSaldo(*args, **kwargs): 

			'''
			<str tipo> = "SALDAR" || "ABONAR"
			<list valor_seleccion> = ['COD_CLIENTE', 'NOMBRE_CLIENTE', 'CONCEPTO', SALDO, ABONO, "COMENTARIO"]
			'''
			conexion = kwargs["conexion"]
			cursor = kwargs["cursor"]
			valor_seleccion = tree.item(tree.selection())["values"]

			if args[0] == "SALDAR":

				# CAPTURA: código última factura (para asignarle al estado "SALDADO")
				cursor.execute("SELECT FACTURA FROM SALDOS WHERE CLIENTE = (?) ORDER BY FACTURA DESC",(str(valor_seleccion[0]).zfill(2),))
				codigo_fact = cursor.fetchone()

				# BORRADO Y ACTUALIZACIÓN: en BBDD.
				cursor.execute("DELETE FROM SALDOS WHERE CLIENTE = (?)", (str(valor_seleccion[0]).zfill(2),))
				cursor.execute("INSERT INTO SALDOS(CLIENTE, NOMBRE, FACTURA, CONCEPTO, SALDO, COMENTARIO) VALUES (?,?,?,?,?,?)",(str(valor_seleccion[0]).zfill(2), valor_seleccion[1], codigo_fact[0], "SALDADO", 0, "NULL") )

				messagebox.showinfo("PAGO EXITOSO", "Se saldó la cuenta con {} exitosamente".format(valor_seleccion[1]), parent=interfaz)

				conexion.commit()
				actualizarDetalle(None)

			elif args[0] == "ABONAR":

				try:

					if entAbonoCliente.get()=="":

						raise ValueError("La entrada está vacía.\nDigíta un valor.")
						return

					# VERIFICACIÓN: del criterio de la EntryUser (divisible por 50)
					elif int(entAbonoCliente.get())%50==0:

						codigo_cliente = str(valor_seleccion[0]).zfill(2)

						# OBTENCIÓN: del saldo de cada factura más sus códigos y el abono (que en todas debe ser el mismo)
						cursor.execute("SELECT SALDO, FACTURA, ABONO FROM SALDOS WHERE CLIENTE = (?)",(codigo_cliente,))
						info_bd = cursor.fetchall()

						# DEFINICIÓN VARIABLES:
						valor_abonar = int(entAbonoCliente.get())
						saldo_total = sum([i[0] for i in info_bd])
						abono_bd = info_bd[0][2]

						# VERIFICACIÓN VALIDEZ: el valor a abonar debe ser el mismo o menor que el saldo más lo abonado.
						if valor_abonar <= saldo_total - abono_bd:

							# En igualdad de valores, se llama de vuelta la función pero con el argumento `SALDAR`
							if valor_abonar == saldo_total - abono_bd:

								abonarSaldo("SALDAR")

							else:

								# ACTUALIZACIÓN: valores cliente seleccionado; tanto en BBDD como en la Interfaz.
								cursor.execute("UPDATE SALDOS SET ABONO =(?) WHERE CLIENTE = (?)", (abono_bd+valor_abonar, codigo_cliente))
						else:

							raise ValueError("No se puede abonar más del saldo pendiente.\nSaldo pendiente: {}".format(self.conversiones.puntoMilConSimbolo(saldo_total-abono_bd)))
							return
					else:

						raise ValueError("Digita un valor válido.")
						return

				except ValueError as e:

					messagebox.showwarning("ERROR", "{}".format(e), parent=interfaz)
					return

				finally:

					borrarEntradas()

				# ACTUALIZACIÓN interfaz Y LIMPIEZA entradas:
				conexion.commit()
				actualizarDetalle(None)

		@conexiones.decoradorBaseDatos3
		def agregarSaldo(*args, **kwargs):
			'''
			<list valor_seleccion> = ['COD_CLIENTE', 'NOMBRE_CLIENTE', 'CONCEPTO', SALDO, ABONO, "COMENTARIO"]
			<int valor> --> valor a añadir
			'''
			cursor = kwargs["cursor"]
			conexion = kwargs["conexion"]
			valor_seleccion = tree.item(tree.selection())["values"]

			try:
				valor = int(valorAgregar.get())

				if not valor % 50 == 0:
					raise ValueError("Digita un valor correcto.")
				else:
					# COMPROBACIÓN: 
					cod_seleccion = str(valor_seleccion[0]).zfill(2)

					# CAPTURAMOS el último código de factura y lo modificamos para que sea el cod_factura siguiente.
					cursor.execute("SELECT FACTURA FROM SALDOS ORDER BY FACTURA DESC")
					cod_fact_sgte = cursor.fetchone()[0]+1

					cursor.execute("SELECT CONCEPTO FROM SALDOS WHERE CLIENTE = (?)", (cod_seleccion,))
					concepto_seleccion = cursor.fetchone()[0]

					# EVITAMOS: remontada, cuando el cliente actualmente NO debe nada (que es cuando el concepto es saldado)
					if concepto_seleccion == "SALDADO":
						cursor.execute("DELETE FROM SALDOS WHERE CLIENTE =(?)", (cod_seleccion,))

					ventana_nueva = simpledialog.askstring(title="COMENTRIO SALDO NUEVO", prompt="Ingresa el comentario que acompañará el saldo nuevo:", parent=interfaz, initialvalue="")		

					if ventana_nueva == None or ventana_nueva == "" or len(ventana_nueva) <= 4:
						comentario_nuevo = "{}{}\n".format(datetime.date.today().strftime('%d/%m: SALDO NUEVO '),self.conversiones.puntoMilConSimbolo(valor)).upper()
					else:
						comentario_nuevo = "{} {} {}\n".format(datetime.date.today().strftime('%d/%m:'),ventana_nueva,self.conversiones.puntoMilConSimbolo(valor)).upper()

					cursor.execute("INSERT INTO SALDOS (CLIENTE, NOMBRE, FACTURA, CONCEPTO, SALDO, ABONO, COMENTARIO) VALUES (?,?,?,?,?,?,?)", (cod_seleccion, valor_seleccion[1], cod_fact_sgte, "0 SALDO_NUEVO {}".format(valor), valor, valor_seleccion[4], comentario_nuevo ))
					messagebox.showinfo(title="OPERACIÓN EXITOSA", message= "Saldo nuevo agregado con éxito.", parent=interfaz)

					# ACTUALIZACION: de interfaz
					conexion.commit()
					actualizarDetalle()

			except ValueError as e:
				messagebox.showwarning(title="ERROR", message= "{}".format(e), parent=interfaz)
			
			# finally:
			# 	borrarEntradas()				

		def disable_selection(event):
			comentario["activestyle"]="none"
			comentario.select_clear(0, END)

		# Declaramos self para tratar posteriormente y cursor y conexion para trabajar con la BBDD
		self = args[0]
		cursor = kwargs["cursor"]
		conexion = kwargs["conexion"]

		# <pandas.DataFrame datos> = columns:["CODIGO", "NOMBRE", "CONCEPTO", SALDO, ABONO, "COMENTARIO"]
		# CREACION ventana para mostrar los morosos y su información respectiva
		interfaz = Toplevel(self.raiz)
		interfaz.geometry("900x600+50+50")
		interfaz.focus_set()
		interfaz.bind("<Escape>", lambda _ : interfaz.destroy())

		# Creamos las variables para guardar las entradas del usuario.
		valorAbono = StringVar()
		valorAgregar = StringVar()

		# EXPERIMENTAL: método para bloquear la Interfaz presente.
		interfaz.grab_set()
		# interfaz.wm_attributes("-topmost", True)

		# PANEL DERECHO:
		info_saldos = Frame(interfaz)
		info_saldos.place(relx=0.5, relwidth=0.48, rely=0.02, relheight=0.96)

		# Creamos la estructura del lado derecho de la ventana
		Label(info_saldos, text="CODIGO CLIENTE", width = 15, anchor="e").place(relx=0.05, rely=0.04)
		Label(info_saldos, text="NOMBRE CLIENTE", width=15, anchor="e").place(relx=0.05, rely=0.15)
		Label(info_saldos, text="CONCEPTO", width=15, anchor="e").place(relx=0.05, rely=.26)
		Label(info_saldos, text="SALDO INICIAL", width=15, anchor="e").place(relx=0.05, rely=.45)
		Label(info_saldos, text="ABONO", width=15, anchor="e").place(relx=0.5, rely=.45)
		Label(info_saldos, text="SALDO TOTAL", width=15, anchor="e").place(relx=0.32, rely=.53)
		Label(info_saldos, text="COMENTARIO", width=15, anchor="e").place(relx=0.05, rely=.63)

		codigo = Label(info_saldos, width=15, anchor="center")
		codigo.place(relx=0.50, rely=0.04)

		nombre = Label(info_saldos, width=25, anchor="center")
		nombre.place(relx=0.5, rely=0.15)

		# Arbol ubicado en el panel derecho.
		concepto = ttk.Treeview(info_saldos, columns=("CANTIDAD", "ARTICULO", "PRECIO"), selectmode=NONE)
		concepto.place(relx=0.45, rely=.26, relwidth=0.45, relheight=0.17)

		concepto.column("#0", width=0, stretch=NO)
		concepto.column("CANTIDAD", width=20, anchor = "e", stretch=NO)
		concepto.column("ARTICULO",width=50, anchor = "e")
		concepto.column("PRECIO", width=30, anchor = "e")

		concepto.heading("CANTIDAD", text="Q", anchor = "e")
		concepto.heading("ARTICULO", text="ARTICULO", anchor = "e")
		concepto.heading("PRECIO", text="PRECIO", anchor = "e")

		saldoInicial = Label(info_saldos, width=15, anchor="center")
		saldoInicial.place(relx=0.08, rely=.49)

		abono = Label(info_saldos, width=15, anchor="center")
		abono.place(relx=0.58, rely=.49)

		saldoTotal = Label(info_saldos, width =15, anchor ="center")
		saldoTotal.place(relx=0.36, rely=0.57)

		comentario = Listbox(info_saldos)
		comentario.place(relx=0.43, rely=0.65, relwidth=0.47, relheight=0.10)

		comentario.bind("<<ListboxSelect>>", disable_selection)

		# BARRA DESPLAZAMIENTO de comentario.
		scrollbar_y = Scrollbar(info_saldos, orient="vertical",  command=comentario.yview)
		comentario.config(yscrollcommand=scrollbar_y.set)
		scrollbar_y.place(relx=.9, rely=.65, relwidth=0.03, relheight=0.1)

		# BOTONES Y USERENTRY:

		entAgregarSaldo = Entry(info_saldos, width=25, textvariable = valorAgregar , validate = "key", validatecommand= (info_saldos.register(self.validaciones.soloNumeros),"%P"))
		entAgregarSaldo.place(relx=0.32, rely=0.78)

		# *Cuando se presione salga una ventana emergente (previa validacion de cantidad a agregar) que pregunte si va agregar algún comentario
		btnAgregarSaldo = Button(info_saldos, text="AGREGAR SALDO", width=14, command = agregarSaldo)
		btnAgregarSaldo.place(relx=0.68, rely=0.78)

		entAbonoCliente = Entry(info_saldos, width=15, textvariable = valorAbono , validate = "key", validatecommand= (info_saldos.register(self.validaciones.soloNumeros),"%P"))
		entAbonoCliente.place(relx=0.34, rely=0.86)

		btnAbonoCliente = Button(info_saldos, text="ABONAR", width=10, command = lambda : abonarSaldo("ABONAR"))
		btnAbonoCliente.place(relx=0.68, rely=0.86)

		btnSaldarCliente = Button(info_saldos, text="SALDAR", width=10, command = lambda : abonarSaldo("SALDAR"))
		btnSaldarCliente.place(relx=0.45, rely=0.94)


		# PANEL IZQUIERDO: Información general de morosos o que han tenido cuenta (CÓDIGO - NOMBRE - SALDO).
		tree = ttk.Treeview(interfaz, columns=('COD_CLIENTE', 'NOMBRE_CLIENTE', 'CONCEPTO', "SALDO", "ABONO", "COMENTARIO"), selectmode=BROWSE)
		tree.place(relx=0.02, relwidth=0.48, rely=0.02, relheight=0.96)

		# Cada que se seleccione un cliente se actualiza el panel derecho
		tree.tag_bind("clienteSeleccionado", "<<TreeviewSelect>>", lambda event: actualizarDetalle(event))

		# CONFIGURACIÓN COLUMNAS: las que tienen `width = 0 && stretch = NO` se ocultan.
		tree.column('#0', width=0, anchor=CENTER, stretch=NO)
		tree.column('COD_CLIENTE', anchor=CENTER, width=50)
		tree.column('NOMBRE_CLIENTE', anchor=CENTER, width=110)
		tree.column('CONCEPTO', anchor=CENTER, width=0, stretch=NO)
		tree.column('SALDO', anchor=CENTER, width=80)
		tree.column('ABONO', anchor=CENTER, width=0, stretch=NO)
		tree.column("COMENTARIO", anchor=CENTER, width = 0, stretch=NO)

		# CONFIGURACIÓN ENCABEZADOS.
		tree.heading('COD_CLIENTE', text='CODIGO', anchor=CENTER)
		tree.heading('NOMBRE_CLIENTE', text='NOMBRE', anchor=CENTER)
		tree.heading('SALDO', text='SALDO TOTAL', anchor=CENTER)


		# RESCATE E INSERCCIÓN DE DATOS.
		datos = self.rescatarSaldos(cursor)
		for i in range(len(datos)):
			# iid -> CÓDIGO DEL CLIENTE (tipo str)
			tree.insert('', 'end', iid= datos.iloc[i,0], values=(str(datos.iloc[i, 0]).zfill(2), datos.iloc[i, 1], datos.iloc[i, 2], self.conversiones.puntoMilConSimbolo(datos.iloc[i, 3]- datos.iloc[i, 4]) , datos.iloc[i, 4], datos.iloc[i, 5]), tags=("clienteSeleccionado",))

		# SELECCIÓN AUTOMÁTICA: cada que se crea el <Toplevel>.
		tree.selection_set("00")

		# ACTUALIZACIÓN PANEL DERECHO:
		# Pasamos como argumento `None` ya que la funcion nos pide un parámetro posicional (sería self dentro del módulo: `conexiones.py`)
		actualizarDetalle()


	def ejecutar(self, **kwargs):

		# error = messagebox.showwarning(title="ERROR", message="No es posible realizar la recarga, verifica que todo esté en orden.")

		# Si la operación es pago de servicios, ejecuta este código:
		if self.menuOperacion.get() == "SERVICIO_PUBLICO":

			# Aquí debe ir la verificación de los patrones de los servicios. Para rellenar la página respectivamente.

			if kwargs["numero"]!="":

				print(kwargs["numero"])
				if kwargs["tipo"]=="GAS":
					print("remitir a la página con los datos del gas")
				elif kwargs["tipo"] == "ENERGIA":
					print("remitir a la página con los datos de la energia")
				else:
					print('Remitir con datos de Agua')
				self.entCodigoServicio.delete(0, END)


		# Para realizar recargas
		elif self.menuOperacion.get() == "RECARGA":

			# $CUANTO ES LO MÍNIMO DE RECARGA Y EL MÍNIMO COMUN DIVISR.
			# if self.entCodigo.get().isdigit() and len(self.entCodigo.get())==10 and self.entOperadorValor.get().isdigit() and (int(self.entOperadorValor.get())%500)==0:
			numeroCelular = kwargs["numero"]
			valorRecarga = kwargs["recarga"]
			operador = kwargs["tipo"]
			if numeroCelular.isdigit() and len(numeroCelular)==10 and valorRecarga.isdigit() and int(valorRecarga)%1000==0:

				
				if operador=="CLARO":
					print("recarga claro")

				elif operador=="MOVISTAR":
					print("recarga movistar")

				elif operador=="TIGO":
					print("recarga tigo")

				elif operador=="WOM":
					print("recarga wom")

				elif operador=="VIRGIN":
					print("recarga virgin")

				elif operador=="ETB":
					print("recarga etb")

				elif operador=="FLASH":
					print("recarga flash")

				elif operador=="KALLEY":
					print("recarga kalley")

				self.entNumeroRecarga.delete(0, END)
				self.entValorRecarga.delete(0, END)

			else:
				self.entNumeroRecarga.delete(0, END)
				self.entValorRecarga.delete(0, END)

				messagebox.showwarning(title="ERROR", message="No es posible realizar la recarga, verifica que todo esté en orden.")

	@conexiones.decoradorBaseDatos3
	# def anhadirArticulo(self, cursor, conexion, codigo):
	def anhadirArticulo(*args, **kwargs):

		# FORMATO: <pd.DataFrame self.listaCompra> = columns = ["NOMBRE", "PRECIO_UNIT", "CANTIDAD_COMPRA", "SUB_TOTAL", "UTILIDAD"]
		# FORMATO: <articulo pd.Series> = nombre -> CODIGO / data -> [ "NOMBRE" "PRECIO_UNIT" "CANTIDAD_STOCK" "UTILIDAD"]

		self = args[0]
		codigo = args[1]
		cursor = kwargs["cursor"]
		conexion = kwargs["conexion"]

		cursor.execute("SELECT CODIGO, ARTICULO, PRECIO, STOCK, UTILIDAD FROM INVENTARIO WHERE CODIGO = (?)", (codigo.upper(), ))

		# Obtenemos el articulo que deseamos agregar
		articulo = cursor.fetchone()

		if articulo == None:
			messagebox.showwarning(title= "ERROR", message= f"No existe artículo con ese código.")
			return


		# FORMATO: <articulo pd.Series> = ["CODIGO" "NOMBRE" "PRECIO_UNIT" "CANTIDAD_STOCK" "UTILIDAD"]
		articulo = pd.Series(data = articulo[1:], name = articulo[0], index = [ "NOMBRE", "PRECIO_UNIT", "CANTIDAD_STOCK", "UTILIDAD"])

		# si `articulo` == None (cuando no está el codigo en BBDD), el tipo de dato en campo  `NOMBRE` será `numpy.float64` debido a que es el tipo de datos
		# que toman cuando los valores son None
		
		# if isinstance(articulo.loc["NOMBRE"],numpy.float64): 
		# if isinstance(articulo.loc["NOMBRE"],numpy.float64): 

		# 	messagebox.showwarning(title= "ERROR", message= f"No existe artículo con ese código.")

		# else:


		if articulo["CANTIDAD_STOCK"] > 0:

			# COMPROBACIÓN: presencia en el carrito de compras.
			if articulo.name in self.listaCompra.index.tolist():

					if articulo["CANTIDAD_STOCK"] >= (self.listaCompra.at[articulo.name,"CANTIDAD_COMPRA"]+1):
						
						# copiar la información del articulo a modificar.
						articulo_modificar = self.listaCompra.loc[articulo.name,:]

						# linea para omitir la advertencia de pandas.Dataframe sobre la reasignacion de valores
						pd.options.mode.chained_assignment = None

						# Realizar las modificaciones pertinentes.
						articulo_modificar.at["CANTIDAD_COMPRA"] += 1
						articulo_modificar.at["SUB_TOTAL"] = articulo_modificar.at["PRECIO_UNIT"] * articulo_modificar.at["CANTIDAD_COMPRA"]
						articulo_modificar.at["UTILIDAD"] = int(articulo_modificar.at["UTILIDAD"]/(articulo_modificar.at["CANTIDAD_COMPRA"]-1)*articulo_modificar.at["CANTIDAD_COMPRA"])

						# actualizar la lista con el articulo modificado.
						self.listaCompra.loc[articulo.name, [ "NOMBRE", "PRECIO_UNIT", "CANTIDAD_COMPRA", "SUB_TOTAL", "UTILIDAD"]] = articulo_modificar
					else:
						messagebox.showwarning(title = "STOCK AGOTADO", message = "No hay unidades de {} disponibles.".format(articulo["NOMBRE"].upper()))

			else:

				# agregamos el campo de subtotal que es equival al precio unitario:
				articulo = pd.concat([articulo, pd.Series(data = [articulo["PRECIO_UNIT"]], index = ["SUB_TOTAL"], name= articulo.name)])

				# Organizamos el orden de los campos:
				articulo = articulo.reindex([ "NOMBRE", "PRECIO_UNIT", "CANTIDAD_STOCK", "SUB_TOTAL", "UTILIDAD"])

				# renombramos correctamente los campos:
				articulo.index = [ "NOMBRE", "PRECIO_UNIT", "CANTIDAD_COMPRA", "SUB_TOTAL", "UTILIDAD"] 

				# Cambiamos el valor de la cantidad en stock por uno; que es la unidad del articulo que se va a comprar:
				articulo.at["CANTIDAD_COMPRA"]=1

				# se crea un df para asignarle índice que corresponde al código del producto
				df_articulo = articulo.to_frame().T
				df_articulo.index = [articulo.name]

				# Agregamos el artículo nuevo en la lista:
				self.listaCompra = pd.concat([self.listaCompra, df_articulo], axis= 0, ignore_index=False)

				self.cantidadListaCompra.config(text=len(self.listaCompra))
				# print(self.listaCompra)

		else:

			messagebox.showwarning(title="PROBLEMA", message= f"No hay {articulo.loc['NOMBRE']} en stock.")
		
	@conexiones.decoradorBaseDatos3
	def modificarArticulo(*args, **kwargs):

		"""
		INTERFAZ para visualizar y modificar el carrito de compra.
		"""

		# ?Cuando selecciono otra acción general, la lista permanece intacta (¿? Analizar si es bueno o no)
		# *Boton para eliminar articulo seleccionado
		# *Botón para comprar desde la interfaz
		# *Al posarse sobre el boton aumentar cuando no haya stock me salga una advertencia y se quite cuando ya no se pose sobre el boton

		def seleccionArticulo(*args, **kwargs):
			# cuando no se puede sumar mas
			if treeVista.get_children():

				codigo = treeVista.selection()[0]

				if validacion[codigo][0] == validacion[codigo][1]:
					btnAumentar["state"]= "disabled"

					# tooltip = ttk.Label(btnAumentar, text="Ya no hay stock", background="#ffffe0", relief="solid")
					# tooltip.place(in_=btnAumentar, relx=0.5, rely=1.2, anchor="n")
					# btnAumentar.tooltip = tooltip

				else:
					btnVaciarCarrito["state"] = "normal"
					btnAumentar["state"] = "normal"
					btnDisminuir["state"] = "normal"

		def salir(event):

			print("chao")
			conexion.commit()
			cursor.close()
			conexion.close()
			interfazArticulos.destroy()

		def actualizarVista(*args):

			# Este condicional es empleado cuando se borra el último articulo del carrito de compra
			if args:

				vaciarCarrito()
				return

			if len(self.listaCompra) == 0:

				btnVaciarCarrito["state"] = "disabled"
				btnAumentar["state"] = "disabled"
				btnDisminuir["state"] = "disabled"


			if len(self.listaCompra) != 0:

				treeVista.delete(*treeVista.get_children())
				valorTotal = self.listaCompra.loc[:,"SUB_TOTAL"].sum()

				contador = 1

				for indice in self.listaCompra.index.tolist():
					treeVista.insert("","end", iid = indice, values = (contador, indice, self.listaCompra.at[indice,"NOMBRE"],self.listaCompra.at[indice,"PRECIO_UNIT"], self.listaCompra.at[indice,"CANTIDAD_COMPRA"], self.listaCompra.at[indice,"SUB_TOTAL"]))
					contador += 1

				lblTotal["text"] = self.conversiones.puntoMilConSimbolo(valorTotal) 

				treeVista.selection_set(treeVista.get_children()[0])


		def vaciarCarrito():

			treeVista.delete(*treeVista.get_children())

			self.listaCompra.drop(self.listaCompra.index, inplace=True)
			self.cantidadListaCompra.config(text=0)		
			btnAumentar["state"]="disabled"
			btnDisminuir["state"]="disabled"
			btnVaciarCarrito["state"] = "disabled"

		def modificarCantidad(tipo):
			# FORMATO: <pd.DataFrame self.listaCompra> = columns = ["NOMBRE", "PRECIO_UNIT", "CANTIDAD_COMPRA", "SUB_TOTAL", "UTILIDAD"]
			

			codigo = treeVista.selection()[0]

			if tipo == "MAS":
				# if validacion[codigo][0] > self.listaCompra.at[codigo, "CANTIDAD_COMPRA"]:
				# MODIFICAR en el carrito la cantidad de compra, y por consiguiente el sub_total 
				self.listaCompra.at[codigo, "CANTIDAD_COMPRA"] += 1
				self.listaCompra.at[codigo, "SUB_TOTAL"] = self.listaCompra.at[codigo, "CANTIDAD_COMPRA"] * self.listaCompra.at[codigo, "PRECIO_UNIT"]
				# MODIFICAR el item correspondiente en la interfaz
				valores = treeVista.item(codigo)["values"]
				treeVista.item(codigo, values = [valores[0],valores[1],valores[2],valores[3], valores[4]+1,valores[3]*(valores[4]+1)])
				# treeVista.item(codigo, values = self.listaCompra.loc[codigo, : ].tolist())
			else:
				if validacion[codigo][1]==1:

					pregunta = messagebox.askquestion(title="CONFIRMACIÓN", message = "Deseas eliminar éste artículo del carrito?", parent=interfazArticulos)
					if pregunta =="yes":
						validacion.pop(codigo)
						self.listaCompra = self.listaCompra.drop(codigo)
						# *actualizar la vista sin el artículo eliminado
						actualizarVista("VACIA") if len(self.listaCompra) == 0 else actualizarVista()
						return
				else:
					self.listaCompra.at[codigo, "CANTIDAD_COMPRA"] -= 1
					self.listaCompra.at[codigo, "SUB_TOTAL"] = self.listaCompra.at[codigo, "CANTIDAD_COMPRA"] * self.listaCompra.at[codigo, "PRECIO_UNIT"]
					# MODIFICAR el item correspondiente en la interfaz
					valores = treeVista.item(codigo)["values"]
					treeVista.item(codigo, values = [valores[0],valores[1],valores[2],valores[3], valores[4]-1,valores[3]*(valores[4]-1)])

			validacion[codigo][1] = self.listaCompra.at[codigo, "CANTIDAD_COMPRA"]
			lblTotal["text"] = self.conversiones.puntoMilConSimbolo(self.listaCompra.loc[:,"SUB_TOTAL"].sum())
			print(validacion)
			seleccionArticulo(None)
									
		self = args[0]
		conexion = kwargs["conexion"]
		cursor = kwargs["cursor"]
		# conexion = sqlite3.connect("BASE_DATOS_PRUEBA.db")
		# cursor = conexion.cursor()

		interfazArticulos = Toplevel()
		interfazArticulos.bind("<Escape>", lambda _ : salir(_))

		interfazArticulos.focus_set()
		interfazArticulos.grab_set()
		interfazArticulos.geometry("500x500")

		treeVista = ttk.Treeview(interfazArticulos, columns = ("ITEM", "CODIGO", "NOMBRE", "PRECIO", "CANTIDAD", "TOTAL"))
		treeVista.place(relx=0.02, relwidth=0.85, rely=0.02, relheight= 0.86)

		treeVista.bind("<<TreeviewSelect>>", lambda event:seleccionArticulo(event))

		Label(interfazArticulos, text = "CANTIDAD", width = 15).place(relx=0.88, rely=0.02)

		btnAumentar = Button(interfazArticulos, text="+", borderwidth = 0, command=lambda : modificarCantidad("MAS"))
		btnAumentar.place(relx=0.92, rely=0.08)


		btnDisminuir = Button(interfazArticulos, text="-", borderwidth = 0, command= lambda : modificarCantidad("MENOS"))
		btnDisminuir.place(relx=0.92, rely=0.12)

		btnVaciarCarrito = Button(interfazArticulos, text = "VACIAR CARRITO", width = 12, command = vaciarCarrito)
		btnVaciarCarrito.place(relx= 0.2, rely = 0.92)

		Label(interfazArticulos, text = "TOTAL:", width = 10).place(relx = 0.60, rely = 0.92)

		lblTotal = Label(interfazArticulos)
		lblTotal.place(relx = 0.77, rely = 0.92)

		treeVista.column("#0", width=0, stretch=NO)
		treeVista.column("ITEM", width = 10, anchor = "center")
		treeVista.column("CODIGO", width = 10, anchor = "center")
		treeVista.column("NOMBRE", width = 10, anchor = "center")
		treeVista.column("PRECIO", width = 10, anchor = "center")
		treeVista.column("CANTIDAD", width = 10, anchor = "center")
		treeVista.column("TOTAL", width = 10, anchor = "center")

		treeVista.heading("ITEM", text = "ITEM")
		treeVista.heading("CODIGO", text="CODIGO")
		treeVista.heading("NOMBRE", text = "NOMBRE")
		treeVista.heading("PRECIO", text = "PRECIO")
		treeVista.heading("CANTIDAD", text = "CANTIDAD")
		treeVista.heading("TOTAL", text = "TOTAL")

		actualizarVista()
		codigos = self.listaCompra.index.tolist()
		cursor.execute("SELECT CODIGO, STOCK FROM INVENTARIO WHERE CODIGO IN ({})".format(', '.join(['?'] * len(codigos))), codigos)

		# *eliminar el bloque sgte agregandole un campo en el carrito de la cantidad que hay en stock
		# *Nos podemos evitar lo de arriba si le pasamos desde la BBDD el stock y la cantidad de compra
		inventario = {}
		for i in cursor.fetchall():
			inventario.update({i[0]:i[1]})
		# FORMATO: validacion = {"codigo_articulo":[cantidad_inventario, cantidad_compra]}
		validacion = {}
		for llave, valor in self.listaCompra.iterrows():
			for i in inventario:
				if llave == i:
					validacion.update({i : [inventario[i], valor["CANTIDAD_COMPRA"]]})
				continue


	# def generarCodigoCliente(self,cursor):
	def generarCodigoCliente(*args, **kwargs):

		self = args[0]
		cursor = args[1]
		# conexion = args[2]
		cursor.execute("SELECT CLIENTE FROM SALDOS")
		# conexion.commit()
		return str(len(set([x[0] for x in cursor.fetchall()]))).zfill(2)

	@conexiones.decoradorBaseDatos3
	def compra(*args, **kwargs):

		self = args[0]
		cursor = kwargs["cursor"]
		conexion = kwargs["conexion"]
		# *Incluir boton para descuentos a la venta general

		# if self.menuOperacion.current()==0 or self.menuOperacion.current() ==1:
		# 	self.ejecutar()
		# 	return

		# generar la factura en el programa y registrarla en una tabla nueva (compras) en BBDD, debe contener:
		# codigoCompra-nombre-marca-cantidadComprada-utilidad.
		# actualizar la tabla inventario.
		
		# nos aseguramos que hayan productos en el carro de compra
		if self.listaCompra.empty:
			messagebox.showwarning(title="ERROR", message="No hay artículos que comprar.")
		else:

			# guardar la compra en BBDD con un id unico y la lista de los productos y posterior eliminar dicha lista

			cursor.execute("SELECT FACTURA FROM VENTAS")

			lista_cod = set(cursor.fetchall())


			# Primero hacemos la inserccion en saldos, si no es para pago inmediato.
			if self.boolAgregarASaldo.get():

				# self.listaCompra = pd.DataFrame(columns = ["CODIGO", "NOMBRE", "PRECIO_UNIT", "CANTIDAD_COMPRA", "SUB_TOTAL", "UTILIDAD"])

				concepto_final = [x.tolist() for x in self.listaCompra.loc[:, ["CANTIDAD_COMPRA", "NOMBRE", "SUB_TOTAL"]].values]
				concepto_final = ' ~ '.join([' '.join(map(str, sublista)) for sublista in concepto_final])
				total = self.listaCompra["SUB_TOTAL"].sum()

				# si es cliente viejo y el código es de dos dígitos. verificamos.
				if self.boolClienteNuevo.get() == False and len(self.entCodigoCliente.get())==2:

					cursor.execute("SELECT NOMBRE FROM SALDOS WHERE CLIENTE = (?)", (self.entCodigoCliente.get(),))

					# si está mas de una vez en la lista no me interesa
					nombre_saldo = cursor.fetchone()

					if nombre_saldo:

						# obtenemos el valor de la ultima factura, para saber cual codigo sigue
						cursor.execute("SELECT FACTURA FROM VENTAS ORDER BY FACTURA DESC" )
						codigo_sgte = cursor.fetchone()[0]+1

						# si hay registro como saldado lo borramos, pero antes obtenemos el abono a la cuenta (debe ser el mismo en todos los registros)
						cursor.execute("SELECT CONCEPTO, ABONO FROM SALDOS WHERE CLIENTE=(?) ORDER BY FACTURA DESC",(self.entCodigoCliente.get(),))
						concepto_abono=cursor.fetchone()

						if concepto_abono[0]=="SALDADO":
							cursor.execute("DELETE FROM SALDOS WHERE CLIENTE = (?)", (self.entCodigoCliente.get(),))

						# verificamos si hay comentario, si lo hay le agregamos la fecha:
						if len(str(self.txtComentarioCliente.get("1.0", "end")).replace("\n","")) >= 4:
							self.txtComentarioCliente.insert("1.0", datetime.date.today().strftime('%d/%m: '))
						else:
							self.txtComentarioCliente.delete("1.0", "end")


						# cursor.execute("DELETE FROM SALDOS WHERE COD_CLIENTE = (?) AND CONCEPTO=(?)",(self.entCodigoCliente.get(),"SALDADO"))
						cursor.execute("INSERT INTO SALDOS (CLIENTE, NOMBRE, FACTURA, CONCEPTO, SALDO, ABONO, COMENTARIO) VALUES (?,?,?,?,?,?,?)",(self.entCodigoCliente.get() ,nombre_saldo[0], codigo_sgte ,concepto_final, total, concepto_abono[1], self.txtComentarioCliente.get("1.0", "end").upper()))
						self.entCodigoCliente.delete(0,END)
						self.txtComentarioCliente.delete("1.0", "end")
						self.checkIncluirSaldo.invoke()

					else:
						messagebox.showwarning(title="ERROR", message=f"No existe deudor con el código {self.entCodigoCliente.get()}")
						self.entCodigoCliente.delete(0, END)
						self.txtComentarioCliente.delete("1.0", "end")
						return

				# si es cliente nuevo, la condición para registrar es que tenga de 4 a 20 caracteres
				elif self.boolClienteNuevo.get():
					if (len(self.entNombreCliente.get())<4 or len(self.entNombreCliente.get())>20):
						messagebox.showwarning(title= "ERROR", message = "El nombre no cumple con los requisitos. (entre 6 y 20 caracteres)")
						return

					else:
						cursor.execute("SELECT FACTURA FROM VENTAS ORDER BY FACTURA DESC")
						codigo_sgte = cursor.fetchone()[0]+1

						# verificamos si hay comentario, si lo hay le agregamos la fecha:
						if len(str(self.txtComentarioCliente.get("1.0", "end")).replace("\n","")) >= 4:
							self.txtComentarioCliente.insert("1.0", datetime.date.today().strftime('%d/%m: '))
						else:
							self.txtComentarioCliente.delete("1.0", "end")


						cursor.execute("INSERT INTO SALDOS (CLIENTE, NOMBRE, FACTURA, CONCEPTO, SALDO, COMENTARIO) VALUES (?,?,?,?,?,?)",(self.entCodigoCliente.get(), self.entNombreCliente.get().upper(), codigo_sgte,concepto_final, total, self.txtComentarioCliente.get("1.0", "end").upper()))
						messagebox.showinfo(title="CREACIÓN EXITOSA", message=f"Cliente {self.entCodigoCliente.get()} creado con éxito.")
						self.checkIncluirSaldo.invoke()

				elif self.entCodigoCliente.get() not in lista_cod:
					messagebox.showinfo(title="ERROR", message="El código no pertenece a ningun morador.")
					self.checkIncluirSaldo.invoke()
					# self.entCodigoCliente.delete(0, END)
					return


			self = args[0]
			cursor = kwargs["cursor"]
			conexion = kwargs["conexion"]

			# self.listaCompra = pd.DataFrame(columns = ["CODIGO", "NOMBRE", "PRECIO_UNIT", "CANTIDAD_COMPRA", "SUB_TOTAL", "UTILIDAD"])
			lista_factura = self.listaCompra
			lista_factura["COD_FACTURA"]=len(lista_cod)
			lista_factura = lista_factura[["COD_FACTURA", "NOMBRE", "PRECIO_UNIT", "CANTIDAD_COMPRA", "SUB_TOTAL", "UTILIDAD"]]
			lista_factura = lista_factura.drop('PRECIO_UNIT', axis=1)

			# cursor.executemany("""
			# 	INSERT INTO HISTORIAL_COMPRA (COD_FACTURA, COD_ARTICULO, ARTICULO, PRECIO_UNIT, CANTIDAD, PRECIO_TOT, GANANCIA_TOT ) VALUES (?,?,?,?,?,?,?)"""
			# 	,lista_factura)
			for llave, valor in lista_factura.iterrows():
				cursor.execute("""INSERT INTO VENTAS (CODIGO, FACTURA, ARTICULO, CANTIDAD, PRECIO_TOT, COSTO_TOT) 
								VALUES (?,?,?,?,?,?)""", (llave, valor["COD_FACTURA"], valor["NOMBRE"], valor["CANTIDAD_COMPRA"], valor["SUB_TOTAL"], valor["SUB_TOTAL"] - valor["UTILIDAD"]))

			# cursor.executemany("""
			# 	INSERT INTO VENTAS (FACTURA, CODIGO, ARTICULO, CANTIDAD, PRECIO_TOT, COSTO_TOT ) VALUES (?,?,?,?,?,?)"""
			# 	,lista_factura.values.tolist())

			# ACTUALIZAMOS LA CANTIDAD PARA CADA ARTÍCULO DE LA LISTA DE COMPRA EN LA BBDD
			# "COD_FACTURA", "NOMBRE", "PRECIO_UNIT", "CANTIDAD_COMPRA", "SUB_TOTAL", "UTILIDAD"
			for llave, valor in lista_factura.iterrows():
				cursor.execute("SELECT STOCK FROM INVENTARIO WHERE CODIGO = (?)", (llave,))
				cantidad = cursor.fetchone()
				cursor.execute("UPDATE INVENTARIO SET STOCK = (?) WHERE CODIGO = (?)",(cantidad[0]-lista_factura.loc[llave, "CANTIDAD_COMPRA"], llave))


			# pregunta = messagebox.askquestion(title="COMPRA",message=f"Total a pagar: $ {sum( i[4] for i in self.listaCompra)}\n¿Deseas imprimir la factura?")
			total = self.listaCompra["SUB_TOTAL"].sum()
			# *INCLUIR UNA ENTRADA CUANDO VAYAN A PAGAR, PARA HACER LOS CAMBIOS AUTOMÁTICAMENTE (NO ES NECESARIO QUE SEA EN UN TOP LEVEL)
			print("el total de la compra fue de: ", total)

			# pregunta = messagebox.askquestion(title="COMPRA", message=f"Total a pagar: $ {total}\n¿Deseas imprimir la factura?")

			# if pregunta == "no":
			# 	pass
			# else:
			# 	# ***APRENDER PDF FORMATO PEQUEÑO
			# 	factura = ""
			# 	for articulo in lista_factura:
			# 	    for campo in articulo:
			# 	        factura += str(campo) + "\t"
			# 	    factura+="\n"
			# 	with open(f"factura_n_{len(lista_cod)}.txt","w") as f:
			# 		f.write(factura)

			# 	print("yes, se guardó el archivo")
			
			if self.facturaImpresa.get():
				print("imprimir factura")
				self.facturaImpresa.set(False)



			self.borrarCampos()

	def borrarCampos(self):

		self.listaCompra.drop(index=self.listaCompra.index, inplace=True)
		if "COD_FACTURA" in self.listaCompra.columns:
			self.listaCompra.drop("COD_FACTURA", axis = 1, inplace=True)
		self.cantidadListaCompra["text"]=0

class InterfazAdministrativa(Tk):

	"""
	Clase que permite la QUERY del inventario, modificaciones y análisis del negocio.
	Contiene sus respectivos widgets interactivos.
	Cada vez que se crea una instacia, el tipo de ventana que arroja es una Toplevel
	"""
	# *REESTRUCTURAR los tipos de datos.
	# *cuando se abra esta interfaz, que la ventana esté enfocada (cuando se crea, el foco está en la ppal)
	# *cambiar los botones de la interfaz a la ventana de inventario (crear, borrar(cuando se selecciona)
	# ...actualizar(al seleccionar))
	# *Poner la fecha en español

	def __init__(self,master=None):
		# super().interfazSaldos(cursor)

		self.master = master
		self.emergente = Toplevel()
		self.emergente.focus_set()
		self.emergente.geometry("810x500")
		self.emergente.title("ADMINISTRACION")
		self.emergente.grab_set()
		self.crearWidgets()

	# def decoradorBaseDatos(funcion):

	# 	def modificadora(self, *args,**kwargs):

	# 		conexion = sqlite3.connect("BASE_DATOS_PRUEBA.db")
	# 		cursor = conexion.cursor()
	# 		funcion(self, cursor,*args)
	# 		conexion.commit()
	# 		cursor.close()
	# 		conexion.close()

	# 	return modificadora

	def crearWidgets(self):

		self.emergente.bind("<Escape>", lambda _ : self.emergente.destroy())

		# *si estamos en el mes actual, bloquear los dias siguientes a la consulta.
		# *bloquear los meses siguientes al actual

		DIA = [str(x).zfill(2) for x in range(1,32)]
		MES = [str(x).zfill(2) for x in range(1,13)]


		self.opcion = StringVar()

		Label(self.emergente, text=time.strftime("%d de %B")).place(relx=.1,rely=.05)
		Label(self.emergente, text="PAPELERÍA VALERIA").place(relx=.55,rely=.05)

		Label(self.emergente, text = "DÍA").place(relx = 0.8, rely= 0.03)
		self.dia = ttk.Combobox(self.emergente, values = DIA, width = 2, state = "readonly")
		self.dia.place(relx = 0.8, rely = 0.07)
		self.dia.set(datetime.date.today().strftime("%d"))

		Label(self.emergente, text = "MES").place(relx = 0.85, rely= 0.03)
		self.mes = ttk.Combobox(self.emergente, values = MES, width = 2, state = "readonly")
		self.mes.place(relx = 0.85, rely = 0.07)
		self.mes.set(datetime.date.today().strftime("%m"))


		Label(self.emergente, text = "AÑO").place(relx = 0.9, rely= 0.03)
		self.anho = ttk.Combobox(self.emergente, value = "2023",  width = 4, state = "disabled")
		self.anho.place(relx = 0.9, rely = 0.07)
		self.anho.current(0)

		# Button(self.emergente, text="CERRAR", command=self.emergente.destroy).place(relx=.85,rely=0.05)
		Label(self.emergente, text="OPERACIÓN",justify='right').place(relx=.15, rely=.15)



		# self.opciones = ttk.Combobox(self.emergente, values= ["CREAR_ARTICULO","VER_ARTICULO","EDITAR_ARTICULO","BORRAR_ARTICULO","VENTAS_DIA","VENTAS_MES","VER_ARTICULOS_TOTALES"], state = "readonly",width=15)
		# self.opciones.place(relx=.55,rely=.15)

		Button(self.emergente, text="CREAR", width=8, command=self.crearArticulo).place(relx=.35, rely=.14)
		Button(self.emergente, text="INVENTARIO", width=10, command=lambda :self.verArticulo("TOTAL")).place(relx=.48, rely=.14)
		Button(self.emergente, text="BUSCAR_UND", width=10, command=lambda: self.verArticulo("ESPECIFICO")).place(relx=.61, rely=.14)

		Button(self.emergente, text="ACTUALIZAR", width=10, command=self.actualizarArticulo).place(relx=.74, rely=.14)
		# self.btnActualizar.bind("<Button-1>",self.verificarCodigo)

		Button(self.emergente, text="ELIMINAR", width=8, command=self.eliminarArticulo).place(relx=.87, rely=.14)
		# self.btnEliminar.bind("<Button-1>",self.verificarCodigo)

		Button(self.emergente, text="<-- GRAFICAR", width=13, command=lambda : self.verGrafico(f'{self.rangoGrafico.get()}',f'{self.tipoGrafico.get()}')).place(relx=.48,rely=.23)

		self.rangoGrafico = ttk.Combobox(self.emergente, values = ["DIA", "MES" ], width=4, state="readonly")
		self.rangoGrafico.place(relx=.34, rely=.22)
		self.rangoGrafico.current(0)

		# 1. articulo vs cantidad_vendida 2. articulo vs utilidad 3. articulo vs cantidad_stock 4. hora vs cantidad_vendida
		self.tipoGrafico = ttk.Combobox(self.emergente, values = ["ARTICULOxVENDIDOS", "ARTICULOxGANANCIA", "HORA/DIAxUTILIDAD"], width=20, state="readonly")
		self.tipoGrafico.place(relx=.29, rely=.28)
		self.tipoGrafico.current(0)

		Button(self.emergente, text="SALDOS", width=12).place(relx=.65, rely=.23)
		Button(self.emergente, text="CONTABILIDAD", width=12, command=self.verContabilidad).place(relx=.78, rely=.23)

		self.frame = Frame(self.emergente)
		self.frame.place(relx=.03,rely=.34,relwidth=.94,relheight=.7)


		# este frame contiene los datos de visualización de inventario y va oculto por defecto:
		# *Debe quedar habilitado para todas las vistas, tanto de tablas como gráficas
		# *Debe poder tener scrollbar vertical, para ver todos los articulos
		# *todos los que hagan uso del widgets, deben llamar una sola funcion, especificando el requerimiento
		# self.frameDos = LabelFrame(self.emergente, text="VISTAS", font=("verdana", 12))
		self.frameDos = Frame(self.emergente)
		self.frameDos.place(relx=.03,rely=.14,relwidth=.94,relheight=.77)
		# Button(self.frameDos, text="CERRAR", width = 7, command= self.cerrarVistaInventario).grid(column= 8 , row=0)
		self.frameDos.place_forget()



		# los widgets que contiene el CREATE-UPDATE

		self.lblCodigo = Label(self.frame,text="Código:",font=10).place(relx=.1,rely=.03)
		self.lblNombre = Label(self.frame,text="Nombre:",font=10).place(relx=.1,rely=.15)
		self.lblMarca = Label(self.frame,text="Marca:",font=10).place(relx=.1,rely=.27)
		self.lblCantidad = Label(self.frame,text="Cantidad:",font=10).place(relx=.1,rely=.39)
		self.lblPrecio = Label(self.frame,text="Precio:",font=10).place(relx=.1,rely=.51)
		self.lblCosto = Label(self.frame,text="Costo:",font=10).place(relx=.1,rely=.63)
		self.lblUtilidad = Label(self.frame,text="Utilidad:",font=10).place(relx=.1,rely=.75)
		self.lblComentario = Label(self.frame,text="Comentario:",font=10).place(relx=.1,rely=.87)

		self.entCodigo = Entry(self.frame,width=15)
		self.entCodigo.place(relx=.5,rely=.03)

		self.entNombre = Entry(self.frame,width=15)
		self.entNombre.place(relx=.5,rely=.15)

		self.entMarca = Entry(self.frame,width=15)
		self.entMarca.place(relx=.5,rely=.27)

		self.entCantidad = Entry(self.frame,width=15)
		self.entCantidad.place(relx=.5,rely=.39)

		self.entPrecio = Entry(self.frame,width=15)
		self.entPrecio.place(relx=.5,rely=.51)

		self.entCosto = Entry(self.frame,width=15)
		self.entCosto.place(relx=.5,rely=.63)

		self.entUtilidad = Entry(self.frame,width=15,state="readonly")
		self.entUtilidad.place(relx=.5,rely=.75)

		self.entComentario = Entry(self.frame,width=15)
		self.entComentario.place(relx=.5,rely=.87)
		

		Button(self.frame,text="Borrar",width=8, command = self.borrarCampos).place(relx=.75,rely=.25)

		# Button(self.frame,text="Ejecutar", width=8, command = self.ejecutar).place(relx=.75, rely=.4)

		Button(self.frame, text="Generar código",width=11, command = self.generarCodigo).place(relx=.75, rely=.45)

	def borrarCampos(self):

		self.entCodigo["state"]="normal"
		self.entCodigo.delete(0,"end")
		self.entNombre.delete(0,"end")
		self.entMarca.delete(0,"end")
		self.entCantidad.delete(0,"end")
		self.entPrecio.delete(0,"end")
		self.entCosto.delete(0,"end")
		self.entUtilidad["state"]="normal"
		self.entUtilidad.delete(0,"end")
		self.entUtilidad["state"]="readonly"
		self.entComentario.delete(0,"end")

	@conexiones.decoradorBaseDatos3
	def generarCodigo(*args, **kwargs):

		self = args[0]
		cursor = kwargs["cursor"]
		conexion = kwargs["conexion"]

		if self.entCodigo["state"]=="normal" and self.entCodigo != "":

			cursor.execute("SELECT CODIGO FROM ART_CREACION ORDER BY CODIGO")

			# enlistado de todos los codigos de la BBDD
			lista = cursor.fetchall()

			if len(lista) <= 100:
				codigo = "PA0"+str(int(lista[-1][0][3:])+1)
			else:
				codigo = "PA"+str(int(lista[-1][0][2:])+1)

			self.entCodigo.insert(0,codigo)

			# Se bloquea la entrada para que no haya problemas con los códigos
			self.entCodigo.config(state='readonly')

		else:
			messagebox.showwarning(title="PROBLEMA CON CÓDIGO",message="Borra el campo del código")


	@conexiones.decoradorBaseDatos3
	def crearArticulo(*args, **kwargs):



		self = args[0]
		cursor = kwargs["cursor"]
		conexion = kwargs["conexion"]

		if self.entCodigo["state"]=="normal":

			messagebox.showwarning(title="ERROR", message="Genera primero el código.")
			self.borrarCampos()

		else:

			articuloNuevo = pd.Series(data = [self.entCodigo.get().upper(),self.entNombre.get().upper(),self.entMarca.get().upper(),self.entCantidad.get().upper(),self.entPrecio.get().upper(),self.entCosto.get().upper(),self.entComentario.get().upper()], index=["CODIGO", "NOMBRE", "MARCA", "CANTIDAD", "PRECIO", "COSTO", "COMENTARIO"])
			faltantes = []

			# se corrige si no hay marca o comentario
			if articuloNuevo.loc["MARCA"] == "":
				articuloNuevo.loc["MARCA"] = "GENERICO"
			if articuloNuevo.loc["COMENTARIO"] == "":
				articuloNuevo.loc["COMENTARIO"] = "NORMAL"

			# # primero se debe comprobar que todos los datos necesarios estén y no esten repetidos los nombres
			for indice in articuloNuevo.index:

				if articuloNuevo.loc[indice] == "" or articuloNuevo.loc[indice] == 0:
					
					faltantes.append('>'+indice+"\n")

			if len(faltantes) != 0:

				return messagebox.showinfo(title="Error", message=f"Faltan estos datos:\n{''.join(faltantes)}")

			else:


				cursor.execute("""
					INSERT INTO INVENTARIO (CODIGO, ARTICULO, MARCA, CANTIDAD, PRECIO, COSTO, COMENTARIO)
					VALUES (?,?,?,?,?,?,?)
					""",tuple(articuloNuevo.values))
				messagebox.showinfo("ARTICULO_NUEVO","Articulo nuevo creado con éxito.")
				self.borrarCampos()

	def cerrarVistaInventario(self):


		# Debemos eliminar contenido y saltar el boton de cerrar la vista
		# btn = 0
		for i in self.frameDos.winfo_children():
			i.destroy()
			# if btn!=0:
			# 	i.destroy()
			# btn+=1
			
		self.frameDos.place_forget()


	@conexiones.decoradorBaseDatos3
	def verArticulo(*args, **kwargs):


		self = args[0]
		tipo = args[1]
		cursor = kwargs["cursor"]
		conexion = kwargs["conexion"]

		def organizar(campo, lugar):

			if len(self.lectura)>0:
				estado = interfazArbol.item("000")["values"][lugar] < interfazArbol.item(str(len(self.lectura)-1).zfill(3))["values"][lugar]

				if campo=="DISPONIBILIDAD":
					self.lectura.sort_values(by=[campo, "CANTIDAD"], ascending=[False, True], inplace= True) if estado else self.lectura.sort_values(by=campo, inplace=True)
				else:
					self.lectura.sort_values(by=campo, ascending=False, inplace=True) if estado else self.lectura.sort_values(by=campo, inplace=True)
						

				for i in interfazArbol.get_children():
					interfazArbol.delete(i)

				for i in range(len(self.lectura)):
					interfazArbol.insert('', 'end',iid=str(i).zfill(3), text = str(i), values=self.lectura.iloc[i, :].tolist(), tags=("item_seleccionado",))
					# interfazArbol.insert(parent='', index='end',iid=self.lectura.loc[i, "CODIGO"], values=self.lectura.iloc[i, :].tolist(), tags=("item_seleccionado",))
			
				interfazArbol.insert('', 'end',iid="111", values=["TOTALES","","","","","","","",self.lectura.iloc[:,3].sum()])

				
		def seleccionItem(event):

			# print("hasta ahora van estos items: \n"+ "\n".join([x for x in interfazArbol.selection()]))

			btnEditarInventario.pack() if len(interfazArbol.selection())!=0 else btnEditarInventario.pack_forget()
				
		# posiciona el label frame que contendrá todas las vistas
		# self.frameDos.place(relx=.03,rely=.19,relwidth=.94,relheight=.8)
		self.frameDos.place(relx=.03,rely=.14, relwidth=.94,relheight=.85)
		
		Button(self.frameDos, text="CERRAR", width = 7, command= self.cerrarVistaInventario).pack(side=RIGHT, anchor="ne")
		btnEditarInventario = Button(self.frameDos, text="EDITAR", width = 9, command= lambda : print("menú para editar inventario"))
		
		# Button(self.frameDos, text="ELIMINAR", width = 7).pack(side=RIGHT, anchor="w")

		if tipo == "TOTAL":
			cursor.execute("""
				SELECT * FROM INVENTARIO ORDER BY ARTICULO
				""")

		elif tipo == "ESPECIFICO":

			cursor.execute("""
				SELECT * FROM INVENTARIO WHERE ARTICULO = (?)
				""", (self.entNombre.get().upper(),))

		self.lectura=cursor.fetchall()
		self.lectura = pd.DataFrame(data = [list(x) for x in self.lectura], columns= ["CODIGO", "NOMBRE", "MARCA", "CANTIDAD", "PRECIO", "COSTO", "UTILIDAD", "COMENTARIO", "DISPONIBILIDAD"])
		
		self.borrarCampos()

		interfazArbol = ttk.Treeview(self.frameDos, height=10)

		interfazArbol['columns'] = ("CODIGO", "NOMBRE", "MARCA", "CANTIDAD", "PRECIO", "COSTO", "UTILIDAD", "COMENTARIO", "DISPONIBILIDAD")

		# Configurar las columnas del Treeview
		interfazArbol.column('#0', anchor= CENTER, width=35)  # Columna oculta para los índices
		interfazArbol.column('CODIGO', anchor=CENTER, width=50)
		interfazArbol.column('NOMBRE', anchor=CENTER, width=110)
		interfazArbol.column('MARCA', anchor=CENTER, width=80)
		interfazArbol.column('CANTIDAD', anchor=CENTER, width=40)
		interfazArbol.column('PRECIO', anchor=CENTER, width=68)
		interfazArbol.column('COSTO', anchor=CENTER, width=68)
		interfazArbol.column('UTILIDAD', anchor=CENTER, width=70)
		interfazArbol.column('COMENTARIO', anchor=CENTER, width=85)
		interfazArbol.column('DISPONIBILIDAD', anchor=CENTER, width=90)

		# Configurar los encabezados de las columnas
		interfazArbol.heading('#0', text='CANTIDAD', anchor=CENTER)
		interfazArbol.heading('CODIGO', text='CODIGO', anchor=CENTER, command= lambda: organizar("CODIGO",0))
		interfazArbol.heading('NOMBRE', text='ARTICULO', anchor=CENTER, command=lambda : organizar("NOMBRE",1))
		interfazArbol.heading('MARCA', text='MARCA', anchor=CENTER, command=lambda : organizar("MARCA",2))
		interfazArbol.heading('CANTIDAD', text='CANT', anchor=CENTER, command=lambda : organizar("CANTIDAD",3))
		interfazArbol.heading('PRECIO', text='PRECIO', anchor=CENTER, command=lambda : organizar("PRECIO",4))
		interfazArbol.heading('COSTO', text='COSTO', anchor=CENTER, command=lambda : organizar("COSTO",5))
		interfazArbol.heading('UTILIDAD', text='UTILIDAD', anchor=CENTER, command=lambda : organizar("UTILIDAD",6))
		interfazArbol.heading('COMENTARIO', text='COMENTARIO', anchor=CENTER, command=lambda : organizar("COMENTARIO",7))
		interfazArbol.heading('DISPONIBILIDAD', text='DISPONIBILIDAD', anchor=CENTER, command=lambda : organizar("DISPONIBILIDAD",8))

		# Agregamos el evento para cuando se selecciona un artículo:
		interfazArbol.tag_bind("item_seleccionado", "<<TreeviewSelect>>", seleccionItem)

		# Insertar los datos en el interfazArbolview
		for i in range(len(self.lectura)):

			# interfazArbol.insert('', 'end', text=i+1, values=self.self.lectura.iloc[i, :].tolist())
			disponibilidad = self.lectura.loc[i,"CANTIDAD"]
			if disponibilidad >= 10:
				k="SUFICIENTE"
			elif 0 < disponibilidad < 10:
				k="POCAS_UNIDADES"
			else:
				k="AGOTADO"
			self.lectura.loc[i, "DISPONIBILIDAD"]=k

			interfazArbol.insert(parent='', index='end',iid=str(i).zfill(3), text = str(i), values=self.lectura.iloc[i, :].tolist(), tags=("item_seleccionado",))
			# interfazArbol.insert(parent='', index='end',iid=self.lectura.loc[i, "CODIGO"], values=self.lectura.iloc[i, :].tolist(), tags=("item_seleccionado",))
			

		interfazArbol.insert('', 'end', iid= "PA111", values=["TOTALES","","","","","","","",self.lectura.iloc[:,3].sum()])

		interfazArbol.pack( fill=BOTH, expand=True)




		# Empacar el Treeview en la ventana
		# interfazArbol.grid(row=1,column=0)
		# interfazArbol.pack( fill=BOTH, expand=True)

	@conexiones.decoradorBaseDatos3
	def actualizarArticulo(*args, **kwargs):
		# *SE NECESITA ACTUALIZAR INVENTARIO, LO MEJOR ES TENER UN ENTRY EN EL INVENTARIO QUE SUME LOS ARTICULOS NUEVOS
		# *SE QUITA EL BOTÓN DE ACTUALIZACIONES INDIVIDUALES ¿?


		self = args[0]
		cursor = kwargs["cursor"]
		conexion = kwargs["conexion"]

		# CONEXION BBDD
		if self.entCodigo["state"]=="readonly":

			self.entCodigo["state"]="normal"

			actualizacion = (self.entNombre.get().upper(), self.entMarca.get().upper(), self.entCantidad.get().upper(), self.entPrecio.get().upper(), self.entCosto.get().upper(), self.entComentario.get().upper(), self.entCodigo.get().upper())

			# conexion = sqlite3.connect("BASE_DATOS_PRUEBA.db")
			# cursor = conexion.cursor()
			cursor.execute("""
				UPDATE INVENTARIO SET ARTICULO=(?), MARCA=(?), CANTIDAD=(?), PRECIO=(?), COSTO=(?), COMENTARIO=(?) WHERE CODIGO=(?);
				""", actualizacion)
			# conexion.commit()
			# cursor.close()
			# conexion.close()
			messagebox.showinfo(title="ACTUALIZACIÓN", message= "Artículo actualizado con éxito.")
			self.borrarCampos()

			return

		# confirmamos sí el código está en la BBDD

		if self.entCodigo.get() != "" and self.entCodigo["state"]=="normal":

			cursor.execute("""
				SELECT CODIGO FROM INVENTARIO
				""")
			lectura = cursor.fetchall()
			confirmacion = False
			for i in lectura: 
				if i[0] == self.entCodigo.get().upper():
					confirmacion= True

			# Si el artículo está en BBDD, mostramos los datos en pantalla y bloqueamos el código.
			if confirmacion:

				cursor.execute("SELECT * FROM INVENTARIO WHERE CODIGO = (?)", (self.entCodigo.get().upper(),) )
				lectura2 = cursor.fetchall()
				self.entCodigo["state"]="readonly"
				
				self.entNombre.insert(0,lectura2[0][1])
				self.entMarca.insert(0,lectura2[0][2])
				self.entCantidad.insert(0,lectura2[0][3])
				self.entPrecio.insert(0,lectura2[0][4])
				self.entCosto.insert(0,lectura2[0][5])
				self.entUtilidad["state"]="normal"
				self.entUtilidad.insert(0,lectura2[0][6])
				self.entUtilidad["state"]="readonly"
				self.entComentario.insert(0,lectura2[0][7])


			else:

				messagebox.showwarning(title="ACTUALIZACIÓN", message=f"El artículo con código {self.entCodigo.get()} NO está en inventario.")
				self.borrarCampos()

		else:

			messagebox.showwarning(title="ERROR", message="Digita porfavor el código del artículo.")
			# self.borrarCampos()

	@conexiones.decoradorBaseDatos3
	def eliminarArticulo(*args, **kwargs):


		self = args[0]
		cursor = kwargs["cursor"]
		conexion = kwargs["conexion"]

		if self.entCodigo.get()!="":

			cursor.execute("SELECT * FROM INVENTARIO WHERE CODIGO = (?)",(self.entCodigo.get().upper(),))

			lectura = cursor.fetchone()
			lectura = pd.Series(data = lectura, index = ["CODIGO", "NOMBRE", "MARCA", "CANTIDAD", "PRECIO", "COSTO", "UTILIDAD", "COMENTARIO", "DISPONIBILIDAD"])
		
			if not isinstance(lectura, pandas.Series):
				messagebox.showwarning(title="ERROR",message="No existe producto con ese código")

			else:
				confirmacion = messagebox.askquestion(title="ELIMINACIÓN_CONFIRMACIÓN", message=f"¿Estás segur@ deseas eliminar el siguiente artículo:\n{lectura.loc['NOMBRE']}-{lectura.loc['MARCA']}?")
				
				if confirmacion == "yes":
					cursor.execute("DELETE FROM INVENTARIO WHERE CODIGO = (?)",(lectura[0][0],))
					messagebox.showinfo(title="ELIMINACION EXITOSA",message=f"{lectura[0][1]} - {lectura[0][2]}, eliminado con éxito.")	

		else:

			messagebox.showwarning(title="ERROR",message="NO has ingresado el código del artículo a eliminar.")

		self.borrarCampos()

	@conexiones.decoradorBaseDatos3		
	def verGrafico(*args, **kwargs):


		self = args[0]
		rango = args[1]
		categoria = args[2]
		cursor = kwargs["cursor"]
		conexion = kwargs["conexion"]

		# *organizar los diagramas de mayor a menor, con posibilidad de cambiar el orden
		# *integrar el gráfico al frameDos, que se pueda manipular de una mejor forma, contemplando la implementación de scroll
		# self.frameDos.place(relx=.03,rely=.19,relwidth=.94,relheight=.80)
		if rango == "DIA":
			# capturamos la opción elegida en la interfaz
			criterio = self.anho.get()+'-'+self.mes.get()+'-'+self.dia.get()
			cursor.execute("SELECT CODIGO, ARTICULO, CANTIDAD, PRECIO_TOT, UTILIDAD FROM VENTAS WHERE DATE(FECHA) = DATE(?)", (criterio,))
			lista_vendidos = cursor.fetchall()

		elif rango == "MES":

			criterio = self.anho.get()+'-'+self.mes.get()+'%'
			cursor.execute("SELECT CODIGO, ARTICULO, CANTIDAD, PRECIO_TOT, UTILIDAD FROM VENTAS WHERE FECHA LIKE (?)", (criterio,))
			lista_vendidos = cursor.fetchall()

		result = {}

		# comprobamos que haya almenos una venta en el diccionario:
		if len(lista_vendidos) != 0:

			# lista vendidos = [(cod_articulo, name_articulo, cantidad_vendida, precio_total_vendido, ganancia_total_vendido),...]
			for item in lista_vendidos:


		    	# si el codigo articulo ya está en el diccionario, quiere decir que la venta (dia o mes) fue más de un artículo, entonces
		    	# se suma a la cantidad ya guardada la nueva y lo mismo al precio total
			    if item[0] in result:

			        result[item[0]][2] += item[2]  # Sumar i[2]
			        result[item[0]][3] += item[3]  # Sumar i[3]

			    # si aún no está en el diccionaro se agrega con la clave como su codigo
			    else:
			        result[item[0]] = list(item)

			lista_final = list(result.values())


			# *Cuando se posa el cursor del mouse muestre informacion como fecha de ventas con su respectiva q (mes)
			# ...o la hora de venta con su respectiva q (dia), más las ganancias, ademas que muestre su valor en y.
			# ... y en algun lugar la sumatoria de los valores en Y


			# ***APRENDER MATPLOTPLIB	
			# GRAFICO ARTICULOS VS Q VENDIDAS
			if self.tipoGrafico.get() == "ARTICULOxVENDIDOS":

				x = [i[1] for i in lista_final]
				y = [i[2] for i in lista_final]

				plt.bar(x,y)
				plt.xlabel("ARTICULOS")
				plt.ylabel("CANTIDAD VENDIDA")
				plt.ylim(0, max(y) + 3)

			# GRAFICO ARTICULOS VS GANANCIAS 
			elif self.tipoGrafico.get() == "ARTICULOxGANANCIA":
				x = [i[1] for i in lista_final]
				y = [i[4] for i in lista_final]

				plt.bar(x,y)
				plt.xlabel("ARTICULOS")
				plt.ylabel("$ UTILIDADES")
				plt.ylim(0, max(y) + 1000)

			# GRAFICO HORA VS GANANCIAS
			elif self.tipoGrafico.get() == "HORA/DIAxUTILIDAD":


				if rango == "DIA":

					# Creo un diccionario con las horas en que el local está abierto
					dicci = {x:0 for x in range(8,24)}

					cursor.execute("SELECT ARTICULO, CANTIDAD, UTILIDAD, CAST(strftime('%H', FECHA) AS INTEGER) FROM VENTAS WHERE DATE(FECHA) = DATE(?)", (criterio,))

				else:

					# Creo un diccionario con los días en que el local abrió
					# *INCLUIR DIA DE SEMANA
					dicci = {x:0 for x in range(1,32)}

					cursor.execute("SELECT ARTICULO, CANTIDAD, UTILIDAD, CAST(strftime('%d', FECHA) AS INTEGER) FROM VENTAS WHERE FECHA LIKE (?)", (criterio,))
				
				horadia_ganancia = cursor.fetchall()
				for venta in horadia_ganancia:
					dicci[venta[3]] = dicci[venta[3]]+venta[2]

				x = dicci.keys()
				y = dicci.values()

				plt.bar(x,y)
				plt.xlabel("HORA DE VENTA") if rango=="DIA" else plt.xlabel("DIA DE VENTA")
				plt.ylabel("$ UTILIDADES")
				plt.ylim(0, max(y) + 1000)

			plt.show()
				

		else:

			messagebox.showinfo(title = "ERROR", message = "No se registran ventas para esa fecha")

	@conexiones.decoradorBaseDatos3
	def verSaldos(*args, **kwargs):
		# *CREAR UNA TABLA DONDE ESTÉ REGISTRADO LAS PERSONAS QUE DEBAN
		# *PERMITIR MODIFICACIONES 
		# self.frameDos.place(relx=.03,rely=.19,relwidth=.94,relheight=.80)
		pass

		

	def verContabilidad(self):
		# *INGRESOSPORVENTASPAPELERIA ENTRY( INGRESOSPORVENTASDULCES )- UTILIDADESPORVENTASPAPELERIA(UTILIDADES TOTALES-SALDOS DEL MES)  - UTILIDADESTOTALES (UTILIDADES VENTAS-GASTOS MES)
		# ...GASTOSPORSERVICIOS (AGUA, ENERGIA) - GASTOSARTICULOS - GASTOSINVERSIONES - GASTOS MENORES
		# self.frameDos.place(relx=.03,rely=.19,relwidth=.94,relheight=.80)
		pass


if __name__=="__main__":

	InterfazPrincipal()

# **UN BOTON PARA EXPORTAR ARCHIVOS IMPORTANTES TIPO PDF
