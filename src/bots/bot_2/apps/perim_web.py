from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.common.schemas.produto_mercado_schema import ProdutoMercadoSchema


class PerimWeb:
    """Automatiza interacoes com o site do Perim usando Selenium.

    Attributes:
        driver: Instancia do webdriver usada para navegar e interagir com a pagina.
        nome_mercado: Nome fixo do mercado utilizado no retorno dos dados.
    """

    def __init__(self, driver: webdriver.Chrome) -> None:
        """Inicializa a classe com o driver de navegador.

        Args:
            driver: WebDriver do Chrome previamente configurado.
        """
        self.driver = driver
        self.nome_mercado: str = "Perim"

    def buscar_produto(self, nome_produto: str) -> ProdutoMercadoSchema:
        """Busca um produto no site e retorna os dados validados.

        Args:
            nome_produto: Nome do produto a ser pesquisado no campo de busca.

        Returns:
            ProdutoMercadoSchema: Dados do produto encontrado, incluindo titulo,
            valor normalizado e link.

        Raises:
            TimeoutException: Quando algum elemento necessario para busca nao fica
                disponivel dentro do tempo limite.
            Exception: Para quaisquer erros inesperados durante a consulta.
        """
        try:
            logger.info(f"Buscando o produto '{nome_produto}' no site Perim")

            self.driver.get("https://www.perim.com.br/")

            campo_busca = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='inputBuscaRapida']"))
            )
            campo_busca.clear()
            campo_busca.send_keys(nome_produto)

            btn_pesquisa = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-search']"))
            )
            btn_pesquisa.click()

            titulo: str = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//p[contains(@class, 'text-success description')]"))
            ).text

            valor: str = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'info-price ng-star-inserted')]"))
            ).text

            link: str = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@class='ghost-link clearfix']"))
            ).get_attribute("href")

            dados_retorno: ProdutoMercadoSchema = ProdutoMercadoSchema(
                nome_mercado=self.nome_mercado,
                termo_pesquisa=nome_produto,
                titulo=titulo,
                valor=valor,
                link=link,
            )

            logger.info(f"Busca pelo produto '{nome_produto}' realizada com sucesso")

            return dados_retorno

        except TimeoutException as e:
            raise TimeoutException(
                "Tempo de carregamento da pagina excedido ao buscar o produto "
                f"| Modulo do erro: {e.__traceback__.tb_frame.f_globals.get('__name__', e.__class__.__module__)} | Linha do erro: {e.__traceback__.tb_lineno}"
            )

        except Exception as e:
            raise Exception(
                "Erro inesperado ao buscar o produto "
                f"| Modulo do erro: {e.__traceback__.tb_frame.f_globals.get('__name__', e.__class__.__module__)} | Linha do erro: {e.__traceback__.tb_lineno}"
            )



