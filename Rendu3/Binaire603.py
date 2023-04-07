
from math import log
from random import randint
from arithmetiqueDansZ import ElmtZnZ
import matplotlib.pyplot as plt

class Binaire603(list):#Voir Object ?
    #list pour transformer un octet en caractère
    lchr=[chr(k) for k in range(256)]
    for k in list(range(32))+list(range(0x7f,0xa1))+[0xad]:  lchr[k]=chr(k+256)
    #dict pour transformer un caractère en octet
    dbin=dict()
    for k in range(256):
        dbin[lchr[k]]=k  #Dictionnaire faisant correspondre un caractère à un octet
    #Le mieux est d'éviter les caractères suivants dans les fichiers à traiter
    dbin['’']=dbin["'"];dbin['\n']=13;dbin['œ']=dbin['æ'];dbin['—']=dbin['-'];dbin['…']=dbin['.'];

    def __init__(self,param):
        """lbin est une liste ne contenant que :
            des entiers de [0..255] qui sont donc assumés comme des octets"
        ou bien une liste de ElmtZnZ(..,256)
        lbin peut aussi être une chaine de caractère
        >>> Binaire603([ElmtZnZ(2,256),3])
        Binaire603([ 0x02, 0x03])
        >>> Binaire603("Trop tôt !")
        Binaire603([ 0x54, 0x72, 0x6f, 0x70, 0x20, 0x74, 0xf4, 0x74, 0x20, 0x21])
        """
        if isinstance(param,str):
            #bc=param.encode('ascii', 'ignore') #byte
            #super().__init__([b for b in param.encode('ascii', 'ignore')])
            lb=[]
            for k,c in enumerate(param):
                if c in Binaire603.dbin:
                    lb.append(Binaire603.dbin[c])
                else:
                    lb.append(ord(c) % 256)
                    #print(f"{c=}:{ascii(c)}",end=' | ')
            super().__init__(lb)
            #super().__init__( [Binaire603.dbin[c] for c in chaine] )
        else:
            lb=[]
            for b in param:
                assert Binaire603.estOctet(b),f"Les éléments d'un Binaire603 doivent convertible en octets, ex : {b}"
                lb.append(int(b))
            super().__init__(lb )
    def toString(self):
        """
        >>> Binaire603("Trop tôt !").toString()
        'Trop tôt !'
        """
        ch=""
        for b in self:
                if b==13:
                     ch+="\n"
                else:
                    ch+=Binaire603.lchr[b]
        return ch
    def sauvegardeDansFichier(self,nomFic,verbose=False):
        "Enregistre dans un fichier nommé nomFic"
        if verbose:print(f"lecture du fichier :{nomFic}")

        if nomFic[-4:].upper()==".TXT":
            with open(nomFic,"wt") as f:
                    f.write(self.toString())
        else:
            with open(nomFic,"wb") as f:
                    for b in self:
                        f.write(bytes([b]))

    def bin603DepuisFichier(nomFic,verbose=False):
        """renvoie un Binaire603 d'après les données d'un fichier
        #>>> b1=Binaire603.exBin603(taille=10,num=5)
        #>>> b1.sauvegardeDansFichier("MonBin.bin")
        #>>> b2=Binaire603.bin603DepuisFichier("MonBin.bin")
        #>>> print(b2)
        # 10 octets :00ff00ff00ff00ff00ff
        #>>> lb=Binaire603.bin603DepuisFichier("Les Miserables.TXT")
        """
        if verbose:print(f"lecture du fichier :{nomFic}")

        if nomFic[-4:].upper()==".TXT":
            with open(nomFic, 'r', encoding="utf8") as f:
                txt = f.read()
            return Binaire603(txt)
        else:
            with open(nomFic,"rb") as f:
                data = f.read()
                if verbose:print(f"data est de type : {type(data)}")
                b=Binaire603(data)
                if verbose:print(f"data : {b}")
            return b

    def exBin603(taille=1000,num=0):
        """Renvoie une instance Exemples de cette classe avec pour num :
        0: 255 fois 255 puis 254 fois 254 etc...
        1: un octet de chaque
        2: octets aléatoires
        3: 254 13 puis 255 14 puis 254 13 puis 255 14 ...
        4: 254 13 puis 255 14 puis 256 15 répétés
        5: et plus: 1000 fois un octet sur deux à 255
        """
        if num==0:
            data=[]
            for i in range(255,0,-1):
                data+=[i]*i
        elif num==1:
            data=[k for k in range(256)]
        elif num==2:
            data=[randint(0,255) for k in range(256)]
        elif num==3:
            data=[13]*254+[14]*255
        elif num==4:
            data=[13]*254+[14]*255+[15]*256
        else:
            data=[(k%2)*255 for k in range(256)]
        while len(data)<taille:
            data+=data
        return Binaire603(data[:taille])

    def estOctet(val):
        """Renvoie true si val est un entier et si il se trouve dans [0..255]
        >>> Binaire603.estOctet(255) and not(Binaire603.estOctet(256))
        True
        >>> not(Binaire603.estOctet(-1))and not(Binaire603.estOctet("coucou")) and not(Binaire603.estOctet([128,12]))
        True
        """
        res=False
        if isinstance(val, ElmtZnZ) and val.n==256:
            res=True

        elif isinstance(val,int) and val>=0 and val <=255:
            res=True

        return res

    def ajouteOctet(self,data):
        """Ajoute un octet ou une liste d'octets tout en vérifiant la validité des données
        >>> a=Binaire603([1,2,3,4]); a.ajouteOctet(10); a
        Binaire603([ 0x01, 0x02, 0x03, 0x04, 0x0a])
        >>> a.ajouteOctet([11,12]);a
        Binaire603([ 0x01, 0x02, 0x03, 0x04, 0x0a, 0x0b, 0x0c])
        """
        if isinstance(data,list):
            for oc in data:
                assert Binaire603.estOctet(oc)
                self+=[oc]
        else:
            assert Binaire603.estOctet(data)
            self+=[data]
    def lisOctet(self,pos):
        """Lis un octet et incrémente pos
            Utilisation val,pos=monBin.lisOctet(pos) comme suit
            >>> a,pos = Binaire603.exBin603(10,1) ,5

            >>> val,pos = a.lisOctet(5)

            >>> val,pos
            (5, 6)
            """
        return self[pos],pos+1

    def __str__(self):
        """Renvoie une chaine de caractère permettant de visualiser Binaire603 self
        >>> str(Binaire603([12,128]))
        '2 octets : 0c80'
        """
        s=f"{len(self)} octets : "

        def octetStr(oc):
            """
            >>> octetStr(12)
            0x0c
            >>> octetStr(ElmtZnZ(17,256))
            0x11

            """

            if isinstance(oc,ElmtZnZ):
                val=oc.rep
            else:
                val=oc
            return f"{val:02x}"

        if len(self)<=150 :
            for oc in self:
                s+=octetStr(oc)
        else:
            for oc in self[:100]:
                s+=" "+octetStr(oc)
            s+="........"
            for oc in self[-50:-1]:
                s+=" "+octetStr(oc)
        return s
    def __repr__(self):
        """Renvoie une chaine de caractère représentant TOUTES les données du Binaire603 self
        sous la forme d'un appel à son constructeur ex: Binaire603([ 0x57, 0x26, 0xfd]) """
        s="Binaire603(["
        for oc in self:
            if isinstance(oc, ElmtZnZ):
                s+=" "+oc.__repr__()+","
            else:
                s+=" "+f"0x{oc:02x}," # https://docs.python.org/fr/3/library/string.html
        return s[:-1]+ "])"
    def __eq__(self,other):
        """Renvoie True lorsque les octets sont égaux deux à deux
        >>> Binaire603([ 0xcb, 0xba])==Binaire603([ 0xcb, 0xba])
        True
        >>> Binaire603([ ElmtZnZ(1,256), ElmtZnZ(2,256)])==Binaire603([1,2])
        True
        >>> Binaire603([ 0xcb, 0xba])==Binaire603([ 0xcb])
        False
        >>> Binaire603([ 0xcb, 0xba])==Binaire603([ 0xcb, 0xbb])
        False
        """
        #todo:  voir le super pour comparé les références
        if len(self)!=len(other): return False
        k,n = 0, len(self)
        res= True
        while res and k<n:
            res= (self[k]==other[k])
            k+=1
        return res


    def lFrequences(self):
        """Renvoie la liste des fréquences de chaque valeur
        Une fréquence est un nombre entre 0 et 1 et correspond à un pourcentage : 0.25=25%
        >>> lf=Binaire603([1,2,3,3,3,3,4,8,8,128]).lFrequences()
        >>> lf[3]
        0.4
        """
        lf = [0]*256
        n = len(self)
        for oc in self:
            lf[oc]+=1/n
        return lf

    def entropie(self):
        """
        >>> Binaire603([6,6,6,6,6,6,6,6,5,5,5,5,5,5,7,7,7,7,8,9]).entropie()
        1.9464393446710155
        """
        h=0
        lf = self.lFrequences()
        for f in lf:
            if f>0:h+=- f*log(f, 2)
        return h


    def afficheTableauDesFrequences(self):

        lf = self.lFrequences()
        print(f"Tableau des fréquences de la liste de {self}")
        s=""
        for b,f in enumerate(lf):
            s+=f"{b:02x}:{Binaire603.lchr[b]}"
            s+=f"{(f*100):5.1f}%|" #https://realpython.com/python-f-strings/
            if (b+1)%8==0:
                 print(s)
                 s=""
        print(s)

    def afficheTableauDesFrequencesDecroissantes(self):
        lf = self.lFrequences()
        lbTries=sorted([k for k in range(256)], key=lambda b:lf[b],reverse=True)
        lbTriesNonNuls=[b for b in lbTries if lf[b]>0]

        print(f"Tableau des fréquences décroissantes de la liste de {self}")
        s=""

        for k,b in enumerate(lbTriesNonNuls) :
            s+=f"{b:02x}:{Binaire603.lchr[b]}"
            s+=f"{(lf[b]*100):5.1f}%|" #https://realpython.com/python-f-strings/
            if (k+1)%8==0:
                 print(s)
                 s=""
            k+=1;
        print(s)
    def afficheHistogrammeDesFrequences(self,titre="Histogramme des fréquences",nbValMax=20):
        """
        Binaire603([1,2,3,3,3,3,4,8,8,128]).afficheHistogrammeDesFrequences()
        nbValMax est à mettre à 256 pour avoir l'intégralité des valeurs affichées
        """
        lf = self.lFrequences()
        lbTries=sorted([k for k in range(256)], key=lambda b:lf[b],reverse=True)
        lbTriesNonNuls=[b for b in lbTries if lf[b]>0]

        lEtiquettes=[ f"{b:02x}:{Binaire603.lchr[b]}" for b in lbTriesNonNuls]
        lVal=[lf[b] for b in lbTriesNonNuls]

        plt.bar(lEtiquettes[:nbValMax], lVal[:nbValMax])
        plt.title(titre)
        plt.show()
    
    def toNumber(self):
        """ Renvoie un entier correspondant à la valeur binaire de self
        >>> Binaire603([0x01,0x02]).toNumber()
        258
        """
        n = 0
        for oc in self:
            n = n*256 + oc
        return n
    
    def fromNumber(n):
        """ Renvoie un Binaire603 correspondant à l'entier n
        >>> Binaire603.fromNumber(258)
        Binaire603([ 0x01, 0x02])
        """
        b = Binaire603("")
        while n > 0:
            b.ajouteOctet(n % 256)
            n //= 256
        b.reverse()
        return b
        



    def nbOctets(val):
        """Renvoie le nb d'octets nécessaire pour coder l'entier val
        >>> Binaire603.nbOctets(12)
        1
        >>> Binaire603.nbOctets(0)
        1
        >>> Binaire603.nbOctets(110000)
        3
        """
        if val==0:return 1
        return  int(log(val,256)+1)
    def ajouteLongueValeur(self,val):
        """Ajoute une valeur entière de taille qulconque de telle façon qu'elle
        puisse être récupérable par lisLongueValeur"""
        nbo=Binaire603.nbOctets(val)
        self.ajouteOctet(nbo) #Nb d 'octets de la longueur du fichier
        l=val
        for k in range(nbo):
            self.ajouteOctet(l%256)
            l=l//256
    def lisLongueValeur(self,pos):
        """Renvoie tout ce qu'il faut pour enregistrer/ajouter une valeur entière
        de taille qulconque"à la position pos
        Renvoie cette valeur et la nouvelle valeur de pos
        >>> monBin=Binaire603([12,13])
        >>> monBin.ajouteOctet(15)
        >>> monBin.ajouteLongueValeur(1000)
        >>> monBin.ajouteLongueValeur(100000)
        >>> pos=2
        >>> v0,pos=monBin.lisOctet(pos)
        >>> v1,pos=monBin.lisLongueValeur(pos)
        >>> v2,pos=monBin.lisLongueValeur(pos)
        >>> v0,v1,v2
        (15, 1000, 100000)
        """
        nbo=self[pos]
        pos+=1
        val=0
        for k in range(nbo):
            val+=self[pos]*256**k
            pos+=1
        return val,pos
    
    def __hash__(self):
        r = 0
        for b in self:
            r = r * 256 + b
        return r


    def demo():
        lb=Binaire603([1,2,3,3,3,3,4,8,8,128])
        lf=lb.lFrequences()
        print(lf[3])
        lb.afficheTableauDesFrequences()
        lb.afficheTableauDesFrequencesDecroissantes()
        lb.afficheHistogrammeDesFrequences()

    def demoEntropie():
        for ext in ["txt","odt","pdf","py","odp","zip","jpg","png","pcx","bmp"]:

            print(f"L'entropie du fichier {'Exemple.'+ext} est de : {Binaire603.bin603DepuisFichier('Exemple.'+ext).entropie():1.3f}")

        for k in range(5):
            monBin=Binaire603.exBin603(num=k,taille=2000) #Bug de clé trop longue pour taille =100000
            print("Bin:",repr(monBin))
            monBin.affFreq()
    def demoLivres():
        for nf in ["Notre Dame de Paris","L Education sentimentale","Guerre et Paix"]:
            lb=Binaire603.bin603DepuisFichier("../" + nf + ".TXT")
            lb.afficheHistogrammeDesFrequences(titre="Fréquence des lettres dans "+nf)
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    Binaire603.demo()
    lb=Binaire603([1,2,3,3,3,3,4,8,8,128])
    lf=lb.lFrequences()
    Binaire603.demoLivres()
    #Binaire603.demoEntropie()
    print("Fin du test")

