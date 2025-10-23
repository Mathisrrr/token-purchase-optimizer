from tkiteasy import *
from math import *
import matplotlib.pyplot as pyplt
import random
import time


X, Y = (800, 800)
# début de la zone de jeu
n = 20  # Nombre de pièce maximal générée dans le jeu.
t = 30  # Temps pour jouer en seconde.
VALMAX = 10  # Valeur maximale des pièces
LIMITE = 15   #La limite de coût à ne pas dépasser

Couleur = {"green": 1, "white": 3, "yellow": 5, "orange": 8, "red": 10}
nombre = {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', "ampersand": "1",
          "eacute": "2", "quotedbl": "3", 'apostrophe': "4", 'parenleft': "5", 'section': "6", 'egrave': '7',
          'exclam': '8', 'ccedilla': '9', 'agrave': '0'}


class piece():                                  #Classe des pièces pour pouvoir accéder aux aux valeurs plus facilement

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.val = random.randint(1,VALMAX)
        self.color = random.choice(list(Couleur.keys()))
        self.cost = Couleur[self.color]
        self.rdt=(self.val-self.cost)/self.cost

class Kasstet():

    def __init__(self):                                     #On initialise avec des paramètres de jeu par défaut
        self.NBP = random.randint(1, n)
        self.temps = t
        self.LIMITE= LIMITE
        self.Valmax=VALMAX


    def InitDisque(self):
        #Cette fonction créer toutes les pièces qui sont aussi appelés disque dans le programme(un disque est une pièce et vice-versa)
        #Cette fonction crée une liste qui contient toutes les pièces du jeu
        self.disque =[]
        a = 0

        if self.NBP % sqrt(self.NBP) == 0:  # Affiche optimal si carré parfait
            self.l = int(sqrt(self.NBP))
        else:  # Sinon
            self.l = int(sqrt(self.NBP) + 1)

        if self.NBP % self.l == 0 and self.NBP % sqrt(self.NBP) != 0:  # Taille des rectangles(coord y)
            self.tercy = 0.65 * Y / (self.l - 1)  # Si Pas besoin d'une ligne pas remplie
        elif self.l ** 2 - self.l > self.NBP:
            self.tercy = 0.65 * Y / (self.l - 1)
        else:
            self.tercy = 0.65 * Y / (self.l)  # Si besoin d'une ligne non remplie

        for y in range(self.l + 1):
            for x in range(self.l):
                if a == self.NBP:                           #Si on a atteint le nombre de pièces, on s'arrête.
                    break
                a += 1
                self.disque.append(piece(x, y))


    def Initgraphique(self):                        #Cette fonction ouvre la fenêtre graphique et met l'image de fonc
        self.g = ouvrirFenetre(X, Y)
        self.g.afficherImage(0, 0, "./Fond.jpg", X, Y)

    def Menu(self):                     #Cette fontion est la première qui est appelés quand on lance le jeu après l'ouverture de la fenêtre,
                                        #Elle permet au joueur d'entrer dans le jeu

        text = [self.g.afficherTexte("Bienvenue dans le jeu du Kasstet'", X / 2, 2 * Y / 5, "Black", int(X / 22)),
                self.g.afficherTexte("Cliquez sur PLAY pour afficher les modes de jeu", X / 2, Y / 2, 'Black',
                                     int(X / 30)),
                self.g.afficherImage(0.4*X, 2*Y/3, "./Play.jpg", int(X/5), int(Y/5))]

        a = True
        while a:
            clic = self.g.attendreClic()
            o = self.g.recupererObjet(clic.x, clic.y)
            if o == text[2]:                        #Si on clique sur l'image, on rentre dans le jeu, sinon rien ne se passe
                self.delete(text)
                a = False
                self.choices()

    def choices(self):              #Cette fonction permet au joueur de sélectionner le mode de jeu, d'affciher les règles du jeu ou bien d'aller dans les paramètres afin de modifier les paramètres de jeu
        a = True
        graph = []
        mode = ["Affichage des règles", "jeu en duo", "Mode robot", "Paramètres"]
        for i in range(len(mode)):
            text = self.g.afficherTexte(mode[i], X / 2, 20 * (i + 1) * Y / 100, "Black", int(X / 20))
            graph.append(text)

        while a:

            clic = self.g.attendreClic()
            o = self.g.recupererObjet(clic.x, clic.y)

            if o in graph:
                self.delete(graph)
                a = False
            if o == graph[0]:
                self.rules()
            if o == graph[1]:
                self.jeuenduo()
            if o == graph[2]:
                self.choices2()
            if o == graph[3]:
                self.settings()

    def settings(self):                             #Cette fonction est le menu de paramétrage du jeu, c'est ici que l'on vient modifier les valeurs de jeu

        txt2="Limite de coût :"
        txt3="Limite de temps :"
        txt4="Nombre de pièces max :"
        txt5="Valeur max d'une pièce :"
        text1 = self.g.afficherTexte("Rentrer les valeurs souhaitées",X/2,0.15*Y,"black",int(X/25))
        text2 = self.g.afficherTexte(f"{txt2} {self.LIMITE}", 0.2 * X, 0.35 * Y, "black", int(X / 30))
        text3 = self.g.afficherTexte(f"{txt3} {self.temps}", 0.2 * X, 0.55 * Y, "black", int(X / 30))
        text4 = self.g.afficherTexte(f"{txt4} {self.NBP}", 0.7 * X, 0.35 * Y, "black", int(X / 30))
        text5 = self.g.afficherTexte(f"{txt5} {self.Valmax}", 0.7 * X, 0.55 * Y, "black", int(X / 30))
        text6 = self.g.afficherTexte("Retour au menu", 0.5 * X, 0.8 * Y, "black", int(X / 25))


        graph=[text1,text2,text3,text4,text5,text6]

        dic={text2:(self.LIMITE,txt2),text3:(self.temps,txt3),text4:(self.NBP,txt4),text5:(self.Valmax,txt5)}
        réglage=True

        while réglage:

            clic=self.g.attendreClic()
            o=self.g.recupererObjet(clic.x,clic.y)
            if o in dic.keys():
                pointe=self.g.dessinerCercle(o.x,o.y+0.05*Y,0.02*X,"black")
                val=self.changetxt(o,dic[o][1],dic[o][0])
                self.g.supprimer(pointe)
                if o==text2:
                    self.LIMITE=val                             #On modifie les valeurs modifiés par le joueur
                if o==text3:
                    self.temps=val
                if o ==text4:
                    self.NBP=val
                if o==text5:
                    self.Valmax=val

            if o == text6:
                self.delete(graph)                                      #Pour retourner au menu de sélection
                réglage=False

                self.choices()


    def changetxt(self,text,txt,val):               #Cette fonction permet de changer le texte en direct sur l'écran, elle renvoie la valeur à la fin de la modification ou
                                                    #la valeur d'avant la modification si la valeur est vide après modification
        ancien=val
        val=str(val)
        tabval = []
        for i in range(len(val)):
            tabval.append(val[i])
        init=tabval

        choix=True
        while choix:
            touche=self.g.attendreTouche()


            if touche=='Return':
                choix=False
                if tabval==[]:
                    tabval=init

            if touche=="BackSpace":
                if tabval!=[]:
                    tabval.pop(-1)

            if touche in nombre.keys():
                tabval.append(nombre[touche])

            val=""

            for i in tabval:
                val+=i

            self.g.changerTexte(text, f"{txt} {val}")

        if val=="":
            self.g.changerTexte(text,f"{txt}{ancien}")
            return ancien
        else:
            return int(val)


    def graph(self):                        #Cette fonction permet l'affichage graphique ordonné des pièces sur le jeu
        x = 0.1*X
        y = 0.3 * Y                     #coin supérieur gauche de la "fenètre des pièces"

        X1 = 0.8 * X                #0,8 et 0,65 --> taille de la "fenêtre des pièces" (proportions de la fenètre (X,Y))
        X2 = 0.65 * Y

        self.trecx = X1 / self.l

        self.g.dessinerLigne(0, Y / 4, X, Y / 4, 'Black')


        self.size = min(((43 / 100) * self.trecx, (43 / 100) * self.tercy))#Fonction de taille optimal pour les cercles
        self.disquegfx = {}
        for piece in self.disque:                                           #Stockage des disques graphiques dans un dico ou le disque graphique et le chiffre sont des clés qui sont associés à la pièce en valeur
            self.disquegfx[
                self.g.dessinerDisque((x + self.trecx / 2) + piece.x * self.trecx, (y + self.tercy / 2) + piece.y * self.tercy, self.size,
                                      piece.color)] = piece
            self.disquegfx[
                self.g.afficherTexte(piece.val, (x + self.trecx / 2) + piece.x * self.trecx, (y + self.tercy / 2) + piece.y * self.tercy,
                                     "black", int(self.size))] = piece


    def affichage(self):                        #Simple fonction d'affichage qui permet uniquement l'affichage des scores
        ttext=int(X / 42)
        player1=self.g.afficherTexte("Points Joueur 1", 0.22*X,0.1*Y,"black",ttext)
        player2=self.g.afficherTexte("Points Joueur 2", 0.77*X,0.1*Y,"black",ttext)
        rappel = self.g.afficherTexte("Rappel des coûts des couleurs: VERT:1 | BLANC:3 | JAUNE:5 | ORANGE:8 | ROUGE:10",
                                      0.5 * X, 0.98 * Y, "black", int(X / 54))
        self.couttxt = self.g.afficherTexte(f"le coût actuel est de {self.cout}", 0.75 * X, 0.22 * Y, "black",
                                            ttext)
        self.scorejoueur1txt = self.g.afficherTexte(str(self.scorejoueur1), 0.22 * X, 0.15 * Y, "black", ttext)
        self.scorejoueur2txt = self.g.afficherTexte(str(self.scorejoueur2), 0.75 * X, 0.15 * Y, "black", ttext)
        limite2 = self.g.afficherTexte("Coût à ne pas dépasser:", 0.20 * X, 0.22 * Y, "black", ttext)
        limite = self.g.afficherTexte(str(self.LIMITE), 0.4 * X, 0.22 * Y, "black", ttext)
        timer = self.g.afficherTexte("temps : ", 0.5 * X, 0.1 * Y, "black", ttext)

        self.sec = self.g.afficherTexte(self.temps, 0.5 * X, 0.15 * Y, "black", ttext)

    def jeuenduo(self):                     #Cette fonction organise la partie jeu en duo du projet
        self.InitDisque()

        numtour=1
        self.graph()
        self.cout = 0
        self.scorejoueur1,self.scorejoueur2=0,0         #On initialise les variables de score
        self.affichage()

        text=self.g.afficherTexte("clic pour démarrer", X / 2, Y / 3.64, "brown", int(X / 40))
        self.g.attendreClic()
        self.g.supprimer(text)
        start = time.time()

        #On fait jouer le premier joueur
        self.scorejoueur1=self.choixpiece(start,self.scorejoueur1,self.scorejoueur1txt,numtour)
        text = self.g.afficherTexte("Le joueur 2 clic pour démarrer", X / 2, Y / 3.64, "brown", int(X / 40))
        self.g.attendreClic()
        numtour=2
        self.g.supprimer(text)
        start = time.time()
        self.g.changerTexte(self.couttxt, f"Le cout actuel est de {self.cout}")

        #On fait jouer le deuxième joueur
        self.scorejoueur2=self.choixpiece(start,self.scorejoueur2,self.scorejoueur2txt,numtour)


        #Affiche le gagnant
        gagnant=True
        if self.scorejoueur1 > self.scorejoueur2:
            gg = 1
        elif self.scorejoueur1 == self.scorejoueur2:            #Si égalité
            a = self.g.afficherTexte("égalité, pas de vainqueur,appuyer sur entrer pour revenir au menu", X / 2, Y / 3.64, "brown", int(X / 45))
            gagnant=False
        else:
            gg = 2

        if gagnant:
            if gg == 1 or gg == 2:
                a = self.g.afficherTexte(f"le vainqueur est le joueur {str(gg)}, appuyer sur entrer pour revenir au menu", X / 2, Y / 3.64, "brown", int(X / 45))

        self.entrer()
        self.retourMenu()               #Permet de revenir au menu

    def choixpiece(self,start,scorejoueur,scorejoueurtxt,numtour):          #Cette fonction permet au joueur de jouer son tour, c'est à dire sélectionner ses pièces,
                                                                            #On lui donne le score du joeur, l'affichage graphique du score du joueur et le numéro du tour
                                                                            #La fonction renvoie le score du joueur
        tour=True
        cpt=0
        stock=[]
        ACT = self.temps
        memoire = []
        cout=0
        self.tempsrestant=self.temps
        while self.tempsrestant > 0 and tour:
            clic = self.g.recupererClic()
            touche = self.g.recupererTouche()
            if clic != None:
                o = self.g.recupererObjet(clic.x, clic.y)                                           #On vérifie que le disque sélectionné n'est pas déjà sélectionné et ne dépasse pas la limite de coût

                if o in self.disquegfx.keys() and self.disquegfx[o] not in memoire and cout+self.disquegfx[o].cost<=self.LIMITE:
                    memoire.append(self.disquegfx)
                    scorejoueur += self.disquegfx[o].val
                    cout +=self.disquegfx[o].cost                                           #On met à jour les variables avec les données de la nouvelles pièce sélectionnées
                    stock.append(self.g.dessinerCercle((X / 10 + self.trecx / 2) + self.disquegfx[o].x * self.trecx, ( 0.3 * Y + self.tercy / 2) + self.disquegfx[o].y * self.tercy, self.size+0.1*self.size,"red"))
                    self.g.changerTexte(scorejoueurtxt, str(scorejoueur))
                    self.g.changerTexte(self.couttxt,f"Le cout actuel est de {cout}")
                    cpt+=1



            courant = time.time()
            delta = int(courant - start)
            self.tempsrestant = self.temps - delta
            if self.tempsrestant != ACT and self.tempsrestant >= 0:  #ACT permet de réduire le nombre d'appel de la fonction
                ACT = self.tempsrestant
                self.g.changerTexte(self.sec, self.tempsrestant)
                self.g.actualiser()

            if self.tempsrestant == 0 or touche == "Return" or len(memoire)==len(self.disque):              #On arrive dans cette boucle à la fin du tour
                tour = False
                if numtour==1:
                    a=self.g.afficherTexte("fin du tour Le joueur suivant se prépare", X / 2, Y / 3.64, "black", int(X / 40))
                if numtour==2:
                    a=self.g.afficherTexte("fin du jeu, appuyer sur entrer pour afficher les résultats", X / 2, Y / 3.64, "black", int(X / 40))
                    self.entrer()
                self.delete(stock)
                self.g.supprimer(a)

                return scorejoueur

    def rules(self):                #Cette fonction permet juste d'afficher les règles du jeu, elle à pour but d'aider à la compréhension du jeu

        text1 = self.g.afficherTexte("Les joueurs on un temps imparti\npour choisir toutes les pièces.\n"
                                     "\nLe joueur 1 choisi sa combinaison \nde pièces en 1er.\n"
                                     "\nPuis c'est au tour du joueur 2.\n"
                                     "\nCelui avec le score le plus élevé\nà la fin du temps imparti gagne.", X / 2,
                                     Y / 2, "Black", int(X / 25))
        text2 = self.g.afficherTexte("REGLES", X / 2, 0.1 * Y, "Black", int(X / 20))

        var = True
        text3 = self.g.afficherTexte("Retour au menu", X / 2, 0.9 * Y, 'Black', int(X / 20))
        text4 = self.g.dessinerLigne(0.2 * X, 0.85 * Y, 0.8 * X, 0.85 * Y, "Black", 2)
        text5 = self.g.dessinerLigne(0.2 * X, 0.95 * Y, 0.8 * X, 0.95 * Y, "Black", 2)
        text6 = self.g.dessinerLigne(0.2 * X, 0.85 * Y, 0.2 * X, 0.95 * Y, "Black", 2)
        text7 = self.g.dessinerLigne(0.8 * X, 0.85 * Y, 0.8 * X, 0.95 * Y, "Black", 2)

        text = [text1, text2, text3, text4, text5, text6, text7]

        while var:
            clic = self.g.attendreClic()
            o = self.g.recupererObjet(clic.x, clic.y)
            if o == text3:
                self.delete(text)
                self.choices()
                var = False

    def choices2(self):                     #Cette fonction permet de choisir l'algo que l'on veut tester, il y en a deux et un mode performance qui permet de tester les performances de nos différents algos
        a=True

        text1 = self.g.afficherTexte("Solution 1", 0.25*X, Y/2, "Black", int(X / 20))
        text2 = self.g.afficherTexte("Solution 2", 0.75*X, Y/2, "Black", int(X / 20))
        text3 = self.g.afficherTexte("Mode performance",0.5*X,0.8*Y,"black", int(X/25))
        text4= self.g.afficherTexte("Retour au menu",0.5*X,0.2*Y,"black", int(X/15))
        graph=[text1,text2,text3,text4]
        while a:
            clic=self.g.attendreClic()
            o = self.g.recupererObjet(clic.x, clic.y)

            if o in graph:
                a=False
                self.delete(graph)

            if o == text1:
                self.algo1()
            if o == text2:
                self.algo2()
            if o == text3:
                self.modeperf()

            if o == text4:
                self.choices()


    def resolvealgo1(self):                     #Ceci est l'algo de résolution naïf, il fonctionne avec un rendement, les pièces sont triées par rendement, càd par ordre de rentabilité
                                                # et on sélectionne les plus rentables jusqu'à avoir atteint la limite de coût
        start=time.time()                        #La fonction renvoie la liste avec les pièces selectionnées,le score obtenu et le temps qu'il a mis pour trouver la solution
        rendement = sorted(self.disque, key=lambda x: x.rdt, reverse=True)
        list = []
        for piece in rendement:
            list.append(piece.rdt)

        cout = 0
        score = 0
        solution = []
        for piece in rendement:
            if cout + piece.cost <= self.LIMITE:                    #Si on peut payer la piece supplémentaire, on la sélectionne
                cout += piece.cost
                score += piece.val
                solution.append(piece)
        stop=time.time()
        return solution,score,stop-start

    def algo1(self):                   # Cette fonction permet de lancer l'algo naïf et d'en exploiter les résultats
            self.InitDisque()

            self.graph()
            (solution,score,chrono)=self.resolvealgo1()        #On récupére les résultats de l'algo

            #self.test(self.disque)
            #self.test(solution)                        #Permet de tester la solution sur le serveur

            text1=self.g.afficherTexte("Appuyer sur entrer pour afficher la solution",X/2,0.1*Y,"black",int(X/43))
            self.entrer()
            self.g.changerTexte(text1,f"Cette solution rapportera {score} points avec une limite de coût de {self.LIMITE}")
            solutiongfx=set()
            largeur = 0.9 * X / len(solution)
            taille = min(int(0.43*largeur),int(0.05 * Y))
            index=0                                             #Affichage graphique des résultats
            for piece in solution:
                solutiongfx.add(self.g.dessinerDisque(0.05*X+index*largeur+largeur/2,0.18*Y,taille,piece.color))
                solutiongfx.add(self.g.afficherTexte(piece.val,0.05*X+index*largeur+largeur/2,0.18*Y,"black",int(taille)))
                solutiongfx.add(self.g.dessinerCercle((X / 10 + self.trecx / 2) + piece.x * self.trecx, ( 0.3 * Y + self.tercy / 2) + piece.y * self.tercy , self.size+0.1*self.size ,"red"))
                index+=1

            text=self.g.afficherTexte("Appuyer sur entrer pour revenir au menu", X / 2, Y / 3.64, "black", int(X / 40))
            self.entrer()
            self.retourMenu()                       #On revient au menu


    def find_key(self,value,dico):              #Fonction qui permet de retrouver la clé d'une valeur dans un dictionnaire
        for k, val in dico.items():             #On lui rentre en paramètre la valeur et le dictionnaire et elle nous renvoie la clé associée
            if value == val:
                return k

    def algo2(self):                    #Cette fonction permet de lancer et de récuperer les résultats de notre algo performant
        self.InitDisque()
        self.graph()


        score=0
        cout=0
        solution = self.resolve()[0]                #On récupère une liste solution où les pièces sont sous formes de tuples
        piecesol=[]
        memoire=[]
        for tuple in solution:                      #Ici, on retrouves les pièces associées au tuples de la solution
            score+=tuple[0]
            cout+=tuple[1]
            for i in range(len(self.disque)):
                if tuple==(self.disque[i].val,self.disque[i].cost) and self.disque[i] not in memoire:
                    memoire.append(self.disque[i])
                    piecesol.append(self.disque[i])
                    continue

        text1 = self.g.afficherTexte("Appuyer sur entrer pour afficher la solution", X / 2, 0.1 * Y, "black",
                                     int(X / 43))
        self.entrer()
        self.g.changerTexte(text1, f"Cette solution rapportera {score} points avec une limite de coût de {self.LIMITE}")           #On affiche notre solution
        solutiongfx = set()
        largeur = 0.9 * X / len(solution)
        taille = min(int(0.43*largeur),int(0.05 * Y))
        index = 0
        for piece in piecesol:
            solutiongfx.add(
                self.g.dessinerDisque(0.05 * X + index * largeur + largeur / 2, 0.18 * Y, taille, piece.color))                         #On déssine les pièces sélectionnées et on les entoures
            solutiongfx.add(self.g.afficherTexte(piece.val, 0.05 * X + index * largeur + largeur / 2, 0.18 * Y, "black",
                                                 int(taille)))
            solutiongfx.add(
                self.g.dessinerCercle((0.1*X  + self.trecx / 2) + piece.x * self.trecx, (0.3 * Y + self.tercy / 2) + piece.y * self.tercy,
                                      self.size + 0.1 * self.size, "red"))
            index += 1

        text = self.g.afficherTexte("Appuyer sur entrer pour revenir au menu", X / 2, Y / 3.64, "black", int(X / 40))
        self.entrer()
        self.retourMenu()                   #Retour au menu

    def resolve(self):                  #Cette fonction est l'algorithme le plus performant permettant de trouver la meilleur solution
        start = time.time()
        coin = []
        for piece in self.disque:  # Création des tuples
            coin.append((piece.val, piece.cost))
        tab=[[0]*(self.LIMITE+2) for i in range(len(coin)+2)]         #On met les entêtes du tableau
        tab[0][0]="X"
        for i in range (self.LIMITE+1):                                         #On met en entête des colonnes du tableau les coûts
            tab[0][i+1]=i

        for i in range(1,len(tab)):                                       #On met en entête des lignes du tableau les tuples

            if i==1:
                tab[i][0]=(0,0)                                 #On rajoute le tuple(0,0)
            else:
                tab[i][0]=coin[i-2]                                 #On met les autres tuples(valeur,cout)

        ligne=-1
        for l in tab:
            ligne+=1

            if ligne == 0 or ligne==1:
                ancien=l                            #On garde en mémoire la ligne d'avant
                continue



            for c in range (len(l)):                         #Init ligne 0
                if c==0:
                    continue

                grid=tab[0][c]-l[0][1]                      #Calcul de la différence de coût

                if grid<0:

                    l[c]=ancien[c]                          #Si on peut pas prendre la pièce, on met la même valeur que la ligne du dessus

                if grid>=0:

                    l[c] = max(ancien[c], l[0][0]+ancien[grid + 1])             #Si on peut prendre la nouvelle pièce, on compare le mieux entre la prendre ou ne pas la prendre

                if c==len(l)-1:
                    ancien=l

        valeur=tab[-1][-1]                              #On a ici le meilleur score qu'il est possible d'atteidre
        dep=self.LIMITE
        solution = []
        ligne=len(tab)-1

        for l in tab[:0:-1]:

            ligne -= 1

            if ligne ==-1:                              #On s'arrête si l'on arrive en haut du tableau
                break
            if ligne ==len(tab)-2:                      #On ne fais rien sur la dernière ligne du tableau
                ancien=l                                   #On initialise à la ligne la plus basse du tableau et on remonte de lignes en lignes
                continue

            if ancien[dep+1]!=l[dep+1]:                     #Si la case du dessus est différente, cela veut dire que l'on a pris la pièce de la ligne d'en dessous
                dep-=ancien[0][1]
                valeur=l[dep+1]

                solution.append(ancien[0])                  #On rajoute donc la pièce à la liste de solution
                ancien=l

            else:

                ancien=l                                    #On change la ligne d'avant pour pouvoir comparer les deux lignes
        stop = time.time()
        return solution,stop-start              #La fonction renvoie une liste de tuples constituant la solution et le temps qu'elle met pour trouver le résultat

    def modeperf(self):         #On rentre ici dans le mode performance qui permet d'analiser les temps de recherche des deux algorithmes
        lim="1000"
        ech="10"
        algo="2"

        choix1=True
        choix2=True
        choix3=True
        text1=self.g.afficherTexte("Veuillez saisir le nombre de pièce maximal, \nappuyer sur entrer, puis saisir l'échelle et \nl'alogorithme voulu",X/2,Y/5,"black",int(X/32))
        text2=self.g.afficherTexte("Nombre de pièce max : 1000",X/2,4*Y/10,'black',int(X/20))
        text3=self.g.afficherTexte("Échelle des résultats : 10",X/2,6*Y/10,'black',int(X/20))
        text5=self.g.afficherTexte("Algo : 2",X/2,7.5*Y/10,'black',int(X/20))
        text4=self.g.afficherTexte("Attention à ne pas être trop gourmand ;)",X/2,9*Y/10,'black',int(X/35))
        text6=self.g.afficherTexte("Le mode 3 permet de comparer les deux algos",X/2,8.2*Y/10,'black',int(X/50))
        pointe=self.g.dessinerCercle(text2.x,text2.y+0.05*Y,int(0.01*X),"black")
        graph=[text1,text2,text3,text4,text5,text6,pointe]

        tablim=[]
        for i in range (len(lim)):
            tablim.append(lim[i])
        tabech=[]
        for i in range (len(ech)):
            tabech.append(ech[i])
        tabalgo=["2"]

        while choix1:                               #On rentre les paramètres pour lancer le mode performance
            touche=self.g.attendreTouche()

            if touche=='Return':
                choix1=False

                if tablim==[]:

                    tablim=['1','0','0','0']


            if touche=="BackSpace":
                if tablim!=[]:
                    tablim.pop(-1)


            if touche in nombre.keys():
                tablim.append(nombre[touche])

            lim=""

            for i in tablim:
                lim+=i

            self.g.changerTexte(text2,f"Nombre de pièce max : {lim}")

        self.g.deplacer(pointe,0,0.2*Y)

        while choix2:                           #Deuxième paramètre
            touche = self.g.attendreTouche()

            if touche == 'Return':
                choix2 = False

                if tabech == []:
                    tabech = ['1', '0']

            if touche == "BackSpace":
                if tabech != []:
                    tabech.pop(-1)

            if touche in nombre.keys():
                tabech.append(nombre[touche])

            ech = ""
            for i in tabech:
                ech += i
            self.g.changerTexte(text3, f"Échelle des résultats : {ech}")

        self.g.deplacer(pointe, 0, 0.2 * Y)
        while choix3:                       #troisième paramètre
            touche=self.g.attendreTouche()

            if touche == 'Return':
                choix3 = False
                if tabalgo == []:
                    tabalgo = ["2"]
            if touche == "BackSpace":
                if tabalgo != []:
                    tabalgo.pop(-1)

            if touche =="1" or touche=="2"or touche =="eacute" or touche =="ampersand" or touche=="3" or touche == "quotedbl" :
                if tabalgo==[]:
                    tabalgo.append(nombre[touche])


            algo = ""
            for i in tabalgo:
                algo += i

            self.g.changerTexte(text5,f"Algo : {algo}")

        self.delete(graph)

        self.performance(int(lim),int(ech),int(algo))               #On lance la fonction qui affiche les graphiques


    def performance(self,lim,echelle,numalgo):                          #Cette fonction reçoit en paramètre les options d'affichages pour les grahiques: le nombre de pièce, l'échelle du graphique et l'algo testé

        text1=self.g.afficherTexte("Chargement des résultats...\nMerci de patienter",X/2,Y/2,"black",int(X/20))
        self.g.actualiser()
        temps=[]
        num=[]
        self.NBP=echelle
        pyplt.xlabel('nombre de pièces')
        pyplt.ylabel('temps en centième de secondes')
        pyplt.title(f'résultat avec LIMITE={self.LIMITE} et VALMAX={self.Valmax}')

        if numalgo==2:                      #Si on teste l'algo 2

            for i in range (lim//echelle):
                self.InitDisque()
                temps.append(self.resolve()[1]*100)
                num.append(self.NBP)
                self.NBP+=echelle

        if numalgo==1:                      #Si on teste l'algo 1
            for i in range (lim//echelle):
                self.InitDisque()
                temps.append(self.resolvealgo1()[2]*100)
                num.append(self.NBP)
                self.NBP+=echelle

        if numalgo==1 or numalgo==2:

            pyplt.plot(num, temps)
            pyplt.show()

        temps1=[]
        temps2=[]
        if numalgo==3:
                                                #Affiche des deux algos comparés

            for i in range (lim//echelle):
                self.InitDisque()
                temps1.append(self.resolvealgo1()[2]*100)
                temps2.append(self.resolve()[1]*100)
                num.append(self.NBP)
                self.NBP+=echelle

            pyplt.plot(num, temps1)
            pyplt.plot(num, temps2)

            pyplt.legend(['Algo 1', 'Algo 2'])
            pyplt.show()


        text2=self.g.afficherTexte("Retour au menu principal",X/4,7*Y/10,'black',int(X/32))
        text3=self.g.afficherTexte("Faire un nouveau test",3*X/4,7*Y/10,'black',int(X/32))

        graph=[text2,text3]

        a=True

        while a:
            clic=self.g.attendreClic()
            o=self.g.recupererObjet(clic.x,clic.y)

            if o in graph:
                a=False
                self.delete(graph)
                self.g.supprimer(text1)
            if o ==graph[0]:
                self.choices()
            if o == graph[1]:
                self.modeperf()




    def affichagetableau(self,tableau):             #Cette fonction permet d'afficher dans la console le tableau de l'algo 2
        print("\n\n")
        for l in tableau:
            print(l)


    def delete(self, list):                 #Cette fonction reçoit une liste d'objet graphique et les supprime tous
        for obj in list:
            self.g.supprimer(obj)

    def test(self,list):                    #Cette fonction recoit une liste de pièce et l'affiche afin de la rentrer sur le serveur de test des solutions
        for piece in list:
            print(f"({piece.val},{-piece.cost})",end=' ')

    def test2(self,list):               #Même chose que la focntion précedénte mais elle reçoit ici des tuples (valeur,coût)
        for piece in list:
            print(piece,end='')

    def entrer(self):                   #Cette fonction permet de faciliter le code, elle permet juste de bloquer le code en attendre que la touche entrer soit appuyée
        b = True

        while b:

            touche = self.g.recupererTouche()
            if touche == "Return":
                b = False

    def retourMenu(self):           #Cette fonction supprime tout les objets à l'écran, simule un chargement et renvoie au menu de sélection des modes
        self.g.supprimerGFX()
        self.g.afficherImage(0, 0, "./Fond.jpg", X, Y)
        text1 = self.g.afficherTexte('Retour au menu en cours ...', X / 2, Y / 2, "black", int(X / 20))
        self.g.actualiser()

        time.sleep(2)
        self.g.supprimer(text1)
        self.choices()


    def jouer(self):                        #Fonction qui lance le jeu
        self.Initgraphique()
        self.Menu()


jeu = Kasstet()                     #On lance notre programme
jeu.jouer()