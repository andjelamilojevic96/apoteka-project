import sqlite3


class Apoteka:
    def __init__(self):
        naziv = input("Naziv apoteke: ")
        n = naziv.title()
        self.naziv = n
        a = input("Adresa: ")
        adresa = a.title()
        self.adresa = adresa
        self.brojzaposlenih = int(input("Broj zaposlenih: "))
        self.zarada = float(input("Mjesecna zarada: "))

    def __str__(self):
        return "Naziv apoteke: " + self.naziv + "\n" + \
               "Adresa: " + self.adresa + "\n" + \
               "Broj zaposlenih: " + str(self.brojzaposlenih) + "\n" + \
               "Zarada: " + str(self.zarada) + "\n"


def create_apoteka(conn, apoteka):
    sql_command = """ INSERT INTO apoteke(naziv, adresa, brojzaposlenih, zarada)
              VALUES(?,?,?,?) """
    cur = conn.cursor()

    params = (apoteka.naziv, apoteka.adresa, apoteka.brojzaposlenih, apoteka.zarada)

    cur.execute(sql_command, params)
    conn.commit()

    return cur.lastrowid


def delete_apoteka(nazivapoteke):
    conn = sqlite3.connect('apoteke.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM apoteke WHERE naziv = (?)", (nazivapoteke,))

    conn.commit()
    conn.close()


def update_zarada(novazarada, starazarada):
    conn = sqlite3.connect('apoteke.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE apoteke SET zarada = (?) WHERE zarada = (?)", (novazarada, starazarada))

    conn.commit()
    conn.close()
