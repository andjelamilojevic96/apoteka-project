from datetime import date


def datum():

    godina = int(input("Godina: "))
    mjesec = int(input("Mjesec: "))
    dan = int(input("Dan: "))
    datum1 = date(godina, mjesec, dan)

    return date.isoformat(datum1)
