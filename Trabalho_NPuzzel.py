'''
1° Atividade de IA
Equipe: 
    Rian Rodrigues Mourão
    Ruan Pablo de Sousa Estácio
'''

from heapq import heappop, heappush
from itertools import count
import random
from collections import deque
import time
import sys


class Metricas:
    def __init__(self) -> None:
        self.passos = 0
        self.inicio_tempo = 0
        self.tempo_execucao = None
        self.memoria = 0
        self.nos_expandidos = 0
        self.ciclos = 0
    
    def zerar_metricas(self):
        self.passos = 0
        self.inicio_tempo = 0
        self.tempo_execucao = None
        self.memoria = 0
        self.nos_expandidos = 0
        self.ciclos = 0

    def comecarCronometro(self):
        self.inicio_tempo = time.time()

    def finalizarCronometro(self):
        self.tempo_execucao = time.time() - self.inicio_tempo
    
    def atualizaMemoria(self, fila=0):
        self.memoria = max(self.memoria, sys.getsizeof(fila))

class Tabuleiro:
    def __init__(self) -> None:
        self.tabuleiro = None
        self.estado_meta = None

    def printarTabuleiro(self, tabuleiro):
        for i in tabuleiro:
            print(i)
    
    def clonarTabuleiro(self):
        nova_matriz = []
        for row in self.tabuleiro:
            nova_matriz.append(row[:])
        return nova_matriz
        
    def getPosicaoPecaVazia(self):
        for linha in range(len(self.tabuleiro)):
            for coluna in range(len(self.tabuleiro)):
                if self.tabuleiro[linha][coluna] == 0:
                    return linha, coluna

    def subir(self):
        pos_zero = self.getPosicaoPecaVazia()
        if pos_zero[0] > 0:
            tabuleiro = self.clonarTabuleiro()
            aux = tabuleiro[pos_zero[0] - 1][pos_zero[1]] 
            tabuleiro[pos_zero[0]][pos_zero[1]] = aux
            tabuleiro[pos_zero[0] - 1][pos_zero[1]] = 0

            return tabuleiro
        
    def descer(self):
        pos_zero = self.getPosicaoPecaVazia()
        if pos_zero[0] < (len(self.tabuleiro) - 1):
            tabuleiro = self.clonarTabuleiro()
            aux = tabuleiro[pos_zero[0] + 1][pos_zero[1]] 
            tabuleiro[pos_zero[0]][pos_zero[1]] = aux
            tabuleiro[pos_zero[0] + 1][pos_zero[1]] = 0

            return tabuleiro
            
    def direitar(self):
        pos_zero = self.getPosicaoPecaVazia()
        if pos_zero[1] < (len(self.tabuleiro) - 1):
            tabuleiro = self.clonarTabuleiro()
            aux = tabuleiro[pos_zero[0]][pos_zero[1] + 1] 
            tabuleiro[pos_zero[0]][pos_zero[1]] = aux
            tabuleiro[pos_zero[0]][pos_zero[1] + 1] = 0

            return tabuleiro


    def esquerdar(self):
        pos_zero = self.getPosicaoPecaVazia()
        if pos_zero[1] > 0:
            tabuleiro = self.clonarTabuleiro()
            aux = tabuleiro[pos_zero[0]][pos_zero[1] - 1] 
            tabuleiro[pos_zero[0]][pos_zero[1]] = aux
            tabuleiro[pos_zero[0]][pos_zero[1] - 1] = 0

            return tabuleiro

    def criarTabuleiro(self, tamanho_matriz: int):
        self.criarEstadoMeta(tamanho_matriz)
        self.tabuleiro = self.estado_meta
        for i in range(10000):
            ale = random.randint(1, 4)
            pos_zero = self.getPosicaoPecaVazia()
            if ale == 1 and pos_zero[0] > 0:
                self.tabuleiro = self.subir()
            if ale == 2 and (pos_zero[0] < (tamanho_matriz - 1)):
                self.tabuleiro = self.descer()
            if ale == 3 and (pos_zero[1] < (tamanho_matriz - 1)):
                self.tabuleiro = self.direitar()
            if ale == 4 and pos_zero[1] > 0:
                self.tabuleiro = self.esquerdar()
    
    def criarEstadoMeta(self, tamanho):
        estado_meta = []
        for linha in range(tamanho):
            linha_meta = []
            for coluna in range(tamanho):
                valor = linha * tamanho + coluna + 1
                if valor == tamanho * tamanho:
                    valor = 0
                linha_meta.append(valor)
            estado_meta.append(linha_meta)
        self.estado_meta = estado_meta


