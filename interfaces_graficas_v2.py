from tkinter import Frame,BROWSE,NONE, BOTH,X, Y, Listbox, Label, LabelFrame, Checkbutton, Scrollbar, Tk, Text, StringVar,Message, BooleanVar, Entry, Button, ttk, messagebox,TOP, OptionMenu, Toplevel, IntVar, NORMAL, RIGHT, LEFT, END, NO, CENTER, YES, HORIZONTAL, VERTICAL

import conexiones
import pandas
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
# from functools import partial

# esta es una prueba inicial

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

	# def codigoServicio(self, **kwargs):

	# 	# kwargs:{tipo: "servicio", codigo: "numerofactura",boton: <tkinter.Button> }

	# 	if kwargs["tipo"]=="GAS":

	# 		# if kwargs["codigo"]=="" or kwargs["codigo"].isdigit() and len(kwargs["codigo"])<11:
	# 		if codigo=="" or codigo.isdigit() and len(codigo)<11:

	# 			if len(codigo)==10:
	# 				kwargs["boton"].config("normal")

	# 			return True
	# 		else:
	# 			return False
	# 	else:
	# 		return True

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


# class InterfazPrincipal(Frame):
class InterfazPrincipal:

	"""
	Interfaz genérica que contiene las operaciones comunes que se hacen en el negocio,
	Pago de servicios, recargas, compra de artículos y tareas administrativas.
	"""

	def __init__(self):
		self.raiz = Tk()
		self.raiz.focus_set()
		self.raiz.geometry("400x470+200+150")
		self.raiz.resizable(False,False)
		# creamos una instancia de la clase validaciones, para usar sus métodos.
		self.validaciones = Validaciones()
		self.crearWidgets()
		self.raiz.mainloop()

	def crearWidgets(self):
		
		self.listaCompra = pd.DataFrame(columns = ["CODIGO", "NOMBRE", "PRECIO_UNIT", "CANTIDAD_COMPRA", "SUB_TOTAL", "UTILIDAD"])


		# ++ CREACIÓN WIDGETS; INTERFAZ PRINCIPAL: 

		Label(self.raiz, text=time.strftime("%d de %B")).place(relx=0.15,rely=0.05)
		Label(self.raiz, text="PAPELERÍA VALERIA").place(relx=0.5,rely=0.05)

		Label(self.raiz, text="OPERACIÓN").place(relx=0.05, rely=0.20)
		self.menuOperacion = ttk.Combobox(self.raiz, values = ["SERVICIO_PUBLICO","RECARGA","COMPRA","ADMINISTRACION", "SALDOS"], state="readonly")
		self.menuOperacion.place(relx=0.5,rely=0.18)

		self.frameOpciones = Frame(self.raiz)
		self.frameOpciones.place(rely=0.30, relx=0, relwidth=1, relheight=.80)



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
			@conexiones.decoradorBaseDatos
			def check(tipo, cursor):
				
				if tipo == "SALDO":

					# si selecciona la opcion incluir a saldo, activa casillo cliente nuevo y el entry Uno de codigo cliente
					if self.boolAgregarASaldo.get():
						print(self.boolAgregarASaldo.get())

						checkClienteNuevo.place(relx=0.6, rely=0.15)
						lblCodigoCliente.place(relx=0.05, rely=0.28)
						self.entCodigoCliente.place(relx=0.5, rely=0.28)
						validarCodigoCliente = self.entCodigoCliente.register(self.validaciones.codigoCliente)
						self.entCodigoCliente.config(validate="key", validatecommand=(validarCodigoCliente, "%P"))

					else:

						checkClienteNuevo.place_forget()
						lblCodigoCliente.place_forget()
						self.entCodigoCliente.delete(0,END)
						self.entCodigoCliente.place_forget()

						if self.boolClienteNuevo.get():
							checkClienteNuevo.invoke()

				# si seleccionamos la casilla de nuevo cliente, se crea el entry del nombre al desactivarla se elimina
				elif tipo == "NUEVO":

					if self.boolClienteNuevo.get():
						self.entCodigoCliente.delete(0,END)
						codigo = self.generarCodigoCliente(cursor)
						self.entCodigoCliente.insert(0, codigo)
						self.entCodigoCliente.config(state="readonly")
						lblNombreCliente.place(relx=0.05, rely=0.41)
						self.entNombreCliente.place(relx=0.5, rely=0.41)
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
			self.boolAgregarASaldo = BooleanVar()
			self.boolClienteNuevo = BooleanVar()

			lblCodigo = Label(self.frameOpciones, text="CÓDIGO ARTICULO").place(relx=0.05, rely=0.02)

			entCodigo = Entry(self.frameOpciones, textvariable = codigoArticulo, width=10)
			entCodigo.place(relx=0.50, rely=0.02)
			validarCodigo = entCodigo.register(self.validaciones.codigoArticulo)
			entCodigo.config(validate = "key", validatecommand = (validarCodigo,'%P'))
			entCodigo.bind("<KeyRelease>", lambda _:verificarLongitud(_))

			self.cantidadListaCompra = Label(self.frameOpciones, text = 0, borderwidth=10, font=7)
			self.cantidadListaCompra.place(relx=0.80, rely=0.02)

			self.checkIncluirSaldo = Checkbutton(self.frameOpciones, text = "INCLUIR A SALDO", variable = self.boolAgregarASaldo, onvalue = True, offvalue = False, command=lambda : check("SALDO"))
			self.checkIncluirSaldo.place(relx=0.05, rely=0.15)
			
			lblCodigoCliente = Label(self.frameOpciones, text = "CODIGO CLIENTE")

			self.entCodigoCliente = Entry(self.frameOpciones, textvariable = codigoCliente)

			checkClienteNuevo = Checkbutton(self.frameOpciones, text = "CLIENTE NUEVO", variable = self.boolClienteNuevo, onvalue = True, offvalue = False, command=lambda: check("NUEVO"))

			lblNombreCliente = Label(self.frameOpciones, text="NOMBRE CLIENTE")

			self.entNombreCliente = Entry(self.frameOpciones, textvariable = nombreCliente)

			Button(self.frameOpciones, text="MODIFICAR", command=self.modificarArticulo).place(relx=0.1, rely=0.74)

			Button(self.frameOpciones, text="FINALIZAR", command= self.compra).place(relx=0.45, rely=0.74)

			Button(self.frameOpciones, text= "SALDOS", command=self.interfazSaldos).place(relx=0.80, rely=0.74)

			Button(self.frameOpciones,text="BORRAR COMPRA",command=borrarCompra).place(relx=0.42,rely=0.59)

	
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
			tipoOperador.bind("<<ComboboxSelected>>", lambda _:self.entNumeroRecarga.delete(0,END))

		elif self.menuOperacion.get()=="ADMINISTRACION":
			InterfazAdministrativa(self.raiz)

		elif self.menuOperacion.get() == "SALDOS":
			self.interfazSaldos()

	@conexiones.decoradorBaseDatos
	def generarCodigoCliente(self, cursor):

		cursor.execute("SELECT COD_CLIENTE FROM SALDOS")
		return str(len(set([x[0] for x in cursor.fetchall()]))).zfill(2)


	def rescatarSaldos(self, cursor):

		# Retorna data frame con los clientes que deben. 

		cursor.execute("SELECT COD_CLIENTE, NOMBRE_CLIENTE, CONCEPTO, SALDO FROM SALDOS")
		saldos = cursor.fetchall()
		codigos = list(set(x[0] for x in saldos))
		codigos.sort()
		df_saldos = pd.DataFrame(data=[[x, "", "", 0] for x in codigos],columns=["COD_CLIENTE","NOMBRE_CLIENTE", "CONCEPTO", "SALDO"])

		for saldo in saldos:

			for indice, data in df_saldos.iterrows():

				if saldo[0] == data[0]:

					# Si el saldo del moroso NO es cero, agregamos el concepto, de los contrario registramos como saldado.
					if saldo[3]!=0:

						# si es lla primera factura, la agregamos tal cual.
						if df_saldos.loc[indice,"NOMBRE_CLIENTE"]=="":

							df_saldos.loc[indice,"CONCEPTO"]=saldo[2]

						# si no (es de la segunda para arriba), le agregamos un separador.
						else:

							df_saldos.loc[indice,"CONCEPTO"]+="/"+saldo[2]

					# si el saldo de la BBDD es cero, le agregamos saldado al concepto.
					# ACLARACIÓN: Solo debe haber un registro como saldado si el cliente no debe nada.
					else:

						df_saldos.loc[indice,"CONCEPTO"]="SALDADO"

					# el nombre y el saldo en cualquier caso se suma. Si es 0 pues el que está a paz
					# le sumará otro cero. y el nombre claramente hay que copiarlo.
					df_saldos.loc[indice,"NOMBRE_CLIENTE"]=saldo[1]
					df_saldos.loc[indice, "SALDO"]+=saldo[3]

					# continuamos con el siguiente registro de la BBDD
					break

		return df_saldos

	@conexiones.decoradorBaseDatos
	def interfazSaldos(self, cursor):

		# MUESTRA la información de las personas que están debiendo.

		# *cuando se abone o salde, `<TREEVIEW tree>` `<FRAME info_saldos>` se actualice automaticamente (<TOPLEVEL interfaz> conserve su predominio)
		# *cada que se abone, le reste a los articulos más antiguos. y si se abona la totalidad de una factura antigua ésta se borre.
		# ...las filas primarias van con fecha + saldo que se debe, en las secundarias van los detalles (cantidad nombre precio)

		def borrarClientesDetalle():

			tree.delete(*tree.get_children())

		def actualizarClienteDetalle(**valores):

			'''
			ACTUALIZAMOS el item seleccionado sin cambiar o anular la selección (tanto en la general como en la detallada)
			'''
			tree.item(valores["codigo"], values=(str(valores["codigo"]).zfill(2), valores["nombre"], "SALDADO", 0))
			concepto_det.delete(*concepto_det.get_children())
			concepto_det.insert("", END, values=[0, "SALDADO", 0])

		def crearClientes(datos):

			'''
			Hacemos la insercción de acuerdo al formato y la información retornada desde `self.rescatarSaldos`
			DEBEN ser todos los clientes que han tenido cuenta, deban o no al momento de la consulta.
			'''

			for i in range(len(datos)):

				tree.insert('', 'end', iid= datos.iloc[i,0], values=datos.iloc[i, :].tolist(), tags=("clienteSeleccionado",))

			# Seleccionamos automaticamente el cliente ADMIN
			tree.selection_set("00")
			# pasamos esta variable como argumento, ya que la funcion nos pide uno posicional que sería self dentro del archivo `conexiones.py`
			event=""
			imprimirDetalle(event)


		@conexiones.decoradorBaseDatos
		def imprimirDetalle(event, cursor):

			'''
			INCORPORAMOS los detalles de la cuenta que se debe.
			HABILITACION de botones y caja de texto (sólo si el cliente debe o lo que es lo mismo el saldo es diferente de 0). 
			<DataFrame datos> = "cod_cliente" "nombre_cliente" cod_factura "concepto" saldo "fecha_saldo"
			'''

			cliente_det = tree.item(tree.selection())["values"]

			# *Que tenga jerarquia por fechas >>>>>> sugerencia: 
			# el concepto con los valores divididos por `/` cada compra y `~` cada articulo de una factura es `cliente_det`[2]
			cursor.execute("SELECT FECHA_SALDO FROM SALDOS WHERE COD_CLIENTE=(?)",(str(tree.item(tree.selection())["values"][0]).zfill(2),))
			conceptos_fechas = cliente_det[2].split("/")
			fechas = []
			contador = 0
			for i in cursor.fetchall():
				fechas.append((i[0],conceptos_fechas[contador]))
				contador+=1
			print(fechas)

			# FORMATO: Dividimos en paquetes de a 3, con divisiones internas de space cada elemento de cada factura (le borramos los espacios)
			concepto = [i.strip() for i in str("~".join(cliente_det[2].split("/"))).split("~")]

			# Pasamos la info de codigo cliente, nombre cliente y saldo en forma de label's.
			Label(info_saldos, width=15, text = cliente_det[0]).place(relx=0.45, rely=0.07)
			Label(info_saldos, width=15, text = cliente_det[1]).place(relx=0.45, rely=0.22)
			Label(info_saldos, width=15, text = cliente_det[3]).place(relx=0.45, rely=.68)

			# Eliminamos detalles previos para evitar que se remonten los conceptos antiguos.
			concepto_det.delete(*concepto_det.get_children())

			# Tratamos la insercción y manejo de los botones inferiores + entrada de acuerdo a si es cero o no el saldo.
			if cliente_det[3]!=0: 

				btnSaldarCliente["state"]="normal"
				btnAbonoCliente["state"]="normal"
				entAbonoCliente["state"]="normal"

				for i in concepto:
					concepto_det.insert("", END, values=i.split())
					concepto_det.insert("", END, values=i.split())

				# for i in fechas:
					# concepto_det.insert("", END, iid=i[0][0:16], values=("", i[0], ""))
					# concepto_det.insert(i[0][0:16], values=())

			else:

				btnAbonoCliente["state"]="disabled"
				entAbonoCliente["state"]="disabled"
				btnSaldarCliente["state"]="disabled"

				concepto_det.insert("", END, values=[0, "SALDADO", 0])

			concepto_det.place(relx=0.45, rely=.4, relwidth=0.45, relheight=0.24)


		@conexiones.decoradorBaseDatos
		def abonarSaldo(tipo, cursor, valor): 

			'''
			<STR tipo> = "SALDAR" || "ABONAR"
			<LIST valor> = ["cod_cliente", "nombre_cliente", "concepto", saldo]

			'''

			if tipo == "SALDAR":

				# En orden descendente para asignarle a saldado el valor de la última factura.
				cursor.execute("SELECT COD_FACTURA FROM SALDOS WHERE COD_CLIENTE = (?) ORDER BY COD_FACTURA DESC",(str(valor[0]).zfill(2),))
				codigo_fact = cursor.fetchall()

				cursor.execute("DELETE FROM SALDOS WHERE COD_CLIENTE = (?)", (str(valor[0]).zfill(2),))
				cursor.execute("INSERT INTO SALDOS(COD_CLIENTE, NOMBRE_CLIENTE, COD_FACTURA, CONCEPTO, SALDO) VALUES (?,?,?,?,?)",(str(valor[0]).zfill(2), valor[1], codigo_fact[0][0], "SALDADO", 0) )

				messagebox.showinfo("PAGO EXITOSO", "SE EFECTÚO EL PAGO CORRECTAMENTE")
				# borrarClientesDetalle()
				actualizarClienteDetalle(codigo = valor[0], nombre = valor[1], factura = codigo_fact[0][0])
				# crearClientes(self.rescatarSaldos(cursor))
		

			elif tipo == "ABONAR":

				if entAbonoCliente.get()!="" and int(entAbonoCliente.get())%100==0:

					codigo_cliente = str(valor[0]).zfill(2)
					cursor.execute("SELECT SALDO, COD_FACTURA FROM SALDOS WHERE COD_CLIENTE = (?)",(codigo_cliente,))
					saldosBD = cursor.fetchall()
					valor_abonar = int(entAbonoCliente.get())
					saldo_total = sum([i[0] for i in saldosBD])

					if valor_abonar ==0:
						return

					# si el abono es menor a lo que debe, se mira hasta cual factura se borra 
					if valor_abonar <= saldo_total:

						# se inicializa la factura en 0, y el codigo de la factura en ""
						sumatoria_saldos = 0
						numero_factura = 0
						codigo_factura = ""

						for i in range(len(saldosBD)):
							if sumatoria_saldos>=valor_abonar:
								codigo_factura=saldosBD[i][1]
								break
							else:
								numero_factura+=1
								sumatoria_saldos+=saldosBD[i][0]

						print("numero_factura: ",numero_factura)
						print("codigo_factura",codigo_factura)
						print("sumatoria_saldos",sumatoria_saldos)
						cursor.execute("SELECT * FROM SALDOS WHERE COD_CLIENTE = (?) AND COD_FACTURA BETWEEN (?) AND (?)", (codigo_cliente, 0, codigo_factura))
						print("cursor.fetchall()",cursor.fetchall())
						print("se efectúa el abono por {}".format(valor_abonar))

					else:
						messagebox.showwarning("ERROR", "No se puede abonar más del valor del saldo total.")


		valorAbono = StringVar()

		interfaz = Toplevel()
		interfaz.geometry("900x600")
		interfaz.focus_set()

		# EXPERIMENTAL: método para poner en primer plano la interfaz
		# interfaz.grab_set()
		# interfaz.wm_attributes("-topmost", True)


		interfaz.bind("<Escape>", lambda _ : interfaz.destroy())

		info_saldos = Frame(interfaz)

		Label(info_saldos, text="CODIGO CLIENTE", width = 15).place(relx=0.05, rely=0.07)
		Label(info_saldos, text="NOMBRE CLIENTE", width=15).place(relx=0.05, rely=0.22)
		Label(info_saldos, text="CONCEPTO", width=15).place(relx=0.05, rely=.40)
		Label(info_saldos, text="SALDO", width=15).place(relx=0.05, rely=.68)

		tree = ttk.Treeview(interfaz, columns=('COD_CLIENTE', 'NOMBRE_CLIENTE', 'CONCEPTO','SALDO'), selectmode=BROWSE)

		tree.tag_bind("clienteSeleccionado", "<<TreeviewSelect>>", lambda event: imprimirDetalle(event))

		# Configuración de columnas
		tree.column('#0', width=0, anchor=CENTER, stretch=NO)  # Columna oculta para los índices
		tree.column('COD_CLIENTE', anchor=CENTER, width=50)
		tree.column('NOMBRE_CLIENTE', anchor=CENTER, width=110)
		tree.column('CONCEPTO', anchor=CENTER, width=0, stretch=NO)
		tree.column('SALDO', anchor=CENTER, width=80)

		# Configuración de encabezados
		tree.heading('#0', text='NUMERO', anchor=CENTER)
		tree.heading('COD_CLIENTE', text='CODIGO', anchor=CENTER)
		tree.heading('NOMBRE_CLIENTE', text='NOMBRE', anchor=CENTER)
		tree.heading('CONCEPTO', text='CONCEPTO', anchor=CENTER)
		tree.heading('SALDO', text='SALDO', anchor=CENTER)

		concepto_det = ttk.Treeview(info_saldos, columns=("CANTIDAD", "ARTICULO", "PRECIO"), selectmode=NONE)

		concepto_det.column("#0", width=0, stretch=NO)
		concepto_det.column("CANTIDAD", width=20, anchor = "e", stretch=NO)	# No ajustamos por defecto ésta columna
		concepto_det.column("ARTICULO",width=50, anchor = "e")
		concepto_det.column("PRECIO", width=30, anchor = "e")

		concepto_det.heading("CANTIDAD", text="Q", anchor = "e")
		concepto_det.heading("ARTICULO", text="ARTICULO", anchor = "e")
		concepto_det.heading("PRECIO", text="PRECIO", anchor = "e")


		btnSaldarCliente = Button(info_saldos, text="SALDAR", width=10, command = lambda : abonarSaldo("SALDAR", tree.item(tree.selection())["values"]))
		btnSaldarCliente.place(relx=0.45, rely=0.78)


		btnAbonoCliente = Button(info_saldos, text="ABONAR", width=10, command = lambda : abonarSaldo("ABONAR", tree.item(tree.selection())["values"]))
		btnAbonoCliente.place(relx=0.68, rely=0.88)

		entAbonoCliente = Entry(info_saldos, width=20, textvariable = valorAbono , validate = "key", validatecommand= (info_saldos.register(self.validaciones.soloNumeros),"%P"))
		entAbonoCliente.place(relx=0.34, rely=0.88)

		# Insercción de datos
		crearClientes(self.rescatarSaldos(cursor))

		# Empaquetar el Treeview y el frame en la ventana de saldos.
		info_saldos.place(relx=0.5, relwidth=0.48, rely=0.02, relheight=0.96)
		tree.place(relx=0.02, relwidth=0.48, rely=0.02, relheight=0.96)

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

	@conexiones.decoradorBaseDatos
	def anhadirArticulo(self, cursor, codigo):

		def agregarArticulo(articulo):


			# articulo = pd.Series(articulo, index = ["CODIGO", "NOMBRE", "PRECIO_UNIT", "CANTIDAD_STOCK", "COSTO_UNIT"])			# articulo = (codigo, nombre, precio_unit, cant_stock, costo_unit)
			# verficamos que la cantidad en stock sea de almenos una para agregar al carro y verificamos que no esté ya en la lista.
			# if articulo[3] > 0:
			if articulo["CANTIDAD_STOCK"] > 0:

				indice_lista = [False,0]

				for i in range(len(self.listaCompra)):
					# verificamos si el articulo i de la lista coincide con el articulo que vamos agregar, es decir, si ya está en la lista.
					# if self.listaCompra[i][0] == articulo[0]:
					if self.listaCompra.loc[i,"CODIGO"] == articulo["CODIGO"]:
						indice_lista[0] = True
						indice_lista[1] = i
						break

				# self.listaCompra = pd.Dataframe(columns = ["CODIGO", "NOMBRE", "PRECIO_UNIT", "CANTIDAD_COMPRA", "SUB_TOTAL", "UTILIDAD"])

				# si está en la lista, comprobamos que el stock tenga mas o sea igual a la cantidad para llevar.
				if indice_lista[0]:

					if articulo["CANTIDAD_STOCK"] >= (self.listaCompra.loc[indice_lista[1],"CANTIDAD_COMPRA"]+1):
						
						articulo_modificar = self.listaCompra.iloc[indice_lista[1],:]
						pd.options.mode.chained_assignment = None

						# agregamos uno mas al carrito:
						articulo_modificar["CANTIDAD_COMPRA"] += 1

						articulo_modificar["SUB_TOTAL"] = articulo_modificar["PRECIO_UNIT"] * articulo_modificar["CANTIDAD_COMPRA"]
						articulo_modificar["UTILIDAD"] = int(articulo_modificar["UTILIDAD"]/(articulo_modificar["CANTIDAD_COMPRA"]-1)*articulo_modificar["CANTIDAD_COMPRA"])
						self.listaCompra.loc[indice_lista[1], ["CODIGO", "NOMBRE", "PRECIO_UNIT", "CANTIDAD_COMPRA", "SUB_TOTAL", "UTILIDAD"]] = articulo_modificar
					else:
						messagebox.showwarning(title = "STOCK AGOTADO", message = f"No hay unidades de {articulo[1].upper()} disponibles.")
				
				#si el articulo no está en el carrito de compra, borramos la cantidad de stock y le agregamos un articulo al carrito y el precio
				else:

					# agregamos el campo de subtotal que es equival al precio unitario:
					articulo = pd.concat([articulo, pd.Series(data = [articulo["PRECIO_UNIT"]], index = ["SUB_TOTAL"])])

					# Organizamos el orden de los campos:
					articulo = articulo.reindex(["CODIGO", "NOMBRE", "PRECIO_UNIT", "CANTIDAD_STOCK", "SUB_TOTAL", "UTILIDAD"])

					# renombramos correctamente los campos:
					articulo.index = ["CODIGO", "NOMBRE", "PRECIO_UNIT", "CANTIDAD_COMPRA", "SUB_TOTAL", "UTILIDAD"] 

					# Cambiamos el valor de la cantidad en stock por uno; que es la unidad del articulo que se va a comprar:
					articulo.at["CANTIDAD_COMPRA"]=1

					# Agregamos el artículo nuevo en la lista:
					self.listaCompra = pd.concat([self.listaCompra, articulo.to_frame().T], axis= 0, ignore_index=True)

					self.cantidadListaCompra.config(text=len(self.listaCompra))

			else:
				messagebox.showwarning(title="PROBLEMA", message= f"No hay {articulo.loc['NOMBRE']} en stock.")


		sql = "SELECT CODIGO, NOMBRE, PRECIO, CANTIDAD, UTILIDAD FROM INVENTARIO_PAPELERIA WHERE CODIGO = (?)"
		argumento = (codigo.upper(), )

		cursor.execute(sql, argumento)

		# Obtenemos el articulo que deseamos agregar
		articulo = cursor.fetchone()
		articulo = pd.Series(articulo, index = ["CODIGO", "NOMBRE", "PRECIO_UNIT", "CANTIDAD_STOCK", "UTILIDAD"])

		# comprobamos que el artículo esté en la base datos:
		agregarArticulo(articulo) if not isinstance(articulo.loc["NOMBRE"],numpy.float64) else messagebox.showwarning(title= "ERROR", message= f"No existe artículo con ese código.")
			
		# self.entCodigo.delete(0, END)
		# codigoArticulo.set("")

	def modificarArticulo(self):

		# * crear esta vista en objeto vistaArbol
		def crearVista():

			Label(modificarArticulos,text="ITEM").grid(column=0, row=0)
			Label(modificarArticulos,text="CÓDIGO").grid(column=1, row=0,pady=20, padx=5)
			Label(modificarArticulos,text="NOMBRE").grid(column=2, row=0)
			Label(modificarArticulos,text="PRECIO").grid(column=3, row=0)
			Label(modificarArticulos,text="CANTIDAD").grid(column=4, row=0)
			Label(modificarArticulos,text="TOTAL").grid(column=5, row=0)
			Label(modificarArticulos,text="ELIMINAR").grid(column=6, row=0)

			valorTotal = self.listaCompra["SUB_TOTAL"].sum()

			# self.listaCompra = ["CODIGO", "NOMBRE", "PRECIO_UNIT", "CANTIDAD_COMPRA", "SUB_TOTAL", "UTILIDAD"])
			# interfaz = "ITEM=POSICION DEL ARTICULO" "CODIGO" "NOMBRE" "PRECIO" "CANTIDAD" "TOTAL" "ELIMINAR"
			if len(self.listaCompra)>0:


				for i in range(len(self.listaCompra)):

					for k in range(7):

						# agregamos el indice a cada articulo agrupandolos por nombre
						if k == 0:

							etiqueta = Label(modificarArticulos, text=i)

						# agregamos el botón para eliminar de a un articulo.
						elif k != 6:
							
							etiqueta = Label(modificarArticulos, text=self.listaCompra.iloc[i, k-1])

						else:

							etiqueta=Button(modificarArticulos,text="Eliminar", command=lambda i=i : quitarArticulo(i))

						etiqueta.grid(column=k, row=i+1)

			Label(modificarArticulos, text="TOTAL------>").grid(column=0,columnspan=2,row=len(self.listaCompra)+2, sticky="nsew")


			self.lblTotal = Label(modificarArticulos, text="$ "+str(valorTotal))
			self.lblTotal.grid(column=5, row=len(self.listaCompra)+2)

			Button(modificarArticulos, text = "ELIMINAR TODO", command= reiniciarLista).grid(column = 6, row=self.lblTotal.grid_info()["row"])

		def reiniciarLista():

			# cuando presionamos eliminar todo, en la interfaz de la modicacion de compra.

			for w in modificarArticulos.winfo_children():
				w.destroy()

			self.listaCompra.drop(self.listaCompra.index, inplace=True)
			self.cantidadListaCompra.config(text=len(self.listaCompra))

			crearVista()

		def quitarArticulo(indice):

			for w in modificarArticulos.winfo_children():
				w.destroy()

			# self.listaCompra = ["CODIGO", "NOMBRE", "PRECIO_UNIT", "CANTIDAD_COMPRA", "SUB_TOTAL", "UTILIDAD"])
			if self.listaCompra.iloc[indice, 3] == 1:
				self.listaCompra.drop(index = indice, inplace=True)
				self.listaCompra.reset_index(drop=True, inplace=True)
			

			else:
				self.listaCompra.iloc[indice, 3]-= 1
				self.listaCompra.iloc[indice, 4] = int(self.listaCompra.iloc[indice, 2] * self.listaCompra.iloc[indice,3])

			self.cantidadListaCompra.config(text=len(self.listaCompra))
			crearVista()
			
		interfazArticulos = Toplevel()
		interfazArticulos.bind("<Escape>", lambda _ : interfazArticulos.destroy())
		interfazArticulos.focus_set()
		interfazArticulos.geometry("500x500")
		modificarArticulos = Frame(interfazArticulos)
		modificarArticulos.pack(expand = True, fill = BOTH)
		crearVista()

	def generarCodigoCliente(self,cursor):

		cursor.execute("SELECT COD_CLIENTE FROM SALDOS")
		return str(len(set([x[0] for x in cursor.fetchall()]))).zfill(2)


	@conexiones.decoradorBaseDatos
	def compra(self, cursor, **kwargs):

		# *incluir una nota cuando el check de incluir a saldo se presione.

		if self.menuOperacion.current()==0 or self.menuOperacion.current() ==1:
			self.ejecutar()
			return

		# generar la factura en el programa y registrarla en una tabla nueva (compras) en BBDD, debe contener:
		# codigoCompra-nombre-marca-cantidadComprada-utilidad.
		# actualizar la tabla inventario.
		
		# nos aseguramos que hayan productos en el carro de compra
		if self.listaCompra.empty:
			messagebox.showwarning(title="ERROR", message="No hay artículos que comprar.")
		else:

			# guardar la compra en BBDD con un id unico y la lista de los productos y posterior eliminar dicha lista

			cursor.execute("SELECT COD_FACTURA FROM HISTORIAL_COMPRA")

			lista_cod = set(cursor.fetchall())

			if self.boolAgregarASaldo.get():

				# self.listaCompra = pd.DataFrame(columns = ["CODIGO", "NOMBRE", "PRECIO_UNIT", "CANTIDAD_COMPRA", "SUB_TOTAL", "UTILIDAD"])

				concepto_final = [x.tolist() for x in self.listaCompra.loc[:, ["CANTIDAD_COMPRA", "NOMBRE", "SUB_TOTAL"]].values]
				concepto_final = ' ~ '.join([' '.join(map(str, sublista)) for sublista in concepto_final])
				total = self.listaCompra["SUB_TOTAL"].sum()

				# si NO marcamos cliente nuevo y el código es de dos dígitos. verificamos.
				if self.boolClienteNuevo.get() == False and len(self.entCodigoCliente.get())==2:

					cursor.execute("SELECT NOMBRE_CLIENTE FROM SALDOS WHERE COD_CLIENTE = (?)", (self.entCodigoCliente.get(),))

					# si está mas de una vez en la lista no me interesa
					nombre_saldo = cursor.fetchone()

					if nombre_saldo:

						cursor.execute("SELECT COD_FACTURA FROM HISTORIAL_COMPRA")
						cursor.execute("DELETE FROM SALDOS WHERE COD_CLIENTE = (?) AND CONCEPTO=(?)",(self.entCodigoCliente.get().upper(),"SALDADO"))
						# codigo_sgte = len(set([x[0] for x in cursor.fetchall()]))
						cursor.execute("INSERT INTO SALDOS (COD_CLIENTE, NOMBRE_CLIENTE, COD_FACTURA, CONCEPTO, SALDO) VALUES (?,?,?,?,?)",(self.entCodigoCliente.get().upper() ,nombre_saldo[0], len(set([x[0] for x in cursor.fetchall()])),concepto_final, total))
						self.entCodigoCliente.delete(0,END)

					else:
						messagebox.showwarning(title="ERROR", message=f"No existe deudor con el código {self.entCodigoCliente.get()}")
						self.entCodigoCliente.delete(0, END)
						return
					# else:)

				# si es cliente nuevo:
				elif self.boolClienteNuevo.get():
					if (len(self.entNombreCliente.get())<4 or len(self.entNombreCliente.get())>20):
						messagebox.showwarning(title= "ERROR", message = "El nombre no cumple con los requisitos. (entre 6 y 20 caracteres)")
						return

					else:
						cursor.execute("SELECT COD_FACTURA FROM HISTORIAL_COMPRA")
						codigo_sgte = len(set([x[0] for x in cursor.fetchall()]))
						cursor.execute("INSERT INTO SALDOS (COD_CLIENTE, NOMBRE_CLIENTE, COD_FACTURA, CONCEPTO, SALDO) VALUES (?,?,?,?,?)",(self.entCodigoCliente.get(), self.entNombreCliente.get(), codigo_sgte,concepto_final, total))
						messagebox.showinfo(title="CREACIÓN EXITOSA", message=f"Cliente {self.entCodigoCliente.get()} creado con éxito.")
						# self.entNombreCliente.delete(0,END)
						self.checkIncluirSaldo.invoke()

				elif self.entCodigoCliente.get() not in lista_cod:
					messagebox.showinfo(title="ERROR", message="El código no pertenece a ningun morador.")
					self.entCodigoCliente.delete(0, END)
					return


			# self.listaCompra = pd.DataFrame(columns = ["CODIGO", "NOMBRE", "PRECIO_UNIT", "CANTIDAD_COMPRA", "SUB_TOTAL", "UTILIDAD"])

			lista_factura = self.listaCompra
			lista_factura["COD_FACTURA"]=len(lista_cod)
			lista_factura = lista_factura[["COD_FACTURA", "CODIGO", "NOMBRE", "PRECIO_UNIT", "CANTIDAD_COMPRA", "SUB_TOTAL", "UTILIDAD"]]

			# cursor.executemany("""
			# 	INSERT INTO HISTORIAL_COMPRA (COD_FACTURA, COD_ARTICULO, ARTICULO, PRECIO_UNIT, CANTIDAD, PRECIO_TOT, GANANCIA_TOT ) VALUES (?,?,?,?,?,?,?)"""
			# 	,lista_factura)
			cursor.executemany("""
				INSERT INTO HISTORIAL_COMPRA (COD_FACTURA, COD_ARTICULO, ARTICULO, PRECIO_UNIT, CANTIDAD, PRECIO_TOT, GANANCIA_TOT ) VALUES (?,?,?,?,?,?,?)"""
				,lista_factura.values.tolist())

			# ACTUALIZAMOS LA CANTIDAD PARA CADA ARTÍCULO DE LA LISTA DE COMPRA EN LA BBDD

			for i in range(len(lista_factura)):
				cursor.execute("SELECT CANTIDAD FROM INVENTARIO_PAPELERIA WHERE CODIGO = (?)", (lista_factura.iloc[i, 1],))
				cantidad = cursor.fetchone()
				cursor.execute("UPDATE INVENTARIO_PAPELERIA SET CANTIDAD = (?) WHERE CODIGO = (?)",(cantidad[0]-lista_factura.iloc[i, 4], lista_factura.iloc[i, 1]))


			# pregunta = messagebox.askquestion(title="COMPRA",message=f"Total a pagar: $ {sum( i[4] for i in self.listaCompra)}\n¿Deseas imprimir la factura?")
			total = self.listaCompra["SUB_TOTAL"].sum()
			pregunta = messagebox.askquestion(title="COMPRA",message=f"Total a pagar: $ {total}\n¿Deseas imprimir la factura?")

			if pregunta == "no":
				pass
			else:
				# ***APRENDER PDF FORMATO PEQUEÑO
				factura = ""
				for articulo in lista_factura:
				    for campo in articulo:
				        factura += str(campo) + "\t"
				    factura+="\n"
				with open(f"factura_n_{len(lista_cod)}.txt","w") as f:
					f.write(factura)

				print("yes, se guardó el archivo")

			
			self.borrarCampos()

	def borrarCampos(self):

		self.listaCompra.drop(index=self.listaCompra.index, inplace=True)
		self.cantidadListaCompra["text"]=0

