import _sqlite3
import os
import platform


def clear_console():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


class ConexionBD:
    def __init__(self, dbname="ActividadFisica.db"):
        self.dbname = dbname
        self.conectar()

    def conectar(self):
        try:
            self.conexion = _sqlite3.connect(self.dbname)
            self.cursor = self.conexion.cursor()
            self.crear_tabla()
        except _sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def crear_tabla(self):
        query = '''
        CREATE TABLE IF NOT EXISTS actividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            duracion INTEGER NOT NULL,
            calorias_quemadas REAL NOT NULL
        )
        '''
        try:
            self.cursor.execute(query)
            self.conexion.commit()
        except _sqlite3.Error as e:
            print(f"Error al crear tabla: {e}")

    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()



class Actividad:
    def __init__(self, nombre, duracion, caloriasQ):
        self.nombre = nombre
        self.duracion = duracion 
        self.caloriasQ = caloriasQ

    def detalles(self):
        return f"Actividad: {self.nombre}, Duración: {self.duracion} minutos, Calorías quemadas: {self.caloriasQ} kcal."

    def __str__(self):
        return self.detalles()



class EjercicioCardio(Actividad):
    def detalles(self):
        return f"Ejercicio: {self.nombre}, Duración: {self.duracion} minutos, Calorías quemadas: {self.caloriasQ} kcal."



class CRUDActividad:
    def __init__(self):
        self.db = ConexionBD()

    def crear_actividad(self, actividad):
        query = "INSERT INTO actividades (nombre, tipo, duracion, calorias_quemadas) VALUES (?, ?, ?, ?)"
        try:
            self.db.cursor.execute(query, (actividad.nombre, actividad.__class__.__name__, actividad.duracion, actividad.caloriasQ))
            self.db.conexion.commit()
            print(f"Actividad '{actividad.nombre}' registrada con éxito.")
        except _sqlite3.Error as e:
            print(f"Error al insertar actividad: {e}")

    def leer_actividades(self):
        query = "SELECT * FROM actividades"
        try:
            self.db.cursor.execute(query)
            return self.db.cursor.fetchall()
        except _sqlite3.Error as e:
            print(f"Error al leer actividades: {e}")
            return []

    def actualizar_actividad(self, id_actividad, nombre=None, duracion=None, caloriasQ=None):
        query = "UPDATE actividades SET "
        params = []
        if nombre:
            query += "nombre = ?, "
            params.append(nombre)
        if duracion:
            query += "duracion = ?, "
            params.append(duracion)
        if caloriasQ:
            query += "calorias_quemadas = ? "
            params.append(caloriasQ)

        query = query.rstrip(", ")
        query += " WHERE id = ?"
        params.append(id_actividad)

        try:
            self.db.cursor.execute(query, params)
            self.db.conexion.commit()
            print("Actividad actualizada con éxito.")
        except _sqlite3.Error as e:
            print(f"Error al actualizar actividad: {e}")

    def eliminar_actividad(self, id_actividad):
        query = "DELETE FROM actividades WHERE id = ?"
        try:
            self.db.cursor.execute(query, (id_actividad,))
            self.db.conexion.commit()
            print("Actividad eliminada con éxito.")
        except _sqlite3.Error as e:
            print(f"Error al eliminar actividad: {e}")

    def cerrar_conexion(self):
        self.db.cerrar()



def obtener_entrada(mensaje, tipo_dato=int, opcional=False):
    while True:
        entrada = input(mensaje)
        if opcional and entrada == "":
            return None
        try:
            return tipo_dato(entrada)
        except ValueError:
            print(f"Por favor, ingresa un valor válido de tipo {tipo_dato.__name__}.")



def registrar_actividad(crud):
    nombre = input("Nombre de la actividad: ")
    duracion = obtener_entrada("Duración (minutos): ", int)
    calorias_quemadas = obtener_entrada("Calorías quemadas: ", float)

    actividad = EjercicioCardio(nombre, duracion, calorias_quemadas)
    crud.crear_actividad(actividad)


def ver_actividades(crud):
    actividades = crud.leer_actividades()
    if actividades:
        for actividad in actividades:
            print(f"ID: {actividad[0]}, Nombre: {actividad[1]}, Tipo: {actividad[2]}, Duración: {actividad[3]} minutos, Calorías: {actividad[4]} kcal")
    else:
        print("No hay actividades registradas.")


def actualizar_actividad(crud):
    id_actividad = obtener_entrada("ID de la actividad a actualizar: ", int)
    print("Deja en blanco los campos que no quieras modificar.")
    nombre = input("Nuevo nombre (opcional): ")
    duracion = obtener_entrada("Nueva duración (opcional): ", int, opcional=True)
    calorias_quemadas = obtener_entrada("Nuevas calorías quemadas (opcional): ", float, opcional=True)

    crud.actualizar_actividad(id_actividad, nombre, duracion, calorias_quemadas)


def eliminar_actividad(crud):
    id_actividad = obtener_entrada("ID de la actividad a eliminar: ", int)
    crud.eliminar_actividad(id_actividad)



def menu():
    clear_console()
    crud = CRUDActividad()
    while True:
        print("SEGUIMIENTO DE EJERCICIO")
        print("Elija la opción correspondiente")
        print("---------------------------------------------")
        print('''
        1.- Registrar nueva actividad 
        2.- Ver todas las actividades registradas
        3.- Actualizar una actividad previa
        4.- Eliminar una actividad
        5.- SALIR   
              ''')
        opc = obtener_entrada("Ingrese una opción: ", int)
        if opc == 1:
            registrar_actividad(crud)
        elif opc == 2:
            ver_actividades(crud)
        elif opc == 3:
            actualizar_actividad(crud)
        elif opc == 4:
            eliminar_actividad(crud)
        elif opc == 5:
            print("CERRANDO EL PROGRAMA............")
            crud.cerrar_conexion()
            break
        else:
            print("Opción inválida, intenta nuevamente.")


menu()
