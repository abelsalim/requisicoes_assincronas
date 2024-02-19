import aiohttp

from asyncio import gather, Semaphore, sleep

from constants.requisicao import requisicao


class RequisicaoAsync:

    def __init__(self, limit_connector=0):
        self.limit_connector = limit_connector
        self.conector = None
        self.session = None

    async def __aenter__(self):
        # Gera connector com limite de conexão preestabelecido
        self.conector = aiohttp.TCPConnector(limit=self.limit_connector)
        # Gera session
        self.session = aiohttp.ClientSession(connector=self.conector)

        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        # Encerra sessão
        await self.session.close()

    async def limitador(self, tasks, limit):
        """
        Descrição breve da função.

        :param tasks: Lista de tasks para execução.
        :type metodo: list.

        :param limit: Inteiro que define o limite para Semaphore.
        :type metodo: int.

        :return: O retorno é uma lista com aguardáveis processados.
        :rtype: (str, bytes, list, dict, str).
        """
        # Define limite do lote
        semaphore = Semaphore(limit)

        async def interno(task):
            # Aplicando delimitação do semaphore
            async with semaphore:
                await sleep(0.00001)

                return await task

        lista_retorno = []

        # Itera iniciando em 0, até a quantidade de tasks num compasso
        # estabelecido pelo limite do semaphore.
        for indice in range(0, len(tasks), limit):
            # Captura as tasks do intervalo estabelecido
            faixa = tasks[indice: indice + limit]

            # Aguarda e retorna execução das tasks
            lista_retorno.extend(
                await gather(*[interno(item) for item in faixa])
            )

        return lista_retorno

    async def valida_parametros_cliente(self, parametros):
        # unificando lista_comparativa do objeto requisicao
        lista_comparativa = [
            item for lista in requisicao.lista_comparativa for item in lista
        ]

        # Itere nos métodos em paralelo com a lista predefinida
        for valor in parametros:
            # Sai se valor existe
            if valor in lista_comparativa:
                continue

            raise AttributeError(
                requisicao.parametro_invalido.format(valor=valor)
            )

    async def cliente(
            self,
            metodo='get',
            parametros_retorno=['status'],
            content_type=None,
            timeout=None,
            **kwargs
        ):
        """
        Descrição breve da função.

        :param metodo: Método de requisição utilizado.
        :type metodo: str.

        :param parametros_retorno: Os atributos selecionáveis do response.
        :type parametros_retorno: list.

        :param content_type: content_type para decodificação do json.
        :type content_type: str.

        :param timeout: Tempo limite para requisições.
        :type timeout: int.

        :param kwargs: Argumentos nomeados variáveis.
                    - url: URL utilizada na conexão.
                    - params: Parâmetros adicionados na url de conexão.
                    - headers: Dicionário que compõe o cabeçalho da conexão.
                    - json: Dicionário que será tratado como json.
                    - data: list/dict/binary/str que substituirá o payload.
        :type kwargs: dict.

        :return: O retorno pode ser o response text, read , json ou status.
        :rtype: Respectivamente str, bytes, list/dict ou str.
        """

        # Valida parâmetros (metodo, retorno) repassados
        await self.valida_parametros_cliente(
            parametros_retorno.__add__([metodo])
        )

        if timeout:
            # Caso time out seja repassado então adicione no kwargs
            kwargs.update(
                {'timeout': aiohttp.ClientTimeout(total=timeout)}
            )

        async with getattr(self.session, metodo)(**kwargs) as response:
            lista_retorno = []
            for retorno in parametros_retorno:
                # Define retorno
                match retorno:
                    case requisicao.retorne_response:
                        # retorno é próprio 'response'
                        retorno = response
                    case _:
                        # Atribui parâmetro ao objeto 'response'
                        retorno = getattr(response, retorno)

                match (retorno.__class__.__qualname__, retorno):
                    # Entra caso retorno se um método
                    case (_, requisicao.retorne_response):
                        lista_retorno.append(await response)
                    # Entra caso retorno se um método
                    case (requisicao.tipo_metodo_retorno, requisicao.retorne_json):
                        lista_retorno.extend(
                            await retorno(content_type=content_type)
                        )
                    # Entra caso retorno se um método
                    case (requisicao.tipo_metodo_retorno, _):
                        lista_retorno.append(await retorno())
                    # Senão executa como atributo
                    case _:
                        lista_retorno.append(retorno)

            return lista_retorno
