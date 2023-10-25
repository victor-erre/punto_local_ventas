# * : Tarea local, propiamente de la función donde se sitúa.
# ** : Tarea global, puede ser de una función dentro de la misma clase, de clase/raiz o en integración con otras clases
# *** : Tarea asignada al modelo de negocio que se está diseñando
# ? : Punto a investigar o analizar a detalle

import sqlite3
import datetime
import time
import os
import locale

locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
 
def conexionBBDD(funcion_ppal):
	"""
	DECORADOR, abre y cierra la conexion con la BBDD. Permite usar el cursor y la conexion para comitear cambios hechos
	dentro de la funcion decorada (accesibles en forma de llave)
	"""

	def funcion_interna(*args, **kwargs):

		# ***ELEGIR el nombre de la BBDD de acuerdo al usuario final
		# ? Conveniencia de cambiar el nombre de la base de datos c/mes
		conexion = sqlite3.connect("BASE_DATOS_{}.db".format(datetime.date.today().strftime('%B').upper()))
		cursor = conexion.cursor()
		kwargs = {"cursor": cursor, "conexion": conexion}
		funcion_ppal(*args, **kwargs)
		conexion.commit()
		cursor.close()
		conexion.close()

	return funcion_interna


@conexionBBDD
def borrarTablas(**kwargs):

	"""
	USO INTERNO: Para formatear la BBDD en caso de modificaciones estructurales
	"""
	try:
		cursor = kwargs["cursor"]
		cursor.executescript("""
			DROP TABLE INVENTARIO;
			DROP TABLE ART_CREACION;
			DROP TABLE ART_ACTUALIZACION; 
			DROP TABLE ART_ELIMINACION; 
			DROP TABLE VENTAS;
			DROP TABLE SALDOS;
		""")

		print("Tablas ELIMINADAS con ÉXITO")

	except:

		print("ERROR -> borrarTablas")

@conexionBBDD
def crearTablas(*args, **kwargs):

	"""
	CREACIÓN de las tablas que contendrá la BBDD
	"""

	cursor = kwargs["cursor"]
	conexion = kwargs["conexion"]

	cursor.execute("""CREATE TABLE INVENTARIO (
												CODIGO VARCHAR(5) NOT NULL,
												ARTICULO VARCHAR(20) NOT NULL,
												MARCA VARCHAR(20) NOT NULL,
												CATEGORIA VARCHAR(15) DEFAULT "GENERAL",
												STOCK INTEGER CHECK(STOCK >= 0 AND STOCK <= 999) NOT NULL, 
												PRECIO INTEGER NOT NULL,
												COSTO INTEGER NOT NULL,
												UTILIDAD INTEGER GENERATED ALWAYS AS (PRECIO - COSTO),
												COMENTARIO VARCHAR(50) DEFAULT "NULL",
												PRIMARY KEY (CODIGO)
												)""")

	cursor.execute("""CREATE TABLE ART_CREACION (
													CODIGO VARCHAR(5),
													ARTICULO VARCHAR(20) NOT NULL,
													MARCA VARCHAR(20) NOT NULL,
													FECHA DATETIME DEFAULT (DATETIME('now','localtime')),
													PRIMARY KEY (CODIGO)
													)
											
					""")

	cursor.execute("""CREATE TABLE ART_ACTUALIZACION (
															CODIGO VARCHAR(5) NOT NULL, 
															ARTICULO VARCHAR(20) NOT NULL, 
															STOCK_VIEJO INTEGER NOT NULL, 
															STOCK_NUEVO INTEGER NOT NULL, 
															PRECIO_VIEJO INTEGER NOT NULL,
															PRECIO_NUEVO INTEGER NOT NULL,
															COSTO_VIEJO INTEGER NOT NULL, 
															COSTO_NUEVO INTEGER NOT NULL, 
															UTILIDAD INTEGER GENERATED ALWAYS AS (PRECIO_NUEVO - COSTO_NUEVO) STORED, 
															COMENTARIO VARCHAR(50) DEFAULT 'NULL', 
															FECHA DATETIME DEFAULT (DATETIME('now','localtime'))
															)
					""")

	cursor.execute("""CREATE TABLE ART_ELIMINACION (CODIGO VARCHAR(5),
														ARTICULO VARCHAR(20) NOT NULL,
														MARCA VARCHAR(20) NOT NULL,
														FECHA DATETIME DEFAULT (DATETIME('now','localtime')),
														PRIMARY KEY (CODIGO))
														
					""")
	cursor.execute("""CREATE TABLE VENTAS (
											FACTURA INTEGER,
											CODIGO VARCHAR(5) NOT NULL,
											ARTICULO VARCHAR(20) NOT NULL,
											CANTIDAD INTEGER NOT NULL,
											PRECIO_TOT INTEGER NOT NULL, 
											COSTO_TOT INTEGER NOT NULL,
											UTILIDAD INTEGER GENERATED ALWAYS AS (PRECIO_TOT - COSTO_TOT),
											FECHA DATETIME DEFAULT (DATETIME('now','localtime'))
	
											)

					""")

	# *Estudiar el almacenamiento de CONCEPTO
	cursor.execute("""CREATE TABLE SALDOS (
											CLIENTE VARCHAR(3) NOT NULL,
											NOMBRE VARCHAR(20) NOT NULL,
											FACTURA INTEGER NOT NULL,
											CONCEPTO TEXT NOT NULL,
											SALDO INTEGER NOT NULL,
											ABONO INTEGER NOT NULL DEFAULT 0,
											COMENTARIO TEXT NOT NULL DEFAULT "NULL",
											FECHA DATETIME DEFAULT (DATETIME('now','localtime'))
											-- PRIMARY KEY (FACTURA)
		)
		""")
	
	cursor.execute("""
					CREATE TRIGGER INVENTARIO_AI AFTER INSERT ON INVENTARIO FOR EACH ROW
					BEGIN
						INSERT INTO ART_CREACION (CODIGO, ARTICULO, MARCA)
						VALUES (NEW.CODIGO, NEW.ARTICULO, NEW.MARCA);
					END;
				""")

	cursor.execute("""CREATE TRIGGER INVENTARIO_AU AFTER UPDATE ON INVENTARIO FOR EACH ROW 
						BEGIN 
							INSERT INTO ART_ACTUALIZACION (CODIGO, ARTICULO, STOCK_VIEJO, STOCK_NUEVO, PRECIO_VIEJO, PRECIO_NUEVO, COSTO_VIEJO, COSTO_NUEVO, COMENTARIO) 
							VALUES (OLD.CODIGO, OLD.ARTICULO, OLD.STOCK, NEW.STOCK, OLD.PRECIO, NEW.PRECIO, OLD.COSTO, NEW.COSTO, NEW.COMENTARIO); 
						END;
					""")

	cursor.execute("""CREATE TRIGGER INVENTARIO_BD BEFORE DELETE ON INVENTARIO FOR EACH ROW
						BEGIN
							INSERT INTO ART_ELIMINACION (CODIGO, ARTICULO, MARCA) 
							VALUES (OLD.CODIGO, OLD.ARTICULO, OLD.MARCA);
						END;
					""")

	# ? crear un trigger para manejar la actualización del inventario desde el uso de la tabla de ventas.

	print("Tablas CREADAS con ÉXITO.")



