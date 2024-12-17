import os
import time
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
        total += 1

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
def monitorar_tempo(inicio):
    return time.time() - inicio

# Função para formatar e imprimir resultados de forma padronizada
def imprimir_tabela(header, resultados, colunas):
    print(f"\n{header}")
    print(f"{'Num Threads/Processos':<25} {'Tempo Threads (s)':<25} {'Tempo Processos (s)':<25}" if colunas == 3 else
          f"{'Num Threads/Processos':<25} {'Tempo Processos (s)':<25}")
    print("-" * (60 if colunas == 3 else 40))

    for resultado in resultados:
        num, *tempos = resultado
        tempos_formatados = [f"{tempo:.4f}" if isinstance(tempo, (float, int)) else "FALHA" for tempo in tempos]
        print(f"{num:<25} {' '.join(f'{t:<25}' for t in tempos_formatados)}")

# Testes incrementais entre valores
def testes_incrementais(intervalo_inicio, intervalo_fim, iteracoes):
    resultados_incrementais = []

    for num in range(intervalo_inicio, intervalo_fim + 1):
        try:
            inicio = time.time()
            executar_processos(iteracoes, num)
            tempo_processos = time.time() - inicio
            resultados_incrementais.append((num, tempo_processos))
        except OSError:
            resultados_incrementais.append((num, "FALHA"))
            break  # Parar após a primeira falha

    return resultados_incrementais

# Função principal
def main():
    resultados_threads = []
    resultados_processos = []
    resultados_incrementais = []

    print("Iniciando testes...\n")

    ################## Potencia de 2 ##################
    for num in NUM_TESTES_POTENCIA_2:
        try:
            # Teste com threads
            inicio = time.time()
            executar_threads(ITERACOES, num)
            tempo_threads = monitorar_tempo(inicio)

            # Teste com processos
            inicio = time.time()
            executar_processos(ITERACOES, num)
            tempo_processos = monitorar_tempo(inicio)
        except OSError:
            tempo_processos = "FALHA"

        resultados_threads.append((num, tempo_threads, tempo_processos))

    imprimir_tabela("Testes com potências de 2:", resultados_threads, colunas=3)

    ################## De 300 a 1000 ##################
    for num in NUM_SEQUENCIA:
        try:
            inicio = time.time()
            executar_threads(ITERACOES, num)
            tempo_threads = monitorar_tempo(inicio)

            inicio = time.time()
            executar_processos(ITERACOES, num)
            tempo_processos = monitorar_tempo(inicio)
        except OSError:
            tempo_processos = "FALHA"

        resultados_processos.append((num, tempo_threads, tempo_processos))

    imprimir_tabela("Testes de 300 a 1000:", resultados_processos, colunas=3)

    ################## Onde processos falha ##################
    resultados_incrementais = testes_incrementais(500, 512, ITERACOES)
    imprimir_tabela("Resultados incrementais entre 500 e 512:", resultados_incrementais, colunas=2)

    ################## Salvar resultados em arquivo ##################
    with open("resultados.saida", "w") as f:
        f.write("Testes com potências de 2:\n")
        f.write(f"{'Num Threads/Processos':<25} {'Tempo Threads (s)':<25} {'Tempo Processos (s)':<25}\n")
        f.write("-" * 60 + "\n")
        for resultado in resultados_threads:
            num, *tempos = resultado
            tempos_formatados = [f"{tempo:.4f}" if isinstance(tempo, (float, int)) else "FALHA" for tempo in tempos]
            f.write(f"{num:<25} {' '.join(f'{t:<25}' for t in tempos_formatados)}\n")

        f.write("\nTestes de 300 a 512:\n")
        f.write(f"{'Num Threads/Processos':<25} {'Tempo Threads (s)':<25} {'Tempo Processos (s)':<25}\n")
        f.write("-" * 60 + "\n")
        for resultado in resultados_processos:
            num, *tempos = resultado
            tempos_formatados = [f"{tempo:.4f}" if isinstance(tempo, (float, int)) else "FALHA" for tempo in tempos]
            f.write(f"{num:<25} {' '.join(f'{t:<25}' for t in tempos_formatados)}\n")

        f.write("\nResultados incrementais entre 500 e 512:\n")
        f.write(f"{'Num Threads/Processos':<25} {'Tempo Processos (s)':<25}\n")
        f.write("-" * 40 + "\n")
        for resultado in resultados_incrementais:
            num, tempo = resultado
            tempo_formatado = f"{tempo:.4f}" if isinstance(tempo, (float, int)) else "FALHA"
            f.write(f"{num:<25} {tempo_formatado:<25}\n")

    print("\nResultados salvos em 'resultados.saida'.")

if __name__ == "__main__":
    main()
