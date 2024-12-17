import os
import time
from multiprocessing import Process
from threading import Thread

# Número de iterações e lista de testes principais
ITERACOES = 10**6
NUM_TESTES_POTENCIA_2 = [2**x for x in range(0, 10)]  # Potências de 2
NUM_TESTES_INTERVALO = [300, 400, 500, 512]  # Testes de 300 a 512

# Função para o cálculo CPU-bound
def calcular(iteracoes):
    total = 0
    for _ in range(iteracoes):
        total += 1

# Executar usando threads
def executar_threads(iteracoes, num_threads):
    threads = []
    for _ in range(num_threads):
        t = Thread(target=calcular, args=(iteracoes // num_threads,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

# Executar usando processos
def executar_processos(iteracoes, num_processos):
    processos = []
    for _ in range(num_processos):
        p = Process(target=calcular, args=(iteracoes // num_processos,))
        p.start()
        processos.append(p)
    for p in processos:
        p.join()

# Função para monitorar desempenho (tempo)
def monitorar_tempo(inicio, tipo, num):
    tempo_total = time.time() - inicio
    return tempo_total

# Testes incrementais entre valores
def testes_incrementais(intervalo_inicio, intervalo_fim, iteracoes):
    print("\nIniciando testes incrementais entre", intervalo_inicio, "e", intervalo_fim)
    resultados_incrementais = []

    for num in range(intervalo_inicio, intervalo_fim + 1):
        try:
            inicio = time.time()
            executar_processos(iteracoes, num)
            tempo_processos = time.time() - inicio
            resultados_incrementais.append((num, tempo_processos))
        except OSError as e:
            resultados_incrementais.append((num, "FALHA"))
            break  # Parar após a primeira falha

    return resultados_incrementais

# Função principal
def main():
    resultados_threads = []
    resultados_processos = []

    print("Iniciando testes...\n")

    # Testes com potências de 2
    print(f"{'Num Threads/Processos':<20} {'Tempo Threads (s)':<20} {'Tempo Processos (s)'}")
    print("-" * 60)

    for num in NUM_TESTES_POTENCIA_2:
        # Teste com threads
        inicio = time.time()
        executar_threads(ITERACOES, num)
        tempo_threads = monitorar_tempo(inicio, "Threads", num)

        # Teste com processos
        inicio = time.time()
        try:
            executar_processos(ITERACOES, num)
            tempo_processos = monitorar_tempo(inicio, "Processos", num)
        except OSError as e:
            tempo_processos = float('inf')

        resultados_threads.append(tempo_threads)
        resultados_processos.append(tempo_processos)

        print(f"{num:<20} {tempo_threads:<20.2f} {tempo_processos:<20.2f}")
    
    # Testes de 300 a 512 (intervalo de 100 em 100)
    print("\nTestes de 300 a 512:")
    print(f"{'Num Threads/Processos':<20} {'Tempo Threads (s)':<20} {'Tempo Processos (s)'}")
    print("-" * 60)

    for num in range(300, 600, 100):
        # Teste com threads
        inicio = time.time()
        executar_threads(ITERACOES, num)
        tempo_threads = monitorar_tempo(inicio, "Threads", num)

        # Teste com processos
        inicio = time.time()
        try:
            executar_processos(ITERACOES, num)
            tempo_processos = monitorar_tempo(inicio, "Processos", num)
        except OSError as e:
            tempo_processos = float('inf')

        resultados_threads.append(tempo_threads)
        resultados_processos.append(tempo_processos)

        print(f"{num:<20} {tempo_threads:<20.2f} {tempo_processos:<20.2f}")

    # Testes incrementais entre 500 e 512
    resultados_incrementais = testes_incrementais(500, 512, ITERACOES)

    print("\nResultados incrementais entre 500 e 512:")
    print(f"{'Num Threads/Processos':<20} {'Tempo Processos (s)'}")
    print("-" * 60)

    for num, tempo in resultados_incrementais:
        print(f"{num:<20} {tempo}")

    # Salvar resultados em arquivo
    with open("resultados.saida", "w") as f:
        f.write(f"{'Num Threads/Processos':<20} {'Tempo Threads (s)':<20} {'Tempo Processos (s)'}\n")
        f.write("-" * 60 + "\n")
        for i, num in enumerate(NUM_TESTES_POTENCIA_2 + [300, 400, 500, 512]):
            f.write(f"{num:<20} {resultados_threads[i]:<20.2f} {resultados_processos[i]:<20.2f}\n")

        f.write("\nResultados incrementais entre 500 e 512:\n")
        for num, tempo in resultados_incrementais:
            f.write(f"{num:<20} {tempo:<20}\n")

    print("\nResultados salvos em 'resultados.saida'.")

if __name__ == "__main__":
    main()
