import sqlite3
from sqlite3 import Error

import apoteka
import lijek
import select
import recept
import zaposleni


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)  # create connection to db_file
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)  # create s table from the create_table_sql statement
    except Error as e:
        print(e)


if __name__ == '__main__':
    # print header
    print("================================================================")
    print("-------------------- DOBRODOSLI U APOTEKU! ---------------------")
    print("================================================================")
    print("\n")

    ulaz = ''
    while ulaz != '0':
        # print header
        print("--------------------- IZABERITE KORISNIKA --------------------- ")
        print("-------- FARMACEUT [1] --- KNJIGOVODJA [2] --- KRAJ PROGRAMA [0]")

        ulaz = input("Izabrani korisnik: ")

        if ulaz == '1':
            print("Prijavljeni ste kao FARMACEUT")
            print("Imate pristup tabelama podataka LIJEKOVI [1] i RECEPTI [2]. IZLAZ[0]: ")
            pristup = ''

            while pristup != '0':
                pristup = input("Unesite komandu za pristup tabeli LIJEKOVI [1] i RECEPTI [2]. IZLAZ[0]: ")
                if pristup == '1':
                    print("---TABELA PODATAKA LIJEKOVI---")
                    operacija = ''
                    while operacija != '0':
                        operacija = input("DODAVANJE [1], BRISANJE[2], IZMJENA[3], ISPIS[4], IZLAZ[0]: ")
                        if operacija == '1':
                            print("DODAVANJE [1]")
                            sql_create_lijekovi_table = """ CREATE TABLE IF NOT EXISTS lijekovi(
                                                               id INTEGER PRIMARY KEY, 
                                                               naziv VARCHAR(30), 
                                                               kolicina INTEGER, 
                                                               cijenasapdv FLOAT, 
                                                               cijenabezpdv FLOAT, 
                                                               datum DATE
                                                           ); """
                            conn = create_connection("apoteke.db")  # create connection to apoteke.db
                            if conn is not None:
                                create_table(conn, sql_create_lijekovi_table)  # create table lijekovi
                                tabela = 'lijekovi'
                                lijek1 = lijek.Lijek()
                                b = lijek.create_lijek(conn, lijek1, tabela)  # create a new record lijek1 in table
                                conn.close()
                            else:
                                print("Error!")

                        elif operacija == '2':
                            print("BRISANJE [2]")
                            n = (input("Unesite id lijeka koji zelite obrisati: "))
                            lijek.delete_lijek(n)  # delete lijek

                        elif operacija == '3':
                            print("IZMJENA [3]")
                            n = input("Unesite naziv lijeka ciju cijenu je potrebno izmjeniti: ")
                            m = float(input("Unesite novu cijenu lijeka: "))
                            nnaziv = n.upper()
                            lijek.update_cijena(m, nnaziv)  # update lijek
                            novacijena = float(m * 0.83)
                            lijek.update_cijenabezpdv(novacijena, nnaziv)

                        elif operacija == '4':
                            print("ISPIS [4]")
                            baza = 'apoteke.db'
                            tabela1 = 'lijekovi'
                            tabela2 = 'lijekovizaotpis'
                            print("TABELA LIJEKOVA: ")
                            print("ID - Naziv - Kolicina - Cijena(PDV) - Cijena - Datum")
                            select.show_all(baza, tabela1)  # select all from lijekovi table
                            print("TABELA LIJEKOVA ZA OTPIS: ")
                            print("ID - Naziv - Kolicina - Cijena(PDV) - Cijena - Datum")
                            select.show_all(baza, tabela2)  # select all from lijekovizaotpis table
                        elif operacija != '0':
                            print("Nepoznata komanda!")
                    duzina_liste = len(lijek.Lijek.ListaZaOtpis)
                    if duzina_liste > 0:
                        sql_create_lijekovizaotpis_table = """ CREATE TABLE IF NOT EXISTS lijekovizaotpis(
                                                                                                id INTEGER PRIMARY KEY, 
                                                                                                naziv VARCHAR(30), 
                                                                                                kolicina INTEGER, 
                                                                                                cijenasapdv FLOAT, 
                                                                                                cijenabezpdv FLOAT, 
                                                                                                datum DATE
                                                                                                ); """
                        # create a connection to apoteka.db
                        conn = create_connection("apoteke.db")

                        if conn is not None:
                            # create a table lijekovizaotpis
                            create_table(conn, sql_create_lijekovizaotpis_table)
                            tabela = 'lijekovizaotpis'
                            # create a list of tuples from lista
                            lista = lijek.create_listalijekovazaotpis(duzina_liste)
                            conn.executemany("""INSERT INTO lijekovizaotpis
                                                        (id, naziv, kolicina, cijenasapdv, cijenabezpdv, datum) 
                                                        VALUES(?,?,?,?,?,?)""",
                                             lista)  # insert lista to lijekovizaotpis table
                            conn.commit()
                            conn.close()

                    else:
                        print("Lista za otpis lijekova je prazna!")
                        continue
                    print("IZLAZ IZ TABELE PODATAKA LIJEKOVA")

                elif pristup == '2':
                    print("---TABELA PODATAKA RECEPTI---")
                    operacija = ''
                    while operacija != '0':
                        operacija = input("DODAVANJE [1], BRISANJE[2], IZMJENA[3], ISPIS[4], IZLAZ[0]: ")
                        if operacija == '1':
                            print("DODAVANJE [1]")
                            sql_create_recepti_table = """ CREATE TABLE IF NOT EXISTS recepti(
                                                                                        brojrecepta INTEGER PRIMARY KEY, 
                                                                                        izdavacrecepta VARCHAR(50), 
                                                                                        pacijent VARCHAR(50),
                                                                                        lijek VARCHAR(50), 
                                                                                        datumizdavanja DATE, 
                                                                                        nacinupotrebe VARCHAR(50)
                                                                                       ); """
                            conn = create_connection("apoteke.db")  # create connection to apoteke.db
                            if conn is not None:
                                create_table(conn, sql_create_recepti_table)  # create table recepti
                                recept1 = recept.Recept()
                                r = recept.create_recept(conn, recept1)  # create a new record recept1 in table recepti
                                conn.close()
                            else:
                                print("Error!")

                        elif operacija == '2':
                            print("BRISANJE [2]")
                            n = int(input("Unesite broj recepta koji zelite obrisati:"))
                            recept.delete_recept(n)  # delete recept

                        elif operacija == '3':
                            print("IZMJENA [3]")
                            brojrecepta = int(input("Unesite broj recepta na kojem zelite izmjeniti naziv lijeka: "))
                            lijek1 = input("Novi lijek: ")
                            lijek = lijek1.upper()
                            recept.update_recept(lijek, brojrecepta)  # update recept

                        elif operacija == '4':
                            tabela = 'recepti'
                            baza = 'apoteke.db'
                            print("ISPIS[4]")
                            print("TABELA RECEPATA: ")
                            print("Br.recepta - Izdavac recepta - Pacijent - Lijek - Datum - Nacin upotrebe")
                            select.show_all(baza, tabela)  # select recept

                        elif operacija != '0':
                            print("Nepoznata komanda! ")
                    print("IZLAZ IZ TABELE PODATAKA RECEPATA!")
                else:
                    print("IZABERITE PRISTUP: ")

        elif ulaz == '2':
            print("Prijavljeni ste kao KNJIGOVODJA")
            print("Imate pristup tabelama podataka ZAPOSLENI [1] i APOTEKE [2]. IZLAZ [0]: ")
            pristup = ''

            while pristup != '0':
                pristup = input("Unesite komandu za pristup tabeli ZAPOSLENI [1] i APOTEKE [2]. IZLAZ [0]: ")
                if pristup == '1':
                    print("---TABELA PODATAKA ZAPOSLENI---")
                    operacija = ''
                    while operacija != '0':
                        operacija = input("DODAVANJE [1], BRISANJE[2], IZMJENA[3], ISPIS[4], IZLAZ[0]: ")
                        if operacija == '1':
                            print("DODAVANJE [1]")
                            sql_create_zaposleni_table = """ CREATE TABLE IF NOT EXISTS zaposleni(
                                                                                        id INTEGER PRIMARY KEY, 
                                                                                        ime VARCHAR(20), 
                                                                                        prezime VARCHAR(30), 
                                                                                        zvanje VARCHAR(30), 
                                                                                        email VARCHAR(50), 
                                                                                        plata FLOAT
                                                                                        ); """
                            conn = create_connection("apoteke.db")  # create connection to apoteke.db

                            if conn is not None:
                                create_table(conn, sql_create_zaposleni_table)  # create table zaposleni
                                zaposleni1 = zaposleni.Zaposleni()  # create zaposleni
                                # create a new record zaposleni1 in table
                                b = zaposleni.create_zaposleni(conn, zaposleni1)
                                conn.close()
                            else:
                                print("Error!")

                        elif operacija == '2':
                            print("BRISANJE [2]")
                            n = int(input("Unesite ID zaoislenog kojeg zelite obrisati:"))
                            zaposleni.delete_zaposleni(n)  # delete zaposleni

                        elif operacija == '3':
                            print("IZMJENA [3]")
                            staraplata = float(input("Stara plata: "))
                            novaplata = float(input("Nova plata: "))
                            zaposleni.update_plata(novaplata, staraplata)  # update zaposleni

                        elif operacija == '4':
                            tabela = 'zaposleni'
                            baza = 'apoteke.db'
                            print("ISPIS[4]")
                            print("TABELA ZAPOSLENI: ")
                            print("ID - Ime - Prezime - Zvanje - Email - Plata")
                            select.show_all(baza, tabela)  # select zaposleni

                        elif operacija != '0':
                            print("Nepoznata komanda! ")
                    print("IZLAZ IZ TABELE PODATAKA ZAPOSLENI")

                elif pristup == '2':
                    print("---TABELA PODATAKA APOTEKE---")
                    operacija = ''
                    while operacija != '0':
                        operacija = input("DODAVANJE [1], BRISANJE[2], IZMJENA[3], ISPIS[4], IZLAZ[0]: ")
                        if operacija == '1':
                            print("DODAVANJE [1]")
                            sql_create_apoteke_table = """ CREATE TABLE IF NOT EXISTS apoteke(
                                                                                                naziv VARCHAR(50), 
                                                                                                adresa VARCHAR(50), 
                                                                                                brojzaposlenih INTEGER, 
                                                                                                zarada FLOAT
                                                                                                ); """
                            conn = create_connection("apoteke.db")  # create connection to apoteke.db
                            if conn is not None:
                                create_table(conn, sql_create_apoteke_table)  # create table apoteke
                                apoteke1 = apoteka.Apoteka()
                                b = apoteka.create_apoteka(conn, apoteke1)  # create a new record apoteke1 in table
                                conn.close()
                            else:
                                print("Error!")

                        elif operacija == '2':
                            print("BRISANJE [2]")
                            n = input("Unesite naziv apoteke koju zelite obrisati iz baze: ")
                            apoteka.delete_apoteka(n)  # delete apoteke

                        elif operacija == '3':
                            print("IZMJENA [3]")
                            print("Izmjena zarade apoteke: ")
                            starazarada = float(input("Stara zarada: "))
                            novazarada = float(input("Nova zarada: "))
                            apoteka.update_zarada(novazarada, starazarada)  # update apoteke plata

                        elif operacija == '4':
                            tabela = 'apoteke'
                            baza = 'apoteke.db'
                            print("ISPIS[4]")
                            print("TABELA APOTEKA: ")
                            print("Naziv - Adresa - Broj zaposlenih - Mjesecna zarada")
                            select.show_all(baza, tabela)  # select apoteke

                        elif operacija != '0':
                            print("Nepoznata komanda! ")
                    print("IZLAZ IZ TABELE PODATAKA APOTEKE")

        elif ulaz != '0':
            print("NEPOZNATA KOMANDA!")
    print("KRAJ!")
    print("================================================================")
