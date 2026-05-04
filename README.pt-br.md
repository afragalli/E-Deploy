# e-deploy

Este projeto contém uma coleção de funções utilitárias que resolvem diferentes problemas de programação do arquivo "Atividade Técnica-2026.txt"

## Estrutura do Projeto

```
e-deploy/
├── answer_1.py          # Verificação de padrão em strings
├── answer_2.py          # Cálculo de progressão aritmética
├── answer_3.py          # Análise de jogo de tabuleiro
├── answer_4.py          # Cálculo de benefícios de rescisão trabalhista
├── constants/
│   └── errors.py        # Constantes de mensagens de erro
├── tests/               # Testes automatizados
└── README.md           # Este arquivo
```

## Descrição dos Arquivos

### `answer_1.py`
- **Função Principal**: `check_b_a_pattern(text: str) -> bool`
- **Descrição**: Verifica se uma string começa com a letra 'B' e termina com a letra 'A'
- **Características**: 
  - Verificação case-sensitive
  - Retorna `True` se a string atender aos critérios, `False` caso contrário

### `answer_2.py`
- **Função Principal**: `get_sequence_value(position: int) -> int`
- **Descrição**: Calcula o valor de uma posição específica em uma progressão aritmética
- **Detalhes**:
  - Sequência: (11, 18, 25, 32, 39...)
  - Termo inicial: 11
  - Razão: 7
  - Fórmula: `a_n = a1 + (position - 1) * r`
  - Posição é 1-indexed (começa em 1)
  - Validação para posições menores que 1

### `answer_3.py`
- **Função Principal**: `analyze_board_game(num_positions: int) -> GameStatistics`
- **Descrição**: Analisa estatísticas de um jogo de tabuleiro unidirecional
- **Funcionalidades**:
  - Calcula o número mínimo de turnos para alcançar a última posição
  - Determina a probabilidade ótima de alcançar a última posição no mínimo de turnos
  - Contabiliza o número total de combinações sem looping
  - Movimentos permitidos: saltos de 1, 2 ou 3 posições
  - Validação para tabuleiros com menos de 3 posições
- **Classe de Retorno**: `GameStatistics` com `min_turns`, `optimal_probability` e `combinations_without_looping`

### `answer_4.py`
- **Função Principal**: `calculate_termination_benefits(hire_date, termination_date, salary) -> TerminationBenefits`
- **Descrição**: Calcula benefícios proporcionais de rescisão contratual segundo a legislação trabalhista brasileira
- **Benefícios Calculados**:
  - **Férias Proporcionais**: Incluem o terço constitucional
  - **13º Salário Proporcional**: Baseado nos meses trabalhados no ano corrente
- **Regras Implementadas**:
  - Mês conta como completo se 15+ dias foram trabalhados
  - Férias calculadas desde o último aniversário de contratação
  - 13º salário calculado desde 1º de janeiro ou data de contratação
  - Validação de datas e salário positivo
- **Classe de Retorno**: `TerminationBenefits` com valores de férias e 13º salário, ambos arredondados para 2 casas decimais

### `constants/errors.py`
Contém constantes de mensagens de erro utilizadas em todo o projeto.

## Como Executar os Testes

Este projeto utiliza o framework **pytest** para testes automatizados.

### Pré-requisitos
- Python 3.8+
- pytest instalado

### Instalação do pytest
```bash
pip install pytest
```

### Executando todos os testes
Execute no diretório raiz:

```bash
pytest
```

### Executando testes específicos
- **Teste do answer_1.py**:
  ```bash
  pytest tests/answer_1_test.py
  ```

- **Teste do answer_2.py**:
  ```bash
  pytest tests/answer_2_test.py
  ```

- **Teste do answer_3.py**:
  ```bash
  pytest tests/answer_3_test.py
  ```

- **Teste do answer_4.py**:
  ```bash
  pytest tests/answer_4_test.py
  ```

### Estrutura dos Testes
Cada arquivo de teste segue a convenção `answer_X_test.py` e contém testes unitários abrangentes para as respectivas funções, incluindo:
- Testes de casos normais
- Testes de casos limite
- Testes de validação de entrada
- Testes de exceções

Os testes garantem a qualidade e robustez das implementações, verificando o comportamento esperado em diversas situações.
