# Prva laboratorijska vjezba iz Uvoda u racunarstvo

from cgi import print_form
from multiprocessing.sharedctypes import Value
from posixpath import split
import string
import sys

konacni_ispis = []
ulazni_podaci = []

#i=0

for linija in sys.stdin:
    ulazni_podaci.append(linija.rstrip())
    #if i == 127:
     #   break
    
    #i = i + 1

#print("")    
#print("Sada krece ispis.")
#print("")

#dodjeljujem odgovarajuce varijable ulaznim podacima
ulazni_nizovi = ulazni_podaci[0].split('|')
stanja = ulazni_podaci[1]
pocetno_stanje = ulazni_podaci[4]
prijelazi = ulazni_podaci[5:]

#stvaram dict za manipuliranje prijelazima
transformacije = {}

#razdvajam stanja u prijelazima
for sadrzaj in prijelazi:
    sadrzaj = sadrzaj.split('->')
    sadrzaj_lijevo = sadrzaj[0].split(',')
    sadrzaj_desno = sadrzaj[1].split(',')

    if '#' in sadrzaj_lijevo or '#' in sadrzaj_desno:
        continue
    else:
        transformacije[sadrzaj[0]] = sadrzaj[1]

ulazni_niz = []
i = 0
for i in range(len(ulazni_nizovi)):
    ulazni_niz.append(ulazni_nizovi[i].split(','))

#print("Ulazni nizovi su:")
#print(ulazni_niz)
#print(" ")
#print("Mogući prijelazi su:")
#print(transformacije)

trenutno_stanje = [pocetno_stanje]
novo_stanje = []
konacna_lista = ''

i = 0

#provjeravam za svaki pojedini ulazni niz
for niz in ulazni_niz:
    i = i + 1
    #print("")
    #print("###", i, "-ti niz ###")
    #print("")

    trenutno_stanje.clear()
    trenutno_stanje = [pocetno_stanje]
    novo_stanje.clear()

    #provjeravam za svaki simbol u svakom pojedinom ulaznom nizu
    #print("Pocetno stanje je", trenutno_stanje)
    for simbol in niz:
        #print("")
        #print("*** Imamo novi simbol", simbol, "***")
        #print("")

        #gledamo postoji li epsilon prijelaza prije nego odradimo prijelaz za pojedine znakove
        for posebna_stanja in trenutno_stanje:
            #print("=> (1€ for) Trenutno stanje je :", trenutno_stanje)
            key = posebna_stanja + ',' + '$'
            if key in transformacije:
                stanja = transformacije.get(key)
                odvojena_stanja = stanja.split(',')
                pomocna = []
                for stanje in odvojena_stanja:
                    if stanje not in pomocna and stanje not in novo_stanje and stanje not in trenutno_stanje:
                        pomocna.append(stanje)
                trenutno_stanje.extend(pomocna)
            #print("=> Novo stanje je :", novo_stanje)        
        trenutno_stanje.extend(novo_stanje)
        novo_stanje.clear()
        trenutno_stanje.sort()
        konacna_lista = ((','.join(map(str, trenutno_stanje)).strip()))
        if konacna_lista != '':
            konacni_ispis.append(konacna_lista)
        else:
            konacni_ispis.append('#')

        #gledamo prijelaze za pojedine znakove
        for posebna_stanja in trenutno_stanje:
            #print("=> (for) Trenutno stanje je :", trenutno_stanje)
            key = posebna_stanja + ',' + simbol
            if key in transformacije:
                stanja = transformacije.get(key)
                odvojena_stanja = stanja.split(',') # ukoliko ima više od jednog novog stanja
                pomocna = []
                for stanje in odvojena_stanja:
                    if stanje not in pomocna and stanje not in novo_stanje:
                        pomocna.append(stanje)
                novo_stanje.extend(pomocna)
            #print("=> Novo stanje je :", novo_stanje)
        trenutno_stanje.clear()
        trenutno_stanje.extend(novo_stanje)
        novo_stanje.clear()

    #print("")
    #print("")
    #gledamo epsilon prijelaze na kraju
    for posebna_stanja in trenutno_stanje:
        #print("=> (2€ for) Trenutno stanje je :", trenutno_stanje)
        key = posebna_stanja + ',' + '$'
        if key in transformacije:
            stanja = transformacije.get(key)
            odvojena_stanja = stanja.split(',')
            pomocna = []
            for stanje in odvojena_stanja:
                if stanje not in pomocna and stanje not in novo_stanje and stanje not in trenutno_stanje:
                    pomocna.append(stanje)
            #novo_stanje.clear()
            trenutno_stanje.extend(pomocna)
        #print("=> Novo stanje je :", novo_stanje)
    #trenutno_stanje.extend(novo_stanje)
    trenutno_stanje.sort()
    konacna_lista = ((','.join(map(str, trenutno_stanje)).strip()))
    if konacna_lista != '':
        konacni_ispis.append(konacna_lista)
    else:
        konacni_ispis.append('#')

    lista = '|'.join(map(str, konacni_ispis))
    print(lista)
    konacni_ispis.clear()
    del(konacna_lista)
    del(lista)