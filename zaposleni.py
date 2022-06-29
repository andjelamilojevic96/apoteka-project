import sqlite3


class Zaposleni:
    def __init__(self):
        self.id = input("ID zaposlenog: ")
        i = input("Ime: ")
        ime = i.title()
        self.ime = ime
        p = input("Prezime: ")
        prezime = p.title()
        self.prezime = prezime
        n = int(input("Unesite zvanje zaposlenog: [1] - Magistar \t [2] - Farmaceutski tehnicar "))
        if n == 1:
            self.zvanje = 'Magistar'
        elif n == 2:
            self.zvanje = 'Farmaceutski tehnicar'
        else:
            self.zvanje = ' '
        email = input("Email (ime.prezime): ")
        self.email = email + '@gmai.com'
        self.plata = float(input("Plata: "))

    def __str__(self):
        return "ID zaposlenog: " + str(self.id) + "\n" + \
               "Ime: " + self.ime + "\n" + \
               "Prezime: " + self.prezime + "\n" + \
               "Zvanje: " + self.zvanje + "\n" + \
               "Email: " + self.email + "\n" +\
               "Plata: " + str(self.plata) + "\n"


def create_zaposleni(conn, zaposleni):
    sql_command = ''' INSERT INTO zaposleni(id, ime, prezime, zvanje, email, plata)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()

    params = (zaposleni.id, zaposleni.ime, zaposleni.prezime, zaposleni.zvanje, zaposleni.email, zaposleni.plata)

    cur.execute(sql_command, params)
    conn.commit()

    return cur.lastrowid


def delete_zaposleni(idzaposlenog):
    conn = sqlite3.connect('zaposleni.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM zaposleni WHERE id = (?)", (idzaposlenog,))

    conn.commit()
    conn.close()


def update_plata(novaplata, staraplata):
    conn = sqlite3.connect('zaposleni.db')

    cursor = conn.cursor()
    cursor.execute("UPDATE zaposleni SET plata = (?) WHERE plata = (?)", (novaplata, staraplata))

    conn.commit()
    conn.close()
