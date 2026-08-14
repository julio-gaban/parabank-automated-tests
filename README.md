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
   git clone <url-do-seu-repositorio>
   cd <nome-da-pasta-do-projeto>

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

├── allure-2.45.0/          # Executável e binários locais do Allure
├── features/
│   ├── environment.py      # Hooks do Behave (WebDriver, timeouts e screenshots)
│   ├── login.feature       # Cenários em Gherkin para Login
│   ├── register.feature    # Cenários em Gherkin para Registro
│   ├── transfer.feature    # Cenários em Gherkin para Transferência
│   └── steps/
│       ├── login_steps.py    # Definições de passos do Login
│       ├── register_steps.py # Definições de passos do Registro
│       └── transfer_steps.py # Definições de passos da Transferência
├── .gitignore              # Arquivos ignorados pelo Git
├── README.md               # Documentação do projeto
└── requirements.txt        # Dependências Python

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