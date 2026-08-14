# language: en

# ==============================================================================
# MÓDULO DE CADASTRO DE USUÁRIOS (REGISTRATION) - PARABANK
# ------------------------------------------------------------------------------
# Este arquivo descreve os cenários de teste BDD para a criação de novas contas.
# Cobertura funcional:
#   - Criação de conta com dados dinâmicos (Caminho Feliz).
#   - Regras de negócio de duplicação de usuário e confirmação de senha.
#   - Validação inline de campos obrigatórios e formatos de dados.
#   - Testes de resiliência e segurança (Injeção de código/SQL).
# ==============================================================================

Feature: User Registration in ParaBank
  As a new ParaBank customer
  I want to create an account
  In order to start using online banking services

  # ----------------------------------------------------------------------------
  # PRÉ-CONDIÇÃO GLOBAL: Executada automaticamente antes de cada cenário
  # ----------------------------------------------------------------------------
  Background:
    Given the user accesses the ParaBank registration page

  # ----------------------------------------------------------------------------
  # CAMINHO FELIZ (HAPPY PATH)
  # Utiliza geração de dados dinâmicos (timestamp) no step para garantir
  # que a conta seja criada com um username inédito em cada execução.
  # ----------------------------------------------------------------------------
  @validData @smoke @regression
  Scenario: Successful user registration with valid dynamic data
    When the user fills in all required registration fields with valid data
    And submits the registration form
    Then the account creation should be successful displaying a welcome message

  # ----------------------------------------------------------------------------
  # REGRA DE NEGÓCIO: UNICIDADE DE USERNAME
  # Valida o bloqueio de cadastro quando o nome de usuário já está em uso.
  # ----------------------------------------------------------------------------
  @existingUsername @negative
  Scenario: Failed registration when username already exists
    When the user fills in the registration form using an existing username "john"
    And submits the registration form
    Then the error message "This username already exists." should be displayed on registration

  # ----------------------------------------------------------------------------
  # REGRA DE NEGÓCIO: DIVERGÊNCIA DE SENHAS
  # Garante que a confirmação de senha seja idêntica à senha informada,
  # incluindo validação de sensibilidade de caixa (Case Sensitivity).
  # ----------------------------------------------------------------------------
  @passwordMismatch @negative
  Scenario Outline: Failed registration with password confirmation mismatch
    When the user enters password "<password>" and confirm password "<confirm_password>"
    And fills in all other required registration fields with valid data
    And submits the registration form
    Then the field error message "Passwords did not match." should be displayed

    Examples:
      | password  | confirm_password |
      | secret123 | secret456        |
      | Pass123!  | pass123!         |
      | demo      | DEMO             |

  # ----------------------------------------------------------------------------
  # VALIDAÇÃO DE CAMPOS OBRIGATÓRIOS (INLINE ERRORS)
  # Mapeia a obrigatoriedade de cada um dos campos do formulário de registro.
  # ----------------------------------------------------------------------------
  @missingFields @negative
  Scenario Outline: Failed registration with missing mandatory fields
    When the user leaves mandatory field "<field_name>" empty
    And submits the registration form
    Then the field error message "<expected_error>" should be displayed

    Examples:
      | field_name       | expected_error                     |
      | First Name       | First name is required.            |
      | Last Name        | Last name is required.             |
      | Address          | Address is required.               |
      | City             | City is required.                  |
      | State            | State is required.                 |
      | Zip Code         | Zip code is required.              |
      | SSN              | Social Security Number is required.|
      | Username         | Username is required.              |
      | Password         | Password is required.              |
      | Confirm Password | Password confirmation is required. |

  # ----------------------------------------------------------------------------
  # VALIDAÇÃO DE FORMATOS E TIPOS DE DADOS
  # Garante que campos com padrões específicos (ZIP, Telefone, SSN) rejeitem
  # entradas inválidas ou alfanuméricas fora do padrão aceito.
  # ----------------------------------------------------------------------------
  @invalidFormats @negative
  Scenario Outline: Failed registration with invalid format or data types
    When the user enters "<invalid_value>" in the field "<field_name>"
    And fills in all other required registration fields with valid data
    And submits the registration form
    Then the field error message "<expected_error>" should be displayed

    Examples:
      | field_name | invalid_value | expected_error                             |
      | Zip Code   | ABCDE         | Zip code must be numeric.                  |
      | Phone      | INVALID_PHONE | Phone number must contain valid digits.    |
      | SSN        | INVALID_SSN   | SSN must be in format XXX-XX-XXXX.         |

  # ----------------------------------------------------------------------------
  # TESTES DE SEGURANÇA E SANITIZAÇÃO (SECURITY & SANITIZATION)
  # Submete caracteres especiais, scripts XSS e payloads de SQL Injection.
  # Valida se o sistema falha de forma graciosa sem exibir exceções brutas (HTTP 500).
  # ----------------------------------------------------------------------------
  @specialCharacters @security @negative
  Scenario Outline: Failed registration with special characters or SQL Injection attempts
    When the user enters "<security_payload>" in username and password fields
    And fills in all other required registration fields with valid data
    And submits the registration form
    Then the account creation should fail gracefully without application errors

    Examples:
      | security_payload          |
      | ' OR '1'='1               |
      | <script>alert(1)</script> |
      | admin'--                  |