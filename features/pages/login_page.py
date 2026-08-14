"""
Módulo de Mapeamento da Tela de Login (Page Object Model - POM).

Este arquivo centraliza a URL, os mapeamentos de elementos (locadores) e as 
interações diretas com o formulário de autenticação da aplicação ParaBank.
"""

from selenium.webdriver.common.by import By


class LoginPage:
    """
    Page Object responsável por encapsular os elementos e ações da página de Login.
    """

    def __init__(self, driver):
        """
        Inicializa o Page Object com a instância do WebDriver e os locadores da tela.

        Args:
            driver (WebDriver): Instância ativa do Selenium WebDriver.
        """
        self.driver = driver
        self.url = "https://parabank.parasoft.com/parabank/index.htm"

        # --- Locadores: Formulário de Autenticação ---
        self.USERNAME_INPUT = (By.NAME, "username")
        self.PASSWORD_INPUT = (By.NAME, "password")
        self.LOGIN_BUTTON = (By.XPATH, "//input[@value='Log In']")
        
        # --- Locadores: Elementos de Validação (Pós-login / Erros) ---
        self.ACCOUNT_OVERVIEW_TITLE = (By.XPATH, "//h1[@class='title']")
        self.ERROR_MESSAGE = (By.XPATH, "//p[@class='error']")
        self.LOGOUT_LINK = (By.XPATH, "//a[contains(@href, 'logout.htm')]")

    def open(self):
        """
        Navega diretamente para a URL inicial/página de login do ParaBank.
        """
        self.driver.get(self.url)

    def login(self, username, password):
        """
        Preenche os campos de usuário e senha e submete o formulário de login.

        Args:
            username (str): Nome de usuário para autenticação.
            password (str): Senha do usuário.
        """
        # Limpa os campos antes do envio para evitar dados duplicados ou resíduos
        self.driver.find_element(*self.USERNAME_INPUT).clear()
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def get_accounts_overview_title(self):
        """
        Obtém o texto do título principal exibido após um login bem-sucedido.

        Returns:
            str: O texto contido no título da página (ex: "Accounts Overview").
        """
        return self.driver.find_element(*self.ACCOUNT_OVERVIEW_TITLE).text

    def get_error_message(self):
        """
        Captura a mensagem de erro retornada no formulário em caso de falha de login.

        Returns:
            str: Texto da mensagem de erro visível na tela.
        """
        return self.driver.find_element(*self.ERROR_MESSAGE).text

    def is_user_logged_in(self):
        """
        Verifica a presença do link de Logout para validar se o usuário está autenticado.

        Returns:
            bool: True se o link de Logout estiver presente no DOM, False caso contrário.
        """
        return len(self.driver.find_elements(*self.LOGOUT_LINK)) > 0