class InterfazAdministrativa(Tk):

	"""
	Clase que permite la QUERY del inventario, modificaciones y análisis del negocio.
	Contiene sus respectivos widgets interactivos.
	Cada vez que se crea una instacia, el tipo de ventana que arroja es una Toplevel
	"""
	# cuando se abra esta interfaz, que la ventana esté enfocada (cuando se crea, el foco está en la ppal)
	# *cambiar los botones de la interfaz a la ventana de inventario (crear, borrar(cuando se selecciona),..
	# actualizar(al seleccionar))
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

	@conexiones.decoradorBaseDatos
	def generarCodigo(self, cursor):

		if self.entCodigo["state"]=="normal" and self.entCodigo != "":

			cursor.execute("SELECT CODIGO FROM ARTICULOS_CREACION ORDER BY CODIGO")

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


	@conexiones.decoradorBaseDatos
	def crearArticulo(self, cursor):


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
					INSERT INTO INVENTARIO_PAPELERIA (CODIGO, NOMBRE, MARCA, CANTIDAD, PRECIO, COSTO, COMENTARIO)
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


	@conexiones.decoradorBaseDatos
	def verArticulo(self,cursor,tipo):

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

			print("hasta ahora van estos items: \n"+ "\n".join([x for x in interfazArbol.selection()]))

			btnEditarInventario.pack() if len(interfazArbol.selection())!=0 else btnEditarInventario.pack_forget()
				
		# posiciona el label frame que contendrá todas las vistas
		# self.frameDos.place(relx=.03,rely=.19,relwidth=.94,relheight=.8)
		self.frameDos.place(relx=.03,rely=.14, relwidth=.94,relheight=.85)
		
		Button(self.frameDos, text="CERRAR", width = 7, command= self.cerrarVistaInventario).pack(side=RIGHT, anchor="ne")
		btnEditarInventario = Button(self.frameDos, text="EDITAR", width = 9, command= lambda : print("menú para editar inventario"))
		
		# Button(self.frameDos, text="ELIMINAR", width = 7).pack(side=RIGHT, anchor="w")

		if tipo == "TOTAL":
			cursor.execute("""
				SELECT * FROM INVENTARIO_PAPELERIA ORDER BY NOMBRE
				""")

		elif tipo == "ESPECIFICO":

			cursor.execute("""
				SELECT * FROM INVENTARIO_PAPELERIA WHERE NOMBRE = (?)
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

	@conexiones.decoradorBaseDatos
	def actualizarArticulo(self,cursor):
		# *SE NECESITA ACTUALIZAR INVENTARIO, LO MEJOR ES TENER UN ENTRY EN EL INVENTARIO QUE SUME LOS ARTICULOS NUEVOS
		# *SE QUITA EL BOTÓN DE ACTUALIZACIONES INDIVIDUALES ¿?

		# CONEXION BBDD
		if self.entCodigo["state"]=="readonly":

			self.entCodigo["state"]="normal"

			actualizacion = (self.entNombre.get().upper(), self.entMarca.get().upper(), self.entCantidad.get().upper(), self.entPrecio.get().upper(), self.entCosto.get().upper(), self.entComentario.get().upper(), self.entCodigo.get().upper())

			# conexion = sqlite3.connect("BASE_DATOS_PRUEBA.db")
			# cursor = conexion.cursor()
			cursor.execute("""
				UPDATE INVENTARIO_PAPELERIA SET NOMBRE=(?), MARCA=(?), CANTIDAD=(?), PRECIO=(?), COSTO=(?), COMENTARIO=(?) WHERE CODIGO=(?);
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
				SELECT CODIGO FROM INVENTARIO_PAPELERIA
				""")
			lectura = cursor.fetchall()
			confirmacion = False
			for i in lectura: 
				if i[0] == self.entCodigo.get().upper():
					confirmacion= True

			# Si el artículo está en BBDD, mostramos los datos en pantalla y bloqueamos el código.
			if confirmacion:

				cursor.execute("SELECT * FROM INVENTARIO_PAPELERIA WHERE CODIGO = (?)", (self.entCodigo.get().upper(),) )
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

	@conexiones.decoradorBaseDatos
	def eliminarArticulo(self,cursor):

		if self.entCodigo.get()!="":

			cursor.execute("SELECT * FROM INVENTARIO_PAPELERIA WHERE CODIGO = (?)",(self.entCodigo.get().upper(),))

			lectura = cursor.fetchone()
			lectura = pd.Series(data = lectura, index = ["CODIGO", "NOMBRE", "MARCA", "CANTIDAD", "PRECIO", "COSTO", "UTILIDAD", "COMENTARIO", "DISPONIBILIDAD"])
		
			if not isinstance(lectura, pandas.Series):
				messagebox.showwarning(title="ERROR",message="No existe producto con ese código")

			else:
				confirmacion = messagebox.askquestion(title="ELIMINACIÓN_CONFIRMACIÓN", message=f"¿Estás segur@ deseas eliminar el siguiente artículo:\n{lectura.loc['NOMBRE']}-{lectura.loc['MARCA']}?")
				
				if confirmacion == "yes":
					cursor.execute("DELETE FROM INVENTARIO_PAPELERIA WHERE CODIGO = (?)",(lectura[0][0],))
					messagebox.showinfo(title="ELIMINACION EXITOSA",message=f"{lectura[0][1]} - {lectura[0][2]}, eliminado con éxito.")	

		else:

			messagebox.showwarning(title="ERROR",message="NO has ingresado el código del artículo a eliminar.")

		self.borrarCampos()

	@conexiones.decoradorBaseDatos		
	def verGrafico(self, cursor, rango, categoria):


		# *organizar los diagramas de mayor a menor, con posibilidad de cambiar el orden
		# *integrar el gráfico al frameDos, que se pueda manipular de una mejor forma, contemplando la implementación de scroll
		# self.frameDos.place(relx=.03,rely=.19,relwidth=.94,relheight=.80)
		if rango == "DIA":
			# capturamos la opción elegida en la interfaz
			criterio = self.anho.get()+'-'+self.mes.get()+'-'+self.dia.get()
			cursor.execute("SELECT COD_ARTICULO, ARTICULO, CANTIDAD, PRECIO_TOT, GANANCIA_TOT FROM HISTORIAL_COMPRA WHERE DATE(FECHA) = DATE(?)", (criterio,))
			lista_vendidos = cursor.fetchall()

		elif rango == "MES":

			criterio = self.anho.get()+'-'+self.mes.get()+'%'
			cursor.execute("SELECT COD_ARTICULO, ARTICULO, CANTIDAD, PRECIO_TOT, GANANCIA_TOT FROM HISTORIAL_COMPRA WHERE FECHA LIKE (?)", (criterio,))
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

					cursor.execute("SELECT ARTICULO, CANTIDAD, GANANCIA_TOT, CAST(strftime('%H', FECHA) AS INTEGER) FROM HISTORIAL_COMPRA WHERE DATE(FECHA) = DATE(?)", (criterio,))

				else:

					# Creo un diccionario con los días en que el local abrió
					# *INCLUIR DIA DE SEMANA
					dicci = {x:0 for x in range(1,32)}

					cursor.execute("SELECT ARTICULO, CANTIDAD, GANANCIA_TOT, CAST(strftime('%d', FECHA) AS INTEGER) FROM HISTORIAL_COMPRA WHERE FECHA LIKE (?)", (criterio,))
				
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

	@conexiones.decoradorBaseDatos
	def verSaldos(self, cursor):
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
