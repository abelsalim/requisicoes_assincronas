import aiohttp
from asyncio import gather, Semaphore

from constants.requisicao import requisicao


class RequisicaoAsync:

    def __init__(self):
        self.session = None

    async def __aenter__(self):
        # Gera session
        self.session = aiohttp.ClientSession()

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

    async def valida_parametros_cliente(self, *args):
        # Itere nos métodos em paralelo com a lista predefinida
        for valor, lista in zip(args, requisicao.lista_comparativa):
            # Sai se valor existe
            if valor in lista:
                continue

            raise AttributeError(
                requisicao.parametro_invalido.format(valor=valor)
            )

    async def cliente(
            self,
            metodo='get',
            retorno='status',
            content_type=None,
            timeout=None,
            **kwargs
        ):
        """
        Descrição breve da função.

        :param metodo: Método de requisição utilizado.
        :type metodo: str.

        :param kwargs: Argumentos nomeados variáveis.
                    - url: URL utilizada na conexão.
                    - params: Parâmetros adicionados na url de conexão.
                    - headers: Diciońario que compõe o cabaçalho da conexão.
                    - json: Dicionário que será tratado como json.
                    - data: list/dict/binary/str que substituirá o payload.
        :type kwargs: dict.

        :return: O retorno pode ser o response text, read , json ou status.
        :rtype: Respectivamente str, bytes, list/dict ou str.
        """

        # Valida parâmetros (metodo, retorno) repassados
        await self.valida_parametros_cliente(metodo, retorno)

        if timeout:
            # Caso time out seja repassado então adicione no kwargs
            kwargs.update(
                {'timeout': aiohttp.ClientTimeout(total=timeout)}
            )

        async with getattr(self.session, metodo)(**kwargs) as response:
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
                    return await response
                # Entra caso retorno se um método
                case (requisicao.tipo_metodo_retorno, requisicao.retorne_json):
                    return await retorno(content_type=content_type)
                # Entra caso retorno se um método
                case (requisicao.tipo_metodo_retorno, _):
                    return await retorno()
                # Senão executa como atributo
                case _:
                    return retorno
