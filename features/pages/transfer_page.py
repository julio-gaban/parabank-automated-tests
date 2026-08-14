"""
Módulo de Mapeamento da Tela de Transferência de Fundos (Page Object Model - POM).

Este arquivo centraliza os locadores e métodos para interagir com o fluxo
de transferência entre contas no ParaBank, incluindo seleção dinâmica de contas via
drop-downs, submissão do formulário e captura dos dados de confirmação/sucesso.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TransferPage:
    """
    Page Object responsável por encapsular os elementos e ações da funcionalidade de Transferência.
    """

    def __init__(self, driver):
        """
        Inicializa o Page Object de Transferência com os locadores da tela.

        Args:
            driver (WebDriver): Instância ativa do Selenium WebDriver.
        """
        self.driver = driver
        self.login_url = "https://parabank.parasoft.com/parabank/index.htm"

        # --- Locadores: Autenticação Inicial ---
        self.USERNAME_INPUT = (By.NAME, "username")
        self.PASSWORD_INPUT = (By.NAME, "password")
        self.LOGIN_BUTTON = (By.XPATH, "//input[@value='Log In']")

        # --- Locadores: Formulário de Transferência ---
        self.TRANSFER_FUNDS_LINK = (By.XPATH, "//a[contains(@href, 'transfer.htm')]")
        self.AMOUNT_INPUT = (By.ID, "amount")
        self.FROM_ACCOUNT_SELECT = (By.ID, "fromAccountId")
        self.TO_ACCOUNT_SELECT = (By.ID, "toAccountId")
        self.TRANSFER_BUTTON = (By.XPATH, "//input[@value='Transfer']")

        # --- Locadores: Confirmação e Resultados da Operação ---
        self.RESULT_TITLE = (By.XPATH, "//div[@id='rightPanel']//h1[@class='title']")
        self.SUCCESS_AMOUNT = (By.ID, "amountResult")
        self.SUCCESS_FROM_ACCOUNT = (By.ID, "fromAccountIdResult")
        self.SUCCESS_TO_ACCOUNT = (By.ID, "toAccountIdResult")

    def open_login_page(self):
        """
        Navega até a página de login do ParaBank.
        """
        self.driver.get(self.login_url)

    def login(self, username, password):
        """
        Realiza a autenticação direta no sistema para liberar o acesso às transferências.

        Args:
            username (str): Nome de usuário para acesso.
            password (str): Senha de acesso.
        """
        self.driver.find_element(*self.USERNAME_INPUT).clear()
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def navigate_to_transfer(self):
        """
        Clica no link 'Transfer Funds' do menu e aguarda a renderização das contas.
        
        Nota de Assincronismo:
            Aguardar a presença do elemento 'fromAccountId' é essencial para evitar 
            TimeoutException/StaleElement, pois o ParaBank popula as contas via AJAX.
        """
        self.driver.find_element(*self.TRANSFER_FUNDS_LINK).click()
        
        # Aguarda a renderização inicial do elemento select antes de manipular as opções
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.FROM_ACCOUNT_SELECT)
        )

    def enter_amount(self, amount):
        """
        Insere a quantia a ser transferida no campo correspondente.

        Args:
            amount (str | float | int): Valor monetário a ser preenchido.
        """
        amount_field = self.driver.find_element(*self.AMOUNT_INPUT)
        amount_field.clear()
        if amount:
            amount_field.send_keys(amount)

    def select_from_account_index(self, index=0):
        """
        Seleciona a conta de origem no drop-down com base no seu índice.

        Args:
            index (int): Posição da opção no elemento <select> (Padrão: 0 - primeira conta).

        Returns:
            str | None: O número da conta selecionada (texto da opção) ou None se o índice for inválido.
        """
        select_elem = Select(self.driver.find_element(*self.FROM_ACCOUNT_SELECT))
        if len(select_elem.options) > index:
            select_elem.select_by_index(index)
            return select_elem.options[index].text
        return None

    def select_to_account_index(self, index=0):
        """
        Seleciona a conta de destino no drop-down com base no seu índice.

        Args:
            index (int): Posição da opção no elemento <select> (Padrão: 0 - primeira conta).

        Returns:
            str | None: O número da conta selecionada (texto da opção) ou None se o índice for inválido.
        """
        select_elem = Select(self.driver.find_element(*self.TO_ACCOUNT_SELECT))
        if len(select_elem.options) > index:
            select_elem.select_by_index(index)
            return select_elem.options[index].text
        return None

    def click_transfer(self):
        """
        Clica no botão para executar a transferência de fundos.
        """
        self.driver.find_element(*self.TRANSFER_BUTTON).click()

    def get_result_title(self):
        """
        Aguardará e retornará o título da página de resultado/sucesso.

        Returns:
            str: Texto do título do resultado (ex: "Transfer Complete!").
        """
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.RESULT_TITLE)
        )
        return self.driver.find_element(*self.RESULT_TITLE).text

    def get_transferred_amount(self):
        """
        Obtém o valor que foi confirmado como transferido na tela de resumo.

        Returns:
            str: O valor exibido na mensagem de sucesso.
        """
        return self.driver.find_element(*self.SUCCESS_AMOUNT).text