@conexionBBDD
def prueba(**kwargs):

	cursor = kwargs["cursor"]
	conexion = kwargs["conexion"]

	# CODIGO-ARTICULO-MARCA-(CATEGORIA)-STOCK-PRECIO-COSTO-(COMENTARIO)
	productos=[("PA001","BORRADOR","PELIKAN","PAPELERIA" ,17, 600, 150, "PEQUENHO"),
				("PA002","LAPIZ","MIRADO2","PAPELERIA" , 15, 1800, 1300, "REGULAR"),
				("PA003","SACAPUNTAS", "GENERICO","PAPELERIA" , 20, 500, 300, "REGULAR"),
				("PA004","LAPICERO", "BIC","PAPELERIA" , 10, 1300, 800, "NEGRO, AZUL"),
				("PA005","CUADERNO", "NORMA","PAPELERIA" , 18, 3500, 2600, "CUADRICULADO 100H"),
				("PA006","CARPETA", "SCRIB","PAPELERIA" , 6, 4200, 3000, "AZUL, ROSADA, NEGRA"),
				("PA007", "MARCADOR", "SHARPIE","PAPELERIA" , 10, 5200, 4100, "AZUL, ROJO, NEGRO"),
				("PA008", "CORRECTOR", "LIQUID PAPER","PAPELERIA" , 3, 5600, 3800, "REGULAR"),
				("PA009", "PEGAMENTO", "SCOTCH","PAPELERIA" , 10, 1200, 950, "PEQUENHO ESCOLAR"),
				("PA010", "RESALTADOR", "FABER-CASTTLE","PAPELERIA" , 5, 3600, 2800, "AMARILLO, VERDE"),
				("PA011", "COMPAS", "TREZOR","PAPELERIA" , 7, 8900, 6200, "METALICO")
				]

	cursor.execute("INSERT INTO SALDOS (CLIENTE, NOMBRE, FACTURA, CONCEPTO, SALDO) VALUES ('00','ADMIN', 0, 'SALDADO', 0)")

	cursor.executemany("INSERT INTO INVENTARIO VALUES(?,?,?,?,?,?,?,?)",productos)

	cursor.execute("INSERT INTO INVENTARIO(CODIGO, ARTICULO, MARCA, STOCK, PRECIO, COSTO) VALUES(?,?,?,?,?,?)", ("PA012", "CARPETA", "FOLIO",  12, 2000, 1300))
	cursor.execute("INSERT INTO VENTAS (CODIGO, ARTICULO, CANTIDAD, PRECIO_TOT, COSTO_TOT) VALUES ('PA000', 'ARTICULO_0', 0, 0, 0)")

	print("Pruebas EJECUTADAS con éxito")

def borrarBBDD(ruta):
	"""
	PRUEBA: si queremos eliminar BBDD del SO, se debe asignar la ruta.
	"""
	try:
		os.remove(ruta)
		print(f"Base de datos {os.path.basename(ruta)} eliminada con éxito")
	except FileNotFoundError as Error:
		print(f"No se pudo debido a que: ", Error)

# ++++++++++++++++++++++++++++    INSTRUCCIÓN DE PRUEBA      +++++++++++++++++++++++++++++++++++++++++++

print("hola")
# borrarBBDD("C:/Users/Victo/Documents/programacion/proyectos_propios/punto_local_ventas/BASE_DATOS_{}.db".format(datetime.date.today().strftime('%B').upper()))
# borrarTablas()	

# crearTablas()

# prueba()