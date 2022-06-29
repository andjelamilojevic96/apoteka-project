import datum
import sqlite3


class Recept:
    def __init__(self):
        self.brojrecepta = int(input("Broj recepta: "))
        izdavac = input("Izdavac recepta(dr/ustanova): ")
        i = izdavac.title()
        self.izdavacrecepta = i
        pacijent = input("Ime i prezime pacijenta: ")
        p = pacijent.title()
        self.pacijent = p
        print("Datum izdavanja recepta: ")
        dat = datum.datum()
        self.datum = dat
        lijek1 = input("Propisani lijek: ")
        lijek = lijek1.upper()
        self.lijek = lijek
        self.nacinupotrebe = input("Nacin upotrebe lijeka: ")

    def __str__(self):
        return "Broj recepta: " + str(self.brojrecepta) + "\n" + \
               "Izdavac: " + self.izdavacrecepta + "\n" + \
               "Pacijent: " + self.pacijent + "\n" + \
               "Propisani lijek: " + self.lijek + "\n" + \
               "Nacin upotrebe: " + self.nacinupotrebe + "\n" +\
               "Datum izdavanja lijeka: " + str(self.datum) + "\n"


def create_recept(conn, recept):
    sql_command = ''' INSERT INTO recepti(brojrecepta, izdavacrecepta, pacijent, lijek, datumizdavanja, nacinupotrebe)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    params = (recept.brojrecepta, recept.izdavacrecepta, recept.pacijent, recept.lijek, recept.datum,
              recept.nacinupotrebe)
    cur.execute(sql_command, params)
    conn.commit()
    return cur.lastrowid


def delete_recept(broj):
    conn = sqlite3.connect('recepti.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM recepti WHERE brojrecepta = (?)", (broj,))

    conn.commit()
    conn.close()


def update_recept(lijek1, broj):
    conn = sqlite3.connect('recepti.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE recepti SET lijek = (?) WHERE brojrecepta = (?)", (lijek1, broj))

    conn.commit()
    conn.close()
