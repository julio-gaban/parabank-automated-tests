"""
Módulo de Definição de Passos (Step Definitions) para o Cadastro de Usuários.

Este arquivo implementa os cenários do BDD para a funcionalidade de registro
do ParaBank. Inclui suporte a geração de dados dinâmicos, preenchimento parcial/inválido
de formulários, testes de injeção/segurança e asserções resilientes de validações inline.
"""

import time
from behave import given, when, then, use_step_matcher
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Configuração do compilador de RegEx do Behave.
# Permite extrair parâmetros com aspas (.*?"), incluindo strings vazias ("")
# e payload de caracteres especiais sem quebrar o parser do BDD.
use_step_matcher("re")

# Mapeamento do nome amigável/negócio usado no arquivo .feature para o ID HTML do DOM
FIELD_MAP = {
    "First Name": "customer.firstName",
    "Last Name": "customer.lastName",
    "Address": "customer.address.street",
    "City": "customer.address.city",
    "State": "customer.address.state",
    "Zip Code": "customer.address.zipCode",
    "Phone": "customer.phoneNumber",
    "SSN": "customer.ssn",
    "Username": "customer.username",
    "Password": "customer.password",
    "Confirm Password": "repeatedPassword"
}


@given(r'the user accesses the ParaBank registration page')
@given(r'que o usuário acessa a página de cadastro do ParaBank')
def step_access_register_page(context):
    """
    Navega diretamente para o formulário de cadastro de novo usuário.
    """
    context.driver.get("https://parabank.parasoft.com/parabank/register.htm")


@when(r'the user fills in all required registration fields with valid data')
@when(r'o usuário preenche todos os campos obrigatórios com dados válidos')
def step_fill_valid_registration(context):
    """
    Gera um nome de usuário único utilizando Unix Timestamp para evitar falhas
    falsas-positivas por duplicidade de usuário em execuções de testes em lote.
    """
    timestamp = str(int(time.time()))
    unique_username = f"user_{timestamp}"
    
    _fill_registration_form(context, username=unique_username)


@when(r'the user fills in the registration form using an existing username "(.*?)"')
@when(r'o usuário preenche o formulário usando um nome de usuário já existente "(.*?)"')
def step_fill_existing_username(context, existing_username):
    """
    Preenche o formulário de cadastro utilizando um username fixo
    para testar a regra de negócio de bloqueio de nomes duplicados.
    """
    _fill_registration_form(context, username=existing_username)


@when(r'the user enters password "(.*?)" and confirm password "(.*?)"')
@when(r'o usuário digita a senha "(.*?)" e a confirmação de senha "(.*?)"')
def step_enter_mismatched_passwords(context, password, confirm_password):
    """
    Armazena senhas customizadas no objeto context para que sejam aplicadas 
    posteriormente durante a montagem/submissão do formulário.
    """
    context.custom_password = password
    context.custom_confirm_password = confirm_password


@when(r'the user leaves mandatory field "(.*?)" empty')
@when(r'o usuário deixa o campo obrigatório "(.*?)" em branco')
def step_leave_field_empty(context, field_name):
    """
    Preenche todo o formulário com dados válidos e limpa apenas o campo
    especificado para validar o disparo do erro inline de campo obrigatório.
    """
    timestamp = str(int(time.time()))
    _fill_registration_form(context, username=f"user_{timestamp}")
    
    # Busca o ID HTML equivalente através do mapa de campos
    field_id = FIELD_MAP.get(field_name)
    if field_id:
        element = context.driver.find_element(By.ID, field_id)
        element.clear()


@when(r'the user enters "(.*?)" in the field "(.*?)"')
@when(r'o usuário digita "(.*?)" no campo "(.*?)"')
def step_enter_invalid_field_value(context, value, field_name):
    """
    Salva temporariamente uma tupla (campo, valor_inválido) no contexto do teste.
    """
    context.custom_invalid_field = (field_name, value)


@when(r'the user enters "(.*?)" in username and password fields')
@when(r'o usuário digita "(.*?)" nos campos de usuário e senha')
def step_enter_security_payload(context, payload):
    """
    Preenche os campos de credenciais com um payload de segurança/sanitização
    (ex: XSS, SQL Injection ou caracteres unicode) para testar a robustez do sistema.
    """
    _fill_registration_form(
        context, 
        username=payload, 
        password=payload, 
        confirm_password=payload
    )


@when(r'fills in all other required registration fields with valid data')
@when(r'preenche todos os outros campos obrigatórios com dados válidos')
def step_fill_remaining_fields(context):
    """
    Completa o preenchimento dos demais campos do formulário, aplicando
    quaisquer overrides previamente salvos no contexto (ex: senhas ou campos inválidos).
    """
    timestamp = str(int(time.time()))
    username = f"user_{timestamp}"
    password = getattr(context, 'custom_password', 'Password123!')
    confirm_password = getattr(context, 'custom_confirm_password', 'Password123!')

    _fill_registration_form(
        context, 
        username=username, 
        password=password, 
        confirm_password=confirm_password
    )

    # Aplica o dado inválido customizado caso ele tenha sido setado em um passo anterior
    if hasattr(context, 'custom_invalid_field'):
        field_name, value = context.custom_invalid_field
        field_id = FIELD_MAP.get(field_name)
        if field_id:
            element = context.driver.find_element(By.ID, field_id)
            element.clear()
            element.send_keys(value)


