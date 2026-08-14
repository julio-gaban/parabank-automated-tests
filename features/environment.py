"""
Módulo de Gerenciamento do Ambiente de Testes (Hooks do Behave).

Este arquivo define as configurações de inicialização e encerramento da suíte
de testes, controlando o ciclo de vida do WebDriver, tempos de sincronização 
e a integração de relatórios com o Allure Framework (captura de evidências).
"""

import os
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def before_scenario(context, scenario):
    """
    Hook executado automaticamente ANTES do início de cada cenário.
    
    Configura e inicializa a instância do navegador Chrome, define estratégias
    de espera (waits) e injeta as variáveis de driver e wait no contexto do Behave.
    
    Args:
        context: Objeto de estado global do Behave compartilhado entre os passos.
        scenario: Objeto com os metadados do cenário prestes a ser executado.
    """
    # Configurações de inicialização do navegador Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")       # Inicia com a tela cheia para evitar quebras por quebra de layout/responsividade
    options.add_argument("--disable-gpu")            # Desabilita aceleração de hardware (evita renderização inconsistente em CI)
    options.add_argument("--no-sandbox")            # Necessário para execução estável em ambientes virtuais/containers
    options.add_argument("--remote-allow-origins=*") # Previne problemas de CORS/WebSockets entre o ChromeDriver e o Chrome

    # Inicialização do WebDriver via Selenium Manager nativo (Selenium 4.6+)
    # O driver e o binário do Chrome são gerenciados e atualizados automaticamente
    context.driver = webdriver.Chrome(options=options)

    # Configuração de esperas explícitas (WebDriverWait) e implícitas
    # context.wait é centralizado para gerenciar a assincronia e AJAX das páginas
    context.wait = WebDriverWait(context.driver, timeout=15, poll_frequency=0.5)
    context.driver.implicitly_wait(5)


def after_scenario(context, scenario):
    """
    Hook executado automaticamente APÓS o término de cada cenário.
    
    Valida o status de execução: caso o cenário tenha falhado, captura uma
    evidência (screenshot) e anexa ao relatório do Allure. Ao final,
    encerra a sessão do navegador com segurança.
    
    Args:
        context: Objeto de estado global do Behave contendo o driver ativo.
        scenario: Objeto com o status final e metadados do cenário executado.
    """
    # 1. Tratamento de Falhas: Anexa evidências no relatório Allure se o teste quebrar
    if scenario.status == "failed":
        try:
            screenshot = context.driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name=f"Falha - {scenario.name}",
                attachment_type=AttachmentType.PNG
            )
        except Exception as e:
            # Garante que um erro ao tirar a print não mascare a exceção real do teste
            print(f"Aviso: Não foi possível anexar o screenshot ao Allure: {e}")

    # 2. Encerramento da Sessão: Fecha todas as abas e destrói o processo do WebDriver
    if hasattr(context, "driver"):
        context.driver.quit()