class No(Tabuleiro):
    def __init__(self):
        self.pai = None

    def movimentosPossiveis(self):
        movimentos = []
        linha, coluna = self.getPosicaoPecaVazia()
        tamanho_tabuleiro = len(self.tabuleiro)
        # Movimento para cima
        if linha > 0:
            nNo = No()
            nNo.pai = self
            nNo.estado_meta = self.estado_meta
            nNo.tabuleiro = self.subir()
            movimentos.append(nNo)

        # Movimento para baixo
        if linha < (tamanho_tabuleiro - 1):
            nNo = No()
            nNo.estado_meta = self.estado_meta
            nNo.pai = self
            nNo.tabuleiro = self.descer()
            movimentos.append(nNo)

        # Movimento para esquerda
        if coluna > 0:
            nNo = No()
            nNo.pai = self
            nNo.estado_meta = self.estado_meta
            nNo.tabuleiro = self.esquerdar()
            movimentos.append(nNo)

        # Movimento para direita
        if coluna < (tamanho_tabuleiro - 1):
            nNo = No()
            nNo.pai = self
            nNo.estado_meta = self.estado_meta
            nNo.tabuleiro = self.direitar()
            movimentos.append(nNo)
        return movimentos
    
    def passos(self):
        atual = self
        passos = [atual]
        
        while atual.pai is not None:
            atual = atual.pai
            passos.append(atual)
        
        passos.reverse()
        return passos

    def pecas_fora_do_lugar(no):
        pos_meta = {}
        tamanho = len(no.tabuleiro)
        fora = 0
        for i in range(tamanho):
            for j in range(tamanho):
                valor = no.estado_meta[i][j]
                pos_meta[valor] = (i, j)
        for i in range(tamanho):
            for j in range(tamanho):
                valor = no.tabuleiro[i][j]
                if pos_meta[valor] != (i, j):
                    fora += 1
        return fora


    def manhattan(no):
        posicao_meta = {}
        tamanho = len(no.tabuleiro)
        for x in range(tamanho):
            for y in range(tamanho):
                valor = no.estado_meta[x][y]
                posicao_meta[valor] = (x, y)

        distancia = 0
        for x1 in range(tamanho):
            for y1 in range(tamanho):
                valor = no.tabuleiro[x1][y1]
                if valor == 0:
                    continue
                x2, y2 = posicao_meta[valor]
                distancia += abs(x1 - x2) + abs(y1 - y2)
        
        return distancia

class BuscaEmLargura:
    def buscar(self, estado_inicial: No):
        metricas_BFS = Metricas()
        metricas_BFS.comecarCronometro() # metrica
        fila = deque() #fifo
        visitados = set()
        fila.append(estado_inicial)

        while len(fila) > 0:
            metricas_BFS.atualizaMemoria(fila) # metrica
            estado_atual = fila.popleft() 

            if estado_atual.tabuleiro == estado_atual.estado_meta:
                passos = estado_atual.passos()
                metricas_BFS.passos = len(passos)
                metricas_BFS.finalizarCronometro() # metrica
                return (metricas_BFS, passos)
            
            tabu_atual = tuple(map(tuple, estado_atual.tabuleiro))
            visitados.add(tabu_atual)
            movimentos = estado_atual.movimentosPossiveis()
            metricas_BFS.ciclos += 1 #metrica

            for movimento in movimentos:
                mov_tabu = tuple(map(tuple, movimento.tabuleiro))
                if mov_tabu not in visitados:
                    metricas_BFS.nos_expandidos += 1 #metrica
                    fila.append(movimento)   
        return None
    

