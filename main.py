import time
import copy

ADANCIME_MAX = 6


def in_bounds(i, j):
    # True - daca pozitia i, j este in bounds, altfel False
    if i < 0 or i > 2 or j < 0 or j > 4:
        return False
    if (i == 0 or i == 2) and (j == 0 or j == 4):
        return False
    return True


def mutari_posibile(jucator, i, j):
    # functia primeste tipul de jucator si coordonatele sale
    # si returneaza o lista cu coordonatele mutarilor disponibile
    coordonate_disponibile = []
    pozitii_fara_diagonale = [[1, 1], [1, 3], [0, 2], [2, 2]]  # pozitiile care nu au muchii diagonale
    if jucator == "hare" and [i, j] in pozitii_fara_diagonale:
        directii = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    elif jucator == "hare":
        directii = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    elif jucator == "hound" and [i, j] in pozitii_fara_diagonale:
        directii = [[-1, 0], [1, 0], [0, 1]]
    else:
        directii = [[-1, 0], [-1, 1], [0, 1], [1, 0], [1, 1]]

    for directie in directii:
        p, q = directie
        if in_bounds(p + i, q + j):
            coordonate_disponibile.append([p + i, q + j])
    return coordonate_disponibile
    # OBS: nu se verifica daca pozitiile returnate se afla deja un animal


