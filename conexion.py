import sqlite3

from PyQt5 import QtSql


class Conexion():
    def create_BD(filename):
        """

        Recibe el nombre de la base de datos.
        Módulo que se ejecuta al principio del programa.
        Crea las tablas y carga municipios y provincias.
        Crea los directorios necesarios.
        :rtype: Object

        """
        try:
            con = sqlite3.connect(database=filename)
            cur = con.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS record (high_score INTEGER NOT NULL,user TEXT NOT NULL,date TEXT NOT NULL,PRIMARY KEY(high_score))')
            con.commit()
            con.close()
        except Exception as error:
            print('Error al crear DB', error)

    def db_connect(filedb):
        try:
            db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(filedb)
            if not db.open():
                print('Error al conectarse')
                return False
            else:
                print('Conexión establecida. ')
                return True
        except Exception as error:
            print('Problemas en conexión. ', error)

    def high_score(newScore):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('insert into record(high_score,user,date) VALUES(:high_score,:user,:date)')
            query.bindValue(':high_score', str(newScore[0]))
            query.bindValue(':user', str(newScore[1]))
            query.bindValue(':date', str(newScore[2]))
            if query.exec():
                print('Inserción correcta')
            else:
                print('Error')

        except Exception as error:
            print('Error al guardar high_score en base de datos', error)
