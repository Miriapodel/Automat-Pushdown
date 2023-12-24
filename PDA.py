# ± nu se poate afla in sigma, sau in oricare alte multime. Este folosit pentru verificare intr-o functie
# Pentru a semnala ca o stare este initiala, in fisierul de configurare va fi trecuta in stilul q0, s
# In actions, tranzitiile sunt de genul: stare_inceput, input, element_scos_de_pe_stiva, element_pus_pe_stiva, stare_viitoare


def citire_fisier(nume_fisier):
    # Adaug toate datele din fisier intr-o variabila

    fisier = []

    try: # verific daca se poate citi din fisier
        with open(nume_fisier) as f:
            for linie in f:
                fisier.append(linie)

        return fisier

    # Tratez cazul in care fisierul nu exista si trimit o eroare

    except:
        print("Fisierul nu exista")
        return None


def citire_secventa(): #citesc secventa de input pe care o primesc
    with open("secventa.in") as f:
        return f.readline()


def file_parser(fisier):
    structura_fisier = {}  # Memorez structura fisierului intr un dictionar
    sectiune_curenta = ''

    for linie in fisier:
        if linie[0] == '[' and linie[-2] == ']':  # Verific daca linia curenta anunta inceputul unei noi sectiuni

            # Populez dictionarul in stilul structurii fisierului. Fiecare sectiune este o cheie ale carei valori sunt
            # datele care se afla in sectunea respectiva

            nume_sectiune = linie.rstrip('\n').strip(']').lstrip('[')
            sectiune_curenta = nume_sectiune
            if nume_sectiune not in structura_fisier:  # Sectiunea curenta este folosita ca o cheie
                if nume_sectiune == 'Actions':
                    structura_fisier[
                        nume_sectiune] = {}  # Daca sectiunea curenta este 'Actions' elementele care urmeaza sa fie citite vor si stocate tot intr un dictionar
                else:
                    structura_fisier[
                        nume_sectiune] = []  # Daca sectiunea curenta nu este 'Actions' elementele care urmeaza sa fie citite vor fi stocate intr o lista
        else:
            if linie[0] != '#' and sectiune_curenta != '':  # Verific daca linia curenta este un comentariu, iar in caz afirmativ o ignor
                data = linie.rstrip('\n')

                if sectiune_curenta == 'Actions':
                    data = data.split(", ")  # Impart linia curenta in parti componente

                    if len(data) < 5:
                        print("Datele din Actions nu sunt complete")
                        return False

                    if data[0] not in structura_fisier[sectiune_curenta]:
                        structura_fisier[sectiune_curenta][data[0]] = {}  # Daca elementul nu a fost adaugat deja in actions, il adaucam ca cheie si creem un dictonar pentru valorile lui

                    if data[1] not in structura_fisier[sectiune_curenta][data[0]]:
                        structura_fisier[sectiune_curenta][data[0]][data[1]] = {}

                    if data[2] not in structura_fisier[sectiune_curenta][data[0]][data[1]]:
                        structura_fisier[sectiune_curenta][data[0]][data[1]][data[2]] = {}

                    if data[3] not in structura_fisier[sectiune_curenta][data[0]][data[1]][data[2]]:
                        structura_fisier[sectiune_curenta][data[0]][data[1]][data[2]][data[3]] = [] # in cazul in care putem merge dintr-o stare in mai multe in acelasi fel
                        structura_fisier[sectiune_curenta][data[0]][data[1]][data[2]][data[3]].append(data[4])
                    else:
                        structura_fisier[sectiune_curenta][data[0]][data[1]][data[2]][data[3]].append(data[4])

                else:
                    structura_fisier[sectiune_curenta].append(data)

    return structura_fisier


# TODO: Cazul in care citind aceleasi simboluri putem merge in doua stari diferite