class Joc:
    """
    Clasa care defineste jocul.
    """

    NR_COLOANE = 5
    NR_LINII = 3
    JMIN = None
    JMAX = None
    GOL = "*"

    def __init__(self, tabla=None):
        if tabla is not None:
            self.matr = tabla
        else:
            self.matr = [[Joc.GOL for _ in range(Joc.NR_COLOANE)] for _ in range(Joc.NR_COLOANE)]
            self.matr[1][0] = "hound"
            self.matr[0][1] = "hound"
            self.matr[2][1] = "hound"
            self.matr[1][4] = "hare"

    @classmethod
    def jucator_opus(cls, jucator):
        if jucator == cls.JMIN:
            return cls.JMAX
        else:
            return cls.JMIN

    def find_hounds(self):
        hounds = []
        for i in range(3):
            for j in range(5):
                if self.matr[i][j] == "hound":
                    hounds.append([i, j])
        return hounds

    def find_hare(self):
        for i in range(3):
            for j in range(5):
                if self.matr[i][j] == "hare":
                    return [i, j]

    def final(self):
        # returneaza simbolul jucatorului castigator sau False daca starea nu e finala

        # o stare e finala daca iepurele nu mai are mutari disponibile pe
        # care sa nu se afle niciun caine
        # sau daca iepurele a trecut de toti cainii
        hare = self.find_hare()  # pozitia iepurelui
        hounds = self.find_hounds()  # pozitia cainilor

        # cazul in care iepurele e blocat:
        pozitii_disponibile_hare = mutari_posibile("hare", *hare)  # pozitiile posibile pe care poate merge iepurele
        stuck_hare = True  # verificam daca iepurele e blocat
        # daca iepurele are cel putin o pozitie disponibila pe care nu se afla niciun caine,
        # inseamna ca iepurele nu e blocat
        for pozitie in pozitii_disponibile_hare:
            if pozitie not in hounds:
                stuck_hare = False
                break
        if stuck_hare:
            return "hound"

        # cazul in care iepurele a trecut de caini:
        escaped = True  # presupunem ca trecut de toti cainii
        # daca gasim un caine mai la stanga in harta, atunci nu a scapat
        for hound in hounds:
            if hound[1] < hare[1]:
                escaped = False
                break
        if escaped:
            return "hare"
        return False

    def mutari_jucator(self, jucator, i, j):
        # jucator = simbolul jucatorului care muta
        # i, j = coordonatele jucatorului care muta
        pozitii_posibile_jucator = mutari_posibile(jucator, i, j)
        pozitii_ocupate = [self.find_hare()] + self.find_hounds()  # pozitiile pe care se afla deja ceva
        l_mutari = []
        for pozitie in pozitii_posibile_jucator:
            if pozitie in pozitii_ocupate:
                continue
            p, q = pozitie
            copie_matr = copy.deepcopy(self.matr)
            copie_matr[i][j] = Joc.GOL
            copie_matr[p][q] = jucator
            l_mutari.append(Joc(copie_matr))
        return l_mutari

    def mutari(self, jucator):
        hare = self.find_hare()
        hounds = self.find_hounds()
        if jucator == "hare":
            return self.mutari_jucator(jucator, *hare)
        else:
            l_mutari = []
            for hound in hounds:
                l_mutari += self.mutari_jucator(jucator, *hound)
            return l_mutari

    def noduri_reachable(self):
        # nodurile reachable din harta, din perspectiva iepurelui

        hounds = self.find_hounds()

        # facem bfs pe harta
        queue = []
        visited = set()
        start = self.find_hare()
        queue.append(start)
        visited.add((start[0], start[1]))
        while queue:
            poz = queue.pop(0)
            for pozitie in mutari_posibile("hare", *poz):
                if pozitie not in hounds and (pozitie[0], pozitie[1]) not in visited:
                    queue.append(pozitie)
                    visited.add((pozitie[0], pozitie[1]))
        return len(visited)  # numarul de pozitii reachable

    def pozitii_deschise(self, jucator):
        if jucator == "hare":
            return self.noduri_reachable()
        return 11 - self.noduri_reachable()

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        if t_final == self.__class__.JMAX:
            return 99 + adancime
        elif t_final == self.__class__.JMIN:
            return -99 - adancime
        else:
            return self.pozitii_deschise(self.__class__.JMAX)

    def __str__(self):
        sir = "  "
        for i in range(1, Joc.NR_COLOANE - 1):
            if self.matr[0][i] == "hound":
                sir += "c"
            elif self.matr[0][i] == "hare":
                sir += "i"
            else:
                sir += Joc.GOL
            if i != 3:
                sir += "-"
        sir += "\n /|\\|/|\\\n"
        for i in range(Joc.NR_COLOANE):
            if self.matr[1][i] == "hound":
                sir += "c"
            elif self.matr[1][i] == "hare":
                sir += "i"
            else:
                sir += Joc.GOL
            if i != 4:
                sir += "-"
        sir += "\n \\|/|\\|/\n  "
        for i in range(1, Joc.NR_COLOANE - 1):
            if self.matr[2][i] == "hound":
                sir += "c"
            elif self.matr[2][i] == "hare":
                sir += "i"
            else:
                sir += Joc.GOL
            if i != 3:
                sir += "-"
        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    O instanta din clasa stare este un nod din arborele minimax
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile
    posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile (tot de tip Stare) din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        # e de tip Stare (cel mai bun succesor)
        self.stare_aleasa = None

    def mutari(self):
        # lista de informatii din nodurile succesoare
        l_mutari = self.tabla_joc.mutari(self.j_curent)

        juc_opus = Joc.jucator_opus(self.j_curent)

        # mai jos calculam lista de noduri-fii (succesori)
        l_stari_mutari = [
            Stare(mutare, juc_opus, self.adancime - 1, parinte=self)
            for mutare in l_mutari
        ]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "\n(Juc curent:" + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):
    # daca sunt la o frunza in arborele minimax sau la o stare finala
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [
        min_max(x) for x in stare.mutari_posibile
    ]  # expandez(constr subarb) fiecare nod x din mutari posibile

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)

    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float("-inf")

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(
                alpha, beta, mutare
            )  # aici construim subarborele pentru stare_noua

            if estimare_curenta < stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if alpha < stare_noua.estimare:
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float("inf")
        # completati cu rationament similar pe cazul stare.j_curent==Joc.JMAX
        for mutare in stare.mutari_posibile:
            # calculeaza estimarea
            stare_noua = alpha_beta(
                alpha, beta, mutare
            )  # aici construim subarborele pentru stare_noua

            if estimare_curenta > stare_noua.estimare:
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if beta > stare_noua.estimare:
                beta = stare_noua.estimare
                if alpha >= beta:
                    break

    stare.estimare = stare.stare_aleasa.estimare

    return stare


