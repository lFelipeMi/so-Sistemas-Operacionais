# Comparação de Eficiência: Processos vs Threads

Este repositório contém o código e a documentação para a análise comparativa de desempenho entre **Processos** e **Threads** em operações CPU-bound. O estudo foi realizado como parte da disciplina de **Sistemas Operacionais** do 5º semestre do curso de Engenharia de Computação no **Instituto Federal de Mato Grosso do Sul - Campus Três Lagoas**.

## Participantes
* **Cleiton Guilhermite** - [GitHub](https://github.com/Draky-Rollgard)
* **Leonardo Araújo** - [GitHub](https://github.com/LeoAboard)
* **Stefany Silva** - [GitHub](https://github.com/stefanytk)
* **Luiz F. Miranda** - [GitHub](https://github.com/lfelipemi)

## Objetivo do Projeto

Este projeto visa identificar as circunstâncias em que o uso de threads ou processos apresenta maior eficiência no contexto de tarefas intensivas em CPU, como o cálculo de fatoriais. Ele também avalia o impacto do **Global Interpreter Lock (GIL)** do Python e a sobrecarga associada ao gerenciamento de processos e threads.

## Estrutura do Repositório

- [Código de implementação](./threadsXprocessos.py): Script em Python responsável por executar os testes de desempenho com threads e processos.
- [Documentação](./ProcessosXThreads.pdf): Detalhes técnicos, metodologia e resultados da análise comparativa.
- [Slides de apresentação](./Apresentação%20-%20Threads%20e%20Processos.pdf): Resumo visual do projeto utilizado para apresentação.

## Metodologia

1. **Cenário de Teste**:
   - Número de iterações: \(10^6\)
   - Tipos de teste:
     - Potências de 2 (1, 2, 4, ..., 512 threads/processos).
     - Valores incrementais (300 a 1000 threads/processos).
     - Testes detalhados entre 500 e 512 processos.

2. **Ambientes Utilizados**:
   - **Dispositivo 1**:
     - **Modelo**: Acer Nitro AN515-55
     - **Processador**: Intel Core i5-10300H
     - **Sistema Operacional**: Windows 11
   - **Dispositivo 2**:
     - **Modelo**: Samsung Book
     - **Processador**: Intel Core i3 11ª geração
     - **Sistema Operacional**: Debian Linux

3. **Ferramentas**:
   - **Linguagem**: Python
   - **Bibliotecas**: `threading`, `multiprocessing`, `math`, `time`

## Resultados

- **Threads**:
  - Mantiveram desempenho mais estável devido ao compartilhamento de memória e às limitações impostas pelo GIL.
- **Processos**:
  - Apresentaram desempenho competitivo inicialmente, mas perderam eficiência com o aumento do paralelismo devido ao custo de gerenciamento.

Para gráficos e análises detalhadas, consulte a [documentação](./ProcessosXThreads.pdf).

## Como Executar o Código

1. Certifique-se de ter o Python 3 instalado.
2. Clone o repositório:
   ```bash
   git clone https://github.com/lFelipeMi/so-Sistemas-Operacionais.git
   cd so-Sistemas-Operacionais.git
   ```
3. Execute o script:
   ```bash
   python threadsXprocessos.py
   ```
4. Verifique os resultados no terminal ou no arquivo gerado `resultados.saida`.

## Conclusão

O estudo confirmou que:
- Threads são mais eficientes em tarefas CPU-bound quando limitadas pelo GIL do Python.
- Processos são vantajosos apenas em pequenos números, mas perdem eficiência com alto paralelismo.

---

## Referências

- **Tanenbaum, A. S.** Sistemas Operacionais Modernos. 3ª edição. Pearson.
- **Beazley, David.** Understanding the Python GIL. PyCon 2010.
- Mais detalhes estão disponíveis na [documentação](./ProcessosXThreads.pdf).

---

## Licença

Este projeto é licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