def verificare_corectitudine_sigma(structura):
    if 'Sigma' not in structura: # Verific daca a fost citita o sectiune Sigma
        print("Nu exista alfabetul")
        return False

    elif len(structura['Sigma']) == 0:  # Verific daca sectiunea este goala
        print("Sectiunea Sigma este goala")
        return False

    else:

        if sorted(structura['Sigma']) != sorted(
                list(set(structura['Sigma']))):  # Verific unicitatea elementelor din limbaj
            print("Alfabetul nu are elemente unice")
            return False

    return True


def verificare_corectitudine_States(structura):
    if 'States' not in structura: # Verific daca a fost citita o sectiune States
        print("Nu exista States")
        return False

    elif len(structura['States']) == 0:  # Verific daca sectiunea States este sau nu goala
        print("Sectiunea States este goala")
        return False

    else:

        # Verific daca exista o stare initiala si cel putin o stare finala

        exista_stare_finala = False
        exista_stare_initiala = False

        for element in structura['States']:
            componente = element.split(
                ", ")  # Impart elementul pe componente pentru a putea fi verificate regulile mai usor
            numar_componente = len(componente)
            if numar_componente == 2:
                if componente[1] == 's':  # Verific daca am gasit o stare initiala
                    if exista_stare_initiala is True:  # Verific daca a mai fost gasita o stare initiala inainte
                        print("Exista mai multe stari initiale")  # In caz afirmativ afisez o eroare ( poate exista o singura stare initiala )
                        return False
                    else:
                        exista_stare_initiala = True
                else:
                    if componente[1] == 'f':  # Verific daca exista o stare finala
                        exista_stare_finala = True
            elif numar_componente == 3:  # Verific daca e posibil ca starea curenta sa fie initiala sau finala
                if componente[1] == 's':
                    if exista_stare_initiala is True:
                        print("Exista mai multe stari initiale")
                        return False
                    else:
                        exista_stare_initiala = True
                if componente[1] == 'f':
                    exista_stare_finala = True

    return True


def verificare_corectitudine_Actions(structura):
    if 'Actions' not in structura:  # Verific daca exista Actions ca sectiune in fisierul de configuratie
        print("Nu exista sectiunea Actions")
        return False

    elif len(structura['Actions']) == 0:  # Verific daca functia de tranzitie e goala sau nu
        print("Sectiunea Actions este goala")
        return False

    # Verific daca datele din actions sunt corecte, mai exact daca cele trei elemente trimise pe cate o linie apartin sectiunii
    # States ( primul element si al treilea ) si sectiunii Sigma ( elementul din mijloc )

    states = [x[0:2] for x in
              structura['States']]  # Salvez doar starile intr-o variabila separata pentru a fi mai usor de accesat

    for action in structura['Actions']:
        if action not in states:  # Verific daca starea apartine multimii de stari
            print("Datele din Actions nu sunt corecte")
            return False
        for element in structura['Actions'][action]:  # Verific daca inputul primit apartine multimii Sigma
            if element not in structura['Sigma']:
                print("Datele din Actions nu sunt corecte")
                return False
            for element2 in structura['Actions'][action][
                element]:  # Verific daca elementul care se scoate de pe stiva apartine multimii Gama
                if element2 not in structura['Gama']:
                    print("Datele din Actions nu sunt corecte")
                    return False
                for element3 in structura['Actions'][action][element][
                    element2]:  # Verific daca elementul care se adauga pe stiva apartine multimii Gama
                    if element3 not in structura['Gama']:
                        print("Datele din Actions nu sunt corecte")
                        return False

                    for element4 in structura['Actions'][action][element][element2][element3]:
                        if element4 not in states:
                            print("Datele din Actions nu sunt corecte")
                            return False

    return True
    # Verific daca functia pentru tranzitii contine elemente corecte


def verificare_corectitudine_Gama(structura):
    if 'Gama' not in structura: # Verific daca a fost citita o sectiune Gama
        print("Nu exista sectiunea Gama")
        return False

    if len(structura['Gama']) == 0: # Verific daca exista macar un element in Gama
        print("Nu exista elemente in Gama")
        return False

    if sorted(structura['Gama']) != sorted(
            list(set(structura['Gama']))):  # Verific unicitatea elementelor din limbaj
        print("Gama nu are elemente unice")
        return False

    return True


