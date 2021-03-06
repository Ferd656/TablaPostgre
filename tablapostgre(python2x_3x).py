# coding=utf-8
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
    |   - Agregar registro                                                          |
    |   - Eliminar registro                                                         |
    |   - Actualizar registro                                                       |
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
        |    - llave: llave única obligatoria                                           |
        |    - USUARIO_ACT: usuario que actualiza                                       |
        |    - FECHA_ACT: fecha de actualizacion                                        |
        +-------------------------------------------------------------------------------+
        """

        # Debe modificar la siguiente variable por un string que contenga las
        # credenciales de su base de datos. Tome las medidas de seguridad que
        # sean necesarias, en caso de que necesite una mayor seguridad, es
        # posible que necesite modificar el código.
        self.__credenciales = "dbname='da0i8gojan20po' " + \
                              "user='lohpwehfinayeb' " + \
                              "password='63c6cf9c32cd53a4185c5ac27bd1e5da52404fffd52f95dda864c1efa8a59bda' " + \
                              "host='ec2-23-21-244-254.compute-1.amazonaws.com' " + \
                              "port='5432'"
        # -------------------------------------------------------------------------------

        self.fecha = str(datetime.now())
        self.usuario = str(usuario)
        self.nombre_tabla = nombre_tabla.lower()
        self.columnas = ["llave TEXT UNIQUE NOT NULL",
                         "usuario_act TEXT NOT NULL",
                         "fecha_act TIMESTAMP NOT NULL"]

        if len(columnas) > 0:
            for x in columnas:
                if (x[:5].lower() != "llave " and
                   x[:12].lower() != "usuario_act " and
                   x[:10].lower() != "fecha_act ") or \
                    (x[:4].lower() != "llave" and
                     x[:11].lower() != "usuario_act" and
                     x[:9].lower() != "fecha_act"):

                    self.columnas.append(x.lower())

        try:
            self.__sql_interno("CREATE TABLE IF NOT EXISTS " + self.nombre_tabla + " (" +
                               ','.join(self.columnas) + ")")

            print("Tabla '" + self.nombre_tabla.lower() +
                  "' generada con las siguientes columnas: " + str(self.columnas).lower())

        except Exception as e:
            print(chr(10)+"Tabla no generada" + chr(10)*2 + str(e))

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
        __conn = psycopg2.connect(self.__credenciales)
        cur = __conn.cursor()
        cur.execute(sql_str)

        try:
            c = cur.fetchall()

        except Exception as e:
            c = e

        __conn.commit()
        __conn.close()

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
        tipo_elementos = ['tabla', 'columna', 'llave']

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

        elif tipo_elemento.lower() == 'llave':
            # Comprueba LLA
            return int(self.__sql_interno("SELECT COUNT(*) FROM " +
                                          self.nombre_tabla +
                                          " WHERE llave = '" +
                                          elemento + "'")[0][0]) > 0

        else:
            raise ValueError("Elemento inválido. Se esperaba: %s" % tipo_elementos)

    def sql(self, sql_str):
        """
        +-------------------------------------------------------------------------------+
        | Ejecuta una sentencia SQL pasada como argumento (string).                     |
        | Debe ser compatible con postgreSQL.                                           |
        |                                                                               |
        | Devuelve, e imprime por pantalla, una notificacion de la ejecucion.           |
        |                                                                               |
        | Utilizar con cautela.                                                         |
        +-------------------------------------------------------------------------------+
        """
        try:
            c = self.__sql_interno(sql_str)

            bitacora = "Sentencia SQL ejecutada por: " + \
                       self.usuario + \
                       " en " + str(self.fecha) + chr(10)*2 + \
                       sql_str

        except Exception as e:
            bitacora = "Sentencia SQL no ejecutada." + chr(10)*2 + str(e)
            c = bitacora

        print(bitacora)
        return c

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

    def eliminame(self):
        """
        +-------------------------------------------------------------------------------+
        | Elimina la tabla creada por la instanciacion de la clase                      |
        | Su uso esta pensado principalmente para casos en los que se necesite          |
        | reciclar un objeto.                                                           |
        |                                                                               |
        | Devuelve, e imprime por pantalla, una notificacion de la eliminacion          |
        | de la tabla.                                                                  |
        |                                                                               |
        | Utilizar con cautela.                                                         |
        +-------------------------------------------------------------------------------+
        """
        if self.__existe():
            try:
                self.__sql_interno("DROP TABLE IF EXISTS " + self.nombre_tabla)

                bitacora = "Tabla '" + self.nombre_tabla + \
                           "' eliminada por: " + self.usuario + \
                           " en " + self.fecha

            except Exception as e:
                bitacora = "Tabla no eliminada." + chr(10)*2 + str(e)
                messagebox.showwarning("Advertencia", bitacora)

        else:
            bitacora = "No se encontró la tabla para eliminar."
            messagebox.showwarning("Advertencia", bitacora)

        print(bitacora)
        return bitacora

    def agregar_registro(self, **kwargs):
        """
        +-------------------------------------------------------------------------------+
        | Agrega un registro a la tabla, recibe como argumento un conjunto de           |
        | valores cuyas llaves corresponden a los nombres de las columnas               |
        | definidas en la instancia.                                                    |
        |                                                                               |
        | Devuelve, e imprime por pantalla, una notificacion de la adicion              |
        | del registro.                                                                 |
        +-------------------------------------------------------------------------------+
        """
        t = [x.lower() for x in self.cols()]

        llave = ("NULL" if kwargs.get("llave") is None else
                 str(kwargs.get("llave")))

        sql_str = "INSERT INTO " + self.nombre_tabla + " (" + \
                  (t[0] if len(t) == 1 else ', '.join(t)) + ") " + \
                  "VALUES('" + llave + \
                  "','" + self.usuario + "', '" + self.fecha + "'"

        t.remove('llave')
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

        if kwargs.get("llave") is not None and \
                self.__existe(tipo_elemento='llave', elemento=llave):
            bitacora = "Registro " + llave + " agregado por: " + self.usuario + \
                       " en " + self.fecha
        else:
            bitacora = "Registro no agregado."
            messagebox.showwarning("Advertencia", bitacora)

        print(bitacora)
        return bitacora

    def eliminar_registro(self, llave):
        """
        +-------------------------------------------------------------------------------+
        | Elimina un registro que contiene una llave dada.                              |
        |                                                                               |
        | Devuelve, e imprime por pantalla, una notificacion de la eliminacion          |
        | del registro.                                                                 |
        +-------------------------------------------------------------------------------+
        """
        if self.__existe(tipo_elemento='llave', elemento=llave):
            self.__sql_interno("DELETE FROM " + self.nombre_tabla +
                               " WHERE llave = '" + llave + "'")
            bitacora = "Registro " + llave + " eliminado por: " + self.usuario + \
                       " en " + self.fecha

        else:
            bitacora = "Registro " + llave + " no fue encontrado en la tabla."
            messagebox.showwarning("Advertencia", bitacora)

        print(bitacora)
        return bitacora

    def actualizar_registro(self, llave, **kwargs):
        """
        +-------------------------------------------------------------------------------+
        | Actualiza un registro de la tabla, recibe como argumento un conjunto de       |
        | valores cuyas llaves corresponden a los nombres de las columnas               |
        | definidas en la instancia.                                                    |
        |                                                                               |
        | Devuelve, e imprime por pantalla, una notificacion de la actualizacion        |
        | del registro.                                                                 |
        +-------------------------------------------------------------------------------+
        """

        if llave is None or len(llave) <= 0:
            bitacora = "Registro no actualizado." + chr(10) + \
                       "Revise:" + chr(10) + chr(10) + \
                       "   - La llave es obligatoria"

            messagebox.showwarning("Advertencia", bitacora)

        elif not isinstance(llave, str):
            bitacora = "Registro no actualizado." + chr(10) + \
                       "Revise:" + chr(10) + chr(10) + \
                       "   - Tipo de dato de llave"

            messagebox.showwarning("Advertencia", bitacora)

        elif not self.__existe(tipo_elemento='llave', elemento=llave):
            bitacora = "Registro no actualizado." + chr(10) + \
                       "Revise:" + chr(10) + chr(10) + \
                       "   - Que la llave exista en la tabla"
            messagebox.showwarning("Advertencia", bitacora)

        else:
            t = [x.lower() for x in self.cols()]

            sql_str = "UPDATE " + self.nombre_tabla + " SET "

            if kwargs.get("llave") is not None:
                sql_str += "llave = '" + str(kwargs.get("llave")) + "'"
                sql_str += ",usuario_act = '" + self.usuario + "'"

            else:
                sql_str += "usuario_act = '" + self.usuario + "'"

            sql_str += ",fecha_act = '" + self.fecha + "'"

            t.remove('llave')
            t.remove('usuario_act')
            t.remove('fecha_act')

            if len(t) > 0:
                for i in t:
                    if kwargs.get(i) is not None:
                        sql_str += "," + i + " = " + \
                                str(kwargs.get(i))

            sql_str += " WHERE llave = '" + llave + "'"

            self.__sql_interno(sql_str)

            bitacora = "Registro '" + llave + "' actualizado por: " + self.usuario + \
                       " en " + str(self.fecha)

        print(bitacora)
        return bitacora

    def agregar_columna(self, columna):
        """
        +-------------------------------------------------------------------------------+
        | Recibe una cadena de texto con el nombre de la columna y su tipo de datos     |
        | para añadir dicha columna a la tabla.                                         |
        |                                                                               |
        | Devuelve, e imprime por pantalla, una notificacion de la actualizacion de     |
        | la tabla.                                                                     |
        +-------------------------------------------------------------------------------+
        """
        c = columna.split(" ")

        if not self.__existe(tipo_elemento='columna', elemento=c[0]):
            self.__sql_interno("ALTER TABLE " + self.nombre_tabla +
                               " ADD COLUMN " + " ".join(c))

            if not not self.__existe(tipo_elemento='columna', elemento=c[0]):
                bitacora = "Columna '" + c[0] + "' agregada por: " + self.usuario + \
                           " en " + str(self.fecha)

            else:
                bitacora = "Columna no agregada."
                messagebox.showwarning("Advertencia", bitacora)

        else:
            bitacora = "Columna ya __existe."
            messagebox.showwarning("Advertencia", bitacora)

        print(bitacora)
        return bitacora

    def eliminar_columna(self, columna):
        """
        +-------------------------------------------------------------------------------+
        | Recibe una cadena de texto con el nombre de la columna para eliminar          |
        | dicha columna de la tabla.                                                    |
        |                                                                               |
        | Devuelve, e imprime por pantalla, una notificacion de la actualizacion de     |
        | la tabla.                                                                     |
        +-------------------------------------------------------------------------------+
        """
        if self.__existe(tipo_elemento='columna', elemento=columna):

            try:
                self.__sql_interno("ALTER TABLE " + self.nombre_tabla +
                                   " DROP COLUMN " + columna)

                bitacora = "Columna '" + columna + "' eliminada por: " + self.usuario + \
                           " en " + str(self.fecha)

            except Exception as e:
                bitacora = "Columna no eliminada." + chr(10)*2 + str(e)
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
