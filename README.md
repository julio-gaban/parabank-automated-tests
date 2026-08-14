# 🏦 ParaBank Automated Testing Framework

Este projeto é uma suíte completa de testes automatizados para a aplicação **ParaBank**, desenvolvida utilizando **Python**, **Behave (BDD)**, **Selenium WebDriver** para interação com o navegador e relatórios dinâmicos com **Allure Framework**.

---

## 📌 Funcionalidades Cobertas

- 🔐 **Autenticação (Login):** Cenários felizes, credenciais inválidas e casos de limite.
- 📝 **Registro de Usuários:** Cadastro com dados dinâmicos (timestamp), campos obrigatórios e validações de erro inline.
- 💸 **Transferência de Fundos:** Fluxos positivos, transferência com saldo insuficiente, contas iguais e entradas de dados inválidas.
- 📸 **Evidências Automáticas:** Captura de screenshot automática e inclusão no Allure quando ocorre falha em qualquer cenário.

---

## 🛠️ Pré-requisitos

Antes de iniciar, certifique-se de ter os seguintes softwares instalados no seu ambiente:

1. **Python 3.10+** (adicionado ao PATH do sistema).
2. **Google Chrome** instalado.
3. **Java Development Kit (JDK 8 ou superior)** — *Necessário para o Allure compilar e abrir o relatório no navegador*.

---

## 🚀 Instalação e Configuração

1. **Clone ou baixe o repositório:**
   ```cmd
   git clone https://github.com/julio-gaban/parabank-automated-tests.git
   cd parabank-automated-tests

## 1. Crie e ative um ambiente virtual (Recomendado):

# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate   

## 2. Instale as dependências do projeto:
pip install -r requirements.txt

## 📂 Estrutura do Projeto:

```text
├── features/
│   ├── login.feature         # Cenários de BDD para Login
│   ├── register.feature      # Cenários de BDD para Cadastro
│   ├── transfer.feature      # Cenários de BDD para Transferências
│   ├── steps/                # Implementação dos Steps em Python
│   │   ├── login_steps.py
│   │   ├── register_steps.py
│   │   └── transfer_steps.py
│   └── environment.py        # Hooks do Behave (Before/After Scenario)
├── .gitignore                # Arquivos ignorados pelo Git
├── requirements.txt          # Dependências do projeto
└── README.md                 # Documentação do projeto
```

## 🧪 Como Executar os Testes

# 1. Limpeza de Resultados Anteriores (Opcional)
Se desejar limpar os resultados de execuções passadas antes de rodar novos testes:

# Windows (CMD):
if exist allure-results rmdir /s /q allure-results
if exist allure-report rmdir /s /q allure-report

# Linux / Mac / PowerShell:
rm -rf allure-results allure-report

# 2. Executando a Suíte com Gerador de Relatório

# Para executar todos os cenários BDD e salvar as evidências na pasta allure-results:

behave -f allure_behave.formatter:AllureFormatter -o allure-results features/

# Para rodar apenas uma feature específica (ex: Transferência):

behave -f allure_behave.formatter:AllureFormatter -o allure-results features/transfer.feature

## 📊 Visualizando o Relatório Allure

Após a execução dos testes, utilize a instalação local do Allure para abrir o painel de relatórios interativo com screenshots e gráficos:

allure-2.45.0\bin\allure.bat serve allure-results

(O comando acima criará um servidor HTTP local e abrirá o relatório automaticamente no seu navegador padrão).

## Evidências da execução dos testes

# Overview do report do Allure:
<img width="1904" height="918" alt="image" src="https://github.com/user-attachments/assets/39a1ad21-a5ea-4ff1-b47d-29331342d262" />

# Erros encontrados nos testes divididos por categorias no report (no caso product defects):
<img width="1902" height="911" alt="image" src="https://github.com/user-attachments/assets/5f11363e-f349-4cdc-9caf-c81e9c7cb014" />

# Suítes de teste com seus respectivos cenários de teste (exemplo de cenário de sucesso):
<img width="1909" height="917" alt="image" src="https://github.com/user-attachments/assets/35bb9b68-7e3d-4e96-b993-ad893c5dce61" />

# Suítes de teste com seus respectivos cenários de teste (exemplo de cenário de falha):
<img width="1900" height="911" alt="image" src="https://github.com/user-attachments/assets/b35b0418-0988-4837-900d-d8a9ff19f92c" />

#Exemplo de screenshot gerado pelo Allure quando um erro ocorre:
<img width="1894" height="917" alt="image" src="https://github.com/user-attachments/assets/9be8fb95-60b7-40c4-8829-724be4de5453" />
<img width="1904" height="909" alt="image" src="https://github.com/user-attachments/assets/86c86e85-fce2-4e41-a877-d6d9e77b8805" />

#Casos de teste separados por cada arquivo de feature ou behavior:
<img width="1904" height="913" alt="image" src="https://github.com/user-attachments/assets/7635a752-f7da-4461-bed8-aa7dd3107055" />

# Gráficos gerados pelo Allure exibindo os status dos testes, duração dos mesmos e a severidade dos erros encontrados:
<img width="1883" height="914" alt="image" src="https://github.com/user-attachments/assets/335a84c1-911b-4781-84af-d66fe513caca" />

# Gráfico da duração dos testes na timeline de sua execução:
<img width="1908" height="906" alt="image" src="https://github.com/user-attachments/assets/3451b574-06d9-4356-bff7-ea616ff34471" />