def verificare_corectitudine_fisier(structura):

    # Verific daca fiecare sectiune este corecta

    corect_Sigma = verificare_corectitudine_sigma(structura)

    if corect_Sigma is False:
        return False

    corect_States = verificare_corectitudine_States(structura)

    if corect_States is False:
        return False

    corect_Actions = verificare_corectitudine_Actions(structura)

    if corect_Actions is False:
        return False

    corect_Gama = verificare_corectitudine_Gama(structura)

    if corect_Gama is False:
        return False

    return True


def determinare_stari_initiala_finala(dfa):
    stare_initiala = 0
    stari_finale = []

    for stare in dfa['States']:
        componente = stare.split(", ")  # Impart string ul pe componente pentru a fi mai usor de verificat conditiile
        numar_componente = len(componente)

        if numar_componente > 1:  # Verific se dau mai multe informatii despre starea curenta ( daca e si stare initiala sau finala )
            if componente[1] == 's':
                stare_initiala = componente[0]
                if numar_componente == 3:  # Verific daca starea curenta poate fi si initiala si finala
                    if componente[2] == 'f':
                        stari_finale.append(componente[0])
            elif componente[1] == 'f':
                stari_finale.append(componente[0])

    return stare_initiala, stari_finale


def next_state(c, dfa):
    for stare in stari_curente: # Merg in starile curente pentru a vedea ce stari voi avea la pasul urmator

        if 'e' in dfa['Actions'][stare]:  # Verific daca din starea curenta se poate pleca automat in alta

            varf_stiva = stiva[-1]  # Elementul care ar trebui scos din stiva

            if varf_stiva in dfa['Actions'][stare]['e']:  # Verific daca exista o tranzitie in care este scos elementul care se afla in varful stivei

                de_pus_pe_stiva = list(dfa['Actions'][stare]['e'][varf_stiva].keys())[0][0:]  # Elementul care trebuie adaugat in stiva

                for element in dfa['Actions'][stare]['e'][varf_stiva][de_pus_pe_stiva]: # Adaug fiecare stare in care se poate merge
                    stari_viitoare.append(element)

                stiva.pop() # scot

                if de_pus_pe_stiva != 'e': # Daca am citit epsilon nu pun nimic pe stiva
                    stiva.append(de_pus_pe_stiva)

            else:
                if 'e' in dfa['Actions'][stare]['e']:  # Verific daca se poate merge automat in alta stare, fara a scoate ceva de pe stiva

                    de_pus_pe_stiva = list(dfa['Actions'][stare]['e']['e'].keys())[0][0:]  # Elementul care trebuie adaugat in stiva

                    for element in dfa['Actions'][stare]['e']['e'][de_pus_pe_stiva]:
                        stari_viitoare.append(element)


                    if de_pus_pe_stiva != 'e':  # Pun elementul pe stiva doar daca este diferit de epsilon
                        stiva.append(de_pus_pe_stiva)

        if c in dfa['Actions'][stare]:  # Verific daca din starea curenta se poate pleca in alta cu simbolul pe care l-am citit

            varf_stiva = stiva[-1]  # Elementul care ar trebui scos din stiva

            # TODO: Cazul in care exista si o varianta in care mai exista o regula cu epsilon, pe langa cea in care se scoate ceva de pe stiva

            if varf_stiva in dfa['Actions'][stare][
                c]:  # Verific daca exista o tranzitie in care este scos elementul care se afla in varful stivei

                de_pus_pe_stiva = list(dfa['Actions'][stare][c][varf_stiva].keys())[0][
                                  0:]  # Elementul care trebuie adaugat in stiva

                for element in dfa['Actions'][stare][c][varf_stiva][de_pus_pe_stiva]:
                    stari_viitoare.append(element)

                stiva.pop()

                if de_pus_pe_stiva != 'e': # Pun pe stiva doar daca e diferit de epsilon
                    stiva.append(de_pus_pe_stiva)

            else:
                if 'e' in dfa['Actions'][stare][c]:  # Verific daca se poate merge automat in alta stare, fara a scoate ceva de pe stiva

                    de_pus_pe_stiva = list(dfa['Actions'][stare][c]['e'].keys())[0][0:]  # Elementul care trebuie adaugat in stiva

                    for element in dfa['Actions'][stare][c]['e'][de_pus_pe_stiva]:
                        stari_viitoare.append(element)

                    if de_pus_pe_stiva != 'e':  # Pun elementul pe stiva doar daca este diferit de epsilon
                        stiva.append(de_pus_pe_stiva)

    if len(stari_viitoare) != 0: # Sterg starile curente doar daca urmeaza un alt pas la care voi avea alte stari
        stari_curente.clear()

    stari_de_verificat = set(stari_viitoare)
    stari_viitoare.clear()

    if len(stari_de_verificat) == 0:
        global de_repetat
        de_repetat = False # ma ajuta in functia tranzitie_fara_citire sa stiu daca mai continui sa merg in alte stari pentru starile care au tranzitii doar cu epsilon

    for element in stari_de_verificat:
        stari_curente.append(element) # pun elementele care vor fi verificate la urmatorul pas in stari_curente


