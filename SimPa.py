# Treća laboratorijska vjezba iz predmeta Uvod u računarstvo

import sys

# Unosenje podataka
ulazni_podaci = []
#i=0
for linija in sys.stdin:
    ulazni_podaci.append(linija.rstrip())
    #if i == 11:
    #    break
    #i = i + 1

# Razvrstavanje podataka
ulazni_nizovi = ulazni_podaci[0]
stanja = ulazni_podaci[1]
ulazni_znakovi = ulazni_podaci[2]
znakovi_stoga = ulazni_podaci[3]
prihvatljiva_stanja = ulazni_podaci[4]
pocetno_stanje = ulazni_podaci[5]
pocetni_znak_stoga = ulazni_podaci[6]
prijelazi = ulazni_podaci[7:]

# Razdvajanje nizova
ulazni_nizovi = ulazni_nizovi.split('|')

# Razdvajanje stanja
stanja = stanja.split(",")

# Razdvajanje ulaznih znakova 
ulazni_znakovi = ulazni_znakovi.split(",")

# Razdvajanje znakova stoga
znakovi_stoga = znakovi_stoga.split(",")

# Razdvajanje prihvatljivih stanja
prihvatljiva_stanja = prihvatljiva_stanja.split(",")

# Provjera funkcija prijelaza
funckije_prijelaza = dict()
for prijelaz in prijelazi:
    prijelaz = prijelaz.split('->')
    funckije_prijelaza[prijelaz[0]] = prijelaz[1]

# Potisni automat
for niz in ulazni_nizovi:
    za_ispis = []
    za_ispis.append((str)(pocetno_stanje + '#' + pocetni_znak_stoga))

    niz = niz.split(',')

    trenutno_stanje = pocetno_stanje

    stog = []
    stog.append(pocetni_znak_stoga)
    
    indeksiranje = 0
    for znak in niz:
        anomalija = 0
        
        if len(stog) > 0:
            uzorak = trenutno_stanje + ',' + znak + ',' + stog[len(stog)-1]
        elif len(stog) == 0:
            uzorak = trenutno_stanje + ',' + znak + ',' + '$'

        if uzorak not in funckije_prijelaza: 
            if len(stog) == 0:
                stog.append('$')
            uzorak = trenutno_stanje + ',' + '$' + ',' + stog[len(stog)-1]
            anomalija = 1

        if uzorak in funckije_prijelaza:
            if anomalija == 1:
                niz.insert(indeksiranje + 1, znak)

            stog.pop(len(stog)-1)
            desna_strana = funckije_prijelaza[uzorak]
            desna_strana = desna_strana.split(',')

            if desna_strana[1] != '$':
                za_stog = (list)(desna_strana[1])
                stog.append(desna_strana[1])

            trenutno_stanje = desna_strana[0]

            if len(stog) == 0:
                stog.reverse()
                stog = "".join(map(str, stog))
                oblik_za_appendanje = (str)(trenutno_stanje + '#' + '$')
            elif len(stog) > 0:
                stog.reverse()
                stog = "".join(map(str, stog))
                oblik_za_appendanje = (str)(trenutno_stanje + '#' + stog)

            za_ispis.append(oblik_za_appendanje)
            stog = (list)(stog)
            stog.reverse()
            
        elif uzorak not in funckije_prijelaza:
            za_ispis.append('fail')
            break
        
        
        if len(stog) > 0:
            epsilon_uzorak = trenutno_stanje + ',' + '$' + ',' + stog[len(stog)-1]
        elif len(stog) == 0:
            epsilon_uzorak = trenutno_stanje + ',' + '$' + ',' + '$'

        if trenutno_stanje in prihvatljiva_stanja and indeksiranje == len(niz)-1:
            break

        if epsilon_uzorak in funckije_prijelaza:

            stog.pop(len(stog)-1)
            desna_strana = funckije_prijelaza[epsilon_uzorak]
            desna_strana = desna_strana.split(',')

            if desna_strana[1] != '$':
                za_stog = (list)(desna_strana[1])
                stog.append(desna_strana[1])

            trenutno_stanje = desna_strana[0]

            if len(stog) == 0:
                stog.reverse()
                stog = "".join(map(str, stog))
                oblik_za_appendanje = (str)(trenutno_stanje + '#' + '$')
            elif len(stog) > 0:
                stog.reverse()
                stog = "".join(map(str, stog))
                oblik_za_appendanje = (str)(trenutno_stanje + '#' + stog)
            za_ispis.append(oblik_za_appendanje)
            stog = (list)(stog)
            stog.reverse()

        if len(stog) > 0:
            epsilon_uzorak = trenutno_stanje + ',' + '$' + ',' + stog[len(stog)-1]
        elif len(stog) == 0:
            epsilon_uzorak = trenutno_stanje + ',' + '$' + ',' + '$'

        if trenutno_stanje in prihvatljiva_stanja and indeksiranje == len(niz)-1:
            break

        if epsilon_uzorak in funckije_prijelaza:

            stog.pop(len(stog)-1)
            desna_strana = funckije_prijelaza[epsilon_uzorak]
            desna_strana = desna_strana.split(',')

            if desna_strana[1] != '$':
                za_stog = (list)(desna_strana[1])
                stog.append(desna_strana[1])

            trenutno_stanje = desna_strana[0]

            if len(stog) == 0:
                stog.reverse()
                stog = "".join(map(str, stog))
                oblik_za_appendanje = (str)(trenutno_stanje + '#' + '$')
            elif len(stog) > 0:
                stog.reverse()
                stog = "".join(map(str, stog))
                oblik_za_appendanje = (str)(trenutno_stanje + '#' + stog)
            za_ispis.append(oblik_za_appendanje)
            stog = (list)(stog)
            stog.reverse()

        indeksiranje = indeksiranje + 1

    if trenutno_stanje in prihvatljiva_stanja and 'fail' not in za_ispis:
        za_ispis.append('1')
    else:
        za_ispis.append('0')
    
    za_ispis = "|".join(map(str, za_ispis))
    print(za_ispis)
    za_ispis = (list)(za_ispis)
    za_ispis.clear()