@when(r'submits the registration form')
@when(r'submete o formulário de cadastro')
def step_submit_registration(context):
    """
    Clica no botão de envio 'Register' para efetivar o cadastro.
    """
    submit_button = context.driver.find_element(By.XPATH, "//input[@value='Register']")
    submit_button.click()


@then(r'the account creation should be successful displaying a welcome message')
@then(r'a criação da conta deve ter sucesso exibindo uma mensagem de boas-vindas')
def step_verify_successful_registration(context):
    """
    Valida se a conta foi criada com sucesso verificando a mensagem de boas-vindas.
    """
    wait = WebDriverWait(context.driver, 10)
    welcome_element = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h1[@class='title']"))
    )
    assert "Welcome" in welcome_element.text or "Account Created" in context.driver.page_source


@then(r'the error message "(.*?)" should be displayed on registration')
@then(r'a mensagem de erro "(.*?)" deve ser exibida no cadastro')
def step_verify_registration_error(context, expected_error):
    """
    Garante a exibição do erro geral de cadastro (ex: usuário já existente).
    """
    wait = WebDriverWait(context.driver, 10)
    error_element = wait.until(
        EC.visibility_of_element_located((
            By.XPATH, "//*[@id='customer.username.errors' or @class='error']"
        ))
    )
    assert expected_error in error_element.text, (
        f"Erro esperado: '{expected_error}', mas o texto retornado foi: '{error_element.text}'"
    )


@then(r'the field error message "(.*?)" should be displayed')
@then(r'a mensagem de erro do campo "(.*?)" deve ser exibida')
def step_verify_field_inline_error(context, expected_error):
    """
    Valida mensagens de erro inline associadas a campos específicos do formulário.

    Estratégia de Resiliência:
        Captura todos os elementos de erro presentes no DOM (`presence_of_all_elements_located`),
        concatena seus conteúdos e realiza uma busca case-insensitive. Caso ocorra timeout,
        executa o fallback varrendo o `body.text` completo para relatório detalhado.
    """
    # Seletor abrangente para spans de erro (.errors), classes gerais e painel principal
    error_xpath = (
        "//*[contains(@id, '.errors') or "
        "contains(@class, 'error') or "
        "//span[contains(@class, 'error')] or "
        "//div[@id='rightPanel']//p]"
    )
    
    try:
        # Aguarda que todos os spans/mensagens de erro sejam carregados no DOM
        error_elements = context.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, error_xpath))
        )
        
        # Consolida todos os textos de erro visíveis em uma única string tratada
        all_errors_text = " | ".join(
            [elem.text.strip() for elem in error_elements if elem.text.strip()]
        )
        
        # Asserção case-insensitive do texto esperado
        assert expected_error.lower() in all_errors_text.lower(), (
            f"Erro esperado: '{expected_error}', "
            f"mas os erros exibidos na tela foram: '{all_errors_text}'"
        )

    except TimeoutException:
        # FALLBACK DIAGNÓSTICO: Varre a página completa se os seletores de erro falharem
        body_text = context.driver.find_element(By.TAG_NAME, "body").text
        
        assert expected_error.lower() in body_text.lower(), (
            f"Timeout: A mensagem de erro '{expected_error}' não foi localizada na tela de registro.\n"
            f"Conteúdo visível capturado na página:\n{body_text[:300]}"
        )


@then(r'the account creation should fail gracefully without application errors')
@then(r'a criação de conta deve falhar de forma amigável sem erros de aplicação')
def step_verify_graceful_failure(context):
    """
    Valida se falhas no cadastro (ex: envio de payloads maliciosos) são tratadas
    sem expor erros não tratados da aplicação, como HTTP 500 ou Stack Traces de Java/Spring.
    """
    page_source = context.driver.page_source.lower()
    assert "internal server error" not in page_source, (
        "A aplicação retornou HTTP 500 (Internal Server Error) em vez de tratar o erro."
    )
    assert "exception" not in page_source, (
        "Foram encontradas exceções não tratadas/Stack Traces expostas no código fonte."
    )


# --- Função Auxiliar Privada de Preenchimento ---
def _fill_registration_form(
    context, 
    username="john_doe", 
    password="Password123!", 
    confirm_password="Password123!"
):
    """
    Função auxiliar interna para centralizar e padronizar a digitação
    nos campos do formulário de cadastro, evitando duplicação de código nos steps.

    Args:
        context: Objeto de estado global do Behave contendo o driver.
        username (str): Nome de usuário para preenchimento.
        password (str): Senha para preenchimento.
        confirm_password (str): Confirmação da senha.
    """
    fields = {
        "customer.firstName": "John",
        "customer.lastName": "Doe",
        "customer.address.street": "123 Main St",
        "customer.address.city": "Beverly Hills",
        "customer.address.state": "CA",
        "customer.address.zipCode": "90210",
        "customer.phoneNumber": "555-0199",
        "customer.ssn": "000-12-3456",
        "customer.username": username,
        "customer.password": password,
        "repeatedPassword": confirm_password
    }

    # Itera sobre o dicionário limpando e enviando as chaves para cada input
    for field_id, value in fields.items():
        element = context.driver.find_element(By.ID, field_id)
        element.clear()
        element.send_keys(value)