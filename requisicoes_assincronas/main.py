from asyncio import create_task

from .utils.requisicao import RequisicaoAsync


class Requisicao(RequisicaoAsync):

    @staticmethod
    async def requisicao_lote(
            self,
            *args,
            metodo='get',
            parametros_retorno=['status'],
            limit=100
        ):
        async with RequisicaoAsync(limit_connector=500) as request:
            # Gera lista de sms para envio
            lista = [
                create_task(
                    request.cliente(
                        metodo=metodo,
                        parametros_retorno=parametros_retorno,
                        **kwargs
                    )
                ) for kwargs in args
            ]

            lista_final = []

            for indice in range(0, len(lista), 10_000):
                # Captura as tasks do intervalo estabelecido
                faixa = lista[indice: indice + 10_000]

                # Captura retorno dos sms enviados
                retorno = [
                    item for item in await request.limitador(
                        tasks=faixa,
                        limit=limit
                    )
                ]

                lista_final.extend(retorno)

            return lista_final

    @staticmethod
    async def requisicao(
            self,
            metodo='get',
            parametros_retorno=['status'],
            timeout=10,
            **kwargs
        ):
        async with RequisicaoAsync(limit_connector=100) as request:
            retorno = await request.cliente(
                metodo=metodo,
                parametros_retorno=parametros_retorno,
                timeout=timeout,
                **kwargs
            )

            return retorno
