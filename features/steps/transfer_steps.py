"""
Módulo de Definição de Passos (Step Definitions) para Transferência de Fundos.

Este arquivo implementa os cenários BDD em Python (Behave) relacionados às operações
de transferência no ParaBank. Trata especificamente de sincronismo AJAX/Angular para 
carregamento dinâmico de contas, seleção de origem/destino e validações de sucesso/erro.
"""

import time
from behave import given, when, then, use_step_matcher
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Configuração do compilador de RegEx do Behave.
# Permite grupos não-capturáveis (?: ... )?, suporte a valores decimais/especiais
# e tratamento seguro de parâmetros em aspas.
use_step_matcher("re")


@given(r'the user is logged into the ParaBank system')
@given(r'que o usuário está logado no sistema ParaBank')
def step_login_user(context):
    """
    Garante pré-condição de sessão autenticada antes de executar os testes de transferência.
    
    Estratégia de Autenticação Idempotente:
        Verifica se o link 'Logout' já está presente. Caso não esteja, efetua o login 
        com as credenciais padrão ('john'/'demo') e aguarda a confirmação de sessão.
    """
    context.driver.get("https://parabank.parasoft.com/parabank/index.htm")
    
    # Checa a existência do botão de logout no DOM para evitar relogins desnecessários
    if len(context.driver.find_elements(By.XPATH, "//a[contains(@href, 'logout.htm')]")) == 0:
        try:
            username_input = context.wait.until(
                EC.element_to_be_clickable((By.NAME, "username"))
            )
            password_input = context.driver.find_element(By.NAME, "password")
            
            username_input.clear()
            username_input.send_keys("john")
            
            password_input.clear()
            password_input.send_keys("demo")
            
            context.driver.find_element(By.XPATH, "//input[@value='Log In']").click()
            
            # Valida a efetivação do login aguardando a renderização do link de logout
            context.wait.until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'logout.htm')]"))
            )
            
        except TimeoutException:
            # Captura a falha de login e emite mensagem clara de diagnóstico para o Allure
            assert False, (
                "[FALHA DE AUTENTICAÇÃO] Não foi possível realizar o login com as credenciais padrão ('john'/'demo'). "
                "Verifique se o usuário existe na base do ParaBank ou se a aplicação exibiu erro na tela."
            )


@given(r'the user navigates to the "Transfer Funds" page')
@given(r'que o usuário navega para a página "Transfer Funds"')
def step_navigate_to_transfer(context):
    """
    Navega até a tela de transferência e aguarda o carregamento das contas via AJAX.
    """
    # 1. Garante que o menu lateral pós-login está visível no DOM
    context.wait.until(EC.presence_of_element_located((By.ID, "leftPanel")))
    
    # 2. Localiza e clica no link de transferência (por texto visível ou href)
    transfer_link = context.wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[text()='Transfer Funds' or contains(@href, 'transfer.htm')]")
        )
    )
    transfer_link.click()
    
    # 3. SINCRONISMO AJAX: Aguarda o elemento <select> 'fromAccountId' ser populado
    # com pelo menos uma tag <option> vinda da requisição do backend
    context.wait.until(
        lambda driver: len(driver.find_elements(By.XPATH, "//select[@id='fromAccountId']/option")) > 0
    )


@when(r'(?:the user )?enters a valid transfer amount "(.*?)"')
@when(r'(?:the user )?enters transfer amount "(.*?)"')
@when(r'(?:o usuário )?informa um valor de transferência válido "(.*?)"')
@when(r'(?:o usuário )?informa o valor de transferência "(.*?)"')
def step_enter_transfer_amount(context, amount):
    """
    Insere o valor monetário informado no campo de quantia da transferência.

    Args:
        context: Objeto de estado do Behave.
        amount (str): Valor a ser transferido.
    """
    amount_input = context.wait.until(EC.visibility_of_element_located((By.ID, "amount")))
    amount_input.clear()
    amount_input.send_keys(amount)


