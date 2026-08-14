# language: en

# ==============================================================================
# MÓDULO DE AUTENTICAÇÃO (LOGIN) - PARABANK
# ------------------------------------------------------------------------------
# Este arquivo descreve os cenários de teste BDD para a funcionalidade de Login.
# Cobre desde o "Caminho Feliz" até validações de segurança (Injeção de Código),
# sensibilidade de caixa (Case Sensitivity) e campos obrigatórios.
# ==============================================================================

Feature: User Authentication in ParaBank
  As a registered ParaBank customer
  I want to log in with my credentials
  In order to safely access my bank account details

  # ----------------------------------------------------------------------------
  # PRÉ-CONDIÇÃO GLOBAL: Executada automaticamente antes de cada cenário
  # ----------------------------------------------------------------------------
  Background:
    Given the user accesses the ParaBank home page

  # ----------------------------------------------------------------------------
  # CAMINHO FELIZ (HAPPY PATH)
  # Valida se o acesso é concedido com credenciais válidas do sistema.
  # ----------------------------------------------------------------------------
  @validCredentials @smoke @regression
  Scenario: Successful login with valid credentials
    When the user enters username "john" and password "demo"
    And clicks the log in button
    Then the login should be successful displaying the "Accounts Overview" page

  # ----------------------------------------------------------------------------
  # MATRIZ DE EXCEÇÃO: CREDENCIAIS INVÁLIDAS E CAMPOS VAZIOS
  # Mapeia erros de negócio quando dados incorretos ou omitidos são fornecidos.
  # ----------------------------------------------------------------------------
  @invalidCredentials @negative
  Scenario Outline: Failed login with invalid or missing credentials
    When the user enters username "<username>" and password "<password>"
    And clicks the log in button
    Then the error message "<expected_error>" should be displayed

    Examples:
      # --- Usuário ou senha incorretos ---
      | username  | password  | expected_error                                 |
      | john      | wrongpass | The username and password could not be verified. |
      | wronguser | demo      | The username and password could not be verified. |
      | wronguser | wrongpass | The username and password could not be verified. |
      
      # --- Validações de campos obrigatórios (vazios) ---
      |           | demo      | Please enter a username and password.          |
      | john      |           | Please enter a username and password.          |
      |           |           | Please enter a username and password.          |

  # ----------------------------------------------------------------------------
  # SENSIBILIDADE DE CAIXA (CASE SENSITIVITY)
  # Garante que as credenciais do ParaBank respeitem letras maiúsculas/minúsculas.
  # ----------------------------------------------------------------------------
  @caseSensitivity @negative
  Scenario Outline: Failed login with case sensitivity variations
    When the user enters username "<username>" and password "<password>"
    And clicks the log in button
    Then the error message "The username and password could not be verified." should be displayed

    Examples:
      | username | password |
      | JOHN     | demo     |
      | john     | DEMO     |
      | JOHN     | DEMO     |

  # ----------------------------------------------------------------------------
  # TESTES DE SEGURANÇA E ROBUSTEZ (SECURITY & SANITIZATION)
  # Verifica o comportamento da aplicação contra payloads de SQL Injection e XSS.
  # A aplicação deve recusar o acesso e tratar os caracteres sem expor erros 500.
  # ----------------------------------------------------------------------------
  @specialCharacters @security @negative
  Scenario Outline: Failed login with special characters and SQL injection attempts
    When the user enters username "<username>" and password "<password>"
    And clicks the log in button
    Then the error message "The username and password could not be verified." should be displayed

    Examples:
      | username       | password     |
      | admin' --      | demo         |
      | ' OR '1'='1    | ' OR '1'='1  |
      | john<script>   | demo         |
      | john           | demo!@#$%^   |