class BuscaProfundidadeIterativa:
    def buscar(self, estado_inicial: No):
        metricas_IDS = Metricas()
        metricas_IDS.comecarCronometro() # metrica
        
        profundidade = 0

        while True:
            pilha = deque()
            vizinhos = set()
            pilha.append((0, estado_inicial))

            while len(pilha) > 0:
                metricas_IDS.atualizaMemoria(pilha) # metrica

                nponto, estado_atual = pilha.pop()

                if estado_atual.tabuleiro == estado_atual.estado_meta:
                    passos = estado_atual.passos()
                    metricas_IDS.passos = len(passos)
                    metricas_IDS.finalizarCronometro() # metrica
                    return (metricas_IDS, passos) 

                if nponto >= profundidade:
                    continue

                vizinhos.add(tuple(map(tuple, estado_atual.tabuleiro)))
                metricas_IDS.ciclos += 1 #metrica
                movimentos = estado_atual.movimentosPossiveis()

                for movimento in movimentos:
                    mov_tabu = tuple(map(tuple, movimento.tabuleiro))

                    if mov_tabu not in vizinhos:
                        pilha.append((nponto+1, movimento))
                        metricas_IDS.nos_expandidos += 1 #metrica

            profundidade += 1


class BuscaAstrela:
    def __init__(self, h, estado_inicial):
        self.heuristica = h
        self.estado = estado_inicial
   

    def buscar(self):
        metricas_A = Metricas()
        metricas_A.zerar_metricas()
        metricas_A.comecarCronometro()
        estado_inicial = self.estado

        fila = []
        heappush(fila, (0, id(estado_inicial), estado_inicial))

        tabu_tupla = tuple(map(tuple, estado_inicial.tabuleiro))
        g_pontos = { tabu_tupla: 0 }
        
        while fila:
            metricas_A.atualizaMemoria()
            
            ignora, _, estado_atual = heappop(fila)
        
            if estado_atual.tabuleiro == estado_atual.estado_meta:
                passos = estado_atual.passos()
                metricas_A.passos = len(passos)
                metricas_A.finalizarCronometro()
                return (metricas_A, passos)
                
            estado_atual_tupla = tuple(map(tuple, estado_atual.tabuleiro))
            
            metricas_A.ciclos += 1
            movimentos = estado_atual.movimentosPossiveis()

            for vizinho in movimentos:
                tentativa_g = g_pontos[estado_atual_tupla] + 1        
                tabu_vizinho_tupla = tuple(map(tuple, vizinho.tabuleiro))
                if tabu_vizinho_tupla not in g_pontos or tentativa_g < g_pontos[tabu_vizinho_tupla]:
                    metricas_A.nos_expandidos += 1
                
                    heappush(fila, (tentativa_g + self.heuristica(vizinho), id(vizinho), vizinho))
                    
                    g_pontos[tabu_vizinho_tupla] = tentativa_g



def mostrarResultado(tupla_busca):
    metricas, passos = tupla_busca
    if passos != 0:
        for i, estado in enumerate(passos):
            print(f"""
           {estado.tabuleiro[0]}
Passo {i:02d}:  {estado.tabuleiro[1]}
           {estado.tabuleiro[2]}""")
        
    print(f"""--------- Metricas calculadas ---------
Quantidade de passos:  {metricas.passos - 1}
Tempo:                 {metricas.tempo_execucao:.3f} segundos
Maximo de memoria:     {metricas.memoria} bytes
Nos expandidos:        {metricas.nos_expandidos}
Fator de ramificacao:  {metricas.nos_expandidos / metricas.ciclos if metricas.ciclos > 0 else 0:.2f}
""")

def mostrarPrevia(puzzel):
    print("Estado Atual | Estado Meta")
    for index, valor in enumerate(puzzel.tabuleiro):
        print(' ', valor, ' | ', puzzel.estado_meta[index])


puzzel = No()
puzzel.criarTabuleiro(4)
# puzzel.tabuleiro = [[5, 7, 0], [2, 1, 4], [8, 6, 3]] # Valor pra teste
# Init
mostrarPrevia(puzzel)

# EXEC
buscas = {
    'BFS' : BuscaEmLargura.buscar(BuscaEmLargura,puzzel),
    'IDS' : BuscaProfundidadeIterativa.buscar(BuscaProfundidadeIterativa, puzzel),
    'A* Pecas Fora' : BuscaAstrela(No.pecas_fora_do_lugar, puzzel).buscar(),
    'A* Manhattan' : BuscaAstrela(No.manhattan, puzzel).buscar()
}

metricas_geral = {}

for busca in buscas:
    print(f"---------- {busca} -----------")
    resultado = buscas[busca]
    if busca:
        mostrarResultado(resultado)
        metricas_geral[busca] = (resultado[0], 0)
    else:
        print("Nao foi possivel encontrar um resultado")
print('\n\n')
print('-------- GERAL --------\n')
for i in metricas_geral:
    print(f'\n{i}: ')
    mostrarResultado(metricas_geral[i])