@when(r'(?:the user )?selects a valid source account and target account')
@when(r'(?:o usuário )?seleciona uma conta de origem e destino válidas')
def step_select_accounts(context):
    """
    Seleciona contas distintas de origem e destino nos seletores dropdown.
    """
    time.sleep(1)  # Pausa de estabilização para o ciclo de digest do Angular/AJAX
    
    from_select = Select(context.wait.until(EC.presence_of_element_located((By.ID, "fromAccountId"))))
    to_select = Select(context.wait.until(EC.presence_of_element_located((By.ID, "toAccountId"))))
    
    if len(from_select.options) > 0 and len(to_select.options) > 0:
        from_select.select_by_index(0)
        # Seleciona a segunda conta se disponível; caso contrário, seleciona a primeira
        target_index = 1 if len(to_select.options) > 1 else 0
        to_select.select_by_index(target_index)


@when(r'(?:the user )?selects the same account as source and target')
@when(r'(?:o usuário )?seleciona a mesma conta para origem e destino')
def step_select_same_account(context):
    """
    Força a seleção da mesma conta tanto na origem quanto no destino 
    para validar regras de transferência para a própria conta.
    """
    time.sleep(1)  # Pausa de estabilização para o ciclo de digest do Angular/AJAX
    
    from_select = Select(context.wait.until(EC.presence_of_element_located((By.ID, "fromAccountId"))))
    to_select = Select(context.wait.until(EC.presence_of_element_located((By.ID, "toAccountId"))))
    
    from_select.select_by_index(0)
    to_select.select_by_index(0)


@when(r'the user enters a transfer amount exceeding the source account balance')
@when(r'o usuário informa um valor de transferência superior ao saldo')
def step_enter_exceeding_amount(context):
    """
    Reutiliza a função de entrada de valor inserindo uma quantia intencionalmente
    alta para testar a validação de estouro de saldo.
    """
    step_enter_transfer_amount(context, "999999999.00")


@when(r'clicks the transfer button')
@when(r'clica no botão de transferência')
def step_click_transfer_button(context):
    """
    Submete o formulário clicando no botão 'Transfer'.
    """
    transfer_button = context.wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@value='Transfer']"))
    )
    transfer_button.click()


@then(r'the transfer should be completed successfully displaying the confirmation message')
@then(r'a transferência deve ser concluída com sucesso exibindo a mensagem de confirmação')
def step_verify_successful_transfer(context):
    """
    Valida se a mensagem de confirmação 'Transfer Complete!' foi exibida após a resposta AJAX.
    """
    result_title = context.wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//h1[@class='title' and contains(text(), 'Transfer Complete!')]")
        )
    )
    assert result_title.is_displayed(), "A mensagem 'Transfer Complete!' não foi exibida na tela."


@then(r'the transfer process should fail displaying error "(.*?)"')
@then(r'o processo de transferência deve falhar exibindo o erro "(.*?)"')
def step_verify_transfer_error(context, expected_error):
    """
    Valida a mensagem de erro retornada em transferências inválidas.

    Estratégia de Diagnóstico:
        Tenta capturar o elemento de erro visível na página. Se ocorrer TimeoutException,
        imprime o texto visível no `body` para ajudar no diagnóstico do relatório Allure.
    """
    error_xpath = "//*[@class='error' or contains(@id, 'error') or contains(@id, 'errors') or @class='title']"
    
    try:
        error_element = context.wait.until(
            EC.visibility_of_element_located((By.XPATH, error_xpath))
        )
        actual_error = error_element.text.strip()
        assert expected_error in actual_error, (
            f"Erro esperado: '{expected_error}', mas a mensagem retornada foi: '{actual_error}'"
        )
        
    except TimeoutException:
        # Fallback de diagnóstico: captura o conteúdo do body se o seletor principal estourar o tempo
        page_text = context.driver.find_element(By.TAG_NAME, "body").text
        assert False, (
            f"Timeout aguardando a mensagem de erro '{expected_error}'. "
            f"Conteúdo visível capturado na página:\n{page_text[:300]}"
        )