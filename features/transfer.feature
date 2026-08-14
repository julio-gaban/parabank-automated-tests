# language: en

# ==============================================================================
# MÓDULO DE TRANSFERÊNCIA DE FUNDOS (FUNDS TRANSFER) - PARABANK
# ------------------------------------------------------------------------------
# Este arquivo descreve os cenários de teste BDD para transferência entre contas.
# Cobertura funcional:
#   - Transferências bem-sucedidas entre contas válidas (Caminho Feliz).
#   - Validação de valores limite (valores zerados, negativos e vazios).
#   - Tratamento de tipos de dados inválidos, símbolos monetários e SQL Injection.
#   - Regras de negócio financeiras: mesma conta de origem/destino e saldo insuficiente.
# ==============================================================================

Feature: Funds Transfer in ParaBank
  As an authenticated ParaBank customer
  I want to transfer funds between my accounts
  In order to manage my finances efficiently

  # ----------------------------------------------------------------------------
  # PRÉ-CONDIÇÕES GLOBAIS
  # Exige autenticação prévia (Sessão Ativa) e navegação até a tela da funcionalidade.
  # ----------------------------------------------------------------------------
  Background:
    Given the user is logged into the ParaBank system
    And the user navigates to the "Transfer Funds" page

  # ----------------------------------------------------------------------------
  # CAMINHO FELIZ (HAPPY PATH)
  # Valida a movimentação bem-sucedida de valores entre duas contas distintas.
  # ----------------------------------------------------------------------------
  @validAmount @smoke @regression
  Scenario: Successful funds transfer with valid amount
    When the user enters a valid transfer amount "100.00"
    And selects a valid source account and target account
    And clicks the transfer button
    Then the transfer should be completed successfully displaying the confirmation message

  # ----------------------------------------------------------------------------
  # ANÁLISE DE VALOR LIMITE (BOUNDARY VALUE ANALYSIS) & VALIDAÇÕES DE MONANTE
  # Testa o comportamento do sistema diante de valores não permitidos:
  #   - Campos vazios (Obrigatoriedade)
  #   - Limite zero (0 / 0.00)
  #   - Valores negativos (-50.00 / -1.50)
  # ----------------------------------------------------------------------------
  @invalidAmount @boundaryAmounts @negative
  Scenario Outline: Failed transfer with invalid or boundary amounts
    When the user enters transfer amount "<amount>"
    And selects a valid source account and target account
    And clicks the transfer button
    Then the transfer process should fail displaying error "<expected_error>"

    Examples:
      # --- Campo Vazio ---
      | amount    | expected_error                             |
      |           | Please enter a valid amount.               |
      
      # --- Valores Zerados ---
      | 0         | Amount must be greater than zero.          |
      | 0.00      | Amount must be greater than zero.          |
      
      # --- Valores Negativos ---
      | -50.00    | Amount must be greater than zero.          |
      | -1.50     | Amount must be greater than zero.          |

  # ----------------------------------------------------------------------------
  # VALIDAÇÃO DE TIPOS DE DADOS E RESILIÊNCIA DO CAMPO DE VALOR
  # Garante que o input só aceite numéricos decimais válidos, rejeitando:
  #   - Letras e strings alfanuméricas (Ex: ABC, 100USD)
  #   - Caracteres monetários não formatados (Ex: $100.00)
  #   - Formatação regional incompatível com o padrão americano (Ex: vírgula no lugar de ponto)
  #   - Payloads de segurança (Injeção de código/SQL)
  # ----------------------------------------------------------------------------
  @invalidDataTypes @negative @security
  Scenario Outline: Failed transfer with invalid data types in amount field
    When the user enters transfer amount "<invalid_amount>"
    And selects a valid source account and target account
    And clicks the transfer button
    Then the transfer process should fail displaying error "Please enter a numeric amount."

    Examples:
      | invalid_amount |
      | ABC            |
      | 100USD         |
      | $100.00        |
      | 50,00          |
      | ' OR '1'='1    |

  # ----------------------------------------------------------------------------
  # REGRA DE NEGÓCIO: CONTA DE ORIGEM E DESTINO IDÊNTICAS
  # Bloqueia tentativas de transferência onde a conta de origem é igual à de destino.
  # ----------------------------------------------------------------------------
  @sameSourceTarget @negative
  Scenario: Failed transfer when selecting same source and target account
    When the user selects the same account as source and target
    And enters a valid transfer amount "50.00"
    And clicks the transfer button
    Then the transfer process should fail displaying error "From account and To account cannot be the same."

  # ----------------------------------------------------------------------------
  # REGRA DE NEGÓCIO: LIMITE DE SALDO (INSUFFICIENT FUNDS)
  # Impede a transferência quando o valor solicitado é maior que o saldo disponível.
  # ----------------------------------------------------------------------------
  @exceedAccountBalance @negative
  Scenario: Failed transfer exceeding available account balance
    When the user enters a transfer amount exceeding the source account balance
    And selects a valid source account and target account
    And clicks the transfer button
    Then the transfer process should fail displaying error "Insufficient funds."