import psycopg2
import datetime


class TablaPostgre:
    """
    Un objeto tabla PostgreSQL
    Simplifica el manejo de base de datos PostgreSQL
    """

    def __init__(self, *args):
        """
        Método constructor.
        El argumento debe ser una lista con dos componentes:
            [0] = Nombre de la tabla
            [1] = lista de columnas
        La lista de columnas debe obedecer a un string válido
        de definición de columnas de PostgreSQL
        """
        self.__credenciales = "dbname='MiBaseDeDatos' user='postgres' " + \
                              "password='12345' host='localhost' port='5432'"
        self.now = datetime.datetime.now()
        self.config = []

        if args == ():
            self.config = ["MITABLA", ["ID INTEGER NOT NULL UNIQUE", "FECHA_ACT DATE NOT NULL"]]
        else:
            self.config = list(args)

        __conn = psycopg2.connect(self.__credenciales)
        cur = __conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS " + self.config[0] + " (" +
                    ','.join(self.config[1]) + ")")
        __conn.commit()
        __conn.close()

    def limpiar(self):
        __conn = psycopg2.connect(self.__credenciales)
        cur = __conn.cursor()
        cur.execute("DROP TABLE IF EXISTS " + self.config[0])
        __conn.commit()
        __conn.close()

    def agregar_item(self, *args):

        if args != ():
            __conn = psycopg2.connect(self.__credenciales)
            # cur = __conn.cursor()

            strng = "INSERT INTO MATERIAS VALUES ("

            for i in args:
                strng += i

            # strng = strng + ")"

            # cur.execute("INSERT INTO MATERIAS VALUES (%s,%s,%s,%s,%s,%s)",
            # (item, now, precio, actualizacion, medida, cantidad))
            # __conn.commit()

            __conn.close()


Tabla1 = TablaPostgre()
