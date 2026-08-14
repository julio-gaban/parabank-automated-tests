"""
Módulo de Definição de Passos (Step Definitions) para o Módulo de Login.

Este arquivo contém a implementação BDD em Python (Behave) que conecta os passos
da funcionalidade 'login.feature' às ações do Selenium WebDriver na interface do ParaBank.
"""

from behave import given, when, then, use_step_matcher
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Configuração do compilador de regex do Behave.
# Permite capturar argumentos delimitados por aspas (.*?"), incluindo strings
# vazias ("") e sequências com caracteres especiais sem estourar ParseError.
use_step_matcher("re")


@given(r'the user accesses the ParaBank home page')
@given(r'que o usuário acessa a página inicial do ParaBank')
def step_access_home_page(context):
    """
    Navega até a URL principal da aplicação sob teste (ParaBank Home).

    Args:
        context: Objeto de estado global do Behave contendo o driver Selenium ativo.
    """
    context.driver.get("https://parabank.parasoft.com/parabank/index.htm")


@when(r'the user enters username "(.*?)" and password "(.*?)"')
@when(r'o usuário insere o nome de usuário "(.*?)" e a senha "(.*?)"')
def step_enter_credentials(context, username, password):
    """
    Localiza os campos do formulário de autenticação, limpa valores prévios e
    digita as credenciais fornecidas no cenário de teste.

    Args:
        context: Objeto de estado global do Behave.
        username (str): Nome de usuário capturado pela Regex.
        password (str): Senha do usuário capturada pela Regex.
    """
    # Localização direta dos elementos de formulário por atributos nativos
    username_input = context.driver.find_element(By.NAME, "username")
    password_input = context.driver.find_element(By.NAME, "password")

    # Limpeza preventiva para evitar concatenação com caracteres padrão/residuais
    username_input.clear()
    username_input.send_keys(username)

    password_input.clear()
    password_input.send_keys(password)


@when(r'clicks the log in button')
@when(r'clica no botão de login')
def step_click_login_button(context):
    """
    Clica no botão para submeter o formulário de login.
    """
    login_button = context.driver.find_element(By.XPATH, "//input[@value='Log In']")
    login_button.click()


@then(r'the login should be successful displaying the "(.*?)" page')
@then(r'o login deve ser realizado com sucesso exibindo a página "(.*?)"')
def step_verify_successful_login(context, expected_title):
    """
    Valida se o login foi concluído com sucesso aguardando a renderização 
    do título principal da tela pós-autenticação (ex: Accounts Overview).

    Args:
        context: Objeto de estado do Behave.
        expected_title (str): Título/texto esperado na página pós-login.
    """
    # Aguarda explicitamente a renderização do cabeçalho da dashboard do usuário
    wait = WebDriverWait(context.driver, 10)
    title_element = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h1[@class='title']"))
    )
    
    actual_title = title_element.text.strip()
    assert expected_title in actual_title, (
        f"Falha de asserção de Login: Esperado '{expected_title}', mas o título "
        f"retornado na tela foi '{actual_title}'."
    )


@then(r'the error message "(.*?)" should be displayed')
@then(r'a mensagem de erro "(.*?)" deve ser exibida')
def step_verify_error_message(context, expected_error):
    """
    Valida a exibição de mensagens de erro em cenários de login incorreto/inválido.
    
    Estratégia de Resiliência:
        Possui um seletor XPath expandido para lidar com variações na renderização
        de erros do ParaBank e um mecanismo de fallback (captura do body.text em TimeoutException)
        para gerar relatórios de erro legíveis no Allure em vez de rastreamentos brutos do Python.

    Args:
        context: Objeto de estado do Behave contendo o context.wait.
        expected_error (str): Trecho do texto da mensagem de erro esperada.
    """
    # Seletor dinâmico que cobre classes de erro, parágrafos do painel e seletores por ID
    error_xpath = (
        "//*[contains(@class, 'error') or "
        "contains(@id, 'error') or "
        "//p[contains(@class, 'error')] or "
        "//div[@id='rightPanel']//p]"
    )
    
    try:
        # Aguarda qualquer um dos elementos de erro ficar visível na tela
        error_element = context.wait.until(
            EC.visibility_of_element_located((By.XPATH, error_xpath))
        )
        
        actual_text = error_element.text.strip()
        
        # Comparação em lowercase para evitar divergências de caixa alta/baixa
        assert expected_error.lower() in actual_text.lower(), (
            f"Erro esperado contendo: '{expected_error}', "
            f"mas a mensagem na tela foi: '{actual_text}'"
        )

    except TimeoutException:
        # FALLBACK DIAGNÓSTICO: Se o seletor explícito falhar em 15s, varre todo o texto
        # do HTML para checar se a mensagem está solta no DOM e exibe um log detalhado
        body_text = context.driver.find_element(By.TAG_NAME, "body").text
        
        assert expected_error.lower() in body_text.lower(), (
            f"Timeout: A mensagem de erro '{expected_error}' não foi localizada pelo seletor XPath.\n"
            f"Conteúdo visível capturado na página:\n{body_text[:300]}"
        )