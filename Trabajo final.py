import json
import os
from datetime import datetime

# Mejora del sistema:
# Se implementa Programación Orientada a Objetos (POO) mediante la clase "Tarea",
# lo que permite representar cada tarea como un objeto con atributos y métodos propios.
# Esto mejora la organización del código, facilita su mantenimiento y permite
# escalar el sistema en el futuro agregando nuevas funcionalidades.
class Tarea:

    def __init__(self, id, descripcion, responsable, fecha_limite, prioridad, estado="Pendiente"):
        self.id = id
        self.descripcion = descripcion
        self.responsable = responsable
        self.fecha_limite = fecha_limite
        self.prioridad = prioridad
        self.estado = estado

# Mejora técnica:
# Este método convierte el objeto Tarea a un diccionario.
# Esto es necesario para poder almacenar los datos en formato JSON,
# ya que JSON no puede guardar directamente objetos de clases.
    def to_dict(self):
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "responsable": self.responsable,
            "fecha_limite": self.fecha_limite,
            "prioridad": self.prioridad,
            "estado": self.estado
        }

# Mejora del diseño del software:
# Se crea la clase "GestorTareas" que centraliza toda la lógica del sistema
# (crear, leer, actualizar y eliminar tareas). Esto separa la lógica del programa
# de la representación de los datos y permite una arquitectura más modular.
class GestorTareas:

    def __init__(self, archivo):
        self.archivo = archivo
        self.tareas = self.cargar_tareas()

    # ---------------------------
    # Cargar tareas
    # ---------------------------
# Mejora funcional:
# Esta función permite recuperar automáticamente las tareas almacenadas en el archivo JSON
# cuando el sistema inicia. Esto asegura persistencia de datos y evita la pérdida de información.
    def cargar_tareas(self):

        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, "r") as f:
                    data = json.load(f)
                    return [Tarea(**t) for t in data]
# Manejo de errores:
# Se captura el error JSONDecodeError en caso de que el archivo esté corrupto
# o mal formateado, evitando que el programa se cierre inesperadamente.            
            except json.JSONDecodeError:
                print("Error leyendo el archivo JSON.")
                return []
        return []

    # ---------------------------
    # Guardar tareas
    # ---------------------------
    def guardar_tareas(self):

        with open(self.archivo, "w") as f:
            json.dump([t.to_dict() for t in self.tareas], f, indent=4)

    # ---------------------------
    # Generar ID
    # ---------------------------
# Mejora del sistema:
# Esta función genera automáticamente un identificador único para cada tarea,
# evitando duplicación de IDs y facilitando la gestión de tareas dentro del sistema.    
    def generar_id(self):

        if not self.tareas:
            return 1
        return max(t.id for t in self.tareas) + 1

    # ---------------------------
    # Validar fecha
    # ---------------------------
# Mejora en la gestión de fechas:
# Se utiliza el módulo datetime para validar que el formato de la fecha sea correcto
# y que la fecha ingresada no sea anterior al día actual.
# Esto ayuda a evitar errores en la planificación de tareas.    
    def validar_fecha(self, fecha):

        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()

            if fecha_obj < datetime.now().date():
                print("La fecha no puede ser pasada.")
                return None

            return fecha_obj.strftime("%Y-%m-%d")

        except ValueError:
            print("Formato incorrecto. Use YYYY-MM-DD.")
            return None

    # ---------------------------
    # Validar prioridad
    # ---------------------------
    def validar_prioridad(self, prioridad):

# Uso de estructuras de datos:
# Se utiliza una tupla para almacenar las prioridades válidas.
# Las tuplas son inmutables, lo que garantiza que los valores permitidos
# no sean modificados accidentalmente durante la ejecución del programa.
        prioridades = ("Alta", "Media", "Baja")

        if prioridad.capitalize() in prioridades:
            return prioridad.capitalize()

        print("Prioridad inválida.")
        return None

    # ---------------------------
    # Crear tarea
    # ---------------------------