def afis_daca_final(stare_curenta):
    # metoda final() returneaza castigatorul sau False daca nu e stare finala
    final = stare_curenta.tabla_joc.final()
    if final:
        print("A castigat " + final)
        return True
    return False


def afis_variante():
    print("  1-4-7\n /|\\|/|\\\n0-2-5-8-10\n \\|/|\\|/\n  3-6-9\n")


def main():
    # initializare algoritm
    raspuns_valid = False

    while not raspuns_valid:
        tip_algoritm = input(
            "Algoritmul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n "
        )
        if tip_algoritm in ["1", "2"]:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")
    # initializare jucatori
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("Doriti sa jucati cu hare sau cu hounds? (hare / hound)\n").lower()
        if Joc.JMIN in ["hare", "hound"]:
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie hare sau hound.")
    Joc.JMAX = "hare" if Joc.JMIN == "hound" else "hound"
    # expresie= val_true if conditie else val_false  (conditie? val_true: val_false)

    # initializare tabla
    tabla_curenta = Joc()
    # apelam constructorul
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, "hound", ADANCIME_MAX)  # conform wikipedia, hounds move first.

    # vector pozitii mapeaza indicii din figura ajutatoare la pozitiile din matrice
    vector_pozitii = [[1, 0], [0, 1], [1, 1], [2, 1], [0, 2], [1, 2], [2, 2], [0, 3], [1, 3], [2, 3], [1, 4]]
    while True:
        if stare_curenta.j_curent == Joc.JMIN:
            # muta jucatorul
            print("Acum muta utilizatorul cu ", stare_curenta.j_curent)
            print("Alege piesa pe care vrei sa o muti si noua ei pozitie")
            afis_variante()
            raspuns_valid = False
            while not raspuns_valid:
                try:
                    pozitie_piesa = int(input("Piesa (indice): "))
                    pozitie_noua = int(input("Pozitie noua (indice): "))

                    if pozitie_piesa in range(11) and pozitie_noua in range(11):
                        coord_piesa = vector_pozitii[pozitie_piesa]
                        coord_pozitie_noua = vector_pozitii[pozitie_noua]
                        if stare_curenta.tabla_joc.matr[coord_piesa[0]][coord_piesa[1]] == Joc.JMIN and \
                                stare_curenta.tabla_joc.matr[coord_pozitie_noua[0]][coord_pozitie_noua[1]] == Joc.GOL:
                            # TODO verifica daca mutarea e valida
                            raspuns_valid = True
                        else:
                            print("Mutare invalida.")
                    else:
                        print("Pozitie invalida")
                except ValueError:
                    print("Indicii trebuie sa fie numere intregi")

            # dupa iesirea din while sigur am valide cele doua pozitii
            # deci pot plasa simbolul pe "tabla de joc"
            stare_curenta.tabla_joc.matr[coord_piesa[0]][coord_piesa[1]] = Joc.GOL
            stare_curenta.tabla_joc.matr[coord_pozitie_noua[0]][coord_pozitie_noua[1]] = Joc.JMIN

            # afisarea starii jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))
            # testez daca jocul a ajuns intr-o stare finala
            # si afisez un mesaj corespunzator in caz ca da
            if afis_daca_final(stare_curenta):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            print("Acum muta calculatorul cu ", stare_curenta.j_curent)
            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))

            # stare actualizata e starea mea curenta in care am setat stare_aleasa (mutarea urmatoare)
            if tip_algoritm == "1":
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)

            # aici se face de fapt mutarea !!!
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc

            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print(
                'Calculatorul a "gandit" timp de '
                + str(t_dupa - t_inainte)
                + " milisecunde."
            )
            if afis_daca_final(stare_curenta):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)


if __name__ == "__main__":
    main()
