# Druga laboratorijska vjezba iz predmeta Uvod u računarstvo

import sys
import numpy as np

# Funkcija za dobivanje novoga stanja
def novo_stanje_funkcija(stanje, simbol):
    key = stanje + ',' + simbol
    if key in transformacije:
        novo_stanje = transformacije.get(key)
        return novo_stanje

# Unosenje podataka
ulazni_podaci = []
i=0
for linija in sys.stdin:
    ulazni_podaci.append(linija.rstrip())
    if i == 36:
        break
    i = i + 1

# Razvrstavanje podataka
stanja = ulazni_podaci[0]
simboli = ulazni_podaci[1]
prihvatljiva_stanja = ulazni_podaci[2]
pocetno_stanje = ulazni_podaci[3]
prijelazi = ulazni_podaci[4:]

# Razdvajanje prijelaza 
transformacije = dict()
for sadrzaj in prijelazi:
    sadrzaj = sadrzaj.split('->')
    transformacije[sadrzaj[0]] = sadrzaj[1]
    sadrzaj[0] = sadrzaj[0].split(',')

# Razdvajanje prihvatljivih stanja u listu
prihvatljiva_stanja = prihvatljiva_stanja.split(',')
#print(prihvatljiva_stanja)

# Dohvacanje broja stanja
stanja = stanja.split(',')
broj_stanja = len(stanja)
#print("Broj stanja je", broj_stanja)

# Dohvacanje broja simbola
simboli = simboli.split(',')
broj_simbola = len(simboli)
#print("Broj simbola je", broj_simbola)

# Stvaranje matrice za Algoritam 3
# Gleda se samo donja kvadratna matrica koja je presetana na false
matrica = np.ones((broj_stanja, broj_stanja), dtype=bool)

for i in range(broj_stanja):
    for j in range(broj_stanja):
        # Gledamo odnose (ne)prihvatljivih stanja
        if (stanja[i] in prihvatljiva_stanja and stanja[j] not in prihvatljiva_stanja or
            stanja[i] not in prihvatljiva_stanja and stanja[j] in prihvatljiva_stanja):
            matrica[i][j] = matrica[j][i] = False

for i in range(broj_stanja):
    for j in range(broj_simbola):
        novo_stanje1 = novo_stanje_funkcija(stanja[i], simboli[j])
        for k in range(broj_stanja):
            if k <= i:
                continue
            novo_stanje2 = novo_stanje_funkcija(stanja[k], simboli[j])

            # Gledamo odnose (ne)prihvatljivih novih stanja
            if (novo_stanje1 in prihvatljiva_stanja and novo_stanje2 not in prihvatljiva_stanja or
                novo_stanje1 not in prihvatljiva_stanja and novo_stanje2 in prihvatljiva_stanja):
                matrica[i][k] = matrica [k][i] = False

for i in range(broj_stanja):
    for j in range(broj_simbola):
        novo_stanje1 = novo_stanje_funkcija(stanja[i], simboli[j])

        # Nadi indeks novo_stanje1
        for l in range(broj_stanja):
            if novo_stanje1 == stanja[l]:
                novo_stanje1_indeks = l

        for k in range(broj_stanja):
            if k <= i:
                continue
            novo_stanje2 = novo_stanje_funkcija(stanja[k], simboli[j])

            # Nadi indeks novo_stanje2
            for l in range(broj_stanja):
                if novo_stanje2 == stanja[l]:
                    novo_stanje2_indeks = l

            # Gledamo u kakvome su odnosu napredovanja
            if matrica[i][k] == True or matrica[k][i] == True:
                if matrica[novo_stanje1_indeks][novo_stanje2_indeks] == False or matrica[novo_stanje2_indeks][novo_stanje1_indeks] == False:
                    matrica[i][k] = matrica[k][i] = False
                else:
                    matrica[i][k] = matrica[k][i] = True

# Konacni ispis
nove_transformacije = dict()
nova_stanja_boolean = [True for i in range(broj_stanja)]
for i in range(broj_stanja):
    for j in range(broj_stanja):
        if i > j:
            if matrica[i][j] == True:
                # Oznacavamo stanja za eliminaciju po istovjetnosti
                if nova_stanja_boolean[j] == True:
                    nova_stanja_boolean[i] = False
                    nove_transformacije[stanja[i]] = stanja[j]
                    # Mijenjamo pocetno stanje ukoliko je istovjetno s drugim stanjem
                    if stanja[i] == pocetno_stanje:
                        pocetno_stanje = stanja[j]

# Gledamo moze li prijeci u odredeno stanje
dozvoljeno_stanje = dict()
for i in range(broj_stanja):
    dozvoljeno_stanje[stanja[i]] = False
dozvoljeno_stanje[pocetno_stanje] = True

# Gledamo mozemo li doci do nekog stanja
for stanje in stanja:
    if stanje == pocetno_stanje or dozvoljeno_stanje[stanje] == True:
        for simbol in simboli:
            novo_stanje = novo_stanje_funkcija(stanje, simbol)
            if novo_stanje != stanja:
                dozvoljeno_stanje[novo_stanje] = True

for stanje in stanja:
    if dozvoljeno_stanje[stanje] == True:
        for simbol in simboli:
            novo_stanje = novo_stanje_funkcija(stanje, simbol)
            if novo_stanje != stanja:
                dozvoljeno_stanje[novo_stanje] = True

# Ispis stanja
nova_stanja = []
for i in range(broj_stanja):
    if nova_stanja_boolean[i] == True and dozvoljeno_stanje[stanja[i]] == True:
        nova_stanja.append(stanja[i])

print(",".join(map(str, nova_stanja)))

# Ispis simbola
print(",".join(map(str, simboli)))

# Ispis prihvatljivih stanja
nova_prihvatljiva_stanja = []
for stanje in nova_stanja:
    if stanje in prihvatljiva_stanja:
        nova_prihvatljiva_stanja.append(stanje)

print(",".join(map(str, nova_prihvatljiva_stanja)))

# Ispis pocetnog stanja
print(pocetno_stanje)

# Ispis prijelazi
for stanje in nova_stanja:
    for simbol in simboli:
        novo_stanje = novo_stanje_funkcija(stanje, simbol)
        if novo_stanje not in nova_stanja:
            novo_stanje = nove_transformacije.get(novo_stanje)
                            
        print(stanje + ',' + simbol + '->' + novo_stanje)
