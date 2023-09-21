import sqlite3
import datetime
import time
import os
 
def decoradorBBDD(funcion_ppal):
	def funcion_interna(*args):
		conexion = sqlite3.connect("BASE_DATOS_PRUEBA.db")
		cursor = conexion.cursor()
		funcion_ppal(cursor, *args)
		conexion.commit()
		cursor.close()
		conexion.close()

		# return resultado
	return funcion_interna


def borrarBBDD(ruta):
	try:
		os.remove(ruta)
		print(f"Base de datos {os.path.basename(ruta)} eliminada con éxito")
	except FileNotFoundError as Error:
		print(f"No se pudo debido a que: ", Error)

	

@decoradorBBDD
def borrarTablas(cursor):

	cursor.executescript("""
		DROP TABLE INVENTARIO_PAPELERIA;
		DROP TABLE ARTICULOS_ACTUALIZACION; 
		DROP TABLE ARTICULOS_ELIMINACION; 
		DROP TABLE ARTICULOS_CREACION;
	""")

	print("tablas eliminadas con éxito")

@decoradorBBDD
def crearTablas(cursor):


	cursor.execute("""CREATE TABLE INVENTARIO_PAPELERIA (CODIGO VARCHAR(5),
														NOMBRE VARCHAR(20) NOT NULL,
														MARCA VARCHAR(20) NOT NULL,
														CANTIDAD INTEGER CHECK(CANTIDAD >= 0 AND CANTIDAD <= 999) NOT NULL, 
														PRECIO INTEGER NOT NULL,
														COSTO INTEGER NOT NULL,
														UTILIDAD INTEGER GENERATED ALWAYS AS (PRECIO - COSTO) STORED, 
														COMENTARIO VARCHAR(50) NOT NULL,
														DISPONIBILIDAD GENERATED ALWAYS AS (CANTIDAD > 0) STORED, 
														PRIMARY KEY (CODIGO))
					""")

	cursor.execute("""CREATE TABLE ARTICULOS_CREACION (CODIGO VARCHAR(5) PRIMARY KEY,
													NOMBRE VARCHAR(20) NOT NULL,
													MARCA VARCHAR(20) NOT NULL,
													FECHA DATETIME DEFAULT (DATETIME('now','localtime')))
											
					""")

	cursor.execute("""CREATE TABLE ARTICULOS_ACTUALIZACION (CODIGO VARCHAR(5), 
															NOMBRE VARCHAR(20) NOT NULL, 
															MARCA VARCHAR(20) NOT NULL , 
															CANTIDAD_NUEVA INTEGER NOT NULL, 
															CANTIDAD_VIEJA INTEGER NOT NULL, 
															PRECIO_NUEVO INTEGER NOT NULL, 
															PRECIO_VIEJO INTEGER NOT NULL, 
															COSTO_NUEVO INTEGER NOT NULL, 
															COSTO_VIEJO INTEGER NOT NULL, 
															UTILIDAD INTEGER GENERATED ALWAYS AS (PRECIO_NUEVO - COSTO_NUEVO) STORED, 
															COMENTARIO VARCHAR(50), 
															DISPONIBILIDAD GENERATED ALWAYS AS (CANTIDAD_NUEVA > 0) STORED,
															FECHA DATETIME DEFAULT (DATETIME('now','localtime')))
					""")

	cursor.execute("""CREATE TABLE ARTICULOS_ELIMINACION (CODIGO VARCHAR(5) PRIMARY KEY,
														NOMBRE VARCHAR(20) NOT NULL,
														MARCA VARCHAR(20) NOT NULL,
														PRECIO INTEGER NOT NULL,
														COSTO INTEGER NOT NULL,
														COMENTARIO VARCHAR(50),
														FECHA DATETIME DEFAULT (DATETIME('now','localtime')))
														
					""")

	cursor.execute("""CREATE TABLE HISTORIAL_COMPRA (COD_FACTURA INTEGER NOT NULL,
													COD_ARTICULO VARCHAR(5),
													ARTICULO VARCHAR(20) NOT NULL,
													PRECIO_UNIT INTEGER NOT NULL, 
													CANTIDAD INTEGER NOT NULL,
													PRECIO_TOT INTEGER NOT NULL, 
													GANANCIA_TOT INTEGER NOT NULL,
													FECHA DATETIME DEFAULT (DATETIME('now','localtime'))
													)

					""")

	cursor.execute("""CREATE TABLE SALDOS (COD_CLIENTE VARCHAR(3) NOT NULL,
											NOMBRE_CLIENTE VARCHAR(20) NOT NULL,
											COD_FACTURA INTEGER NOT NULL,
											CONCEPTO TEXT NOT NULL,
											SALDO INTEGER NOT NULL,
											ABONO INTEGER NOT NULL DEFAULT 0,
											COMENTARIO TEXT NOT NULL DEFAULT "NULL",
											FECHA_SALDO DATETIME DEFAULT (DATETIME('now', 'localtime'))

		)
		""")
	cursor.execute("INSERT INTO SALDOS (COD_CLIENTE, NOMBRE_CLIENTE, COD_FACTURA, CONCEPTO, SALDO) VALUES ('00','ADMIN', 0, 'SALDADO', 0)")
	
	# cursor.execute("CREATE UNIQUE INDEX IND_COMPRA ON HISTORIAL_COMPRA(COD_FACTURA)")

	cursor.execute("""
					CREATE TRIGGER INVENTARIO_PAPELERIA_BI BEFORE INSERT ON INVENTARIO_PAPELERIA FOR EACH ROW
					BEGIN
						INSERT INTO ARTICULOS_CREACION (CODIGO, NOMBRE, MARCA)
						VALUES (NEW.CODIGO, NEW.NOMBRE, NEW.MARCA);
					END;
				""")

	cursor.execute("""CREATE TRIGGER INVENTARIO_PAPELERIA_AU AFTER UPDATE ON INVENTARIO_PAPELERIA FOR EACH ROW 
						BEGIN 
							INSERT INTO ARTICULOS_ACTUALIZACION (CODIGO, NOMBRE, MARCA, CANTIDAD_NUEVA, CANTIDAD_VIEJA, PRECIO_NUEVO, PRECIO_VIEJO, COSTO_NUEVO, COSTO_VIEJO, COMENTARIO) 
							VALUES (OLD.CODIGO, OLD.NOMBRE, OLD.MARCA, NEW.CANTIDAD, OLD.CANTIDAD, NEW.PRECIO, OLD.PRECIO, NEW.COSTO, OLD.COSTO, NEW.COMENTARIO); 
						END;
					""")

	cursor.execute("""CREATE TRIGGER INVENTARIO_PAPELERIA_BD BEFORE DELETE ON INVENTARIO_PAPELERIA FOR EACH ROW
						BEGIN
							INSERT INTO ARTICULOS_ELIMINACION (CODIGO, NOMBRE, MARCA, PRECIO, COSTO, COMENTARIO) 
							VALUES (OLD.CODIGO, OLD.NOMBRE, OLD.MARCA, OLD.PRECIO, OLD.COSTO, OLD.COMENTARIO);
						END;
					""")

	print("tablas creadas con éxito.")

