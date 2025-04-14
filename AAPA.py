import numpy as np
import matplotlib.pyplot as plt
import random
from collections import deque

import numpy as np
import matplotlib.pyplot as plt
import random

# ------------------ FUNÇÕES DE AMBIENTE ------------------

def exibir(matriz):    
    global posAPAx, posAPAy
    plt.imshow(matriz, 'gray')
    plt.nipy_spectral() 
    plt.plot([posAPAy], [posAPAx], marker='o', color='r', ls='')
    plt.title("Ambiente do Agente")
    plt.show(block=False)
    plt.pause(0.5)    
    plt.clf()

def encontrar_sujeiras(matriz):
    sujeiras = []
    for i in range(1, 5):
        for j in range(1, 5):
            if matriz[i][j] == 2:
                sujeiras.append((i, j))
    return sujeiras

def calcular_distancia(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def encontrar_sujeira_mais_proxima(pos, sujeiras):
    if not sujeiras:
        return None
    return min(sujeiras, key=lambda x: calcular_distancia(pos, x))

def bfs_caminho(matriz, inicio, objetivo):
    direcoes = [(-1, 0, 'acima'), (1, 0, 'abaixo'), (0, -1, 'esquerda'), (0, 1, 'direita')]
    fila = deque()
    fila.append((inicio[0], inicio[1], []))
    visitados = set()
    visitados.add((inicio[0], inicio[1]))
    
    while fila:
        x, y, caminho = fila.popleft()
        
        if (x, y) == objetivo:
            return caminho
        
        for dx, dy, acao in direcoes:
            nx, ny = x + dx, y + dy
            if 1 <= nx <= 4 and 1 <= ny <= 4 and matriz[nx][ny] != 1 and (nx, ny) not in visitados:
                visitados.add((nx, ny))
                fila.append((nx, ny, caminho + [acao]))
    
    return []

def funcaoMapear():
    caminho = []
    for i in range(1, 5):
        linha = range(1, 5) if i % 2 != 0 else range(4, 0, -1)
        for j in linha:
            caminho.append((i, j))
    return caminho

# ------------------ INICIALIZAÇÃO DO AMBIENTE ------------------

N = 6  # matriz 6x6 com paredes
sala = np.ones((N, N), dtype=int)

for i in range(1, 5):
    for j in range(1, 5):
        sala[i][j] = 0

# Adicionando sujeira (2) aleatoriamente
for _ in range(random.randint(5, 10)):
    i, j = random.randint(1, 4), random.randint(1, 4)
    sala[i][j] = 2

# ------------------ AGENTE REATIVO SIMPLES ------------------

def agenteReativoSimples(percepcao):
    estado, (x, y) = percepcao
    if estado == 2:
        return 'aspirar'
    else:
        global caminho_agente
        if caminho_agente:
            prox = caminho_agente.pop(0)
            dx, dy = prox[0] - x, prox[1] - y
            if dx == 1:
                return 'abaixo'
            elif dx == -1:
                return 'acima'
            elif dy == 1:
                return 'direita'
            elif dy == -1:
                return 'esquerda'
        return 'NoOp'

# ------------------ AGENTE BASEADO EM OBJETIVO ------------------

def agenteObjetivo(percepcao):
    estado, (x, y) = percepcao
    global sala
    
    if estado == 2:
        return 'aspirar'
    
    sujeiras = encontrar_sujeiras(sala)
    if not sujeiras:
        return 'NoOp'
    
    sujeira_alvo = encontrar_sujeira_mais_proxima((x, y), sujeiras)
    caminho = bfs_caminho(sala, (x, y), sujeira_alvo)
    
    if caminho:
        return caminho[0]
    else:
        return 'NoOp'

# ------------------ EXECUÇÃO DO AGENTE REATIVO SIMPLES ------------------

print("==== AGENTE REATIVO SIMPLES ====")

# Inicializar posição e caminho
posAPAx, posAPAy = 1, 1
caminho_agente = funcaoMapear().copy()

while caminho_agente:
    percepcao = (sala[posAPAx][posAPAy], (posAPAx, posAPAy))
    acao = agenteReativoSimples(percepcao)
    print(f"Percepção: {percepcao[0]} Ação: {acao}")
    
    if acao == 'aspirar':
        sala[posAPAx][posAPAy] = 0
    elif acao == 'acima' and sala[posAPAx - 1][posAPAy] != 1:
        posAPAx -= 1
    elif acao == 'abaixo' and sala[posAPAx + 1][posAPAy] != 1:
        posAPAx += 1
    elif acao == 'esquerda' and sala[posAPAx][posAPAy - 1] != 1:
        posAPAy -= 1
    elif acao == 'direita' and sala[posAPAx][posAPAy + 1] != 1:
        posAPAy += 1

    exibir(sala)

# ------------------ ENCERRA PRIMEIRA EXECUÇÃO E LIMPA TELA ------------------

plt.close()  # Fecha janela do gráfico

input("\n[Enter] para iniciar o agente baseado em objetivo...")

# ------------------ REINICIALIZAÇÃO DO AMBIENTE ------------------

# Limpa o ambiente e garante pelo menos 5 sujeiras em posições diferentes
sala = np.ones((N, N), dtype=int)
for i in range(1, 5):
    for j in range(1, 5):
        sala[i][j] = 0

posicoes_validas = [(i, j) for i in range(1, 5) for j in range(1, 5)]
sujeira_nova = random.sample(posicoes_validas, k=5)
for i, j in sujeira_nova:
    sala[i][j] = 2

# Mostrar o estado inicial da sala
print("\nEstado inicial da sala para o agente baseado em objetivo:")
print(sala)
exibir(sala)

# ------------------ EXECUÇÃO DO AGENTE BASEADO EM OBJETIVO ------------------

print("\n==== AGENTE BASEADO EM OBJETIVO ====")

posAPAx, posAPAy = 1, 1
pontos = 0
iteracao = 1

while True:
    estado_atual = sala[posAPAx][posAPAy]
    percepcao = (estado_atual, (posAPAx, posAPAy))

    print(f"\nIteração {iteracao}:")
    print(f"Posição atual: ({posAPAx},{posAPAy})")
    print(f"Estado da célula: {estado_atual}")
    
    acao = agenteObjetivo(percepcao)
    print(f"Ação decidida: {acao}")

    if acao == 'aspirar':
        sala[posAPAx][posAPAy] = 0
        pontos += 10
        print("Sujeira removida!")
    elif acao == 'acima' and sala[posAPAx - 1][posAPAy] != 1:
        posAPAx -= 1
        pontos -= 1
    elif acao == 'abaixo' and sala[posAPAx + 1][posAPAy] != 1:
        posAPAx += 1
        pontos -= 1
    elif acao == 'esquerda' and sala[posAPAx][posAPAy - 1] != 1:
        posAPAy -= 1
        pontos -= 1
    elif acao == 'direita' and sala[posAPAx][posAPAy + 1] != 1:
        posAPAy += 1
        pontos -= 1
    elif acao == 'NoOp':
        if not encontrar_sujeiras(sala):
            print("Toda a sujeira foi removida! Missão cumprida.")
            break
        else:
            print("Não foi possível encontrar um caminho para a sujeira mais próxima.")
            break

    exibir(sala)
    iteracao += 1

plt.close()
print("\nPontos totais ->", pontos)