# Mejora funcional:
# Esta función permite registrar nuevas tareas solicitando información al usuario
# y validando los datos ingresados (fecha y prioridad). Posteriormente, la tarea
# es almacenada en memoria y guardada en el archivo JSON.
    def crear_tarea(self):

        descripcion = input("Descripción: ")
        responsable = input("Responsable: ")

        while True:
            fecha = input("Fecha límite (YYYY-MM-DD): ")
            fecha_valida = self.validar_fecha(fecha)

            if fecha_valida:
                break

        while True:
            prioridad = input("Prioridad (Alta/Media/Baja): ")
            prioridad_valida = self.validar_prioridad(prioridad)

            if prioridad_valida:
                break

        tarea = Tarea(
            self.generar_id(),
            descripcion,
            responsable,
            fecha_valida,
            prioridad_valida
        )

        self.tareas.append(tarea)

        self.guardar_tareas()

        print("Tarea creada exitosamente.")

    # ---------------------------
    # Mostrar tareas
    # ---------------------------
    def mostrar_tareas(self):

        if not self.tareas:
            print("No hay tareas registradas.")
            return

        fecha_actual = datetime.now().date()

        for tarea in self.tareas:

            fecha_tarea = datetime.strptime(tarea.fecha_limite, "%Y-%m-%d").date()
# Mejora de productividad:
# Se calcula automáticamente cuántos días faltan para la fecha límite,
# permitiendo mostrar alertas si una tarea está próxima a vencer o vencida.
# Esto ayuda a los equipos a priorizar mejor sus actividades.
            dias_restantes = (fecha_tarea - fecha_actual).days

            estado_extra = ""

            if dias_restantes < 0:
                estado_extra = "Tarea vencida"
            elif dias_restantes <= 3:
                estado_extra = "Próxima a vencer"

            print("----------------------------")
            print(f"ID: {tarea.id}")
            print(f"Descripción: {tarea.descripcion}")
            print(f"Responsable: {tarea.responsable}")
            print(f"Fecha límite: {tarea.fecha_limite} ({dias_restantes} días) {estado_extra}")
            print(f"Prioridad: {tarea.prioridad}")
            print(f"Estado: {tarea.estado}")
            print("----------------------------")

    # ---------------------------
    # Actualizar tarea
    # ---------------------------
    def actualizar_tarea(self):

        try:
            id_tarea = int(input("Ingrese ID de la tarea: "))
# Manejo de errores:
# Se captura un ValueError en caso de que el usuario ingrese un ID no numérico,
# evitando que el sistema se detenga por una entrada inválida.
        except ValueError:
            print("ID inválido.")
            return

        for tarea in self.tareas:

            if tarea.id == id_tarea:

                tarea.descripcion = input("Nueva descripción: ")
                tarea.responsable = input("Nuevo responsable: ")

                while True:
                    fecha = input("Nueva fecha límite (YYYY-MM-DD): ")
                    fecha_valida = self.validar_fecha(fecha)

                    if fecha_valida:
                        tarea.fecha_limite = fecha_valida
                        break

                while True:
                    prioridad = input("Nueva prioridad (Alta/Media/Baja): ")
                    prioridad_valida = self.validar_prioridad(prioridad)

                    if prioridad_valida:
                        tarea.prioridad = prioridad_valida
                        break

                estado = input("Estado (Pendiente/Completo): ")

                if estado.capitalize() in ("Pendiente", "Completo"):
                    tarea.estado = estado.capitalize()
# Persistencia de datos:
# Después de cada modificación (crear, actualizar o eliminar),
# el sistema guarda automáticamente los cambios en el archivo JSON,
# garantizando que la información no se pierda al cerrar el programa.
                self.guardar_tareas()

                print("Tarea actualizada.")
                return

        print("Tarea no encontrada.")

    # ---------------------------
    # Eliminar tarea
    # ---------------------------
    def eliminar_tarea(self):

        try:
            id_tarea = int(input("Ingrese ID a eliminar: "))
        except ValueError:
            print("ID inválido.")
            return

        for tarea in self.tareas:

            if tarea.id == id_tarea:

                self.tareas.remove(tarea)

                self.guardar_tareas()

                print("Tarea eliminada.")

                return

        print("Tarea no encontrada.")


def menu():
# Mejora del sistema:
# El usuario puede definir el nombre del archivo JSON donde se almacenarán las tareas.
# Esto permite utilizar el gestor para diferentes proyectos o equipos de trabajo.
    nombre_archivo = input("Nombre del archivo de tareas: ")

    archivo = f"{nombre_archivo}.json"

    gestor = GestorTareas(archivo)

    while True:

        print("\n--- GESTOR DE TAREAS ---")
        print("1. Crear tarea")
        print("2. Mostrar tareas")
        print("3. Actualizar tarea")
        print("4. Eliminar tarea")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            gestor.crear_tarea()

        elif opcion == "2":
            gestor.mostrar_tareas()

        elif opcion == "3":
            gestor.actualizar_tarea()

        elif opcion == "4":
            gestor.eliminar_tarea()

        elif opcion == "5":
            print("Saliendo del sistema.")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()