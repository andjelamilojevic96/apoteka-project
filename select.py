import sqlite3


def show_all(baza, tabela):
    conn = sqlite3.connect(baza)
    cursor = conn.cursor()

    sqlcommand = "SELECT * FROM "
    cursor.execute(sqlcommand + tabela)

    item = cursor.fetchall()

    for i in item:
        print(i)

    conn.commit()
    conn.close()
