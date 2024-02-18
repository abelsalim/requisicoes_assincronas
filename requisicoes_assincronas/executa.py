from asyncio import run, gather

from constants.ibge import ibge
from models.requisicao import RequisicaoAsync


async def main():
    async with RequisicaoAsync() as request:

        retorno = await gather(
            *[request.cliente(
                retorno='json',
                timeout=10,
                **{'url': ibge.get_ranking}
            ) for _ in range(4)]
        )

        for conteudo in retorno:
            print(f'\n{conteudo}', end=f'\n{35 * '-'}')


run(main())