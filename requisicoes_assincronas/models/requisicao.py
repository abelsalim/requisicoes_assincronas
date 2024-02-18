import aiohttp

from utils.funcoes import set_trace
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
            # Atribui parâmetro ao método response
            retorno = getattr(response, retorno)
            set_trace()
            match retorno.__class__.__qualname__:
                # Entra caso retorno se um método
                case requisicao.tipo_metodo_retorno:
                    return await retorno()
                # Senão executa como atributo
                case _:
                    return retorno