@decoradorBBDD
def prueba(cursor):

	productos=[("PA001","BORRADOR","PELIKAN", 17, 600, 150, "PEQUENHO"),
				("PA002","LAPIZ","MIRADO2", 15, 1800, 1300, "REGULAR"),
				("PA003","SACAPUNTAS", "GENERICO", 20, 500, 300, "REGULAR"),
				("PA004","LAPICERO", "BIC", 10, 1300, 800, "NEGRO, AZUL"),
				("PA005","CUADERNO", "NORMA", 18, 3500, 2600, "CUADRICULADO 100H"),
				("PA006","CARPETA", "SCRIB", 6, 4200, 3000, "AZUL, ROSADA, NEGRA"),
				("PA007", "MARCADOR", "SHARPIE", 10, 5200, 4100, "AZUL, ROJO, NEGRO"),
				("PA008", "CORRECTOR", "LIQUID PAPER", 3, 5600, 3800, "REGULAR"),
				("PA009", "PEGAMENTO", "SCOTCH", 10, 1200, 950, "PEQUENHO ESCOLAR"),
				("PA010", "RESALTADOR", "FABER-CASTTLE", 5, 3600, 2800, "AMARILLO, VERDE"),
				("PA011", "COMPAS", "TREZOR", 7, 8900, 6200, "METALICO")
				]

	cursor.executemany("INSERT INTO INVENTARIO_PAPELERIA (CODIGO, NOMBRE, MARCA, CANTIDAD, PRECIO, COSTO, COMENTARIO ) VALUES(?,?,?,?,?,?,?)",productos)

	cursor.execute("INSERT INTO HISTORIAL_COMPRA (COD_FACTURA, COD_ARTICULO, ARTICULO, PRECIO_UNIT, CANTIDAD, PRECIO_TOT, GANANCIA_TOT) VALUES (0, 'PA000', 'ADMIN', 0, 0, 0, 0)")

	print("pruebas ejecutadas con éxito")

# ++++++++++++++++++++++++++++    INSTRUCCIÓN DE PRUEBA      +++++++++++++++++++++++++++++++++++++++++++

borrarBBDD("C:/Users/Victo/Documents/programacion/proyectos_propios/punto_local_ventas/BASE_DATOS_PRUEBA.db")

crearTablas()

prueba()

# borrarTablas()	
