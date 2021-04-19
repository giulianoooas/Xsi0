import tkinter as tk

root = tk.Tk()
root.title("X si 0")
root.config(bg = "green")
pozitii = [] # ce pozitii modific
nrPlayeri = 1 #by default jocul merge player vs pc, dar poate fi si player vs player, deci nrPlayeri apartine [1,2]

class Semn:
    """
        Imi voi crea fiecare patratica a tablei pentru x si 0
    """
    def __init__(self,master,i,j,simbol):
        self.simbol = simbol
        self.b = tk.Button(master, command = self.command, text = "", width = 10,
                    height = 5, font = (40,),bg = "aqua", fg = "green")
        self.b.grid(row = i, column = j)
        self.i = i
        self.j = j

    def command(self):
        pozitii.extend([self.i,self.j])
        if len(pozitii) == 2:
            self.b.config(bg = "green") #cand apasa un buton vreau ca el sa fie verde
    
    def coloreaza(self):
        self.b.config(bg = "aqua")
        if self.simbol == 1:
            return
        self.b.config(text = self.simbol, state = tk.DISABLED)

class Joc:
    tabla = None
    rand = 0
    simboluri = ["X", "0"]
    """
        tabla de x si 0 are 3 valori posibile:
            1 - adica pot sa pun fie x fie 0
            x - e pus deja x
            0 - e pus deja 0
        rand imi va retine ce jucator e in momentul acela la joc:
            0 - playerul
            1 - mpc
    """

    @classmethod
    def alegeX(cls):
        cls.simboluri = ["X","0"]
    
    @classmethod
    def alegeO(cls):
        cls.simboluri = ["0","X"]

    @classmethod
    def creazaTabla(cls):
        # ma asigur mereu ca jocul incepe bine
        cls.tabla = [
            [1,1,1],
            [1,1,1],
            [1,1,1]
        ]
        cls.rand = 0

    def __init__(self):
        self.creazaTabla()
        self.AfisareTura = tk.Label(root,state = tk.DISABLED, borderwidth = 1, 
                    relief = "solid",justify = tk.CENTER, font = (30,), text = self.simboluri[self.rand],
                    width = 20, bg = "aqua", fg = "green")
        self.AfisareTura.pack(padx = 10,pady = 10)
        self.tablaDeJoc = tk.Frame(root)
        self.tablaDeJoc.pack()
        self.casute = [[Semn(self.tablaDeJoc,i,j,1) for j in range(3)] for i in range(3)]
        self.next = tk.Button(root,text = "next",command = self.makeMove, font = (20,),
                    bg = "aqua", fg = "green")
        self.next.pack(padx = 10,pady = 10)
        self.AfisareCastigator = None
        self.replay = tk.Button(root,text = "replay",command = self.destroy, font = (20,),
                    bg = "aqua", fg = "green")
        self.replay.pack(padx = 10,pady = 10)

    
    def genereazaMutari(self,tabla,rand = None):
        #Functie ce imi va genera toate mutarile posibile ale unui table de joc
        if rand == None or rand not in [0,1]:
            rand = self.rand
        mutari = []
        for i in range(3):
            for j in range(3):
                if tabla[i][j] == 1:
                    copie = [linie.copy() for linie in tabla]
                    copie[i][j] = self.simboluri[rand]
                    mutari.append(copie)
        return mutari
    
    def win(self,tabla):
        """
            Aici am 3 valori posibile:
                0 = Nu s-a terminat inca meciul
                1 = am castigat
                2 = remiza
        """

        if tabla[0][0] == tabla[1][1]and tabla[1][1] == tabla[2][2] and tabla[2][2] != 1: #diagonala principala
            return 1
        
        if tabla[2][0] == tabla[1][1] and tabla[1][1]== tabla[0][2] and tabla[1][1] != 1:#diagonala secundara
            return 1

        if tabla[0][0] == tabla[0][1] and tabla[0][1] == tabla[0][2] and tabla[0][0] != 1:#prima linie
            return 1

        if tabla[1][0] == tabla[1][1] and tabla[1][1] == tabla[1][2] and tabla[1][1] != 1:#a doua linie
            return 1

        if tabla[2][0] == tabla[2][1] and tabla[2][1] == tabla[2][2] and tabla[2][2] != 1:# a treia linie
            return 1

        if tabla[0][0] == tabla[1][0] and tabla[1][0] == tabla[2][0] and tabla[0][0] != 1: # prima coloana
            return 1

        if tabla[0][1] == tabla[1][1] and tabla[1][1] == tabla[2][1] and tabla[1][1] != 1: # a doua coloana
            return 1

        if tabla[0][2] == tabla[1][2] and tabla[1][2] == tabla[2][2] and tabla[2][2] != 1: #a treia coloana
            return 1

        for i in tabla:
            for j in i:
                if j == 1:
                    return 0

        return 2

    def estimare(self,tabla):
        """
            Daca ajung la o conformatie castigatoare returnez 100
            la remiza 50, altfel pentru fiecare pierdere scad cate 10
        """
        win = self.win(tabla)
        if win == 1:
            return 100
        if win == 2:
            return 50
        nr = 0
        for i in self.genereazaMutari(tabla,1-self.rand):
            if self.win(i) == 1:
                nr -= 10
        return nr

    def MinMax(self,tabla,adancime,minmax,alfa,beta):
        if adancime <= 0:
            return tabla
        succ = self.genereazaMutari(tabla)
        if len(succ) == 0:
            return tabla
        
        r = None
        if minmax:
            for i in succ:
                if r == None:
                    r = i
                    continue
                val = self.MinMax(i,adancime - 1,not minmax, alfa,beta)
                if self.estimare(val) > self.estimare(r):
                    r = i
                alfa = max(alfa,self.estimare(i))
                if alfa >= beta:
                    break
        else:
            for i in succ:
                if r == None:
                    r = i
                    continue
                val = self.MinMax(i,adancime - 1,not minmax, alfa,beta)
                if self.estimare(val) < self.estimare(r):
                    r = i
                beta = min(alfa,self.estimare(i))
                if alfa >= beta:
                    break
        return r

    def makeMove(self):
        global pozitii
        """
            Acum voi face miscarea in functie de randul persoanei
        """
        if self.rand == 0 or nrPlayeri == 2:
            try:
                i,j = pozitii[0],pozitii[1]
                self.casute[i][j].simbol = self.simboluri[self.rand]
                self.casute[i][j].coloreaza()
                self.tabla[i][j] = self.simboluri[self.rand]
                self.rand = 1 - self.rand
                self.AfisareTura.config(text = self.simboluri[self.rand])
            except:
                pass
            finally:
                pozitii = []
                if nrPlayeri == 1 and self.rand == 1: #daca urmeaza mutarea calculatorului ma voi asigura ca nu pot muta si eu
                    for i in self.casute:
                        for j in i:
                            j.b.config(state = tk.DISABLED)
        else:
            tabla = self.MinMax(self.tabla,5,True,float("-inf"),float("+inf"))
            self.tabla = [i.copy() for i in tabla]
            for i in range(3):
                for j in range(3):
                    self.casute[i][j].simbol = self.tabla[i][j]
                    self.casute[i][j].coloreaza()
                    if self.tabla[i][j] == 1: #ma asigur ca mereu voi putea sa mut si eu dupa ce muta pc-ul
                        self.casute[i][j].b.config(state = "normal")

            self.rand = 1 - self.rand
            self.AfisareTura.config(text = self.simboluri[self.rand])

        self.stop()

    def stop(self):
        rand = 1 - self.rand
        if self.win(self.tabla) == 1:
            self.next.config(state = tk.DISABLED)
            for i in self.casute:
                for j in i:
                    j.b.config(state = tk.DISABLED)
            self.AfisareCastigator = tk.Label(root,state = tk.DISABLED, borderwidth = 1, 
                    relief = "solid",justify = tk.CENTER, font = (30,), text = f"A castigat {self.simboluri[rand]}",
                    width = 20, bg = "aqua", fg = "green")
            self.AfisareCastigator.pack(pady = 10)
        elif self.win(self.tabla) == 2:
            self.next.config(state = tk.DISABLED)
            for i in self.casute:
                for j in i:
                    j.b.config(state = tk.DISABLED)
            self.AfisareCastigator = tk.Label(root,state = tk.DISABLED, borderwidth = 1, 
                    relief = "solid",justify = tk.CENTER, font = (30,), text = "Remiza",
                    width = 20, bg = "aqua", fg = "green")
            self.AfisareCastigator.pack(pady = 10)
    
    def destroy(self):
        self.AfisareTura.destroy()
        self.tablaDeJoc.destroy()
        self.next.destroy()
        self.replay.destroy()
        try:
            self.AfisareCastigator.destroy()
        except:
            pass
        main()

