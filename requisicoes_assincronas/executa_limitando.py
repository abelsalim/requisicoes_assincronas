import asyncio

from asyncio import create_task

from models.requisicao import RequisicaoAsync


async def mostra_numero(numero):
    return numero


async def main():
    async with RequisicaoAsync(limit_connector=100) as request:
        lista_numeros = [
            create_task(mostra_numero(numero)) for numero in range(1, 10)
        ]

        retorno = [
            item for item in await request.limitador(
                tasks=lista_numeros,
                limit=2
            )
        ]

        print(retorno)


asyncio.run(main())