def tranzitie_fara_citire(dfa):
    global de_repetat

    de_repetat = True # variabila care ma ajuta sa stiu daca mai trebuie sa verific daca mai exista stari cu tranzitii doar cu epsilon

    while de_repetat is True:
        next_state('±', dfa) # pun '±' pentru a semnala ca vreau sa caut doar tranzitiile care se fac doar cu epsilon. '±' nu se poate afla in sigma


def emulate_dfa(dfa, sir_input, stare_inceput):
    stari_curente.append(stare_inceput)  # Pun starile asupra carora se va aplica input ul in aceasta variabila
    for c in sir_input:  # Iau fiecare caracter din input
        if c not in dfa['Sigma']:  # Daca caracterul pe care il citesc nu se afla in limbaj, afisez o eroare
            print("Sirul nu este recunoscut de automat")
            return False

        next_state(c, dfa) # functie care cauta starile viitoare in care se va duce PDA-ul

    tranzitie_fara_citire(dfa) # Verific la final daca ne mai putem duce in alte stari doar cu epsilon, fara sa scoatem sau sa punem ceva pe stiva

    if len(stiva) != 0 and stiva[-1] == '$': # conditia ca input-ul sa fie recunoscut -> in stiva sa mai ramana doar $
        return True

    return False


def start_app():
    nume_fisier = "config2.in"  # Citesc numele fisierului in care se afla configuratia
    date_fisier = citire_fisier(nume_fisier)  # Colectez toate informatiile din fisier in aceasta variabila

    if date_fisier is not None:
        structura_fisier = file_parser(date_fisier)  # Structurez informatiile pe sectiuni intr un dictionar

        if structura_fisier is not False:
            verificare_corectitudine_fisier(structura_fisier)  # Verific daca datele primite sunt corecte

            stare_init, stari_fin = determinare_stari_initiala_finala(structura_fisier)

            secventa = citire_secventa()  # Citesc inputul care urmeaza sa fie procesat

            print(emulate_dfa(structura_fisier, secventa, stare_init))  # Afisez daca secventa a fost sau nu acceptata de automat


stiva = ['$'] # stiva care are deja $ in ea la inceput. Nu mai este nevoie de o stare suplimentara ca sa fie pus $ in stiva
de_repetat = True
stari_curente = [] # Starile care urmeaza sa fie verificate la un pas urmator
stari_viitoare = []  # Aici voi pune starile care urmeaza sa fie procesate dupa ce sunt procesate cele curente

start_app()  # Functia care porneste automatul si citirea fisierului de configuratie