def main():
    global nrPlayeri
    nrPlayeri = 1
    Joc.alegeX()
    def start():
        joc = Joc() # functia ce incepe jocul
        AlegeNrPlayeri.destroy()
        AlegeSimbol.destroy()
        Start.destroy()
    
    AlegeNrPlayeri = tk.Frame(root,padx = 10, pady = 10)
    AlegeNrPlayeri.pack(padx = 10, pady = 10)

    AlegeSimbol = tk.Frame(root,padx = 10, pady = 10)
    AlegeSimbol.pack(padx = 10, pady = 10)

    Start = tk.Button(root,text = "start",command = start, font = (20,),
                    bg = "aqua", fg = "green")
    Start.pack(padx = 10,pady = 10)


    # ma voi ocupa acum de partea de alegere a playerilor
    tk.Label(AlegeNrPlayeri,state = tk.DISABLED,justify = tk.CENTER, font = (30,), text = "Alege numarul de Playeri: ",
                    width = 20).grid(row = 0, column = 1)
    
    def a1P():
        global nrPlayeri
        nrPlayeri = 1
        b1.config(state = tk.DISABLED)
        b2.config(state = "normal")
    
    def a2P():
        global nrPlayeri
        nrPlayeri = 2
        b2.config(state = tk.DISABLED)
        b1.config(state = "normal")

    b1 = tk.Button(AlegeNrPlayeri, text = "1 Player", font = (30,),command = a1P, state = tk.DISABLED)
    b2 = tk.Button(AlegeNrPlayeri, text = "2 Player", font = (30,),command = a2P)
    b1.grid(row = 1, column = 0, pady = 5,padx = 2)
    b2.grid(row = 1, column = 2, pady = 5,padx = 2)

    # ma voi ocupa acum de partea de alegere a simbolului
    tk.Label(AlegeSimbol,state = tk.DISABLED,justify = tk.CENTER, font = (30,), text = "Alege simbolul: ",
                    width = 20).grid(row = 0, column = 1)
    
    def aX():
        Joc.alegeX()
        b3.config(state = tk.DISABLED)
        b4.config(state = "normal")
    
    def aO():
        Joc.alegeO()
        b4.config(state = tk.DISABLED)
        b3.config(state = "normal")

    b3 = tk.Button(AlegeSimbol, text = "  X  ", font = (30,),command = aX, state = tk.DISABLED)
    b4 = tk.Button(AlegeSimbol, text = "  0  ", font = (30,),command = aO)
    b3.grid(row = 1, column = 0, pady = 5,padx = 2)
    b4.grid(row = 1, column = 2, pady = 5,padx = 2)

if __name__ == "__main__":
    main()
root.mainloop()