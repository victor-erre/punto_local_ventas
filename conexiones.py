import sqlite3
import datetime
import locale

locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
# class Pruebas:

# 	def decoradorBaseDatos5(funcion):

# 		def modificadora(*args,**kwargs):
# 			conexion = sqlite3.connect("BASE_DATOS_PRUEBA.db")
# 			cursor = conexion.cursor()
# 			cursor.execute("DROP TABLE IF EXISTS PRUEBA_BBDD")
# 			cursor.execute("CREATE TABLE PRUEBA_BBDD (NOMBRE VARCHAR(3) DEFAULT 'JOE', EDAD INTEGER(3) DEFAULT 34 )")
# 			cursor.execute("INSERT INTO PRUEBA_BBDD VALUES (?,?)", ("JAIME",90))
# 			cursor.execute("INSERT INTO PRUEBA_BBDD(NOMBRE) VALUES (?)", ("GOMEZ",))
# 			kwargs = {"conexion":conexion, "cursor":cursor}
# 			funcion(*args, **kwargs)
# 			# print(args[0], type(args[0]))
# 			conexion.commit()
# 			cursor.close()
# 			conexion.close()

# 		return modificadora

# 	def __init__(self):
# 		self.var1 = "variable_uno"
# 		self.var2 = "variable_dos"
# 		self.var3 = "variable_tres"

# 	@decoradorBaseDatos5
# 	def generarCodigoCliente(*args, **kwargs):
# 		self = args[0]
# 		self.var4 = "variable_cuatro"
# 		print(self.var1)
# 		print(self.var4)
# 		conexion = kwargs["conexion"]
# 		cursor = kwargs["cursor"]
# 		cursor.execute("SELECT SUM(EDAD) FROM PRUEBA_BBDD")
# 		sumaEdad = cursor.fetchone()[0]
# 		print(sumaEdad)


# def decoradorBaseDatos2(funcion):

# 	def modificadora(var1 ,*args,**kwargs):

# 		conexion = sqlite3.connect("BASE_DATOS_PRUEBA.db")
# 		cursor = conexion.cursor()
# 		kwargs = {"conexion":conexion, "cursor":cursor}
# 		funcion(var1, *args, **kwargs)
# 		conexion.commit()
# 		cursor.close()
# 		conexion.close()

# 	return modificadora


# def decoradorBaseDatos(funcion):

# 	def modificadora(self, *args,**kwargs):

# 		conexion = sqlite3.connect("BASE_DATOS_PRUEBA.db")
# 		cursor = conexion.cursor()
# 		funcion(self, cursor, conexion, *args, **kwargs)
# 		conexion.commit()
# 		cursor.close()
# 		conexion.close()

# 	return modificadora

def decoradorBaseDatos3(funcion):

	def modificadora(*args,**kwargs):
		conexion = sqlite3.connect("BASE_DATOS_{}.db".format(datetime.date.today().strftime('%B').upper()))
		cursor = conexion.cursor()
		kwargs = {"conexion":conexion, "cursor":cursor}
		funcion(*args, **kwargs)
		conexion.commit()
		cursor.close()
		conexion.close()

	return modificadora

# entero = 2
# cadena = "prueba"
# diccionario = {"llave":"valor"}
# buleano = False
# pruebaGeneral = Pruebas()
# pruebaGeneral.generarCodigoCliente()
