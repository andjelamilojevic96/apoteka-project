from datetime import date
import sqlite3


class Lijek:
    ListaZaOtpis = []

    def __init__(self):
        self.id = input("ID lijeka: ")
        naziv = input("Naziv lijeka: ")
        n = naziv.upper()
        self.naziv = n
        self.kolicina = int(input("Kolicina u apoteci: "))
        self.cijenasapdv = float(input("Cijena sa PDV: "))
        self.cijenabezpdv = (self.cijenasapdv - self.cijenasapdv*0.17)
        print("Datum isteka roka trajanja lijeka: ")
        godina = int(input("Godina: "))
        mjesec = int(input("Mjesec: "))
        dan = int(input("Dan: "))
        datum1 = date(godina, mjesec, dan)
        self.datum = date.isoformat(datum1)
        today = date.today()
        if datum1 <= today:
            print("Lijek je pred istek roka trajanja! Lijek se dodaje u listu za otpis lijekova. \n")
            Lijek.ListaZaOtpis.append(self)

    def __str__(self):
        return "ID lijeka: " + self.id + "\n" + \
               "Naziv: " + self.naziv + "\n" + \
               "Kolicina: " + str(self.kolicina) + "\n" + \
               "Cijena sa PDV: " + str(self.cijenasapdv) + "\n" + \
               "Cijena bez pdv: " + str(self.cijenabezpdv) + "\n" +\
               "Datum isteka roka trajanja: " + self.datum + "\n"


def create_lijek(conn, lijek, tabela):
    sql_command = "INSERT INTO " + str(tabela) +\
                  "(id, naziv, kolicina, cijenasapdv, cijenabezpdv, datum) VALUES(?,?,?,?,?,?)"
    cur = conn.cursor()
    params = (lijek.id, lijek.naziv, lijek.kolicina, lijek.cijenasapdv, lijek.cijenabezpdv, lijek.datum)
    cur.execute(sql_command, params)
    conn.commit()
    return cur.lastrowid


def delete_lijek(lijek):
    conn = sqlite3.connect('lijekovi.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM lijekovi WHERE id = (?)", (lijek,))

    conn.commit()
    conn.close()


def update_cijena(cijena, naziv):
    conn = sqlite3.connect('lijekovi.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE lijekovi SET cijenasapdv = (?) WHERE naziv = (?)", (cijena, naziv))

    conn.commit()
    conn.close()


def update_cijenabezpdv(cijena, naziv):
    conn = sqlite3.connect('lijekovi.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE lijekovi SET cijenabezpdv = (?) WHERE naziv = (?)", (cijena, naziv))

    conn.commit()
    conn.close()


def create_listalijekovazaotpis(n):
    listalijekova = []
    for i in range(0, n):
        a = Lijek.ListaZaOtpis[i].id
        b = Lijek.ListaZaOtpis[i].naziv
        c = Lijek.ListaZaOtpis[i].kolicina
        d = Lijek.ListaZaOtpis[i].cijenasapdv
        e = Lijek.ListaZaOtpis[i].cijenabezpdv
        f = Lijek.ListaZaOtpis[i].datum

        listalijekova.append((a, b, c, d, e, f))
    return listalijekova
