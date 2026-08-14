"""
Módulo de Mapeamento da Tela de Registro de Usuário (Page Object Model - POM).

Este arquivo centraliza a URL, os locadores dos campos do formulário de cadastro,
botões de ação e mensagens de retorno (sucesso e erros) do ParaBank.
"""

from selenium.webdriver.common.by import By


class RegisterPage:
    """
    Page Object responsável por encapsular os elementos e ações da página de Registro.
    """

    def __init__(self, driver):
        """
        Inicializa o Page Object de Registro com a instância do WebDriver e seus locadores.

        Args:
            driver (WebDriver): Instância ativa do Selenium WebDriver.
        """
        self.driver = driver
        self.url = "https://parabank.parasoft.com/parabank/register.htm"

        # --- Locadores: Dados Pessoais e Endereço ---
        self.FIRST_NAME_INPUT = (By.ID, "customer.firstName")
        self.LAST_NAME_INPUT = (By.ID, "customer.lastName")
        self.ADDRESS_INPUT = (By.ID, "customer.address.street")
        self.CITY_INPUT = (By.ID, "customer.address.city")
        self.STATE_INPUT = (By.ID, "customer.address.state")
        self.ZIP_CODE_INPUT = (By.ID, "customer.address.zipCode")
        self.PHONE_INPUT = (By.ID, "customer.phoneNumber")
        self.SSN_INPUT = (By.ID, "customer.ssn")

        # --- Locadores: Credenciais de Acesso ---
        self.USERNAME_INPUT = (By.ID, "customer.username")
        self.PASSWORD_INPUT = (By.ID, "customer.password")
        self.CONFIRM_PASSWORD_INPUT = (By.ID, "repeatedPassword")
        
        # --- Locadores: Ações ---
        self.REGISTER_BUTTON = (By.XPATH, "//input[@value='Register']")
        
        # --- Locadores: Feedback e Validações ---
        self.SUCCESS_TITLE = (By.XPATH, "//h1[@class='title']")
        self.SUCCESS_MESSAGE = (By.XPATH, "//div[@id='rightPanel']/p")
        self.USERNAME_ERROR = (By.ID, "customer.username.errors")

    def open(self):
        """
        Navega diretamente para a URL da página de registro do ParaBank.
        """
        self.driver.get(self.url)

    def fill_registration_form(self, data):
        """
        Preenche os campos do formulário de registro dinamicamente com base em um dicionário.

        Args:
            data (dict): Dicionário contendo os dados do formulário. Chaves esperadas:
                - first_name, last_name, address, city, state, zip_code,
                  phone, ssn, username, password, confirm_password.
                Usa .get() com valor padrão vazio ("") para evitar erros se uma chave faltar.
        """
        self.driver.find_element(*self.FIRST_NAME_INPUT).send_keys(data.get("first_name", ""))
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(data.get("last_name", ""))
        self.driver.find_element(*self.ADDRESS_INPUT).send_keys(data.get("address", ""))
        self.driver.find_element(*self.CITY_INPUT).send_keys(data.get("city", ""))
        self.driver.find_element(*self.STATE_INPUT).send_keys(data.get("state", ""))
        self.driver.find_element(*self.ZIP_CODE_INPUT).send_keys(data.get("zip_code", ""))
        self.driver.find_element(*self.PHONE_INPUT).send_keys(data.get("phone", ""))
        self.driver.find_element(*self.SSN_INPUT).send_keys(data.get("ssn", ""))
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(data.get("username", ""))
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(data.get("password", ""))
        self.driver.find_element(*self.CONFIRM_PASSWORD_INPUT).send_keys(data.get("confirm_password", ""))

    def submit_form(self):
        """
        Clica no botão para submeter o formulário de cadastro.
        """
        self.driver.find_element(*self.REGISTER_BUTTON).click()

    def get_success_message(self):
        """
        Obtém o texto da mensagem de confirmação exibida após o registro concluído com sucesso.

        Returns:
            str: Texto de boas-vindas/sucesso contido no painel principal.
        """
        return self.driver.find_element(*self.SUCCESS_MESSAGE).text

    def get_username_error(self):
        """
        Captura o texto de erro específico do campo de nome de usuário (ex: usuário já existente).

        Returns:
            str: Texto da mensagem de erro inline do campo de nome de usuário.
        """
        return self.driver.find_element(*self.USERNAME_ERROR).text