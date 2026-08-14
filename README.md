Markdown
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

### 1. Clone ou baixe o repositório:
```bash
git clone [https://github.com/julio-gaban/parabank-automated-tests.git](https://github.com/julio-gaban/parabank-automated-tests.git)
cd parabank-automated-tests
```
### 2. Crie e ative um ambiente virtual (Recomendado):

#### Windows:

**DOS**
```bash
python -m venv venv
.\venv\Scripts\activate.bat
```

#### Linux / Mac:

**Bash**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências do projeto:

#### Bash
```bash
pip install -r requirements.txt
```

(Ou instale individualmente):

#### Bash
```bash
pip install behave selenium webdriver-manager allure-behave
```

📂 Estrutura do Projeto

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

## 🧪 Como Executar os Testes gerando o Relatório de Testes nativo do Behave
Se desejar executar todos os testes da suíte:
```bash
behave
```
Se desejar executar um arquivo de feature em específico:
```bash
# Executar apenas os testes de login
behave features/login.feature

# Executar apenas os testes de cadastro
behave features/register.feature

# Executar apenas os testes de transferência
behave features/transfer.feature
```
Se desejar executar um ou mais cenários de uma tag específica:
```bash
behave --tags=@[tag_do_cenario]
```

### Gerando o relatório simples em HTML

Instale o formatador:
```bash
pip install behave-html-formatter
```
Execute gerando o arquivo HTML:
```bash
behave -f html -o report.html
```
### Gerando o relatório no Formato JUnit (XML)
Opção útil para integração contínua (CI/CD) em pipelines como GitHub Actions, Jenkins ou Azure DevOps:
```bash
behave --junit --junit-directory reports_junit
```

## 🧪 Como Executar os Testes gerando o Relatório de Testes com o Allure

### Obter versão mais recente do Allure
```text
O Allure Framework foi integrado ao projeto para fornecer relatórios de execução claros e detalhados. Ele gera um dashboard web interativo que exibe o histórico de testes, tempo de execução, severidade das falhas e captura automática de screenshots no exato momento de um erro, facilitando a triagem de bugs por desenvolvedores e QAs.

Faça o o download da versão mais recente do Allure no link: https://github.com/allure-framework/allure2/releases
Extraia a pasta do arquivo baixado
Copie e cole a pasta do Allure na pasta raiz do projeto
```

Ou para o Windows, o Allure está disponível através do instalador de linha de comando do Scoop. Para instalar o Allure, baixe e instale o Scoop e execute o seguinte comando no PowerShell:
```bash
scoop install allure
```

Ou no Linux/MacOS, utilizando o Homebrew:
```bash
$ brew install allure
```
### 1. Limpeza de Resultados Anteriores (Opcional)
Se desejar limpar os resultados de execuções passadas antes de rodar novos testes:

#### Windows (CMD):

**DOS**

```bash
if exist allure-results rmdir /s /q allure-results
if exist allure-report rmdir /s /q allure-report
```

#### Linux / Mac / PowerShell:

**Bash**
```bash
rm -rf allure-results allure-report
```

### 2. Executando a Suíte com Gerador de Relatório

Para executar todos os cenários BDD e salvar as evidências:

**Bash**
```bash
behave -f allure_behave.formatter:AllureFormatter -o allure-results features/
```

Para rodar apenas uma feature específica (ex: Transferência):

**Bash** 
```bash
behave -f allure_behave.formatter:AllureFormatter -o allure-results features/transfer.feature
```

Para rodar cenários por Tag específica:

**Bash**
```bash
behave -f allure_behave.formatter:AllureFormatter -o allure-results --tags=@tag_do_cenario
```

### 📊 Visualizando o Relatório Allure
Após a execução dos testes, utilize o Allure para abrir o painel de relatórios interativo com screenshots e gráficos:

**DOS**
```bash
allure-2.45.0\bin\allure.bat serve allure-results
```

(O comando acima criará um servidor HTTP local e abrirá o relatório automaticamente no seu navegador padrão).

## 📸 Evidências da Execução dos Testes

### 📈 Overview do Report no Allure
<img width="1904" height="918" alt="image" src="https://github.com/user-attachments/assets/39a1ad21-a5ea-4ff1-b47d-29331342d262" />

### ❌ Erros Encontrados Divididos por Categoria (Product Defects)
<img width="1902" height="911" alt="image" src="https://github.com/user-attachments/assets/5f11363e-f349-4cdc-9caf-c81e9c7cb014" />

### ✅ Suítes de Teste - Exemplo de Cenário de Sucesso
<img width="1909" height="917" alt="image" src="https://github.com/user-attachments/assets/35bb9b68-7e3d-4e96-b993-ad893c5dce61" />

### ⚠️ Suítes de Teste - Exemplo de Cenário de Falha
<img width="1900" height="911" alt="image" src="https://github.com/user-attachments/assets/b35b0418-0988-4837-900d-d8a9ff19f92c" />

### 🖼️ Screenshots Automáticos Anexados no Allure em Caso de Erro
<img width="1894" height="917" alt="image" src="https://github.com/user-attachments/assets/9be8fb95-60b7-40c4-8829-724be4de5453" />
<img width="1904" height="909" alt="image" src="https://github.com/user-attachments/assets/86c86e85-fce2-4e41-a877-d6d9e77b8805" />

### 📑 Casos de Teste Separados por Feature/Behavior
<img width="1904" height="913" alt="image" src="https://github.com/user-attachments/assets/7635a752-f7da-4461-bed8-aa7dd3107055" />

### 📊 Gráficos de Status, Duração e Severidade
<img width="1883" height="914" alt="image" src="https://github.com/user-attachments/assets/335a84c1-911b-4781-84af-d66fe513caca" />

### ⏱️ Timeline da Duração dos Testes
<img width="1908" height="906" alt="image" src="https://github.com/user-attachments/assets/3451b574-06d9-4356-bff7-ea616ff34471" />
