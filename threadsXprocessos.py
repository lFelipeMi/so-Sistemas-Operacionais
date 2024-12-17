import os
import time
from math import factorial
from multiprocessing import Process
from threading import Thread

# Número de iterações e lista de testes principais
ITERACOES = 10**6
NUM_TESTES_POTENCIA_2 = [2**x for x in range(0, 10)]  # Potências de 2
NUM_SEQUENCIA = [300, 400, 500, 600, 700, 800, 900, 1000]

# Função para o cálculo CPU-bound 
def calcular(iteracoes):
    total = 0
    for _ in range(iteracoes):
        total += factorial(10) * 2  

def executar_threads(iteracoes, num_threads):
    threads = []
    for _ in range(num_threads):
        t = Thread(target=calcular, args=(iteracoes // num_threads,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

def executar_processos(iteracoes, num_processos):
    processos = []
    for _ in range(num_processos):
        p = Process(target=calcular, args=(iteracoes // num_processos,))
        p.start()
        processos.append(p)
    for p in processos:
        p.join()

# Função para monitorar desempenho (tempo)
def monitorar_tempo():
    return time.perf_counter()

def imprimir_tabela(header, resultados, colunas):
    print(f"\n{header}")
    print(f"{'Num Threads/Processos':<25} {'Tempo Threads (s)':<25} {'Tempo Processos (s)':<25}" if colunas == 3 else
          f"{'Num Threads/Processos':<25} {'Tempo Processos (s)':<25}")
    print("-" * (60 if colunas == 3 else 40))

    for resultado in resultados:
        num, *tempos = resultado
        tempos_formatados = [f"{tempo:.4f}" if isinstance(tempo, (float, int)) else "FALHA" for tempo in tempos]
        print(f"{num:<25} {' '.join(f'{t:<25}' for t in tempos_formatados)}")

def executar_testes(lista_tamanhos, iteracoes, resultados):
    for num in lista_tamanhos:
        try:
            inicio = time.time()
            executar_threads(iteracoes, num)
            tempo_threads = time.time() - inicio

            inicio = time.time()
            executar_processos(iteracoes, num)
            tempo_processos = time.time() - inicio
        except OSError:
            tempo_processos = "FALHA"

        resultados.append((num, tempo_threads, tempo_processos))

# Testes incrementais entre valores
def testes_incrementais(intervalo_inicio, intervalo_fim, iteracoes):
    resultados_incrementais = []
    falhou = False

    for num in range(intervalo_inicio, intervalo_fim + 1):
        if falhou:
            resultados_incrementais.append((num, "FALHA"))
            continue

        try:
            inicio = monitorar_tempo()
            executar_processos(iteracoes, num)
            tempo_processos = monitorar_tempo() - inicio
            resultados_incrementais.append((num, tempo_processos))
        except OSError:
            resultados_incrementais.append((num, "FALHA"))
            falhou = True  # Interromper tentativas subsequentes

    return resultados_incrementais


# Função principal
def main():
    resultados_1 = []
    resultados_2 = []
    resultados_incrementais = []

    print("Iniciando testes...\n")

    executar_testes(NUM_TESTES_POTENCIA_2, ITERACOES, resultados_1)
    imprimir_tabela("Testes com potências de 2:", resultados_1, colunas=3)


    executar_testes(NUM_SEQUENCIA, ITERACOES, resultados_2)
    imprimir_tabela("Testes de 300 a 1000:", resultados_2, colunas=3)

    resultados_incrementais = testes_incrementais(500, 512, ITERACOES)
    imprimir_tabela("Resultados incrementais entre 500 e 512:", resultados_incrementais, colunas=2)


    ################## Salvar resultados em arquivo ##################
    with open("resultados.saida", "w") as f:
        f.write("Testes com potências de 2:\n")
        f.write(f"{'Num Threads/Processos':<25} {'Tempo Threads (s)':<25} {'Tempo Processos (s)':<25}\n")
        f.write("-" * 75 + "\n")
        for resultado in resultados_1:
            num, *tempos = resultado
            tempos_formatados = [f"{tempo:.4f}" if isinstance(tempo, (float, int)) else "FALHA" for tempo in tempos]
            f.write(f"{num:<25} {' '.join(f'{t:<25}' for t in tempos_formatados)}\n")

        f.write("\nTestes de 300 a 1000:\n")
        f.write(f"{'Num Threads/Processos':<25} {'Tempo Threads (s)':<25} {'Tempo Processos (s)':<25}\n")
        f.write("-" * 75 + "\n")
        for resultado in resultados_2:
            num, *tempos = resultado
            tempos_formatados = [f"{tempo:.4f}" if isinstance(tempo, (float, int)) else "FALHA" for tempo in tempos]
            f.write(f"{num:<25} {' '.join(f'{t:<25}' for t in tempos_formatados)}\n")

        f.write("\nResultados incrementais entre 500 e 512:\n")
        f.write(f"{'Num Threads/Processos':<25} {'Tempo Processos (s)':<25}\n")
        f.write("-" * 50 + "\n")
        for resultado in resultados_incrementais:
            num, tempo = resultado
            tempo_formatado = f"{tempo:.4f}" if isinstance(tempo, (float, int)) else "FALHA"
            f.write(f"{num:<25} {tempo_formatado:<25}\n")

    print("\nResultados salvos em 'resultados.saida'.")

if __name__ == "__main__":
    main()
