import sqlite3

def decoradorBaseDatos(funcion):

	def modificadora(self, *args,**kwargs):

		conexion = sqlite3.connect("BASE_DATOS_PRUEBA.db")
		cursor = conexion.cursor()
		funcion(self, cursor, *args, **kwargs)
		conexion.commit()
		cursor.close()
		conexion.close()

	return modificadora


def decoradorBaseDatos2(funcion):

	def modificadora(self, *args,**kwargs):

		conexion = sqlite3.connect("BASE_DATOS_PRUEBA.db")
		cursor = conexion.cursor()
		funcion(self, cursor, conexion, *args, **kwargs)
		conexion.commit()
		cursor.close()
		conexion.close()

	return modificadora