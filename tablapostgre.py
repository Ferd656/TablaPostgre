"""
+-------------------------------------------------------------------------------+
| MODULO DE CLASE PARA EL MANEJO DE TABLAS POSTGRESQL                           |
| Desarrollado por: Ferdianndo Feoli Juarez                                     |
| Ultima actualizacion: 03/02/2019                                              |
|                                                                               |
| https://github.com/Ferd656                                                    |
| https://stackoverflow.com/story/ferdinandfeoli                                |
| http://www.linkedin.com/in/ferdinandfeoli                                     |
|                                                                               |
| Te ha sido de utilidad? En la siguiente direccion                             |
| puedes realizar una donacion voluntaria para apoyar el trabajo:               |
| https://paypal.me/Feoli                                                       |
|                                                                               |
+-------------------------------------------------------------------------------+
"""
# ---- Librerías necesarias ----
import getpass
import psycopg2
import pandas as pd
from datetime import datetime
from tkinter import messagebox
# ------------------------------


class TablaPostgre:
    """
    +-------------------------------------------------------------------------------+
    | Un objeto tabla PostgreSQL.                                                   |
    |                                                                               |
    | Simplifica el manejo de tablas en base de datos PostgreSQL al facilitar la    |
    | reutilizacion de las interacciones mas comunes:                               |
    |                                                                               |
    |   - Crear tabla (al inicializar metodo constructor)                           |
    |   - Ejecutar sentencia SQL personalizada (postgre)                            |
    |   - Enlistar columnas                                                         |
    |   - Contar filas                                                              |
    |   - Eliminar tabla                                                            |
    |   - Agregar item                                                              |
    |   - Eliminar item                                                             |
    |   - Actualizar item                                                           |
    |   - Agregar columna                                                           |
    |   - Eliminar columna                                                          |
    |   - Obtener tabla en DataFrame                                                |
    |                                                                               |
    | NOTA: Debe definir las credenciales de su base de datos mediante el código.   |
    |       Las credenciales por defecto son un ejemplo y por lo tanto              |
    |       no necesariamente son funcionales.                                      |
    +-------------------------------------------------------------------------------+
    """

    def __init__(self, usuario=getpass.getuser(),
                 nombre_tabla='mi_tabla',
                 columnas=()):
        """
        +-------------------------------------------------------------------------------+
        | Metodo constructor.                                                           |
        |                                                                               |
        | En este metodo se crea la tabla.                                              |
        |                                                                               |
        | Se pasa como argumento una lista con tres componentes:                        |
        |                                                                               |
        |    [0] = Nombre/ID del usuario que accede al objeto                           |
        |    [1] = Nombre de la tabla                                                   |
        |    [2] = Lista de columnas                                                    |
        |                                                                               |
        | La lista de columnas debe obedecer a una cadena valida para la definicion     |
        | de columnas de PostgreSQL.                                                    |
        | Documentacion: https://www.postgresql.org/docs                                |
        |                                                                               |
        | Una instancia de esta clase siempre creara una tabla con al menos las         |
        | siguientes columnas:                                                          |
        |                                                                               |
        |    - ITEM: llave única                                                        |
        |    - USUARIO_ACT: usuario que actualiza                                       |
        |    - FECHA_ACT: fecha de actualizacion                                        |
        +-------------------------------------------------------------------------------+
        """

        # Debe modificar la siguiente variable por un string que contenga las
        # credenciales de su base de datos. Tome las medidas de seguridad que
        # sean necesarias, en caso de que necesite una mayor seguridad, es
        # posible que necesite modificar el código.
        self.__credenciales = "dbname='ddmm9si91h4s8e' " + \
                              "user='twukjajaejjrpo' " + \
                              "password='e30899662c91c928a021e4eccbdc4cf19d07c17db028b31c8a6a6bf5391b6224' " + \
                              "host='ec2-54-243-228-140.compute-1.amazonaws.com' " + \
                              "port='5432'"
        # -------------------------------------------------------------------------------

        self.fecha = str(datetime.now())
        self.usuario = str(usuario)
        self.nombre_tabla = nombre_tabla.lower()
        self.columnas = ["item TEXT UNIQUE NOT NULL",
                         "usuario_act TEXT NOT NULL",
                         "fecha_act TIMESTAMP NOT NULL"]

        if len(columnas) > 0:
            for x in columnas:
                if (x[:5].lower() != "item " and
                   x[:12].lower() != "usuario_act " and
                   x[:10].lower() != "fecha_act ") or \
                    (x[:4].lower() != "item" and
                     x[:11].lower() != "usuario_act" and
                     x[:9].lower() != "fecha_act"):

                    self.columnas.append(x.lower())

        self.__sql_interno("CREATE TABLE IF NOT EXISTS " + self.nombre_tabla + " (" +
                           ','.join(self.columnas) + ")")

        if self.__existe():
            print("Tabla '" + self.nombre_tabla.lower() +
                  "' generada con las siguientes columnas: " + str(self.columnas).lower())
        else:
            print(chr(10)+"Tabla no generada")

    def __sql_interno(self, sql_str):
        """
        +-------------------------------------------------------------------------------+
        | Ejecuta una sentencia SQL pasada como argumento (string).                     |
        | Debe ser compatible con postgreSQL.                                           |
        | Si encuentra valores resultantes de la ejecición SQL devuelve dichos valores. |
        | En caso de fallar, mostrara una excepcion por pantalla.                       |
        |                                                                               |
        | Utilizar con cautela.                                                         |
        +-------------------------------------------------------------------------------+
        """
        c = ""
        try:
            __conn = psycopg2.connect(self.__credenciales)
            cur = __conn.cursor()
            cur.execute(sql_str)

            try:
                c = cur.fetchall()

            except Exception as e:
                c = e

            __conn.commit()
            __conn.close()

        except Exception as e:
            mensaje_error = chr(10) + "Alerta de excepción:" + chr(10)*2 + \
                  "    Se recomienda validar credenciales." if \
                  e.__class__.__name__ == "OperationalError" else \
                  chr(10) + "Alerta de excepción:" + chr(10)*2 + \
                  chr(32)*4 + str(e) + chr(10) + \
                  "Consulte la documentación de PostgreSQL en: " + \
                  "https://www.postgresql.org/docs"

            print(mensaje_error)
            messagebox.showerror("Excepción", mensaje_error)

        return c

    def __existe(self, elemento='', tipo_elemento='tabla'):
        """
        +-------------------------------------------------------------------------------+
        | Comprueba si un elemento existe. Debe estblecer el tipo de elemento que       |
        | desea comprobar y seguidamente su nombre.                                     |
        |                                                                               |
        | Devuelve verdadero o falso.                                                   |
        +-------------------------------------------------------------------------------+
        """
        tipo_elementos = ['tabla', 'columna', 'item']

        try:
            if tipo_elemento.lower() == 'tabla':
                # Comprueba tabla
                return self.__sql_interno("SELECT EXISTS(SELECT 1 FROM pg_catalog.pg_class AS c " +
                                          "JOIN pg_catalog.pg_namespace AS n " +
                                          "ON n.oid = c.relnamespace " +
                                          "WHERE c.relname = '" + self.nombre_tabla + "' AND " +
                                          "c.relkind = 'r');") != []

            elif tipo_elemento.lower() == 'columna':
                # Comprueba columna
                return self.__sql_interno("SELECT column_name FROM information_schema.columns " +
                                          "WHERE table_name = '" + self.nombre_tabla + "' AND " +
                                          "column_name='" + elemento + "'") != []

            elif tipo_elemento.lower() == 'item':
                # Comprueba item
                return int(self.__sql_interno("SELECT COUNT(*) FROM " +
                                              self.nombre_tabla +
                                              " WHERE item = '" +
                                              elemento + "'")[0][0]) > 0

            else:

                raise ValueError("Elemento inválido. Se esperaba: %s" % tipo_elementos)

        except Exception as e:
            mensaje_error = chr(10) + "Alerta de excepción:" + chr(10)*2 + \
                  "    Se recomienda validar credenciales." if \
                  e.__class__.__name__ == "OperationalError" else \
                  chr(10) + "Alerta de excepción:" + chr(10)*2 + \
                  chr(32)*4 + str(e) + chr(10) + \
                  "Consulte la documentación de PostgreSQL en: " + \
                  "https://www.postgresql.org/docs"
            print(mensaje_error)
            return False

    def sql(self, sql_str):
        """
        +-------------------------------------------------------------------------------+
        | Ejecuta una sentencia SQL pasada como argumento (string).                     |
        | Debe ser compatible con postgreSQL.                                           |
        |                                                                               |
        | Devuelve, e imprime por pantalla, un registro de la ejecucion.                |
        |                                                                               |
        | Utilizar con cautela.                                                         |
        +-------------------------------------------------------------------------------+
        """
        self.__sql_interno(sql_str)

        bitacora = "Sentencia SQL ejecutada por: " + \
                   self.usuario + \
                   " el " + str(self.fecha) + chr(10) + chr(10) + \
                   sql_str

        print(bitacora)
        return bitacora

    def cols(self):
        """
        +-------------------------------------------------------------------------------+
        | Devuelve una lista con los nombres de las columnas contenidas en la tabla.    |
        +-------------------------------------------------------------------------------+
        """
        lst = []
        sql_str = "SELECT column_name " + \
                  "FROM information_schema.columns " + \
                  "WHERE table_name = '%s'" % self.nombre_tabla

        aux = self.__sql_interno(sql_str)

        for i in aux:
            lst.append(i[0])

        return lst

    def n_filas(self):
        """
        +-------------------------------------------------------------------------------+
        | Devuelve el numero de filas (registros) de la tabla.                          |
        +-------------------------------------------------------------------------------+
        """
        sql_str = "SELECT count(*) " + \
                  "FROM " + self.nombre_tabla

        aux = self.__sql_interno(sql_str)

        return int(aux[0][0])

    def eliminar(self):
        """
        +-------------------------------------------------------------------------------+
        | Elimina la tabla creada por la instanciacion de la clase                      |
        | Su uso esta pensado principalmente para casos en los que se necesite          |
        | reciclar un objeto.                                                           |
        |                                                                               |
        | Devuelve, e imprime por pantalla, un registro de la eliminacion de la tabla.  |
        |                                                                               |
        | Utilizar con cautela.                                                         |
        +-------------------------------------------------------------------------------+
        """
        if self.__existe():
            self.__sql_interno("DROP TABLE IF EXISTS " + self.nombre_tabla)

            if not self.__existe():
                bitacora = "Tabla '" + self.nombre_tabla + \
                           "' eliminada por: " + self.usuario + \
                           " el " + self.fecha

            else:
                bitacora = "Tabla no eliminada."
                messagebox.showwarning("Advertencia", bitacora)

        else:
            bitacora = "No se encontró la tabla para eliminar."
            messagebox.showwarning("Advertencia", bitacora)

        print(bitacora)
        return bitacora

    def agregar_item(self, **kwargs):
        """
        +-------------------------------------------------------------------------------+
        | Agrega un item a la tabla, recibe como argumento un conjunto de               |
        | valores cuyas llaves corresponden a los nombres de las columnas               |
        | definidas en la instancia.                                                    |
        |                                                                               |
        | Devuelve, e imprime por pantalla, un registro de la adicion del item.         |
        +-------------------------------------------------------------------------------+
        """
        t = [x.lower() for x in self.cols()]

        item = ("NULL" if kwargs.get("item") is None else
                str(kwargs.get("item")))

        sql_str = "INSERT INTO " + self.nombre_tabla + " (" + \
                  (t[0] if len(t) == 1 else ', '.join(t)) + ") " + \
                  "VALUES('" + item + \
                  "','" + self.usuario + "', '" + self.fecha + "'"

        t.remove('item')
        t.remove('usuario_act')
        t.remove('fecha_act')

        if len(t) > 0:
            for i in t:
                sql_str += "," + ("'" + str(kwargs.get(i)) + "'" if
                                  isinstance(kwargs.get(i), str) else
                                  "NULL" if kwargs.get(i) is None else
                                  str(kwargs.get(i)))

        sql_str += ")"

        self.__sql_interno(sql_str)

        if kwargs.get("item") is not None and self.__existe(tipo_elemento='item', elemento=item):
            bitacora = "Item " + item + " agregado por: " + self.usuario + \
                       " el " + self.fecha
        else:
            bitacora = "Item no agregado."
            messagebox.showwarning("Advertencia", bitacora)

        print(bitacora)
        return bitacora

    def eliminar_item(self, item):
        """
        +-------------------------------------------------------------------------------+
        | Elimina un registro que contiene un item dado.                                |
        |                                                                               |
        | Devuelve, e imprime por pantalla, un registro de la eliminacion del item.     |
        +-------------------------------------------------------------------------------+
        """
        if self.__existe(tipo_elemento='item', elemento=item):
            self.__sql_interno("DELETE FROM " + self.nombre_tabla +
                               " WHERE item = '" + item + "'")
            bitacora = "Item " + item + " eliminado por: " + self.usuario + \
                       " el " + self.fecha

        else:
            bitacora = "Item " + item + " no fue encontrado en la tabla."
            messagebox.showwarning("Advertencia", bitacora)

        print(bitacora)
        return bitacora

    def actualizar_item(self, llave, **kwargs):
        """
        +-------------------------------------------------------------------------------+
        | Actualiza un item de la tabla, recibe como argumento un conjunto de           |
        | valores cuyas llaves corresponden a los nombres de las columnas               |
        | definidas en la instancia.                                                    |
        |                                                                               |
        | Devuelve, e imprime por pantalla, un registro de la actualizacion del item.   |
        +-------------------------------------------------------------------------------+
        """

        if llave is None or len(llave) <= 0:
            bitacora = "Item no actualizado." + chr(10) + \
                       "Revise:" + chr(10) + chr(10) + \
                       "   - La llave es obligatoria"

            messagebox.showwarning("Advertencia", bitacora)

        elif not isinstance(llave, str):
            bitacora = "Item no actualizado." + chr(10) + \
                       "Revise:" + chr(10) + chr(10) + \
                       "   - Tipo de dato de llave"

            messagebox.showwarning("Advertencia", bitacora)

        elif not self.__existe(tipo_elemento='item', elemento=llave):
            bitacora = "Item no actualizado." + chr(10) + \
                       "Revise:" + chr(10) + chr(10) + \
                       "   - Que la llave exista en la tabla"
            messagebox.showwarning("Advertencia", bitacora)

        else:
            t = [x.lower() for x in self.cols()]

            sql_str = "UPDATE " + self.nombre_tabla + " SET "

            if kwargs.get("item") is not None:
                sql_str += "item = '" + str(kwargs.get("item")) + "'"
                sql_str += ",usuario_act = '" + self.usuario + "'"

            else:
                sql_str += "usuario_act = '" + self.usuario + "'"

            sql_str += ",fecha_act = '" + self.fecha + "'"

            t.remove('item')
            t.remove('usuario_act')
            t.remove('fecha_act')

            if len(t) > 0:
                for i in t:
                    if kwargs.get(i) is not None:
                        sql_str += "," + i + " = " + \
                                str(kwargs.get(i))

            sql_str += " WHERE item = '" + llave + "'"

            self.__sql_interno(sql_str)

            bitacora = "Item '" + llave + "' actualizado por: " + self.usuario + \
                       " el " + str(self.fecha)

        print(bitacora)
        return bitacora

    def agregar_columna(self, columna):
        """
        +-------------------------------------------------------------------------------+
        | Recibe una cadena de texto con el nombre de la columna y su tipo de datos     |
        | para añadir dicha columna a la tabla.                                         |
        |                                                                               |
        | Devuelve, e imprime por pantalla, un registro de la actualizacion de          |
        | la tabla.                                                                     |
        +-------------------------------------------------------------------------------+
        """
        c = columna.split(" ")

        if not self.__existe(tipo_elemento='columna', elemento=c[0]):
            self.__sql_interno("ALTER TABLE " + self.nombre_tabla +
                               " ADD COLUMN " + " ".join(c))

            if not not self.__existe(tipo_elemento='columna', elemento=c[0]):
                bitacora = "Columna '" + c[0] + "' agregada por: " + self.usuario + \
                           " el " + str(self.fecha)

            else:
                bitacora = "Columna no agregada."
                messagebox.showwarning("Advertencia", bitacora)

        else:
            bitacora = "Columna ya existe."
            messagebox.showwarning("Advertencia", bitacora)

        print(bitacora)
        return bitacora

    def eliminar_columna(self, columna):
        """
        +-------------------------------------------------------------------------------+
        | Recibe una cadena de texto con el nombre de la columna para eliminar          |
        | dicha columna de la tabla.                                                    |
        |                                                                               |
        | Devuelve, e imprime por pantalla, un registro de la actualizacion de          |
        | la tabla.                                                                     |
        +-------------------------------------------------------------------------------+
        """
        if not not self.__existe(tipo_elemento='columna', elemento=columna):
            self.__sql_interno("ALTER TABLE " + self.nombre_tabla +
                               " DROP COLUMN " + columna)

            if not self.__existe(tipo_elemento='columna', elemento=columna):
                bitacora = "Columna '" + columna + "' eliminada por: " + self.usuario + \
                           " el " + str(self.fecha)

            else:
                bitacora = "Columna no eliminada."
                messagebox.showwarning("Advertencia", bitacora)

        else:
            bitacora = "Columna no encontrada."
            messagebox.showwarning("Advertencia", bitacora)

        print(bitacora)
        return bitacora

    def dataframe(self):
        """
        +-------------------------------------------------------------------------------+
        | Devuelve la tabla como dataframe.                                             |
        +-------------------------------------------------------------------------------+
        """
        __conn = psycopg2.connect(self.__credenciales)
        sql_str = "SELECT * FROM " + self.nombre_tabla
        df = pd.read_sql_query(sql_str, con=__conn)

        return df
