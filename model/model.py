import networkx as nx
from database.DAO import DAO
from itertools import combinations


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._nodes = []
        self.idMap = {}
        self._solBest = []
        self._votiBest = -1
        self._n = 0

    def buildGraph(self, anno, minimo):
        self._grafo.clear()
        self.idMap = {}

        self._nodes = DAO.getNodi(anno, minimo)
        for n in self._nodes:
            self.idMap[n.nome] = n

        self._grafo.add_nodes_from(self._nodes)

        for nomeC, nomeG in DAO.getCoppia(anno):
            if nomeC in self.idMap:
                self.idMap[nomeC].generi.add(nomeG)

        for c1, c2 in combinations(self._nodes, 2):
            peso = len(c1.generi & c2.generi)
            if peso > 0:
                self._grafo.add_edge(c1, c2, weight=peso)

    def getNodes(self):
        return sorted(self._nodes, key=lambda c: c.nome)

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    def getTop5(self):
        archi = []
        for u, v, dati in self._grafo.edges(data=True):
            nomi = sorted([str(u), str(v)])
            archi.append((nomi[0], nomi[1], dati["weight"]))
        archi.sort(key=lambda x: (-x[2], x[0], x[1]))
        return archi[:5]

    def getCasaSommaMax(self):
        peso = -1
        casa = None
        for n in self._grafo.nodes:
                p =  self._grafo.degree(n, weight="weight")
                if p > peso:
                    peso = p
                    casa = n
        return casa, peso

    def getPesiUno(self):
        count = 0
        for u,v,dati in  self._grafo.edges(data=True):
            if dati["weight"]==1:
                count += 1
        return count

    def getGradoMax(self):
        best = None
        for n in sorted(self._nodes, key=str):
            if best is None or self._grafo.degree(n) > self._grafo.degree(best):
                best = n
        return best, self._grafo.degree(best)

    def getPesoMax(self):
        best = None
        for n in sorted(self._nodes, key=str):
            if best is None or self._grafo.degree(n, weight="weight") > self._grafo.degree(best, weight="weight"):
                best = n
        return best, self._grafo.degree(best, weight="weight")

    def getComponenti(self):
        componenti = list(nx.connected_components(self._grafo))
        numero = len(componenti)
        piuGrande = 0
        for c in componenti:
            if len(c) > piuGrande:
                piuGrande = len(c)
        return numero, piuGrande

    def getTopArchi(self):
        archi = []
        for u, v, dati in self._grafo.edges(data=True):
            nomi = sorted([str(u), str(v)])
            archi.append((nomi[0], nomi[1], dati["weight"]))
        archi.sort(key=lambda x: (-x[2], x[0], x[1]))
        return archi[:3]

    def getAnni(self):
        return DAO.getAnni()


    def getGruppo(self,partenza,n):
        self._n = n
        self._solBest = []
        self._votiBest = -1
        self._ricorsione([partenza])
        return self._solBest, self._votiBest

    def _ricorsione(self,parziale):
        if len(parziale) == self._n :
            votoParziale = sum(casa.voti for casa in parziale )
            if votoParziale > self._votiBest:
                self._solBest = list(parziale)
                self._votiBest = votoParziale
            return

        for n in self._grafo.nodes:
            if n in parziale:
                continue
            if self._ammissibile(parziale,n):
                parziale.append(n)
                self._ricorsione(parziale)
                parziale.pop()


    def _ammissibile(self,parziale,n):
        adiacente = False
        for p in parziale:
            if self._grafo.has_edge(p,n):
                adiacente = True
                if self._grafo[p][n]["weight"] == 1:
                    return False
        return adiacente


"""
PUNTO 2
a. L'utente sceglie una casa di partenza da ddCasa e inserisce in txtN un intero positivo N.

b. Bottone "Trova Gruppo": con un algoritmo RICORSIVO trovare un gruppo di case tale che
   - il gruppo contiene ESATTAMENTE N case;
   - la PRIMA casa del gruppo è quella scelta dall'utente;
   - ogni casa aggiunta dopo la prima è ADIACENTE AD ALMENO UNA delle case già nel gruppo;
   - nel gruppo NON possono esserci due case collegate da un ARCO DI PESO 1;
   - tra tutti i gruppi ammissibili si sceglie quello che MASSIMIZZA LA SOMMA DEI VOTI
     (total_votes) dei film dell'anno prodotti dalle case del gruppo.

c. Stampare:
   - le case del gruppo in ORDINE ALFABETICO, ciascuna con numero di film e voti totali;
   - il numero di case del gruppo;
   - i voti complessivi della soluzione ottima.
   Messaggio se non esiste nessun gruppo valido.

VALORI DI CONTROLLO (M=4)
2019, partenza Netflix:
  N=2 -> 864617   (Columbia Pictures, Netflix)
  N=3 -> 1445605  (Columbia Pictures, Netflix, Walt Disney Pictures)
  N=4 -> 1985350  (+ Warner Bros.)
  N=5 -> 2488383  (+ BRON Studios)
2019, partenza A24:
  N=3 -> 1222289  (A24, Columbia Pictures, Warner Bros.)
  N=4 -> 1725322  (A24, BRON Studios, Columbia Pictures, Warner Bros.)
  -> Walt Disney Pictures NON può entrare: arco A24 - Disney ha peso 1
2018, partenza Netflix, N=3 -> 1735656 (Netflix, Paramount Pictures, Universal Pictures)
2017, partenza Netflix, N=3 -> 2979331 (Netflix, Twentieth Century Fox, Universal Pictures)

Voti delle case usate (2019): Columbia Pictures 594932, Walt Disney Pictures 580988,
Warner Bros. 539745, BRON Studios 503033, Netflix 269685, A24 87612
"""


